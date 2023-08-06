from __future__ import annotations

import pytest
import torch
from torch import nn
from torch.utils.data import DataLoader

from rebasin import interpolation as interp
from tests.fixtures.datasets import RandomDataset
from tests.fixtures.models import MLP


def loss_fn(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    return ((x - y) ** 2).sum()  # type: ignore[no-any-return]


def test_loss_fn() -> None:
    """Test that loss_fn is working as expected."""
    l1 = loss_fn(torch.tensor([1.0]), torch.tensor([2.0]))
    l2 = loss_fn(torch.tensor([1.0]), torch.tensor([1.0]))
    assert l1 > l2


class TestInterpolation:
    """Test sanity checks of Interpolation class."""
    @property
    def models(self) -> list[nn.Module]:
        return [MLP(5), MLP(5)]

    @property
    def train_dataloader(
            self
    ) -> torch.utils.data.DataLoader[tuple[torch.Tensor, torch.Tensor]]:
        return DataLoader(RandomDataset(shape=(5,), length=10))

    @property
    def val_dataloader(
            self
    ) -> torch.utils.data.DataLoader[tuple[torch.Tensor, torch.Tensor]]:
        return DataLoader(RandomDataset(shape=(5,), length=4))

    def test_sanity_checks_model(self) -> None:
        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=[],
                loss_fn=loss_fn,
                train_dataloader=self.train_dataloader,
                val_dataloader=self.val_dataloader
            )

        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=MLP(5),  # type: ignore[arg-type]
                loss_fn=loss_fn,
                train_dataloader=self.train_dataloader,
                val_dataloader=self.val_dataloader,
                input_indices=1
            )

        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=[*self.models, "not a model"],  # type: ignore[list-item]
                loss_fn=loss_fn,
                train_dataloader=self.train_dataloader,
                val_dataloader=self.val_dataloader,
                input_indices=1
            )

    def test_sanity_checks_loss_fn(self) -> None:
        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=self.models,
                loss_fn=0,
                train_dataloader=self.train_dataloader,
                val_dataloader=self.val_dataloader
            )

    def test_sanity_checks_dataloaders(self) -> None:
        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=self.models,
                loss_fn=loss_fn,
                train_dataloader=0,  # type: ignore[arg-type]
                val_dataloader=self.val_dataloader
            )

        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=self.models,
                loss_fn=loss_fn,
                train_dataloader=self.train_dataloader,
                val_dataloader=0  # type: ignore[arg-type]
            )

    def test_sanity_checks_devices(self) -> None:
        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=self.models,
                loss_fn=loss_fn,
                train_dataloader=self.train_dataloader,
                val_dataloader=self.val_dataloader,
                devices=["cpu", "cpu"],
                device_interp=None
            )

        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=self.models,
                loss_fn=loss_fn,
                train_dataloader=self.train_dataloader,
                val_dataloader=self.val_dataloader,
                devices=["cpu", "cpu", "cpu"],  # too long
                device_interp="cpu"
            )

        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=self.models,
                loss_fn=loss_fn,
                train_dataloader=self.train_dataloader,
                val_dataloader=self.val_dataloader,
                devices=None,
                device_interp="cpu"
            )

    def test_sanity_checks_input_indices(self) -> None:
        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=self.models,
                loss_fn=loss_fn,
                train_dataloader=self.train_dataloader,
                val_dataloader=self.val_dataloader,
                input_indices=0.5  # type: ignore[arg-type]
            )

        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=self.models,
                loss_fn=loss_fn,
                train_dataloader=self.train_dataloader,
                val_dataloader=self.val_dataloader,
                input_indices=[0.5]  # type: ignore[list-item]
            )

        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=self.models,
                loss_fn=loss_fn,
                train_dataloader=self.train_dataloader,
                val_dataloader=self.val_dataloader,
                input_indices=["not", "an", "int"]  # type: ignore[list-item]
            )

    def test_sanity_checks_output_indices(self) -> None:
        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=self.models,
                loss_fn=loss_fn,
                train_dataloader=self.train_dataloader,
                val_dataloader=self.val_dataloader,
                output_indices=0.5  # type: ignore[arg-type]
            )

        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=self.models,
                loss_fn=loss_fn,
                train_dataloader=self.train_dataloader,
                val_dataloader=self.val_dataloader,
                output_indices=[0.5]  # type: ignore[list-item]
            )

        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=self.models,
                loss_fn=loss_fn,
                train_dataloader=self.train_dataloader,
                val_dataloader=self.val_dataloader,
                output_indices=["not", "an", "int"]  # type: ignore[list-item]
            )

    def test_sanity_checks_save_vars(self) -> None:
        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=self.models,
                loss_fn=loss_fn,
                train_dataloader=self.train_dataloader,
                val_dataloader=self.val_dataloader,
                savedir=0  # type: ignore[arg-type]
            )

        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=self.models,
                loss_fn=loss_fn,
                train_dataloader=self.train_dataloader,
                val_dataloader=self.val_dataloader,
                save_all="not a bool"  # type: ignore[arg-type]
            )

        with pytest.raises(AssertionError):
            interp.Interpolation(
                models=self.models,
                loss_fn=loss_fn,
                train_dataloader=self.train_dataloader,
                val_dataloader=self.val_dataloader,
                save_all=True,
                savedir=None
            )


