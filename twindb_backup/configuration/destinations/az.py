"""Azure Blob Storage destination configuration"""
import typing as t
from dataclasses import dataclass


# Parameters taken from:
# https://learn.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.containerclient?view=azure-python#keyword-only-parameters
@dataclass
class AZClientConfig:
    """Azure Blob Container Client Configuration

    Attributes:
        api_version (str, optional): The version of the Azure Storage API to use. Defaults to None.
        secondary_hostname (str, optional): The secondary hostname to use for the storage account. Defaults to None.
        max_block_size (int): The maximum size of a block in bytes. Defaults to 4MB.
        max_single_put_size (int): The maximum size of a single put operation in bytes. Defaults to 64MB.
        min_large_block_upload_threshold (int): The minimum size threshold for large block uploads in bytes.
            Defaults to 4MB + 1.
        use_byte_buffer (bool): Whether to use a byte buffer for uploads. Defaults to False.
        max_page_size (int): The maximum size of a page in bytes. Defaults to 4MB.
        max_single_get_size (int): The maximum size of a single get operation in bytes. Defaults to 32MB.
        max_chunk_get_size (int): The maximum size of a chunk in bytes for get operations. Defaults to 4MB.
        audience (str, optional): The audience for the Azure Storage account. Defaults to None.
    """

    api_version: t.Optional[str] = None
    secondary_hostname: t.Optional[str] = None
    max_block_size: int = 4 * 1024 * 1024  # 4MB
    max_single_put_size: int = 64 * 1024 * 1024  # 64MB
    min_large_block_upload_threshold: int = (4 * 1024 * 1024) + 1  # 4MB + 1
    use_byte_buffer: bool = False
    max_page_size: int = 4 * 1024 * 1024  # 4MB
    max_single_get_size: int = 32 * 1024 * 1024  # 32MB
    max_chunk_get_size: int = 4 * 1024 * 1024  # 4MB
    audience: t.Optional[str] = None

    def validate(self) -> None:
        """Validates the configuration parameters for the Azure destination.

        Raises:
            ValueError: Raises a ValueError if the type hint or value is incorrect for any of the parameters.
        """

        if self.api_version is not None and not isinstance(self.api_version, str):
            raise ValueError("api_version must be a string or undefined")
        if self.secondary_hostname is not None and not isinstance(self.secondary_hostname, str):
            raise ValueError("secondary_hostname must be a string or undefined")
        if not isinstance(self.max_block_size, int) or self.max_block_size <= 0:
            raise ValueError("max_block_size must be a positive integer")
        if not isinstance(self.max_single_put_size, int) or self.max_single_put_size <= 0:
            raise ValueError("max_single_put_size must be a positive integer")
        if not isinstance(self.min_large_block_upload_threshold, int) or self.min_large_block_upload_threshold <= 0:
            raise ValueError("min_large_block_upload_threshold must be a positive integer")
        if not isinstance(self.use_byte_buffer, bool):
            raise ValueError("use_byte_buffer must be a boolean")
        if not isinstance(self.max_page_size, int) or self.max_page_size <= 0:
            raise ValueError("max_page_size must be a positive integer")
        if not isinstance(self.max_single_get_size, int) or self.max_single_get_size <= 0:
            raise ValueError("max_single_get_size must be a positive integer")
        if not isinstance(self.max_chunk_get_size, int) or self.max_chunk_get_size <= 0:
            raise ValueError("max_chunk_get_size must be a positive integer")
        if self.audience is not None and not isinstance(self.audience, str):
            raise ValueError("audience must be a string or undefined")

    def __post_init__(self) -> None:
        self.validate()


@dataclass
class AZConfig:
    """Azure Blob Storage Configuration

    Attributes:
        client_config (AZClientConfig): Configuration for the Azure Blob Container Client.
        connection_string (str): Connection string for the Azure storage account.
        container_name (str): Name of the container in the Azure storage account.
        remote_path (str, optional): Remote base path in the container to store backups. Defaults to "/".
    """

    client_config: AZClientConfig
    connection_string: str
    container_name: str
    remote_path: str = "/"

    def validate(self) -> None:
        """Validates the configuration parameters for the Azure destination.

        Raises:
            ValueError: Raises a ValueError if the type hint or value is incorrect for any of the parameters.
        """

        if not isinstance(self.client_config, AZClientConfig):
            raise ValueError("client_config must be an instance of AZClientConfig")
        if not isinstance(self.connection_string, str):
            raise ValueError("connection_string must be a string")
        if not isinstance(self.container_name, str):
            raise ValueError("container_name must be a string")
        if not isinstance(self.remote_path, str):
            raise ValueError("remote_path must be a string")

    def __post_init__(self) -> None:
        self.validate()
        self.remote_path = self.remote_path.strip("/") if self.remote_path != "/" else self.remote_path


def drop_empty_dict_factory(d):
    """Drop empty values from a dictionary"""
    return {k: v for k, v in d if v is not None}
