import os

import torch


def set_device_name(name):
    os.environ['DEVICE'] = name


def get_device_name():
    return os.environ['DEVICE']


def get_device(i=0):
    name = get_device_name()

    device = f'cuda:{i}' if (str_is_empty(name) or 'gpu' in name) and torch.cuda.device_count() >= i + 1 else 'cpu'

    return torch.device(device)


def set_device_memory(device_name, process_memory_fraction=0.5):
    if 'gpu' in device_name:
        torch.cuda.set_per_process_memory_fraction(
            process_memory_fraction,
            get_device()
        )
        torch.cuda.empty_cache()


def str_is_empty(value):
    return value is None or len(value) == 0


set_device_name('')
