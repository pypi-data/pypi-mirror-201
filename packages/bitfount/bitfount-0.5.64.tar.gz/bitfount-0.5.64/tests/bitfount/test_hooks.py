"""Tests bitfount.hooks module."""
from __future__ import annotations

import inspect
import logging
from typing import Any, Type
from unittest.mock import Mock

from _pytest.logging import LogCaptureFixture
import pytest

from bitfount.federated.pod import Pod
from bitfount.hooks import (
    _HOOK_DECORATED_ATTRIBUTE,
    HOOK_TYPE_TO_PROTOCOL_MAPPING,
    BaseAlgorithmHook,
    BaseHook,
    BasePodHook,
    HookType,
    _registry,
    registry,
)
from tests.utils.helper import unit_test


@unit_test
class TestHooks:
    """Tests bitfount.hooks module."""

    @pytest.fixture(autouse=True)
    def cleanup_registry(self) -> None:
        """Cleans up the registry."""
        _registry.clear()

    @pytest.fixture
    def custom_pod_hook(self) -> BasePodHook:
        """Returns a custom pod hook."""

        class MyPodHook(BasePodHook):
            """Custom pod hook."""

            def on_pod_startup_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
                """Dummy method implementation."""
                print("on_pod_startup_start")

        return MyPodHook()

    def test_all_hook_types_have_a_protocol(self) -> None:
        """Tests that all hook types have a protocol."""
        for hook_type in HookType:
            assert hook_type in HOOK_TYPE_TO_PROTOCOL_MAPPING

    @pytest.mark.parametrize("base_hook", [BasePodHook, BaseAlgorithmHook])
    def test_base_hooks_implement_protocol_correctly(
        self, base_hook: Type[BaseHook]
    ) -> None:
        """Tests that base hooks implement the protocol correctly."""
        assert not inspect.isabstract(base_hook)
        assert issubclass(base_hook, BaseHook)
        base_hook_obj = base_hook()

        if base_hook == BasePodHook:
            assert base_hook_obj.type == HookType.POD
        elif base_hook == BaseAlgorithmHook:
            assert base_hook_obj.type == HookType.ALGORITHM
        assert isinstance(
            base_hook_obj, HOOK_TYPE_TO_PROTOCOL_MAPPING[base_hook_obj.type]
        )
        assert base_hook_obj.hook_name == base_hook_obj.__class__.__name__

    def test_base_pod_hook_methods_are_decorated(self) -> None:
        """Tests that base pod hook methods are decorated."""
        hook = BasePodHook()
        assert getattr(hook.on_pod_shutdown_end, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_pod_shutdown_start, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_pod_startup_end, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_pod_startup_error, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_pod_startup_start, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_pod_init_end, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_pod_init_error, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_pod_init_start, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_task_end, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_task_start, _HOOK_DECORATED_ATTRIBUTE)

    def test_base_algorithm_hook_methods_are_decorated(self) -> None:
        """Tests that base algorithm hook methods are decorated."""
        hook = BaseAlgorithmHook()
        assert getattr(hook.on_init_end, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_init_start, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_run_start, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_run_end, _HOOK_DECORATED_ATTRIBUTE)

    @pytest.mark.parametrize("base_hook", [BasePodHook, BaseAlgorithmHook])
    def test_hook_registration(self, base_hook: Type[BaseHook]) -> None:
        """Tests that hooks are registered correctly."""
        hook = base_hook()
        hook.register()
        assert hook.registered
        assert len(registry[hook.type]) == 1
        assert hook.hook_name in [i.hook_name for i in registry[hook.type]]

    @pytest.mark.parametrize("base_hook", [BasePodHook, BaseAlgorithmHook])
    def test_same_hook_cant_be_registered_multiple_times(
        self, base_hook: Type[BaseHook], caplog: LogCaptureFixture
    ) -> None:
        """Tests that the same hook can't be registered multiple times."""
        hook = base_hook()
        hook.register()
        hook.register()
        assert len(registry[hook.type]) == 1
        assert "Hook already registered" in caplog.text

    def test_hook_type_can_have_multiple_hooks_registered_against_it(
        self, custom_pod_hook: BasePodHook
    ) -> None:
        """Tests that a hook type can have multiple hooks registered against it.

        The hook names have to be different.
        """
        pod_hook = BasePodHook()
        pod_hook.register()
        assert pod_hook.registered
        custom_pod_hook.register()
        assert custom_pod_hook.registered
        assert len(registry[HookType.POD]) == 2

    def test_hook_exception_is_automatically_caught_and_logged(
        self, caplog: LogCaptureFixture
    ) -> None:
        """Tests that hook exceptions are automatically caught and logged."""

        class MyHook(BasePodHook):
            """Custom hook."""

            def on_pod_startup_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
                """Dummy method implementation."""
                raise ValueError("Test")

        hook = MyHook()
        hook.on_pod_startup_start(Mock())
        assert "Exception in hook on_pod_startup_start" in caplog.text

    def test_hook_runs_successfully_and_is_logged(
        self, caplog: LogCaptureFixture
    ) -> None:
        """Tests that hook runs successfully and is logged."""
        caplog.set_level(logging.DEBUG)

        class MyHook(BasePodHook):
            """Custom hook."""

            def on_pod_startup_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
                """Dummy method implementation."""
                print("on_pod_startup_start")

        hook = MyHook()
        hook.on_pod_startup_start(Mock())
        assert "Calling hook on_pod_startup_start" in caplog.text
        assert "Called hook on_pod_startup_start" in caplog.text
