from enum import Enum
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, root_validator


class StorageIntegrationType(str, Enum):
    STORAGE_INTEGRATION = "STORAGE_INTEGRATION"


class IntegrationProvider(str, Enum):
    AWS_S3 = "aws-s3"
    GCP_GCS = "gcp-gcs"
    AZURE_BLOB = "azure-blob"


class StorageIntegrationMetadata(BaseModel):
    storageRoot: str


class GCSCredentials(BaseModel):
    class Config:
        extra = "allow"

    keyFileContent: Dict[str, Any]


class AWSS3Credentials(BaseModel):
    awsAccessKeyId: str
    awsSecretAccessKey: str
    region: Optional[str] = None


class StorageIntegration(BaseModel):
    class Config:
        extra = "allow"

    id: str
    name: str
    fqn: str
    tenantName: str
    type: StorageIntegrationType
    integrationProvider: IntegrationProvider

    metaData: StorageIntegrationMetadata
    authData: Optional[Union[AWSS3Credentials, GCSCredentials]] = None

    @root_validator(pre=True)
    def check_empty_auth_data(cls, values):
        if not values.get("authData"):
            values["authData"] = None
        return values

    @root_validator()
    def check_auth_data(cls, values):
        if not values.get("authData"):
            return values
        if values["integrationProvider"] == IntegrationProvider.AWS_S3:
            if not isinstance(values["authData"], AWSS3Credentials):
                raise ValueError("authData must be of type AWSS3Credentials")
        elif values["integrationProvider"] == IntegrationProvider.GCP_GCS:
            if not isinstance(values["authData"], GCSCredentials):
                raise ValueError("authData must be of type GCSCredentials")
        return values