class TestLerpSimple:
    """Test the LerpSimple class."""

    @property
    def mlps(self) -> list[nn.Module]:
        return [MLP(5), MLP(5)]

    @property
    def train_dl_mlp(
            self
    ) -> torch.utils.data.DataLoader[tuple[torch.Tensor, torch.Tensor]]:
        return DataLoader(RandomDataset(shape=(5,), length=10))

    @property
    def val_dl_mlp(
            self
    ) -> torch.utils.data.DataLoader[tuple[torch.Tensor, torch.Tensor]]:
        return DataLoader(RandomDataset(shape=(5,), length=2))

    def test_settings_are_plausible(self) -> None:
        model_a, model_b = self.mlps

        # Must be different models
        for p1, p2 in zip(model_a.parameters(), model_b.parameters(), strict=True):
            assert not torch.allclose(p1, p2)

        # Must produce different outputs
        x = torch.rand(5)
        assert not torch.allclose(model_a(x), model_b(x))

        # Must have different losses
        val_dl = self.val_dl_mlp
        x, y = next(iter(val_dl))
        loss_a = loss_fn(model_a(x), y)
        loss_b = loss_fn(model_b(x), y)

        assert loss_a != loss_b

    def test_mlp(self) -> None:
        lerp = interp.LerpSimple(
            models=self.mlps,
            train_dataloader=self.train_dl_mlp,
            val_dataloader=self.val_dl_mlp,
            loss_fn=loss_fn
        )
        lerp.interpolate(steps=10)

        assert len(lerp.losses_interpolated) == 10
        assert len(lerp.losses_original) == 2

        # With random data, there should be no duplicate losses.
        assert len(set(lerp.losses_original)) == 2
        assert len(set(lerp.losses_interpolated)) == 10


@pytest.mark.skipif(not torch.cuda.is_available(), reason="GPU tests")
class TestInterpolationGPU:
    @staticmethod
    def test_mlp() -> None:
        models = [MLP(5).to("cuda"), MLP(5)]
        devices = ["cuda", "cpu"]
        lerp = interp.LerpSimple(
            models=models,
            loss_fn=loss_fn,
            devices=devices,
            device_interp="cuda",
            train_dataloader=DataLoader(RandomDataset(shape=(5,), length=10)),
            val_dataloader=DataLoader(RandomDataset(shape=(5,), length=2))
        )
        lerp.interpolate(steps=10)
        assert len(lerp.losses_interpolated) == 10
        assert len(lerp.losses_original) == 2

    @pytest.mark.skipif(torch.cuda.device_count() < 2, reason="Not enough GPUs")
    def test_mlp_multi_gpu(self) -> None:
        """Test whether it works with :code:`device_interp not in devices`."""

        models = [MLP(5).to("cuda:0"), MLP(5).to("cuda:1")]
        devices = ["cuda:0", "cuda:1"]
        lerp = interp.LerpSimple(
            models=models,
            loss_fn=loss_fn,
            devices=devices,
            device_interp="cpu",
            train_dataloader=DataLoader(RandomDataset(shape=(5,), length=10)),
            val_dataloader=DataLoader(RandomDataset(shape=(5,), length=2))
        )
        lerp.interpolate(steps=10)
        assert len(lerp.losses_interpolated) == 10
        assert len(lerp.losses_original) == 2
