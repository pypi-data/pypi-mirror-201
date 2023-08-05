#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
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
"""Initialization of the BentoML integration for ZenML.

The BentoML integration allows you to use the BentoML model serving
to implement continuous model deployment.
"""
from typing import List, Type

from zenml.integrations.constants import BENTOML
from zenml.integrations.integration import Integration
from zenml.stack import Flavor

BENTOML_MODEL_DEPLOYER_FLAVOR = "bentoml"


class BentoMLIntegration(Integration):
    """Definition of BentoML integration for ZenML."""

    NAME = BENTOML
    REQUIREMENTS = [
        "bentoml>=1.0.10",
    ]

    @classmethod
    def activate(cls) -> None:
        """Activate the BentoML integration."""
        from zenml.integrations.bentoml import materializers  # noqa
        from zenml.integrations.bentoml import model_deployers  # noqa
        from zenml.integrations.bentoml import services  # noqa
        from zenml.integrations.bentoml import steps  # noqa

    @classmethod
    def flavors(cls) -> List[Type[Flavor]]:
        """Declare the stack component flavors for KServe.

        Returns:
            List of stack component flavors for this integration.
        """
        from zenml.integrations.bentoml.flavors import (
            BentoMLModelDeployerFlavor,
        )

        return [BentoMLModelDeployerFlavor]


BentoMLIntegration.check_installation()
