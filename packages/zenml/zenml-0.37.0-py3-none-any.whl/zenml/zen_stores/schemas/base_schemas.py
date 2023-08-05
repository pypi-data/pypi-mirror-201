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
"""Base classes for SQLModel schemas."""

from datetime import datetime
from typing import TypeVar
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

from zenml.models.base_models import BaseResponseModel

B = TypeVar("B", bound=BaseResponseModel)


class BaseSchema(SQLModel):
    """Base SQL Model for ZenML entities."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)


class NamedSchema(BaseSchema):
    """Base Named SQL Model."""

    name: str


class ShareableSchema(NamedSchema):
    """Base shareable SQL Model."""

    is_shared: bool
