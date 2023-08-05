import abc
import os
import wandb
import json
import torch
import pytorch_lightning as pl
from pytorch_lightning.loggers import TensorBoardLogger


class WandbArtifactCallbackBase(pl.callbacks.Callback):
    def __init__(self, wandb_run, lookup_output_dir, torch_model_name,
                 torch_model_params, pl_model_params, model_dir):
        self.wandb_run = wandb_run
        self.model_dir = model_dir
        self.torch_model_name = torch_model_name
        self.lookup_output_dir = lookup_output_dir
        self.torch_model_params = torch_model_params
        self.pl_model_params = pl_model_params

    def on_train_start(self, trainer, pl_module):
        # lookup files
        lookup_artifact = wandb.Artifact("lookup_csv", type="lookup_tables")
        lookup_artifact.add_dir(self.lookup_output_dir)
        self.wandb_run.log_artifact(lookup_artifact, aliases=[self.wandb_run.name])
        # torch model params
        torch_model_params_path = os.path.join(self.model_dir, "torch_model_params.json")
        with open(torch_model_params_path, "w") as f:
            json.dump(self.torch_model_params, f)
        torch_params_artifact = wandb.Artifact("torch_params", type="params")
        torch_params_artifact.add_file(torch_model_params_path)
        self.wandb_run.log_artifact(torch_params_artifact, aliases=[self.wandb_run.name])
        # pl model params
        pl_model_params_path = os.path.join(self.model_dir, "pl_model_params.json")
        with open(pl_model_params_path, "w") as f:
            json.dump(self.pl_model_params, f)
        pl_params_artifact = wandb.Artifact("pl_params", type="params")
        pl_params_artifact.add_file(pl_model_params_path)
        self.wandb_run.log_artifact(pl_params_artifact, aliases=[self.wandb_run.name])

    def on_train_epoch_end(self, trainer, pl_module):
        # torch model
        model_path = os.path.join(self.model_dir, f"model.pt")
        torch.save(getattr(pl_module, self.torch_model_name).state_dict(), model_path)
        torch_model_artifact = wandb.Artifact(f"torch_model_epoch_{pl_module.current_epoch}", type="model")
        torch_model_artifact.add_file(model_path)
        self.wandb_run.log_artifact(torch_model_artifact, aliases=[self.wandb_run.name])

    def on_train_end(self, trainer, pl_module):
        # pl model
        model_path = os.path.join(self.model_dir, f"model.pt")
        torch.save(pl_module.state_dict(), model_path)
        pl_model_artifact = wandb.Artifact(f"pl_model_epoch_{pl_module.current_epoch}", type="model")
        pl_model_artifact.add_file(model_path)
        self.wandb_run.log_artifact(pl_model_artifact, aliases=[self.wandb_run.name])


class MLflowCallbackBase(pl.callbacks.Callback):
    """
    This callback updates metrics on MLflow after every train epoch and validation epoch

    Abstract Method::
        - update_mlflow_metrics
    """

    def on_train_start(self, trainer, pl_module):
        self.log_artifacts_start(trainer, pl_module)
        pass

    def on_validation_epoch_start(self, trainer, pl_module):
        if not trainer.sanity_checking:
            self.update_mlflow_metrics(trainer, pl_module, "Train")

    def on_validation_epoch_end(self, trainer, pl_module):
        self.update_mlflow_metrics(trainer, pl_module, "Validation")

    def on_train_epoch_end(self, trainer, pl_module):
        self.log_artifacts_epoch(trainer, pl_module)
        pass

    def on_train_end(self, trainer, pl_module):
        self.log_artifacts_end(trainer, pl_module)
        self.register_model(trainer, pl_module)
        pass

    @abc.abstractmethod
    def update_mlflow_metrics(self, trainer, pl_module, phase):
        """
        Log metrics to mlflow using mlflow.log_metrics

        :param trainer: trainer passed from on_*_epoch_end methods, you can find your logger, callback_metrics and logged_metrics here
        :param pl_module: the trained model passed from on_*_epoch_end methods
        :param phase: Train or Validation phase in the training process

        Example:

        def update_mlflow_metrics(self, trainer, pl_module, phase):
            mlflow.log_metrics(
                metrics={f"{phase}/loss": loss_from_training,
                         f"{phase}/acc": acc_from_trainer},
                step=pl_module.current_epoch
            )
        """
        pass

    @abc.abstractmethod
    def register_model(self, trainer, pl_module):
        """
        Register model to MLflow host
        """
        pass

    @abc.abstractmethod
    def log_artifacts_start(self, trainer, pl_module):
        """
        Log all run-specific or dataset related metadata that are available before training
        """
        pass

    @abc.abstractmethod
    def log_artifacts_epoch(self, trainer, pl_module):
        """
        Log network weights from current epoch
        """
        pass

    @abc.abstractmethod
    def log_artifacts_end(self, trainer, pl_module):
        """
        Log all metadata that is only available after training complete
        """
        pass


