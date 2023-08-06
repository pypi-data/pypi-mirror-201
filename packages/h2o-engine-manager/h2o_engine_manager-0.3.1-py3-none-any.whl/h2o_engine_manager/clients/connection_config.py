import os
from typing import Callable, NamedTuple, Optional

import h2o_authn
import h2o_discovery
from h2o_engine_manager.clients.h2o_cli_config import CLIConfig

# Default path to h2o cli config file.
DEFAULT_CONFIG_PATH = "~/.h2oai/h2o-cli-config.toml"
# Name of the platform client in the discovery response.
PLATFORM_CLIENT_NAME = "platform"
# Name of the AIEM service in the discovery response.
AIEM_SERVICE_NAME = "engine-manager"


class ConnectionConfig(NamedTuple):
    """Object holding connection configuration for the AIEM server."""

    aiem_url: str
    token_provider: Callable[[], str]


def get_connection(
    aiem_url: str,
    refresh_token: str,
    issuer_url: str,
    client_id: str,
    client_secret: Optional[str] = None,
) -> ConnectionConfig:
    """Creates ConnectionConfig object. Initializes and tests token provider."""

    # init token provider
    tp = h2o_authn.TokenProvider(
        issuer_url=issuer_url,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
    )
    # test token refresh
    tp()

    return ConnectionConfig(aiem_url=aiem_url, token_provider=tp)


def discover_aiem_url(
    token_provider: Callable[[], str],
    environment_url: Optional[str] = None,
    config_path: str = DEFAULT_CONFIG_PATH,
) -> ConnectionConfig:
    """Creates ConnectionConfig object by discovering AIEM server URL. Tests given token provider.

    Args:
        token_provider (Callable[[], str]): Token provider. Must be initialized before calling this function.
        environment_url (str): URL of the env passed to discovery service. If left empty, the H2O CLI will be read.
        config_path (str): Path to the h2o cli config file. If not provided, the default path is used.
    """
    # Resolve environment_url value
    environment_url, _ = _resolve_config_with_cli_if_none(
        environment_url=environment_url, platform_token=None, config_path=config_path
    )

    # Read AIEM URL from discovery svc
    d = h2o_discovery.discover(environment=environment_url)
    aiem_url = d.services.get(AIEM_SERVICE_NAME).uri
    if not aiem_url:
        raise ConnectionError("Unable to discover AIEM server URL connection value.")

    # test token refresh
    token_provider()

    return ConnectionConfig(
        aiem_url=aiem_url,
        token_provider=token_provider,
    )


def discover_platform_connection(
    environment_url: Optional[str] = None,
    platform_token: Optional[str] = None,
    config_path: str = DEFAULT_CONFIG_PATH,
) -> ConnectionConfig:
    """Creates ConnectionConfig object by discovering platform connection configuration from the discovery server.
    Can be used to authorize against the platform OIDC client only.

    Args:
        environment_url (Optional[str]): URL of the env passed to discovery service. If left empty, the H2O CLI will be read.
        platform_token (Optional[str]): Platform token. If not provided, the token is read from the h2o cli config file.
        config_path (str): Path to the h2o cli config file. If not provided, the default path is used.

    """
    # Read H2O CLI config for environment_url, platform_token
    environment_url, platform_token = _resolve_config_with_cli_if_none(
        environment_url=environment_url,
        platform_token=platform_token,
        config_path=config_path,
    )

    # Discover AIEM server URL
    d = h2o_discovery.discover(environment=environment_url)
    aiem_url = d.services.get(AIEM_SERVICE_NAME).uri
    if not aiem_url:
        raise ConnectionError("Unable to discover AIEM server URL connection value.")

    if not platform_token:
        raise ValueError(
            "Please set the 'platform_token' argument or configure the H2O CLI."
        )

    # Init token provider
    client_id = d.clients.get(PLATFORM_CLIENT_NAME).oauth2_client_id
    if not client_id:
        raise ConnectionError(
            "Unable to discover platform oauth2_client_id connection value."
        )

    tp = h2o_authn.TokenProvider(
        issuer_url=d.environment.issuer_url,
        client_id=client_id,
        refresh_token=platform_token,
    )
    # Test token refresh
    tp()

    return ConnectionConfig(
        aiem_url=aiem_url,
        token_provider=tp,
    )


def _resolve_config_with_cli_if_none(
    environment_url: Optional[str] = None,
    platform_token: Optional[str] = None,
    config_path: str = DEFAULT_CONFIG_PATH,
):
    """Attempts to read H2O CLI config file for unset environment_url and platform_token values.
    Any error while reading the file is ignored and None values are returned if not already set.
    """
    # Resolve config_path
    if config_path == DEFAULT_CONFIG_PATH:
        config_path = os.path.abspath(os.path.expanduser(DEFAULT_CONFIG_PATH))

    cli_cfg = CLIConfig(config_path)

    # Resolve environment_url value
    if environment_url is None:
        environment_url = cli_cfg.url

    # Resolve platform_token value
    if platform_token is None:
        platform_token = cli_cfg.token

    return environment_url, platform_token
