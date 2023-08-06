"""
Wrapper for retrieving configurations and safely logging their retrieval
"""
import re

from pydantic import BaseModel
from pydantic import BaseSettings
from pydantic import Field

from dkist_service_configuration.logging import logger


class ConfigurationBase(BaseSettings):
    """Settings base which logs configured settings while censoring secrets"""

    log_level: str = Field("INFO", env="LOGURU_LEVEL")

    class Config:
        secret_patterns: tuple = ("pass", "secret", "token")

    def _is_secret(self, field_name: str) -> bool:
        for pattern in self.Config.secret_patterns:
            if re.search(pattern, field_name):
                return True
        return False

    def log_configurations(self):
        for field_name in self.__fields__:
            if self._is_secret(field_name=field_name):
                logger.info(f"{field_name}: <CENSORED>")
            logger.info(f"{field_name}: {getattr(self, field_name)}")


class MeshService(BaseModel):
    """Model of the metadata for a node in the service mesh"""

    host: str = Field(..., alias="mesh_address")
    port: int = Field(..., alias="mesh_port")


class MeshServiceConfigurationBase(ConfigurationBase):
    """
    Settings base for services using a mesh configuration to define connections in the form
    {
        "upstream_service_name": {"mesh_address": "localhost", "mesh_port": 6742}
    }
    """

    service_mesh: dict[str, MeshService] = Field(default_factory=dict, env="MESH_CONFIG")

    def service_mesh_detail(self, service_name) -> MeshService | None:
        return self.service_mesh.get(service_name)
