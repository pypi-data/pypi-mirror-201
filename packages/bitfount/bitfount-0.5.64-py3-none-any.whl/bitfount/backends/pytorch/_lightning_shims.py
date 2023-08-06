"""Shims to allow compat between different PyTorch Lightning versions."""
from packaging.version import Version, parse as version_parse
import pytorch_lightning

_LIGHTNING_VERSION: Version = version_parse(pytorch_lightning.__version__)

if _LIGHTNING_VERSION < Version("1.9.0"):
    from pytorch_lightning.loggers import (  # type: ignore[attr-defined] # Reason: Older versions of Lightning _do_ have this attr # noqa: B950
        LightningLoggerBase as LightningLoggerBase,
    )
else:
    from pytorch_lightning.loggers import Logger as LightningLoggerBase  # noqa: F401
