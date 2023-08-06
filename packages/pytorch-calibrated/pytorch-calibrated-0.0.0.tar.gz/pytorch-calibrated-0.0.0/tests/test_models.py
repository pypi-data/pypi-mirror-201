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
"""Tests for models."""
import unittest

import numpy as np
import torch
from absl.testing import parameterized

from pytorch_calibrated.configs import CategoricalFeatureConfig, NumericalFeatureConfig
from pytorch_calibrated.enums import Monotonicity
from pytorch_calibrated.models import CalibratedLinear

from .utils import train_calibrated_module


class TestCalibratedLinear(parameterized.TestCase, unittest.TestCase):
    """Tests for the `CalibratedLinear` module."""

    @parameterized.parameters(
        {
            "feature_configs": [
                NumericalFeatureConfig(
                    feature_name="numerical_feature",
                    data=np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
                    num_keypoints=5,
                    monotonicity=Monotonicity.NONE,
                ),
                CategoricalFeatureConfig(
                    feature_name="categorical_feature",
                    categories=["a", "b", "c"],
                    monotonicity_pairs=[("a", "b")],
                ),
            ],
            "output_min": None,
            "output_max": None,
            "output_calibration_num_keypoints": None,
            "expected_linear_monotonicities": [
                Monotonicity.NONE,
                Monotonicity.INCREASING,
            ],
            "expected_output_calibrator_monotonicity": Monotonicity.INCREASING,
        },
        {
            "feature_configs": [
                NumericalFeatureConfig(
                    feature_name="numerical_feature",
                    data=np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
                    num_keypoints=5,
                    monotonicity=Monotonicity.NONE,
                ),
                CategoricalFeatureConfig(
                    feature_name="categorical_feature",
                    categories=["a", "b", "c"],
                    monotonicity_pairs=None,
                ),
            ],
            "output_min": -1.0,
            "output_max": 1.0,
            "output_calibration_num_keypoints": 10,
            "expected_linear_monotonicities": [
                Monotonicity.INCREASING,
                Monotonicity.INCREASING,
            ],
            "expected_output_calibrator_monotonicity": Monotonicity.NONE,
        },
        {
            "feature_configs": [
                NumericalFeatureConfig(
                    feature_name="numerical_feature",
                    data=np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
                    num_keypoints=5,
                    monotonicity=Monotonicity.DECREASING,
                ),
                CategoricalFeatureConfig(
                    feature_name="categorical_feature",
                    categories=["a", "b", "c"],
                    monotonicity_pairs=None,
                ),
            ],
            "output_min": 0.0,
            "output_max": None,
            "output_calibration_num_keypoints": None,
            "expected_linear_monotonicities": [
                Monotonicity.INCREASING,
                Monotonicity.INCREASING,
            ],
            "expected_output_calibrator_monotonicity": Monotonicity.INCREASING,
        },
    )
    # pylint: disable-next=too-many-arguments
    def test_initialization(
        self,
        feature_configs,
        output_min,
        output_max,
        output_calibration_num_keypoints,
        expected_linear_monotonicities,
        expected_output_calibrator_monotonicity,
    ) -> None:
        """Tests that `CalibratedLinear` initialization works."""
        calibrated_linear = CalibratedLinear(
            feature_configs=feature_configs,
            output_min=output_min,
            output_max=output_max,
            output_calibration_num_keypoints=output_calibration_num_keypoints,
        )
        self.assertListEqual(calibrated_linear.feature_configs, feature_configs)
        self.assertEqual(calibrated_linear.output_min, output_min)
        self.assertEqual(calibrated_linear.output_max, output_max)
        self.assertEqual(
            calibrated_linear.output_calibration_num_keypoints,
            output_calibration_num_keypoints,
        )
        self.assertEqual(len(calibrated_linear.calibrators), len(feature_configs))
        for calibrator in calibrated_linear.calibrators.values():
            self.assertEqual(calibrator.output_min, output_min)
            self.assertEqual(calibrator.output_max, output_max)
        self.assertListEqual(
            calibrated_linear.linear.monotonicities, expected_linear_monotonicities
        )
        if (
            output_min is not None
            or output_max is not None
            or output_calibration_num_keypoints
        ):
            self.assertFalse(calibrated_linear.linear.use_bias)
            self.assertTrue(calibrated_linear.linear.weighted_average)
        else:
            self.assertTrue(calibrated_linear.linear.use_bias)
            self.assertFalse(calibrated_linear.linear.weighted_average)
        if not output_calibration_num_keypoints:
            self.assertEqual(calibrated_linear.output_calibrator, None)
        else:
            self.assertEqual(calibrated_linear.output_calibrator.output_min, output_min)
            self.assertEqual(calibrated_linear.output_calibrator.output_max, output_max)
            self.assertEqual(
                calibrated_linear.output_calibrator.monotonicity,
                expected_output_calibrator_monotonicity,
            )

    # TODO: add more parameterized tests
    @parameterized.parameters(
        {
            "output_min": None,
            "output_max": None,
            "calibrator_kernel_datas": [
                torch.tensor([[0.0], [1.0], [1.0], [1.0]]).double(),
                torch.tensor([[1.0], [2.0], [3.0]]).double(),
            ],
            "linear_kernel_data": torch.tensor([[1.0], [2.0]]).double(),
            "output_calibrator_kernel_data": None,
            "inputs": torch.tensor([[1.0, 0], [2.0, 1], [3.0, 2], [4.0, 1]]).double(),
            "expected_outputs": torch.tensor([[2.0], [5.0], [8.0], [7.0]]).double(),
        },
        {
            "output_min": 0.0,
            "output_max": 1.0,
            "calibrator_kernel_datas": [
                torch.tensor([[1.0], [-0.5], [-0.5], [1.0]]).double(),
                torch.tensor([[1.0], [0.5], [0.0]]).double(),
            ],
            "linear_kernel_data": torch.tensor([[0.3], [0.7]]).double(),
            "output_calibrator_kernel_data": torch.tensor(
                [[0.0], [1.0], [-1.0], [1.0]]
            ).double(),
            "inputs": torch.tensor([[1.0, 0], [2.0, 1], [3.0, 2], [4.0, 1]]).double(),
            "expected_outputs": torch.tensor([[1.0], [0.5], [0.0], [0.05]]).double(),
        },
    )
    # pylint: disable-next=too-many-arguments
    def test_forward(
        self,
        output_min,
        output_max,
        calibrator_kernel_datas,
        linear_kernel_data,
        output_calibrator_kernel_data,
        inputs,
        expected_outputs,
    ) -> None:
        """Tests that forward returns expected result."""
        calibrated_linear = CalibratedLinear(
            feature_configs=[
                NumericalFeatureConfig(
                    feature_name="numerical_feature",
                    data=np.array([1.0, 2.0, 3.0, 4.0]),
                    num_keypoints=4,
                    monotonicity=Monotonicity.NONE,
                ),
                CategoricalFeatureConfig(
                    feature_name="categorical_feature",
                    categories=["a", "b", "c"],
                    monotonicity_pairs=None,
                ),
            ],
            output_min=output_min,
            output_max=output_max,
            output_calibration_num_keypoints=output_calibrator_kernel_data.size()[0]
            if output_calibrator_kernel_data is not None
            else None,
        )
        for i, calibrator in enumerate(calibrated_linear.calibrators.values()):
            calibrator.kernel.data = calibrator_kernel_datas[i]
        calibrated_linear.linear.kernel.data = linear_kernel_data
        if output_calibrator_kernel_data is not None:
            calibrated_linear.output_calibrator.kernel.data = (
                output_calibrator_kernel_data
            )
        outputs = calibrated_linear(inputs)
        self.assertTrue(torch.allclose(outputs, expected_outputs))

    def test_constrain(self) -> None:
        """Tests that constrain properly constrains all layers."""
        output_min, output_max = -1.0, 1.0
        calibrated_linear = CalibratedLinear(
            feature_configs=[
                NumericalFeatureConfig(
                    feature_name="numerical_feature",
                    data=np.array([1.0, 2.0, 3.0, 4.0]),
                    num_keypoints=4,
                    monotonicity=Monotonicity.NONE,
                ),
                CategoricalFeatureConfig(
                    feature_name="categorical_feature",
                    categories=["a", "b", "c"],
                    monotonicity_pairs=None,
                ),
            ],
            output_min=-output_min,
            output_max=output_max,
            output_calibration_num_keypoints=5,
        )
        calibrated_linear.calibrators["numerical_feature"].kernel.data = torch.tensor(
            [[-2.0], [1.0], [2.0], [1.0]]
        ).double()
        calibrated_linear.calibrators["categorical_feature"].kernel.data = torch.tensor(
            [[2.0], [0.5], [-2.0]]
        ).double()
        calibrated_linear.linear.kernel.data = torch.tensor([[1.0], [2.0]]).double()
        calibrated_linear.output_calibrator.kernel.data = torch.tensor(
            [[0.0], [1.0], [0.5], [1.0], [-1.0]]
        ).double()
        calibrated_linear.constrain()
        for calibrator in calibrated_linear.calibrators.values():
            keypoint_outputs = calibrator.keypoints_outputs()
            self.assertTrue(torch.all(keypoint_outputs >= output_min))
            self.assertTrue(torch.all(keypoint_outputs <= output_max))
        self.assertEqual(torch.sum(calibrated_linear.linear.kernel.data), 1.0)
        output_calibrator_keypoint_outputs = (
            calibrated_linear.output_calibrator.keypoints_outputs()
        )
        self.assertTrue(torch.all(output_calibrator_keypoint_outputs >= output_min))
        self.assertTrue(torch.all(output_calibrator_keypoint_outputs <= output_max))

    def test_training(self) -> None:  # pylint: disable=too-many-locals
        """Tests `CalibratedLinear` training on data from f(x) = 0.7|x_1| + 0.3x_2."""
        num_examples, num_categories = 3000, 3
        output_min, output_max = 0.0, num_categories - 1
        x_1_numpy = np.random.uniform(-output_max, output_max, size=num_examples)
        x_1 = torch.from_numpy(x_1_numpy)[:, None]
        num_examples_per_category = num_examples // num_categories
        x2_numpy = np.concatenate(
            [[c] * num_examples_per_category for c in range(num_categories)]
        )
        x_2 = torch.from_numpy(x2_numpy)[:, None]
        training_examples = torch.column_stack((x_1, x_2))
        linear_coefficients = torch.tensor([0.7, 0.3]).double()
        training_labels = torch.sum(
            torch.column_stack((torch.absolute(x_1), x_2)) * linear_coefficients,
            dim=1,
            keepdim=True,
        )
        randperm = torch.randperm(training_examples.size()[0])
        training_examples = training_examples[randperm]
        training_labels = training_labels[randperm]

        calibrated_linear = CalibratedLinear(
            feature_configs=[
                NumericalFeatureConfig(
                    "x1",
                    x_1_numpy,
                    num_keypoints=4,
                ),
                CategoricalFeatureConfig(
                    "x2", [0, 1, 2], monotonicity_pairs=[(0, 1), (1, 2)]
                ),
            ],
            output_min=output_min,
            output_max=output_max,
        )

        loss_fn = torch.nn.MSELoss()
        optimizer = torch.optim.Adam(
            calibrated_linear.parameters(recurse=True), lr=1e-1
        )

        with torch.no_grad():
            initial_predictions = calibrated_linear(training_examples)
            initial_loss = loss_fn(initial_predictions, training_labels)

        train_calibrated_module(
            calibrated_linear,
            training_examples,
            training_labels,
            loss_fn,
            optimizer,
            500,
            num_examples // 10,
        )

        with torch.no_grad():
            trained_predictions = calibrated_linear(training_examples)
            trained_loss = loss_fn(trained_predictions, training_labels)

        self.assertLess(trained_loss, initial_loss)
        self.assertLess(trained_loss, 0.0175)
