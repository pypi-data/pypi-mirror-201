import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import ResNetModel, BertModel


class VariationalEncoder(nn.Module):
    def __init__(self, latent_dims, input_dim):
        super().__init__()
        self.linear1 = nn.Linear(input_dim, input_dim//2)
        self.linear2 = nn.Linear(input_dim//2, latent_dims)
        self.linear3 = nn.Linear(input_dim//2, latent_dims)

        self.N = torch.distributions.Normal(0, 1).to
        self.kl = 0

    def forward(self, x):
        x = F.relu(self.linear1(x))
        mu =  self.linear2(x)
        sigma = torch.exp(self.linear3(x))
        z = mu + sigma*self.N.sample(mu.shape)
        self.kl = (sigma**2 + mu**2 - torch.log(sigma) - 1/2).sum()
        return z


class AISearchVAEEncoder(nn.Module):
    def __init__(self, latent_dims, input_dim, nlp_encoder_path, cv_path):
        super().__init__()

        self.nlp_encoder = BertModel.from_pretrained(nlp_encoder_path, cache_dir="/mnt/bert/")
        for param in self.nlp_encoder.parameters():
            param.requires_grad = False
        
        self.cv_encoder = ResNetModel.from_pretrained(cv_path, cache_dir="/mnt/resnet/")
        for param in self.cv_encoder.parameters():
            param.requires_grad = False

        self.linear1 = nn.Linear(input_dim, input_dim//2)
        self.linear2 = nn.Linear(input_dim//2, latent_dims)
        self.linear3 = nn.Linear(input_dim//2, latent_dims)

        self.N = torch.distributions.Normal(0, 1)
        self.kl = 0

    def forward(self, nlp_in, img_in):
        nlp_in = self.nlp_encoder(**nlp_in).last_hidden_state[:,0,:].to(dtype=torch.float32)
        img_in = self.cv_encoder(**img_in).pooler_output.flatten(start_dim=1)
        combined_in = torch.cat([nlp_in, img_in], dim=1)
        vae_in = F.relu(self.linear1(combined_in))
        mu =  self.linear2(vae_in)
        device = mu.device
        sigma = torch.exp(self.linear3(vae_in))
        z = mu + sigma*self.N.sample(mu.shape).to(device)
        self.kl = (sigma**2 + mu**2 - torch.log(sigma) - 1/2).sum()
        return combined_in, z


class AISearchEncoder(nn.Module):
    def __init__(self, latent_dims, input_dim, nlp_encoder_path, cv_path, freeze=False):
        super().__init__()

        self.nlp_encoder = BertModel.from_pretrained(nlp_encoder_path, cache_dir="/mnt/bert/")    
        self.cv_encoder = ResNetModel.from_pretrained(cv_path, cache_dir="/mnt/resnet/")
        if freeze:
            for param in self.nlp_encoder.parameters():
                param.requires_grad = False
            for param in self.cv_encoder.parameters():
                param.requires_grad = False

        self.linear1 = nn.Linear(input_dim, input_dim//2)
        self.linear2 = nn.Linear(input_dim//2, latent_dims)

    def forward(self, nlp_in, img_in):
        nlp_in = self.nlp_encoder(**nlp_in).last_hidden_state[:,0,:].to(dtype=torch.float32)
        img_in = self.cv_encoder(**img_in).pooler_output.flatten(start_dim=1)
        combined_in = torch.cat([nlp_in, img_in], dim=1)
        vae_in = F.relu(self.linear1(combined_in))
        z =  self.linear2(vae_in)

        return combined_in, z


class Decoder(nn.Module):
    def __init__(self, latent_dims, input_dim):
        super().__init__()
        self.linear1 = nn.Linear(latent_dims, input_dim//2)
        self.linear2 = nn.Linear(input_dim//2, input_dim)

    def forward(self, z):
        z = F.relu(self.linear1(z))
        z = torch.sigmoid(self.linear2(z))
        return z


class AISearchVAE(nn.Module):
    def __init__(self, latent_dims, input_dim, nlp_encoder_path, cv_path):
        super().__init__()
        self.encoder = AISearchVAEEncoder(latent_dims, input_dim, nlp_encoder_path, cv_path)
        self.decoder = Decoder(latent_dims, input_dim)

    def forward(self, nlp_in, img_in):
        combined_in, z = self.encoder(nlp_in, img_in)
        reconstruction = self.decoder(z)
        return reconstruction, z, combined_in


class AISearchAE(nn.Module):
    def __init__(self, latent_dims, input_dim, nlp_encoder_path, cv_path):
        super().__init__()
        self.encoder = AISearchEncoder(latent_dims, input_dim, nlp_encoder_path, cv_path)
        self.decoder = Decoder(latent_dims, input_dim)

    def forward(self, nlp_in, img_in):
        combined_in, z = self.encoder(nlp_in, img_in)
        reconstruction = self.decoder(z)
        return reconstruction, z, combined_in


class LinearVAE(nn.Module):
    def __init__(self, latent_dims, input_dim):
        super().__init__()
        self.encoder = VariationalEncoder(latent_dims, input_dim)
        self.decoder = Decoder(latent_dims, input_dim)

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z), z