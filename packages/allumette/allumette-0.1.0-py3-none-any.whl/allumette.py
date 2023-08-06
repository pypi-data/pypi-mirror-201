import datetime
import contextlib
import os

__all__ = ["new_timestamp", "timestamp", "directory", "npimg"]

def new_timestamp():
    return datetime.datetime.now().isoformat(timespec="seconds").replace(":", "h", 1).replace(":", "m", 1) + "s"

timestamp = new_timestamp()

@contextlib.contextmanager
def directory(path: str):
    cwd = os.getcwd()
    try:
        os.makedirs(path, exist_ok=True)
        os.chdir(path)
        yield
    except Exception as e:
        raise e #?
    finally:
        os.chdir(cwd)

from typing_extensions import TYPE_CHECKING
if TYPE_CHECKING:
    import torch 

def npimg(x: "torch.Tensor"):
    import torch 
    import numpy
    assert x.ndim == 4
    return (x.detach().cpu().moveaxis(1, -1).clamp(0.0, 1.0) * 255).to(torch.uint8).numpy()