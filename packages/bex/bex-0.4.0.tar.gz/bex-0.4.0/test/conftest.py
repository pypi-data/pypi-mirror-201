import pytest
import torch

@pytest.fixture(scope="session", params=["cpu", "cuda"])
def device(request):
    if request.param == "cuda" and not torch.cuda.is_available():
        pytest.skip("CUDA not available on this system")
    return request.param

