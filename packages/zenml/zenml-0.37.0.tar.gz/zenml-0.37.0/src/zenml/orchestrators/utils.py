#  Copyright (c) ZenML GmbH 2021. All Rights Reserved.
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
"""Utility functions for the orchestrator."""

import random
from typing import TYPE_CHECKING, Dict, Optional
from uuid import UUID

from zenml.client import Client
from zenml.config.global_config import (
    CONFIG_ENV_VAR_PREFIX,
    GlobalConfiguration,
)
from zenml.constants import (
    ENV_ZENML_ACTIVE_STACK_ID,
    ENV_ZENML_ACTIVE_WORKSPACE_ID,
    ENV_ZENML_SECRETS_STORE_PREFIX,
    ENV_ZENML_STORE_PREFIX,
)
from zenml.logger import get_logger
from zenml.utils import uuid_utils

if TYPE_CHECKING:
    from zenml.orchestrators import BaseOrchestrator

logger = get_logger(__name__)


def get_orchestrator_run_name(pipeline_name: str) -> str:
    """Gets an orchestrator run name.

    This run name is not the same as the ZenML run name but can instead be
    used to display in the orchestrator UI.

    Args:
        pipeline_name: Name of the pipeline that will run.

    Returns:
        The orchestrator run name.
    """
    user_name = Client().active_user.name
    return f"{pipeline_name}_{user_name}_{random.Random().getrandbits(32):08x}"


def get_run_id_for_orchestrator_run_id(
    orchestrator: "BaseOrchestrator", orchestrator_run_id: str
) -> UUID:
    """Generates a run ID from an orchestrator run id.

    Args:
        orchestrator: The orchestrator of the run.
        orchestrator_run_id: The orchestrator run id.

    Returns:
        The run id generated from the orchestrator run id.
    """
    run_id_seed = f"{orchestrator.id}-{orchestrator_run_id}"
    return uuid_utils.generate_uuid_from_string(run_id_seed)


def is_setting_enabled(
    is_enabled_on_step: Optional[bool],
    is_enabled_on_pipeline: Optional[bool],
) -> bool:
    """Checks if a certain setting is enabled within a step run.

    This is the case if:
    - the setting is explicitly enabled for the step, or
    - the setting is neither explicitly disabled for the step nor the pipeline.

    Args:
        is_enabled_on_step: The setting of the step.
        is_enabled_on_pipeline: The setting of the pipeline.

    Returns:
        True if the setting is enabled within the step run, False otherwise.
    """
    if is_enabled_on_step is not None:
        return is_enabled_on_step
    if is_enabled_on_pipeline is not None:
        return is_enabled_on_pipeline
    return True


def get_config_environment_vars() -> Dict[str, str]:
    """Gets environment variables to set for mirroring the active config.

    Returns:
        Environment variable dict.
    """
    global_config = GlobalConfiguration()
    environment_vars = {}

    for key in global_config.__fields__.keys():
        if key == "store":
            continue

        value = getattr(global_config, key)
        if value is not None:
            environment_vars[CONFIG_ENV_VAR_PREFIX + key.upper()] = str(value)

    if global_config.store:
        store_dict = global_config.store.dict(exclude_none=True)
        secrets_store_dict = store_dict.pop("secrets_store", None) or {}

        for key, value in store_dict.items():
            if key == "password":
                # Don't include the password as we use the token to authenticate
                # with the server
                continue

            environment_vars[ENV_ZENML_STORE_PREFIX + key.upper()] = str(value)

        for key, value in secrets_store_dict.items():
            environment_vars[
                ENV_ZENML_SECRETS_STORE_PREFIX + key.upper()
            ] = str(value)

    # Make sure to use the correct active stack/workspace which might come
    # from a .zen repository and not the global config
    environment_vars[ENV_ZENML_ACTIVE_STACK_ID] = str(
        Client().active_stack_model.id
    )
    environment_vars[ENV_ZENML_ACTIVE_WORKSPACE_ID] = str(
        Client().active_workspace.id
    )

    return environment_vars
