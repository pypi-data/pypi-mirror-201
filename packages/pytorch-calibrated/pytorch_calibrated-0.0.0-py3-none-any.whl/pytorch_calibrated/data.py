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
"""Useful classes and functions for handling data for calibrated modeling."""
from typing import Generator, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import torch
from absl import logging

from .configs import CategoricalFeatureConfig, NumericalFeatureConfig
from .enums import FeatureType


class CSVData:
    """Class for handling CSV data for calibrated modeling.

    Attributes:
        - All `__init__` arguments.
        data: A pandas `DataFrame` containing the loaded CSV data.
        headers: The list of headers available from the loaded data.
        num_examples: The number of examples in the dataset.
        prepared_data: The prepared data. This will be `None` if `prepare(...)` has not
            been called.

    Example:

    ```python
    csv_data = CSVData("path/to/data.csv")
    feature_configs = [
        NumericalFeatureConfig(
            feature_name="numerical_feature"
            data=csv_data("numerical_feature")  # must match feature column header
        ),
        CategoricalFeatureConfig(
            feature_name="categorical_feature"
            categories=np.unique(csv_data("categorical_feature"))  # uses all categories
        ),
    ]
    csv_data.prepare(feature_configs, "target", ...)  # must match target column header
    for examples, labels in csv_data.batch(64):
        training_step(...)
    ```
    """

    def __init__(
        self,
        dataset: Union[str, pd.DataFrame],
    ) -> None:
        """Initializes an instance of `CSVData`.

        Loads a CSV file if filepath is provided. Otherwise it will use the provided
        DataFrame.

        Args:
            dataset: Either a string filepath pointing to the CSV data that should be
                loaded or a `pd.DataFrame` containing the data that should be used.
                The CSV file or DataFrame must have a header.
        """
        self.dataset = dataset
        if isinstance(dataset, str):
            self.data = pd.read_csv(dataset)
        else:
            self.data = dataset.copy()
        self.headers = list(self.data.columns)
        self.num_examples = len(self.data)
        self.prepared_data = None
        self._prepared_data_tensor, self._targets_tensor = None, None

    def __call__(self, header: str, prepared: bool = False) -> np.ndarray:
        """Selects the data for the column with the given header.

        Args:
            header: The header of the column for which data is selected.

        Returns:
            The selected data as a numpy array.

        Raises:
            ValueError: If the provided header is not available in the data.
            ValueError: If `prepared` is true but `prepare(...)` has not been called.
        """
        if not header in self.headers:
            raise ValueError(f"Column {header} does not exist: {self.headers}.")
        if prepared:
            if self.prepared_data is None:
                raise ValueError(
                    "CSV.prepare(...) must be called first for prepared data."
                )
            return self.prepared_data[header].to_numpy()
        return self.data[header].to_numpy()

    def prepare(
        self,
        feature_configs: List[Union[NumericalFeatureConfig, CategoricalFeatureConfig]],
        target_header: Optional[str],
        inplace: bool = True,
    ) -> None:
        """Prepares the data for calibrated modeling.

        Args:
            feature_configs: Feature configs that specify how to prepare the data.
            target_header: The header for the target column. If `None`, it will be
                assumed that there is no target column present (e.g. for inference)
            inplace: If True, original `data` attribute will be updated. If False, a
                copy of the original data will be prepared and the original will be
                preserved.

        Raises:
            ValueError: If a feature in `feature_configs` is not in the dataset.
        """
        if self.prepared_data is not None:
            logging.info("Prepare has already been called. Doing nothing.")
            return
        selected_features = [
            feature_config.feature_name for feature_config in feature_configs
        ]
        unavailable_features = set(selected_features) - set(self.data.columns)
        if len(unavailable_features) > 0:
            raise ValueError(f"Features {unavailable_features} not found in dataset.")
        self.prepared_data = self.data if inplace else self.data.copy()
        for feature_config in feature_configs:
            if feature_config.feature_type == FeatureType.CATEGORICAL:
                feature_data = self.prepared_data[feature_config.feature_name].map(
                    feature_config.category_indices
                )
                if feature_config.missing_input_value is not None:
                    feature_data = feature_data.fillna(
                        feature_config.missing_input_value
                    )
                self.prepared_data[feature_config.feature_name] = feature_data
        if target_header is not None:
            self._targets_tensor = torch.from_numpy(
                self.prepared_data.pop(target_header).values
            )[:, None].double()
        self._prepared_data_tensor = torch.from_numpy(
            self.prepared_data[selected_features].values
        ).double()

    def batch(
        self, batch_size: int
    ) -> Generator[Union[Tuple[torch.Tensor, torch.Tensor], torch.Tensor], None, None]:
        """A generator that yields a tensor with `batch_size` examples.

        Args:
            batch_size: The size of each batch returns during each iteration.

        Yields:
            If prepared with a target column: a tuple (examples, targets) of
                `torch.Tensor` of shape `(batch_size, num_features)` and
                `(batch_size, 1)`, repsectively.
            If prepared without a target column: a `torch.Tensor` of shape
                `(batch_size, num_features)`.

        Raises:
            ValueError: If `prepare(...)` is not called first.
        """
        if self.prepared_data is None:
            raise ValueError("CSVData.prepare(...) must be called first.")

        for i in range(0, self.num_examples, batch_size):
            if self._targets_tensor is not None:
                yield (
                    self._prepared_data_tensor[i : i + batch_size],
                    self._targets_tensor[i : i + batch_size],
                )
            else:
                yield self._prepared_data_tensor[i : i + batch_size]
