from typing import List

from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.dai_version.dai_version import DAIVersion
from h2o_engine_manager.clients.dai_version.page import DAIVersionsPage
from h2o_engine_manager.clients.dai_version.token_api_client import (
    TokenApiDAIVersionClient,
)
from h2o_engine_manager.clients.exception import ApiException
from h2o_engine_manager.gen.dai_version_service import ApiException as GenApiException
from h2o_engine_manager.gen.dai_version_service.api.dai_version_service_api import (
    DAIVersionServiceApi,
)
from h2o_engine_manager.gen.dai_version_service.configuration import (
    Configuration as DAIVersionConfiguration,
)


class DAIVersionClient:
    """DAIVersionClient manages Driverless AI versions."""

    def __init__(self, connection_config: ConnectionConfig):
        """Initializes DAIVersionClient.

        Args:
            connection_config (ConnectionConfig): AIEM connection configuration object.
        """

        configuration_dai_version = DAIVersionConfiguration(
            host=connection_config.aiem_url
        )
        with TokenApiDAIVersionClient(
            configuration_dai_version, connection_config.token_provider
        ) as api_dai_version_client:
            self.api_version_instance = DAIVersionServiceApi(api_dai_version_client)

    def list_versions(
        self,
        page_size: int = 0,
        page_token: str = "",
        order_by: str = "",
        filter: str = "",
    ) -> DAIVersionsPage:
        exc = None
        list_response = None

        try:
            list_response = (
                self.api_version_instance.d_ai_version_service_list_dai_versions(
                    page_size=page_size,
                    page_token=page_token,
                    order_by=order_by,
                    filter=filter,
                )
            )
        except GenApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return DAIVersionsPage(list_response)

    def list_all_versions(
        self, order_by: str = "", filter: str = ""
    ) -> List[DAIVersion]:
        all_versions: List[DAIVersion] = []
        next_page_token = ""
        while True:
            versions_list = self.list_versions(
                page_size=0,
                page_token=next_page_token,
                order_by=order_by,
                filter=filter,
            )
            all_versions = all_versions + versions_list.dai_versions
            next_page_token = versions_list.next_page_token
            if next_page_token == "":
                break

        return all_versions
