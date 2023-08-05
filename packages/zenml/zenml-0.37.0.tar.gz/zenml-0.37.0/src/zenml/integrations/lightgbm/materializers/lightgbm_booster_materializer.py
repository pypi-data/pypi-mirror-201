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
"""Implementation of the LightGBM booster materializer."""

import os
import tempfile
from typing import Any, Type

import lightgbm as lgb

from zenml.enums import ArtifactType
from zenml.io import fileio
from zenml.materializers.base_materializer import BaseMaterializer

DEFAULT_FILENAME = "model.txt"


class LightGBMBoosterMaterializer(BaseMaterializer):
    """Materializer to read data to and from lightgbm.Booster."""

    ASSOCIATED_TYPES = (lgb.Booster,)
    ASSOCIATED_ARTIFACT_TYPE = ArtifactType.MODEL

    def load(self, data_type: Type[Any]) -> lgb.Booster:
        """Reads a lightgbm Booster model from a serialized JSON file.

        Args:
            data_type: A lightgbm Booster type.

        Returns:
            A lightgbm Booster object.
        """
        super().load(data_type)
        filepath = os.path.join(self.uri, DEFAULT_FILENAME)

        # Create a temporary folder
        temp_dir = tempfile.mkdtemp(prefix="zenml-temp-")
        temp_file = os.path.join(str(temp_dir), DEFAULT_FILENAME)

        # Copy from artifact store to temporary file
        fileio.copy(filepath, temp_file)
        booster = lgb.Booster(model_file=temp_file)

        # Cleanup and return
        fileio.rmtree(temp_dir)
        return booster

    def save(self, booster: lgb.Booster) -> None:
        """Creates a JSON serialization for a lightgbm Booster model.

        Args:
            booster: A lightgbm Booster model.
        """
        super().save(booster)

        filepath = os.path.join(self.uri, DEFAULT_FILENAME)

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = os.path.join(tmp_dir, "model.txt")
            booster.save_model(tmp_path)
            fileio.copy(tmp_path, filepath)
