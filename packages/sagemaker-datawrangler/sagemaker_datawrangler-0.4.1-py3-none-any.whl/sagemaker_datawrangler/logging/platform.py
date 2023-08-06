import json
import os

from sagemaker_datawrangler._version import version_info

LL_INTERNAL_METADATA_FILE = "/opt/.sagemakerinternal/internal-metadata.json"
KGW_APP_METADATA_FILE = "/opt/ml/metadata/resource-metadata.json"

PROD = "prod"
DEVO = "devo"


def _get_studio_metadata():
    """Read Studio metadata file from conventional place

    Returns: Studio metadata dictionary

    """
    if not os.path.exists(LL_INTERNAL_METADATA_FILE):
        return None

    with open(LL_INTERNAL_METADATA_FILE) as f:
        metadata = json.load(f)
    return metadata


def parse_app_arn(app_arn):
    """Parse arn and return region and accountId info
    Args:
        app_arn: an ARN string

    Returns: a dictionary

    """
    if not app_arn:
        return {}

    # app arn format arn:aws:sagemaker:us-east-2:583903115294:app/...
    splited = app_arn.split("/")[0].split(":")

    return {
        "Region": splited[3],
        "AccountId": splited[4],
    }


def _get_kgw_app_metadata():
    """Read Kernel Gateway App (KGW) metadata file from platform conventional place.

    Example format:
    ```
    {
      "AppType": "KernelGateway",
      "DomainId": "d-wbkeatwf4ga6",
      "UserProfileName": "default-1607568379370",
      "ResourceArn": "some arn",
      "ResourceName": "sagemaker-data-wrang-ml-m5-4xlarge-54eebb9b8b7e2055bdd94fd073ee",
      "AppImageVersion": ""
    }
    ```
    Returns: KGW metadata dictionary

    """
    if not os.path.exists(KGW_APP_METADATA_FILE):
        return None

    with open(KGW_APP_METADATA_FILE) as f:
        raw_metadata = json.load(f)

    # parse accountId and region from app ARN and extend the raw metadata
    return dict(raw_metadata, **parse_app_arn(raw_metadata.get("ResourceArn")))


def _get_application_stage(studio_metadata: dict):
    if studio_metadata is not None:
        return studio_metadata.get("Stage", PROD)
    return DEVO


def _get_default_app_context(app_metadata=None):
    app_context = {"ganymede_version": ".".join(map(str, version_info))}
    if app_metadata is not None:
        app_context["app_metadata"] = app_metadata
    return app_context


STUDIO_METADATA = _get_studio_metadata()
KGW_METADATA = _get_kgw_app_metadata()
APP_CONTEXT = _get_default_app_context(app_metadata=KGW_METADATA)
STAGE = _get_application_stage(STUDIO_METADATA)
