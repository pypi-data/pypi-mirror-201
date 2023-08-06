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
"""Tests for configuration objects."""
import unittest

import numpy as np
from absl.testing import parameterized

from pytorch_calibrated.configs import CategoricalFeatureConfig, NumericalFeatureConfig
from pytorch_calibrated.enums import FeatureType, InputKeypointsInit, Monotonicity


# pylint: disable-next=missing-class-docstring
class TestConfigs(parameterized.TestCase, unittest.TestCase):
    @parameterized.parameters(
        {
            "data": np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
            "num_keypoints": 5,
            "input_keypoints_init": InputKeypointsInit.QUANTILES,
            "missing_input_value": None,
            "monotonicity": Monotonicity.NONE,
            "expected_input_keypoints": np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
        },
        {
            "data": np.array(
                [1.0] * 10 + [2.0] * 10 + [3.0] * 10 + [4.0] * 10 + [5.0] * 10
            ),
            "num_keypoints": 5,
            "input_keypoints_init": InputKeypointsInit.QUANTILES,
            "missing_input_value": None,
            "monotonicity": Monotonicity.INCREASING,
            "expected_input_keypoints": np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
        },
        {
            "data": np.array(
                [1.0] * 10 + [2.0] * 10 + [3.0] * 10 + [4.0] * 10 + [5.0] * 10
            ),
            "num_keypoints": 5,
            "input_keypoints_init": InputKeypointsInit.UNIFORM,
            "missing_input_value": None,
            "monotonicity": Monotonicity.INCREASING,
            "expected_input_keypoints": np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
        },
        {
            "data": np.array(
                [1.0] * 10 + [2.0] * 8 + [3.0] * 6 + [4.0] * 4 + [5.0] * 2 + [6.0]
            ),
            "num_keypoints": 4,
            "input_keypoints_init": InputKeypointsInit.QUANTILES,
            "missing_input_value": None,
            "monotonicity": Monotonicity.INCREASING,
            "expected_input_keypoints": np.array([1.0, 3.0, 4.0, 6.0]),
        },
        {
            "data": np.array(
                [1.0] * 10 + [2.0] * 8 + [3.0] * 6 + [4.0] * 4 + [5.0] * 2 + [6.0]
            ),
            "num_keypoints": 10,
            "input_keypoints_init": InputKeypointsInit.QUANTILES,
            "missing_input_value": None,
            "monotonicity": Monotonicity.NONE,
            "expected_input_keypoints": np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]),
        },
    )
    # pylint: disable-next=too-many-arguments
    def test_numerical_feature_config_initialization(
        self,
        data,
        num_keypoints,
        input_keypoints_init,
        missing_input_value,
        monotonicity,
        expected_input_keypoints,
    ) -> None:
        """Tests that numerical feature configs initialize properly."""
        feature_name = "test_feature"
        config = NumericalFeatureConfig(
            feature_name,
            data,
            num_keypoints,
            input_keypoints_init,
            missing_input_value,
            monotonicity,
        )
        self.assertEqual(config.feature_type, FeatureType.NUMERICAL)
        self.assertEqual(config.feature_name, feature_name)
        self.assertTrue((config.data == data).all())
        self.assertEqual(config.num_keypoints, num_keypoints)
        self.assertEqual(config.input_keypoints_init, input_keypoints_init)
        self.assertEqual(config.missing_input_value, missing_input_value)
        self.assertEqual(config.monotonicity, monotonicity)
        self.assertTrue(np.allclose(config.input_keypoints, expected_input_keypoints))

    @parameterized.parameters(
        {
            "categories": ["a", "b", "c"],
            "missing_input_value": None,
            "monotonicity_pairs": None,
            "expected_category_indices": {"a": 0, "b": 1, "c": 2},
            "expected_monotonicity_index_pairs": [],
        },
        {
            "categories": ["a", "b", "c", "d"],
            "missing_input_value": -1.0,
            "monotonicity_pairs": [("a", "b"), ("c", "d")],
            "expected_category_indices": {"a": 0, "b": 1, "c": 2, "d": 3},
            "expected_monotonicity_index_pairs": [(0, 1), (2, 3)],
        },
    )
    # pylint: disable-next=too-many-arguments
    def test_categorical_feature_config_initialization(
        self,
        categories,
        missing_input_value,
        monotonicity_pairs,
        expected_category_indices,
        expected_monotonicity_index_pairs,
    ) -> None:
        """Tests that categorical feature configs initialize properly."""
        feature_name = "test_feature"
        config = CategoricalFeatureConfig(
            feature_name, categories, missing_input_value, monotonicity_pairs
        )
        self.assertEqual(config.feature_type, FeatureType.CATEGORICAL)
        self.assertEqual(config.feature_name, feature_name)
        self.assertEqual(config.categories, categories)
        self.assertEqual(config.missing_input_value, missing_input_value)
        if monotonicity_pairs:
            self.assertListEqual(config.monotonicity_pairs, monotonicity_pairs)
        else:
            self.assertEqual(config.monotonicity_pairs, monotonicity_pairs)
        self.assertEqual(config.category_indices, expected_category_indices)
        self.assertEqual(
            config.monotonicity_index_pairs, expected_monotonicity_index_pairs
        )
