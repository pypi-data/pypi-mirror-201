# Copyright 2023 SOTAI Labs Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""PyTorch implementation of calibrated modeling."""
# This version must always be one version ahead of the current release, so it
# matches the current state of development, which will always be ahead of the
# current release.
#
# NOTE: as part of the release flow, update this version immediately after release.
__version__ = "0.0.0"

from pytorch_calibrated import configs, data, enums, layers, models

__all__ = ["configs", "data", "enums", "layers", "models"]
