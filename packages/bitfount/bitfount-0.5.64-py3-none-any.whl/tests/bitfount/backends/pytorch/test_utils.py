"""Tests for PyTorch-specific utils."""
from importlib import reload
from typing import Callable, Generator

from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch
import pytest
from pytest import fixture
from pytest_mock import MockerFixture

import bitfount.backends.pytorch.utils
from bitfount.backends.pytorch.utils import _autodetect_gpu
import bitfount.config
from bitfount.data.datafactory import _get_default_data_factory
from tests.utils.helper import backend_test, get_debug_logs, unit_test


def mock_device_count(count: int = 0) -> Callable[[], int]:
    """Mock device counter for CUDA."""

    def f() -> int:
        return count

    return f


@backend_test
@unit_test
class TestAutodetectGPU:
    """Tests for `_autodetect_gpu` function."""

    @fixture(autouse=True)
    def clear_cache(self) -> Generator:
        """Clears the cache before each test."""
        reload(bitfount.backends.pytorch.utils)
        _autodetect_gpu.cache_clear()
        yield
        _autodetect_gpu.cache_clear()

    def test_autodetect_gpu_cpu_only(
        self, caplog: LogCaptureFixture, monkeypatch: MonkeyPatch
    ) -> None:
        """Tests auto-detecting GPU count when only CPU."""
        # Mock out CUDA device count
        caplog.set_level("INFO")
        monkeypatch.setattr("torch.cuda.device_count", mock_device_count(0))

        gpu_info = _autodetect_gpu()

        assert gpu_info == {"accelerator": "cpu", "devices": None}
        assert (
            caplog.records[0].msg == "No supported GPU detected. Running model on CPU."
        )

    def test_autodetect_1_gpu(
        self, caplog: LogCaptureFixture, monkeypatch: MonkeyPatch
    ) -> None:
        """Tests auto-detecting GPU when only one GPU."""
        # Mock out CUDA device count
        caplog.set_level("INFO")
        monkeypatch.setattr("torch.cuda.device_count", mock_device_count(1))
        monkeypatch.setattr("torch.cuda.get_device_name", lambda x: f"GPU_{x}")

        gpu_info = _autodetect_gpu()

        assert gpu_info == {"accelerator": "gpu", "devices": 1}
        assert (
            caplog.records[0].msg == "CUDA support detected. GPU (GPU_0) will be used."
        )

    def test_autodetect_multiple_gpu(
        self, caplog: LogCaptureFixture, monkeypatch: MonkeyPatch
    ) -> None:
        """Tests auto-detecting GPU when multiple GPUs."""
        # Mock out CUDA device count
        caplog.set_level("INFO")
        monkeypatch.setattr("torch.cuda.device_count", mock_device_count(2))
        monkeypatch.setattr("torch.cuda.get_device_name", lambda x: f"GPU_{x}")

        gpu_info = _autodetect_gpu()

        assert gpu_info == {"accelerator": "gpu", "devices": 1}
        assert caplog.records[0].levelname == "WARNING"
        assert (
            caplog.records[0].msg
            == "Bitfount model currently only supports one GPU. Will use GPU 0 (GPU_0)."
        )
        assert (
            caplog.records[1].msg == "CUDA support detected. GPU (GPU_0) will be used."
        )

    def test_mps_detected_and_used(
        self, caplog: LogCaptureFixture, mocker: MockerFixture, monkeypatch: MonkeyPatch
    ) -> None:
        """Tests that MPS is detected and used."""
        caplog.set_level("INFO")
        monkeypatch.setattr("bitfount.config.BITFOUNT_USE_MPS", True)
        reload(bitfount.backends.pytorch.utils)
        mock_torch = mocker.patch("bitfount.backends.pytorch.utils.torch")
        mock_torch.backends.mps.is_available.return_value = True

        gpu_info = _autodetect_gpu()

        assert gpu_info == {"accelerator": "mps", "devices": 1}
        assert caplog.records[0].levelname == "INFO"
        assert (
            caplog.records[0].msg
            == "Metal support detected. Running model on Apple GPU."
        )

    def test_mps_detected_but_not_used(
        self, caplog: LogCaptureFixture, mocker: MockerFixture, monkeypatch: MonkeyPatch
    ) -> None:
        """Tests that MPS is detected but not used."""
        caplog.set_level("INFO")
        monkeypatch.setattr("bitfount.config.BITFOUNT_USE_MPS", False)
        reload(bitfount.backends.pytorch.utils)
        mock_torch = mocker.patch("bitfount.backends.pytorch.utils.torch")
        mock_torch.backends.mps.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 0

        gpu_info = _autodetect_gpu()

        assert gpu_info == {"accelerator": "cpu", "devices": None}
        assert caplog.records[0].levelname == "INFO"
        assert (
            caplog.records[0].msg
            == "Metal support detected, but has been switched off."
        )

    @pytest.mark.parametrize(
        argnames="mps_pytorch_support",
        argvalues=(True, False),
    )
    def test_mps_not_supported(
        self,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        mps_pytorch_support: bool,
    ) -> None:
        """Tests handling if MPS is not supported.

        Tests the cases where:
        - it is supported by pytorch but not available
        - it is not supported by pytorch
        """
        mock_torch = mocker.patch("bitfount.backends.pytorch.utils.torch")
        # Mock out there being no explicit GPUs
        mock_torch.cuda.device_count.return_value = 0
        if mps_pytorch_support:
            # Mark the support as not available even if the pytorch version supports
            # it, i.e. as though running on Intel metal
            mock_torch.backends.mps.is_available.return_value = False
        else:
            # This will force an AttributeError to be raised on `.mps` access
            # i.e. as though pytorch version doesn't support MPS at all
            del mock_torch.backends.mps

        caplog.set_level("DEBUG")
        gpu_info = _autodetect_gpu()

        assert gpu_info == {"accelerator": "cpu", "devices": None}

        if not mps_pytorch_support:
            assert "Pytorch version does not support MPS." in get_debug_logs(caplog)

    def test_autodetect_caching_with_mps(
        self, mocker: MockerFixture, monkeypatch: MonkeyPatch
    ) -> None:
        """Tests that autodetect caching works with MPS."""
        monkeypatch.setattr("bitfount.config.BITFOUNT_USE_MPS", True)
        reload(bitfount.backends.pytorch.utils)
        mock_torch = mocker.patch("bitfount.backends.pytorch.utils.torch")
        mock_torch.backends.mps.is_available.return_value = True

        gpu_info = _autodetect_gpu()
        assert gpu_info == {"accelerator": "mps", "devices": 1}
        mock_torch.backends.mps.is_available.assert_called_once()
        gpu_info2 = _autodetect_gpu()
        assert gpu_info2 == {"accelerator": "mps", "devices": 1}
        # Ensure that the MPS check is still only called once even though the function
        # is called twice
        mock_torch.backends.mps.is_available.assert_called_once()


@backend_test
@unit_test
class TestDefaultDataFactoryLoading:
    """Tests for loading the default data factory when PyTorch installed."""

    def test_load_pytorch_default_data_factory(self, monkeypatch: MonkeyPatch) -> None:
        """Test that the default data factory can load."""
        # Ensure PyTorch is set as the engine variable
        monkeypatch.setattr(
            "bitfount.config.BITFOUNT_ENGINE", bitfount.config._PYTORCH_ENGINE
        )

        # Create a fake class and set that as the PyTorch data factory
        class FakeDataFactory:
            pass

        monkeypatch.setattr(
            "bitfount.backends.pytorch.data.datafactory._PyTorchDataFactory",
            FakeDataFactory,
        )

        df = _get_default_data_factory()
        assert isinstance(df, FakeDataFactory)
