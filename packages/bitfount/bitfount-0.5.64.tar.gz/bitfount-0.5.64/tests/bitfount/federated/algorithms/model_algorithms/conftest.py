"""Pytest configuration for model algorithm tests."""
from unittest.mock import Mock

from _pytest.fixtures import fixture

from bitfount.federated.model_reference import BitfountModelReference
from tests.utils import PytestRequest


@fixture(params=[True, False])
def model(request: PytestRequest) -> Mock:
    """Returns mock model."""
    spec = BitfountModelReference if request.param else None
    mod = Mock(steps=10, spec=spec)
    mod.fit = Mock()
    mod.evaluate = Mock()
    mod.evaluate.return_value = ([0.9], [0.8])
    mod.backend_tensor_shim = Mock()
    mod.datastructure = Mock()
    mod.schema = Mock()
    mod.hyperparameters = {}
    mod.model_version = 1
    mod.get_weights = Mock()
    return mod
