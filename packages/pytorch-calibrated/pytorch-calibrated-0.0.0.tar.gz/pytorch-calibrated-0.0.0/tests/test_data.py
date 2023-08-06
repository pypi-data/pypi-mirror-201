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
"""Tests for data utilities."""
import unittest
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd
import torch
from absl.testing import parameterized

from pytorch_calibrated.configs import CategoricalFeatureConfig, NumericalFeatureConfig
from pytorch_calibrated.data import CSVData


# pylint: disable-next=missing-class-docstring
class TestCSVData(parameterized.TestCase, unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Creates a base data file for all of the tests to use."""
        cls.numerical_data = {"header": "numerical", "data": np.array([1, 2, 3, 4])}
        cls.categorical_data = {
            "header": "categorical",
            "data": np.array(["a", "b", "c", "d"]),
        }
        cls.target_data = {"header": "target", "data": np.array([0.2, 0.5, 0.4, 0.9])}
        cls.data = pd.DataFrame(
            {
                cls.numerical_data["header"]: cls.numerical_data["data"],
                cls.categorical_data["header"]: cls.categorical_data["data"],
                cls.target_data["header"]: cls.target_data["data"],
                "unknown": cls.numerical_data["data"],
            }
        )
        cls.headers = list(cls.data.columns)
        cls.tempdir = TemporaryDirectory()  # pylint: disable=consider-using-with
        cls.datapath = f"{cls.tempdir.name}/test_data.csv"
        cls.data.to_csv(cls.datapath, index=False)
        cls.categories = cls.categorical_data["data"][:-1]
        cls.missing_category = cls.categorical_data["data"][-1]
        cls.missing_input_value = -1.0
        cls.feature_configs = [
            NumericalFeatureConfig(
                cls.numerical_data["header"], cls.numerical_data["data"]
            ),
            CategoricalFeatureConfig(
                cls.categorical_data["header"],
                categories=cls.categories,
                missing_input_value=cls.missing_input_value,
            ),
        ]

    @classmethod
    def tearDownClass(cls) -> None:
        """Cleans up temporary directory after each test."""
        cls.tempdir.cleanup()

    def test_initialization(self) -> None:
        """Tests that `CSVData` initialization works as expected."""
        csv_data = CSVData(self.datapath)
        self.assertEqual(csv_data.dataset, self.datapath)
        self.assertTrue(csv_data.data.equals(self.data))
        self.assertListEqual(csv_data.headers, self.headers)
        self.assertEqual(csv_data.num_examples, len(self.data))
        self.assertIsNone(csv_data.prepared_data)
        # pylint: disable=protected-access
        self.assertIsNone(csv_data._prepared_data_tensor)
        self.assertIsNone(csv_data._targets_tensor)
        # pylint: enable=protected-access

    def test_call(self) -> None:
        """Tests that the correct column data is returned when called."""
        csv_data = CSVData(self.datapath)
        self.assertTrue(
            np.all(
                csv_data(self.numerical_data["header"]) == self.numerical_data["data"]
            )
        )
        self.assertTrue(
            np.all(
                csv_data(self.categorical_data["header"])
                == self.categorical_data["data"]
            )
        )
        self.assertTrue(
            np.all(csv_data(self.target_data["header"]) == self.target_data["data"])
        )

    @parameterized.parameters(
        {"include_target": True, "inplace": True},
        {"include_target": True, "inplace": False},
        {"include_target": False, "inplace": True},
        {"include_target": False, "inplace": False},
    )
    def test_prepare(self, include_target, inplace) -> None:
        """Tests that the data is prepared as expected."""
        csv_data = CSVData(self.datapath)
        csv_data.prepare(
            self.feature_configs,
            self.target_data["header"] if include_target else None,
            inplace=inplace,
        )
        original_categorical_data = pd.Series(
            csv_data(self.categorical_data["header"], False)
        )
        categorical_data = pd.Series(csv_data(self.categorical_data["header"], True))
        if inplace:
            self.assertTrue((original_categorical_data == categorical_data).all())
        for i, category in enumerate(self.categories):
            self.assertTrue((categorical_data[categorical_data == category] == i).all())
        self.assertTrue(
            (
                categorical_data[categorical_data == self.missing_category]
                == self.missing_input_value
            ).all()
        )
        # pylint: disable=protected-access
        self.assertEqual(
            csv_data._prepared_data_tensor.size()[1], len(self.feature_configs)
        )
        if include_target:
            self.assertEqual(
                csv_data._prepared_data_tensor.size()[0],
                csv_data._targets_tensor.size()[0],
            )
            self.assertEqual(csv_data._targets_tensor.size()[1], 1)
        else:
            self.assertIsNone(csv_data._targets_tensor)
        # pylint: enable=protected-access

    @parameterized.parameters(
        {
            "include_target": True,
            "batch_size": 1,
            "expected_example_batches": [
                torch.tensor([[1, 0]]).double(),
                torch.tensor([[2, 1]]).double(),
                torch.tensor([[3, 2]]).double(),
                torch.tensor([[4, -1]]).double(),
            ],
            "expected_target_batches": [
                torch.tensor([[0.2]]).double(),
                torch.tensor([[0.5]]).double(),
                torch.tensor([[0.4]]).double(),
                torch.tensor([[0.9]]).double(),
            ],
        },
        {
            "include_target": True,
            "batch_size": 2,
            "expected_example_batches": [
                torch.tensor([[1, 0], [2, 1]]).double(),
                torch.tensor([[3, 2], [4, -1]]).double(),
            ],
            "expected_target_batches": [
                torch.tensor([[0.2], [0.5]]).double(),
                torch.tensor([[0.4], [0.9]]).double(),
            ],
        },
        {
            "include_target": True,
            "batch_size": 3,
            "expected_example_batches": [
                torch.tensor([[1, 0], [2, 1], [3, 2]]).double(),
                torch.tensor([[4, -1]]).double(),
            ],
            "expected_target_batches": [
                torch.tensor([[0.2], [0.5], [0.4]]).double(),
                torch.tensor([[0.9]]).double(),
            ],
        },
        {
            "include_target": False,
            "batch_size": 4,
            "expected_example_batches": [
                torch.tensor([[1, 0], [2, 1], [3, 2], [4, -1]]).double(),
            ],
            "expected_target_batches": None,
        },
    )
    def test_batch(
        self,
        include_target,
        batch_size,
        expected_example_batches,
        expected_target_batches,
    ) -> None:
        """Tests that batches of data are properly generated."""
        csv_data = CSVData(self.datapath)
        csv_data.prepare(
            self.feature_configs, self.target_data["header"] if include_target else None
        )
        for i, batch in enumerate(csv_data.batch(batch_size)):
            if include_target:
                example_batch, target_batch = batch
                self.assertTrue(
                    torch.allclose(target_batch, expected_target_batches[i])
                )
            else:
                example_batch = batch
            self.assertTrue(torch.allclose(example_batch, expected_example_batches[i]))
