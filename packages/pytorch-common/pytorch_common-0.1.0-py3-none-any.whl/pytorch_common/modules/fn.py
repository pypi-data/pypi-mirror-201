import torch
from torch          import as_tensor
from .fit_context   import FitContextFactory



class Fn:
    @staticmethod
    def train(ctx, data_loader):
        """Default train function. It perform a nomal trainig process.

        Args:
            ctx: Contain all object required to perform a train process. See FitContextFactory class to see a context detail.
            data_loader: Data loader with train data.

        Returns:
            float: mean of loss_fn result.
        """
        ctx.model.train()
        total_loss = 0

        for index, (features, target) in enumerate(data_loader):
            features, target = features.to(ctx.device), target.to(ctx.device)
            prediction = ctx.model(features)

            ctx.model.zero_grad()
            loss = ctx.loss_fn(prediction, target)
            loss.backward()
            ctx.optimizer.step()
            total_loss += loss.item()

        return total_loss / len(data_loader)


    @staticmethod
    def validation(ctx, data_loader):
        """Default validation function. It perform a nomal model validation process.

        Args:
            ctx: Contain all object required to perform a train process. See FitContextFactory class to see a context detail.
            data_loader: Data loader with validation data.

        Returns:
            a (y_pred, y_true) tuple.
        """
        y_pred, y_true = [], []
        ctx.model.eval()
        with torch.no_grad():
            for index, (features, target) in enumerate(data_loader):
                prediction = ctx.model(features.to(ctx.model.device))

                y_pred.extend(prediction.cpu().numpy())
                y_true.extend(target.cpu().numpy())

        return as_tensor(y_pred).cpu(), as_tensor(y_true).cpu()


    @staticmethod
    def validation_score(model, data_loader, score_fn):
        """Apply an score function to Fn.validation function result.

        Args:
            model (CommonMixin): A trained model.
            data_loader:  Data loader with validation data.
            score_fn: custom funcion used to evalidate model performance. i.e: MSE, RMSE, Binary Cross Entropy, etc...

        Returns:
            a score function result.
        """
        ctx = FitContextFactory(model)
        y_pred, y_true = Fn.validation(ctx, data_loader)
        return score_fn(y_true.numpy(), y_pred.numpy())
