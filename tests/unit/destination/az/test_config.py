from dataclasses import asdict

import pytest

from twindb_backup.configuration.destinations.az import AZClientConfig, AZConfig, drop_empty_dict_factory

from .util import AZClientConfigParams, AZConfigParams


def test_initialization_success():
    """Test initialization of AZConfig with all parameters set."""
    client_params = AZClientConfigParams()
    config_params = AZConfigParams()
    client_config = AZClientConfig(**dict(client_params))

    c = AZConfig(client_config=client_config, **dict(config_params))

    # AZConfig Assertions
    assert c.client_config == client_config
    assert c.connection_string == config_params.connection_string
    assert c.container_name == config_params.container_name
    assert (
        c.remote_path == config_params.remote_path.strip("/")
        if config_params.remote_path != "/"
        else config_params.remote_path
    )
    assert c.max_concurrency == config_params.max_concurrency

    # AZClientConfig Assertions
    assert c.client_config.api_version == client_params.api_version
    assert c.client_config.secondary_hostname == client_params.secondary_hostname
    assert c.client_config.max_block_size == client_params.max_block_size
    assert c.client_config.max_single_put_size == client_params.max_single_put_size
    assert c.client_config.min_large_block_upload_threshold == client_params.min_large_block_upload_threshold
    assert c.client_config.use_byte_buffer == client_params.use_byte_buffer
    assert c.client_config.max_page_size == client_params.max_page_size
    assert c.client_config.max_single_get_size == client_params.max_single_get_size
    assert c.client_config.max_chunk_get_size == client_params.max_chunk_get_size
    assert c.client_config.audience == client_params.audience
    assert c.client_config.connection_timeout == client_params.connection_timeout


def test_initialization_success_defaults():
    """Test initialization of AZConfig with only required parameters set and ensure default values."""
    client_params = AZClientConfigParams(only_required=True)
    config_params = AZConfigParams(only_required=True)
    client_config = AZClientConfig(**dict(client_params))

    c = AZConfig(client_config=client_config, **dict(config_params))

    # AZConfig Assertions
    assert c.client_config == client_config
    assert c.connection_string == config_params.connection_string
    assert c.container_name == config_params.container_name
    assert c.remote_path == "/"
    assert c.max_concurrency == 1

    # AZClientConfig Assertions
    assert c.client_config.api_version == None
    assert c.client_config.secondary_hostname == None
    assert c.client_config.max_block_size == 4 * 1024 * 1024  # 4MB
    assert c.client_config.max_single_put_size == 64 * 1024 * 1024  # 64MB
    assert c.client_config.min_large_block_upload_threshold == (4 * 1024 * 1024) + 1  # 4MB + 1
    assert c.client_config.use_byte_buffer == False
    assert c.client_config.max_page_size == 4 * 1024 * 1024  # 4MB
    assert c.client_config.max_single_get_size == 32 * 1024 * 1024  # 32MB
    assert c.client_config.max_chunk_get_size == 4 * 1024 * 1024  # 4MB
    assert c.client_config.audience == None
    assert c.client_config.connection_timeout == 20


def test_invalid_params():
    """Test initialization of AZConfig with invalid parameters."""

    # Invalidate AZConfig
    with pytest.raises(ValueError):  # Invalid client_config
        AZConfig(client_config={}, connection_string="test_connection_string", container_name="test_container")
    with pytest.raises(ValueError):  # Invalid connection_string
        AZConfig(client_config=AZClientConfig(), connection_string=123, container_name="test_container")
    with pytest.raises(ValueError):  # Invalid remote_path
        AZConfig(
            client_config=AZClientConfig(),
            connection_string="test_connection_string",
            container_name="test_container",
            remote_path=1,
        )
    with pytest.raises(ValueError):  # Invalid container_name
        AZConfig(client_config=AZClientConfig(), connection_string="test_connection_string", container_name=1)
    with pytest.raises(ValueError):  # Invalid max_concurrency
        AZConfig(
            client_config=AZClientConfig(),
            connection_string="test_connection_string",
            container_name="test_container",
            max_concurrency="1",
        )

    # Invalidate AZClientConfig
    with pytest.raises(ValueError):  # Invalid api_version
        AZClientConfig(api_version=123)
    with pytest.raises(ValueError):  # Invalid secondary_hostname
        AZClientConfig(secondary_hostname=123)
    with pytest.raises(ValueError):  # Invalid max_block_size
        AZClientConfig(max_block_size="123")
    with pytest.raises(ValueError):  # Invalid max_single_put_size
        AZClientConfig(max_single_put_size="123")
    with pytest.raises(ValueError):  # Invalid min_large_block_upload_threshold
        AZClientConfig(min_large_block_upload_threshold="123")
    with pytest.raises(ValueError):  # Invalid use_byte_buffer
        AZClientConfig(use_byte_buffer="123")
    with pytest.raises(ValueError):  # Invalid max_page_size
        AZClientConfig(max_page_size="123")
    with pytest.raises(ValueError):  # Invalid max_single_get_size
        AZClientConfig(max_single_get_size="123")
    with pytest.raises(ValueError):  # Invalid max_chunk_get_size
        AZClientConfig(max_chunk_get_size="123")
    with pytest.raises(ValueError):  # Invalid audience
        AZClientConfig(audience=123)
    with pytest.raises(ValueError):  # Invalid connection_timeout
        AZClientConfig(connection_timeout="123")


def test_drop_empty_dicts_some_undefined():
    """Test drop_empty_dict_factory helper function."""

    client_config = AZClientConfig(**dict(AZClientConfigParams(only_required=True)))

    # Convert to dict and drop attributes with None values
    client_config_dict = asdict(client_config, dict_factory=drop_empty_dict_factory)

    # Assert that the dict does not contain any None values
    assert "api_version" not in client_config_dict
    assert "secondary_hostname" not in client_config_dict
    assert "audience" not in client_config_dict


def test_drop_empty_dicts_all_defined():
    """Test drop_empty_dict_factory helper function doesn't drop any attributes when all are defined."""

    client_config = AZClientConfig(**dict(AZClientConfigParams()))

    # Convert to dict and drop attributes with None values
    client_config_dict_drop_empty = asdict(client_config, dict_factory=drop_empty_dict_factory)

    # Convert to dict
    client_config_dict = asdict(client_config)

    # Assert that the dicts are the same
    assert client_config_dict == client_config_dict_drop_empty
