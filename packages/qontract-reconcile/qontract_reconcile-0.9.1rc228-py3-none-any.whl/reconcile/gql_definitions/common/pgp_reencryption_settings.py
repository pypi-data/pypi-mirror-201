"""
Generated by qenerate plugin=pydantic_v1. DO NOT MODIFY MANUALLY!
"""
from collections.abc import Callable  # noqa: F401 # pylint: disable=W0611
from datetime import datetime  # noqa: F401 # pylint: disable=W0611
from enum import Enum  # noqa: F401 # pylint: disable=W0611
from typing import (  # noqa: F401 # pylint: disable=W0611
    Any,
    Optional,
    Union,
)

from pydantic import (  # noqa: F401 # pylint: disable=W0611
    BaseModel,
    Extra,
    Field,
    Json,
)


DEFINITION = """
query PgpReencryptionSettings {
  pgp_reencryption_settings: pgp_reencrypt_settings_v1{
    public_gpg_key
    aws_account_output_vault_path
    reencrypt_vault_path
    skip_aws_accounts {
      name
    }
  }
}
"""


class ConfiguredBaseModel(BaseModel):
    class Config:
        smart_union = True
        extra = Extra.forbid


class AWSAccountV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")


class PgpReencryptSettingsV1(ConfiguredBaseModel):
    public_gpg_key: str = Field(..., alias="public_gpg_key")
    aws_account_output_vault_path: str = Field(
        ..., alias="aws_account_output_vault_path"
    )
    reencrypt_vault_path: str = Field(..., alias="reencrypt_vault_path")
    skip_aws_accounts: Optional[list[AWSAccountV1]] = Field(
        ..., alias="skip_aws_accounts"
    )


class PgpReencryptionSettingsQueryData(ConfiguredBaseModel):
    pgp_reencryption_settings: Optional[list[PgpReencryptSettingsV1]] = Field(
        ..., alias="pgp_reencryption_settings"
    )


def query(query_func: Callable, **kwargs: Any) -> PgpReencryptionSettingsQueryData:
    """
    This is a convenience function which queries and parses the data into
    concrete types. It should be compatible with most GQL clients.
    You do not have to use it to consume the generated data classes.
    Alternatively, you can also mime and alternate the behavior
    of this function in the caller.

    Parameters:
        query_func (Callable): Function which queries your GQL Server
        kwargs: optional arguments that will be passed to the query function

    Returns:
        PgpReencryptionSettingsQueryData: queried data parsed into generated classes
    """
    raw_data: dict[Any, Any] = query_func(DEFINITION, **kwargs)
    return PgpReencryptionSettingsQueryData(**raw_data)