class TensorboardCallbackBase(pl.callbacks.Callback):
    """
    Update model parameter histograms and metric scalars on tensorboard

    Abstract Method::
        - update_metrics_scalar

    Attributes::
        - tensorboard_logger: TensorBoardLogger from pytorch lightning to add graphs
    """

    def __init__(self, **tb_kwargs):
        """
        :param tensorboard_logger: TensorBoardLogger from pytorch lightning to add graphs
        """
        self.tensorboard_logger = TensorBoardLogger(**tb_kwargs)

    def on_train_start(self, trainer, pl_module):
        self.tensorboard_logger.log_graph(pl_module)
    
    def on_validation_epoch_start(self, trainer, pl_module):
        if not trainer.sanity_checking:
            self.update_parameter_histogram(pl_module)
            self.update_metrics_scalar(trainer, pl_module, "Train")

    def on_validation_epoch_end(self, trainer, pl_module):
        self.update_metrics_scalar(trainer, pl_module, "Validation")

    def update_parameter_histogram(self, pl_module):
        for name, params in pl_module.named_parameters():
            self.tensorboard_logger.experiment.add_histogram(name, params, pl_module.current_epoch, max_bins=512)

    @abc.abstractmethod
    def update_metrics_scalar(self, trainer, pl_module, phase):
        """
        update scalar metrics to tensorboard

        :param trainer: trainer passed from on_*_epoch_end methods, you can find your logger, callback_metrics and logged_metrics here
        :param pl_module: the trained model passed from on_*_epoch_end methods
        :param phase: Train or Validation phase in the training process

        Example::

        def update_metrics_scalar(self, trainer, pl_module, phase):
            epoch = pl_module.current_epoch
            trainer_logger = trainer.logger
            self.tensorboard_logger.experiment.add_scalar(f"loss/{phase}", loss_from_trainer_logger, epoch)
            self.tensorboard_logger.experiment.add_scalar(f"acc/{phase}", acc_from_trainer_logger, epoch)
        """
        pass


class AttnVisCallbackBase(pl.callbacks.Callback):
    """
    Visualize attention importance using wandb's line_series plot

    Abstract Method::
        - get_attn_weights

    Attributes::
        - transformer_prefix: a str indicating what type of transformer is this e.g. context/sequence
        - cols: input feature columns
        - sample_inputs: sample inputs to generate attention weights
        - epochs: list of epoch numbers
        - avg_attn_weights: list of lists containing average attention weights for each epoch
        - device: gpu or cpu device
    """

    def __init__(self, transformer_prefix, cols, sample_inputs, device):
        """
        :param transformer_prefix: a str indicating what type of transformer is this e.g. context/sequence
        :param cols: input feature columns
        :param sample_inputs: sample inputs to generate attention weights
        """
        self.transformer_prefix = transformer_prefix
        self.cols = cols
        self.sample_inputs = sample_inputs
        self.epochs = []
        self.avg_attn_weights = [[] for _ in range(len(self.cols))]
        self.device = device

    def on_validation_epoch_end(self, trainer, pl_module):
        self.epochs.append(pl_module.current_epoch)
        avg_attn_weight = self.get_attn_weights(pl_module)
        for i in range(len(self.cols)):
            self.avg_attn_weights[i].append(avg_attn_weight[i])
        wandb.log(
            {
                f"attention_importance_line_{self.transformer_prefix}": wandb.plot.line_series(
                    xs=self.epochs, ys=self.avg_attn_weights,
                    keys=self.cols,
                    title=f"Attention Importance Line - {self.transformer_prefix}",
                    xname="step"
                )
            }
        )

    @abc.abstractmethod
    def get_attn_weights(self, pl_module):
        """
        Using self.sample_inputs, calculate average attention on input features

        :param pl_module: the trained model passed from on_validation_epoch_end method
        :return: a list of averaged attention in the order of self.cols

        Example::

        def get_attn_weights(self, pl_module):
            tmp_in = self.sample_inputs.to(self.device)
            transformer_layer = pl_module.transformer_layer
            attn_layer = transformer_layer.encoder.layers[0].self_attn
            tmp_out = transformer_layer.embedding_layer(tmp_in)
            _, attn_weight = attn_layer(tmp_out, tmp_out, tmp_out, need_weights=True)
            avg_attn_weight = attn_weight.mean(0).mean(0).detach().tolist()
            return avg_attn_weight
        """
        return []


class VZArtifactCallback(pl.callbacks.Callback):
    def __init__(self, torch_model_params, model_dir, params_to_pop=None):
        self.model_dir = model_dir
        self.torch_model_params = torch_model_params
        if params_to_pop:
            for p in params_to_pop:
                self.torch_model_params.pop(p, None)

    def on_train_start(self, trainer, pl_module):
        torch_model_params_path = os.path.join(self.model_dir, "torch_model_params.json")
        with open(torch_model_params_path, "w") as f:
            json.dump(self.torch_model_params, f)

#     def on_train_end(self, trainer, pl_module):
#         model_path = os.path.join(self.model_dir, f"model_{trainer.current_epoch}.pt")
#         torch.save(pl_module.torch_model.state_dict(), model_path)
        
    def on_train_epoch_end(self, trainer, pl_module):
        if trainer.global_rank == 0:
            model_path = os.path.join(self.model_dir, f"model_{trainer.current_epoch}.pt")
            torch.save(pl_module.torch_model.state_dict(), model_path)