import pytest
import torch
import numpy as np
from bex.utils import transform_embedding, get_successful_cf


@pytest.fixture(scope="module")
def char_embed():
    return torch.randn(48, 3)

@pytest.fixture(scope="module")
def font_embed():
    return torch.randn(48, 3)

@pytest.fixture(scope="module")
def z():
    return torch.randn(2, 3, 11)

def test_transform_embedding_shape(device, z, char_embed, font_embed):

    z = z.to(device)
    result = transform_embedding(z, char_embed, font_embed)
    assert result.shape == (2, 3, 101), "Output shape mismatch"

def test_transform_embedding_one_hot(device, z, char_embed, font_embed):

    z = z.to(device)
    result = transform_embedding(z, char_embed, font_embed, one_hot=True)
    result_char_font = result[:, :, :-5]

    unique_values = np.unique(result_char_font.cpu().numpy())
    assert set(unique_values) == {0, 1}, "one_hot failed"

def test_transform_embedding_no_one_hot(device, z, char_embed, font_embed):

    z = z.to(device)
    result = transform_embedding(z, char_embed, font_embed, one_hot=False)
    result_char_font = result[:, :, :-5]

    unique_values = np.unique(result_char_font.cpu().numpy())
    assert not set(unique_values).issubset({0, 1}), "Values should not be binary"


def test_get_successful_cf_all_successful(device, char_embed, font_embed):
    z = torch.tensor([[0.1, 0.5, 0.9, 0.5, 0.5, 0.5]]).to(device)
    z_perturbed = torch.tensor([[[0.1, 0.5, 0.9, 0.5, 0.5, 0.5]]]).to(device)

    logits = torch.tensor([[0.2, 0.8]]).to(device)
    perturbed_logits = torch.tensor([[0.8, 0.2]]).to(device)

    successful_cf, sce, non_causal_flip, causal_flip, trivial = get_successful_cf(
        z_perturbed, z, perturbed_logits, logits, char_embed, font_embed
    )

    assert torch.all(successful_cf == True)
    assert sce == 1.0
    assert non_causal_flip == 1.0
    assert causal_flip == 0.0
    assert trivial == 0.0


def test_get_successful_cf_all_unsuccessful(device, char_embed, font_embed):
    z = torch.tensor([[0.5, 0.5, 0.5, 0.5, 0.5, 0.5]]).to(device)
    z_perturbed = torch.tensor([[[0.5, 0.5, 0.5, 0.5, 0.5, 0.5]]]).to(device)
    logits = torch.tensor([[0.2, 0.8]]).to(device)
    perturbed_logits = torch.tensor([[0.2, 0.8]]).to(device)

    successful_cf, sce, non_causal_flip, causal_flip, trivial = get_successful_cf(
        z_perturbed, z, perturbed_logits, logits, char_embed, font_embed
    )

    assert torch.all(successful_cf == False)
    assert sce == 0.0
    assert non_causal_flip == 0.0
    assert causal_flip == 0.0
    assert trivial == 0.0


def test_get_successful_cf_mixed_success(device, char_embed, font_embed):

    z_perturbed = torch.tensor([[[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                                  [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]]])
    z = torch.tensor([[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]])

    logits = torch.tensor([[1, 0, 0, 0]])
    perturbed_logits = torch.tensor([[1, 0, 0, 0], [0, 1, 0, 0]])

    successful_cf, sce, non_causal_flip, causal_flip, trivial = get_successful_cf(
        z_perturbed, z, perturbed_logits, logits, char_embed, font_embed)

    assert successful_cf.shape == (1, 2)
    assert successful_cf[0, 0] == 0
    assert successful_cf[0, 1] == 1

    assert sce == 0.5
    assert non_causal_flip == 1.0
    assert causal_flip == 0.0
    assert trivial == 0.0
