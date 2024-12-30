import collections
from unittest.mock import MagicMock, patch

from azure.storage.blob import ContainerClient

import twindb_backup.destination.az as az
from twindb_backup.configuration.destinations.az import AZClientConfig, AZConfig


class AZClientConfigParams(collections.Mapping):
    def __init__(self, only_required=False) -> None:

        if not only_required:
            self.api_version = "2021-04-10"
            self.secondary_hostname = "secondary.example.com"
            self.max_block_size = 128 * 1024 * 1024  # 128MB
            self.max_single_put_size = 128 * 1024 * 1024  # 128MB
            self.min_large_block_upload_threshold = 128 * 1024 * 1024  # 128MB
            self.use_byte_buffer = False
            self.max_page_size = 128 * 1024 * 1024  # 128MB
            self.max_single_get_size = 128 * 1024 * 1024  # 128MB
            self.max_chunk_get_size = 128 * 1024 * 1024  # 128MB
            self.audience = "https://example.com"

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__[key]


class AZConfigParams(collections.Mapping):
    def __init__(self, only_required=False) -> None:
        self.container_name = "test_container"
        self.connection_string = "DefaultEndpointsProtocol=https;AccountName=ACCOUNT_NAME;AccountKey=ACCOUNT_KEY;EndpointSuffix=core.windows.net"

        if not only_required:
            self.remote_path = "/himom/"

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__[key]


def mocked_az():
    with patch("twindb_backup.destination.az.AZ._connect") as mc:
        mc.return_value = MagicMock(spec=ContainerClient)

        client_params = AZClientConfigParams()
        config_params = AZConfigParams()

        az_config = AZConfig(client_config=AZClientConfig(**dict(client_params)), **dict(config_params))

        c = az.AZ(config=az_config)

    return c
