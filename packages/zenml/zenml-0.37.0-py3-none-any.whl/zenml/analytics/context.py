#  Copyright (c) ZenML GmbH 2023. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""The analytics module of ZenML.

This module is based on the 'analytics-python' package created by Segment.
The base functionalities are adapted to work with the ZenML analytics server.
"""
from types import TracebackType
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union
from uuid import UUID

from zenml import __version__, analytics
from zenml.constants import ENV_ZENML_SERVER, handle_bool_env_var
from zenml.environment import Environment, get_environment
from zenml.logger import get_logger

if TYPE_CHECKING:
    from zenml.models.server_models import (
        ServerDatabaseType,
        ServerDeploymentType,
    )
    from zenml.utils.analytics_utils import AnalyticsEvent

Json = Union[Dict[str, Any], List[Any], str, int, float, bool, None]

logger = get_logger(__name__)


class AnalyticsContext:
    """Client class for ZenML Analytics v2."""

    def __init__(self) -> None:
        """Initialization.

        Use this as a context manager to ensure that analytics are initialized
        properly, only tracked when configured to do so and that any errors
        are handled gracefully.
        """
        self.analytics_opt_in: bool = False

        self.user_id: Optional[UUID] = None
        self.client_id: Optional[UUID] = None
        self.server_id: Optional[UUID] = None

        self.database_type: Optional["ServerDatabaseType"] = None
        self.deployment_type: Optional["ServerDeploymentType"] = None

    @property
    def in_server(self) -> bool:
        """Flag to check whether the code is running in a ZenML server.

        Returns:
            True if running in a server, False otherwise.
        """
        return handle_bool_env_var(ENV_ZENML_SERVER)

    def __enter__(self) -> "AnalyticsContext":
        """Enter analytics context manager.

        Returns:
            The analytics context.
        """
        # Fetch the analytics opt-in setting
        from zenml.config.global_config import GlobalConfiguration

        gc = GlobalConfiguration()
        self.analytics_opt_in = gc.analytics_opt_in

        if not self.analytics_opt_in:
            return self

        try:
            # Fetch the `user_id`
            if self.in_server:
                from zenml.zen_server.auth import get_auth_context

                # If the code is running on the server, use the auth context.
                auth_context = get_auth_context()
                if auth_context is not None:
                    self.user_id = auth_context.user.id
            else:
                # If the code is running on the client, use the default user.
                default_user = gc.zen_store.get_user()
                self.user_id = default_user.id

            # Fetch the `client_id`
            if self.in_server:
                # If the code is running on the server, there is no client id.
                self.client_id = None
            else:
                # If the code is running on the client, attach the client id.
                self.client_id = gc.user_id

            # Fetch the store information including the `server_id`
            store_info = gc.zen_store.get_store_info()

            self.server_id = store_info.id
            self.deployment_type = store_info.deployment_type
            self.database_type = store_info.database_type
        except Exception as e:
            self.analytics_opt_in = False
            logger.debug(f"Analytics initialization failed: {e}")

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        """Exit context manager.

        Args:
            exc_type: Exception type.
            exc_val: Exception value.
            exc_tb: Exception traceback.

        Returns:
            True.
        """
        if exc_val is not None:
            logger.debug(f"Sending telemetry 2.0 data failed: {exc_val}")

        return True

    def identify(self, traits: Optional[Dict[str, Any]] = None) -> bool:
        """Identify the user through segment.

        Args:
            traits: Traits of the user.

        Returns:
            True if tracking information was sent, False otherwise.
        """
        success = False
        if self.analytics_opt_in and self.user_id is not None:
            success, _ = analytics.identify(
                user_id=self.user_id,
                traits=traits,
            )

        return success

    def group(
        self,
        group_id: UUID,
        traits: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Group the user.

        Args:
            group_id: Group ID.
            traits: Traits of the group.

        Returns:
            True if tracking information was sent, False otherwise.
        """
        success = False
        if self.analytics_opt_in and self.user_id is not None:
            if traits is None:
                traits = {}

            traits.update({"group_id": group_id})

            success, _ = analytics.group(
                user_id=self.user_id,
                group_id=group_id,
                traits=traits,
            )

        return success

    def track(
        self,
        event: "AnalyticsEvent",
        properties: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Track an event.

        Args:
            event: Event to track.
            properties: Event properties.

        Returns:
            True if tracking information was sent, False otherwise.
        """
        from zenml.utils.analytics_utils import AnalyticsEvent

        if properties is None:
            properties = {}

        if (
            not self.analytics_opt_in
            and event.value
            not in {
                AnalyticsEvent.OPT_OUT_ANALYTICS,
                AnalyticsEvent.OPT_IN_ANALYTICS,
            }
            or self.user_id is None
        ):
            return False

        # add basics
        properties.update(Environment.get_system_info())
        properties.update(
            {
                "environment": get_environment(),
                "python_version": Environment.python_version(),
                "version": __version__,
                "client_id": str(self.client_id),
                "user_id": str(self.user_id),
                "server_id": str(self.server_id),
                "deployment_type": str(self.deployment_type),
                "database_type": str(self.database_type),
            }
        )

        for k, v in properties.items():
            if isinstance(v, UUID):
                properties[k] = str(v)

        success, _ = analytics.track(
            user_id=self.user_id,
            event=event,
            properties=properties,
        )

        logger.debug(
            f"Sending analytics: User: {self.user_id}, Event: {event}, "
            f"Metadata: {properties}"
        )

        return success
