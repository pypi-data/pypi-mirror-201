import torch


class PersistentMixin:
    def save(self, path):
        """Save model param values to file.pt.

        Args:
            path (str): Path of file.pt (Don't include .pt extension)
        """
        checkpoint = self.state_dict()
        torch.save(checkpoint, f'{path}.pt')


    def load(self, path):
        """Loas model param values from file.pt.

        Args:
            path (str): Path of file.pt (Don't include .pt extension)
        """
        checkpoint = torch.load(f'{path}.pt')
        self.load_state_dict(checkpoint)
