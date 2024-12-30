import socket
from dataclasses import asdict
from unittest.mock import MagicMock, patch

import azure.core.exceptions as ae
import pytest
from azure.storage.blob import ContainerClient

import twindb_backup.destination.az as az
from twindb_backup.configuration.destinations.az import AZClientConfig, AZConfig, drop_empty_dict_factory

from .util import AZClientConfigParams, AZConfigParams


def test_init_param():
    """Test initialization of AZ with all parameters set, mocking the _connect method."""
    with patch("twindb_backup.destination.az.AZ._connect") as mc:
        mc.return_value = MagicMock(spec=ContainerClient)

        client_params = AZClientConfigParams()
        config_params = AZConfigParams()
        client_config = AZClientConfig(**dict(client_params))
        config = AZConfig(client_config=client_config, **dict(config_params))

        c = az.AZ(config=config)

        assert isinstance(c.container_client, ContainerClient)
        az.AZ._connect.assert_called_once()


def test_init_param_defaults():
    """Test initialization of AZ with only required parameters set, ensuring default values, mocking the _connect method."""
    with patch("twindb_backup.destination.az.AZ._connect") as mc:
        mc.return_value = MagicMock(spec=ContainerClient)

        client_params = AZClientConfigParams()
        config_params = AZConfigParams()
        client_config = AZClientConfig(**dict(client_params))
        config = AZConfig(client_config=client_config, **dict(config_params))

        c = az.AZ(config=config)

        assert isinstance(c.container_client, ContainerClient)
        az.AZ._connect.assert_called_once()


def test_init_conn_string_valid():
    """Test initialization of AZ with valid connection string."""
    with patch("twindb_backup.destination.az.ContainerClient.exists") as mc:
        mc.return_value = True

        client_params = AZClientConfigParams()
        config_params = AZConfigParams()
        client_config = AZClientConfig(**dict(client_params))
        config = AZConfig(client_config=client_config, **dict(config_params))

        c = az.AZ(config=config)

        az.ContainerClient.exists.assert_called_once()
        assert isinstance(c.container_client, ContainerClient)


def test_init_conn_string_invalid():
    """Test initialization of AZ with invalid connection string, expecting ValueError."""
    with patch("twindb_backup.destination.az.ContainerClient.exists") as mc:
        mc.return_value = True

        client_params = AZClientConfigParams()
        config_params = AZConfigParams()
        client_config = AZClientConfig(**dict(client_params))
        config = AZConfig(client_config=client_config, **dict(config_params))
        config.connection_string = "invalid_connection_string"

        with pytest.raises(ValueError, match="Connection string is either blank or malformed."):
            _ = az.AZ(config=config)


def test_init_container_not_exists():
    """Test initialization of AZ with container not existing, mocking the create_container method."""
    with patch("twindb_backup.destination.az.ContainerClient.exists") as mc:
        mc.return_value = False
        with patch("twindb_backup.destination.az.ContainerClient.create_container") as mc_create_container:
            mc_create_container.return_value = MagicMock(spec=ContainerClient)

            client_params = AZClientConfigParams()
            config_params = AZConfigParams()
            client_config = AZClientConfig(**dict(client_params))
            config = AZConfig(client_config=client_config, **dict(config_params))

            c = az.AZ(config=config)

            az.ContainerClient.exists.assert_called_once()
            az.ContainerClient.create_container.assert_called_once()
            assert isinstance(c.container_client, ContainerClient)


def test_init_container_create_fails():
    """Test initialization of AZ with container not existing, fails to create container, re-raising error."""
    with patch("twindb_backup.destination.az.ContainerClient.exists") as mc:
        mc.return_value = False
        with patch("twindb_backup.destination.az.ContainerClient.create_container") as mc_create_container:
            mc_create_container.side_effect = ae.HttpResponseError()

            client_params = AZClientConfigParams()
            config_params = AZConfigParams()
            client_config = AZClientConfig(**dict(client_params))
            config = AZConfig(client_config=client_config, **dict(config_params))

            with pytest.raises(Exception):
                c = az.AZ(config=config)

                az.ContainerClient.exists.assert_called_once()
                az.ContainerClient.create_container.assert_called_once()
                assert isinstance(c.container_client, ContainerClient)


def test_init_success():
    """Test initialization of AZ with existing container, mocking the from_connection_string method."""
    with patch("twindb_backup.destination.az.ContainerClient.from_connection_string") as mc:
        mc.return_value = MagicMock(spec=ContainerClient)

        client_params = AZClientConfigParams()
        config_params = AZConfigParams()
        client_config = AZClientConfig(**dict(client_params))
        config = AZConfig(client_config=client_config, **dict(config_params))

        c = az.AZ(config=config)

        az.ContainerClient.from_connection_string.assert_called_once_with(
            conn_str=config.connection_string,
            container_name=config.container_name,
            **asdict(config.client_config, dict_factory=drop_empty_dict_factory)
        )
        mc.return_value.exists.assert_called_once()
        mc.return_value.create_container.assert_not_called()
        assert isinstance(c.container_client, ContainerClient)
