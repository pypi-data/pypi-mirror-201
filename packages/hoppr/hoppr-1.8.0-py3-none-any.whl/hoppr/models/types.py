"""
Enumeration to indicate how a plugin may change a BOM
"""
from __future__ import annotations

from typing import Any

from hoppr_cyclonedx_models.cyclonedx_1_4 import Component
from hoppr_cyclonedx_models.cyclonedx_1_4 import CyclonedxSoftwareBillOfMaterialsStandard as Bom  # type: ignore[import]
from pydantic_yaml import YamlIntEnum, YamlStrEnum


class BomAccess(YamlIntEnum):
    """
    Enumeration to indicate how a plugin may change a BOM
    """

    # pylint: disable=duplicate-code
    NO_ACCESS = 0
    COMPONENT_ACCESS = 1
    FULL_ACCESS = 2

    def has_access_to(self, obj: Any) -> bool:
        """
        Determine whether the specified value allows updates to an object
        """
        match self:
            case BomAccess.NO_ACCESS:
                return obj is None
            case BomAccess.COMPONENT_ACCESS:
                return isinstance(obj, Component)
            case BomAccess.FULL_ACCESS:
                return isinstance(obj, Bom)


class PurlType(YamlStrEnum):
    """
    Enumeration of supported purl types
    """

    # pylint: disable=duplicate-code
    DEB = "deb"
    DOCKER = "docker"
    GENERIC = "generic"
    GIT = "git"
    GITHUB = "github"
    GITLAB = "gitlab"
    GOLANG = "golang"
    HELM = "helm"
    MAVEN = "maven"
    NPM = "npm"
    PYPI = "pypi"
    REPO = "repo"
    RPM = "rpm"
