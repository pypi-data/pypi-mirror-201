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
"""Tests for CategoricalCalibrator module."""
import unittest

import numpy as np
import torch
from absl.testing import parameterized

from pytorch_calibrated.enums import CategoricalCalibratorInit
from pytorch_calibrated.layers.categorical_calibrator import CategoricalCalibrator

from .utils import train_calibrated_module


# pylint: disable-next=missing-class-docstring
class TestCategoricalCalibrator(parameterized.TestCase, unittest.TestCase):
    # pylint: disable=too-many-arguments
    @parameterized.parameters(
        {
            "num_categories": 4,
            "missing_input_value": None,
            "output_min": None,
            "output_max": None,
            "monotonicity_pairs": None,
            "kernel_init": CategoricalCalibratorInit.CONSTANT,
        },
        {
            "num_categories": 4,
            "missing_input_value": None,
            "output_min": None,
            "output_max": None,
            "monotonicity_pairs": None,
            "kernel_init": CategoricalCalibratorInit.UNIFORM,
        },
        {
            "num_categories": 5,
            "missing_input_value": 100.0,
            "output_min": 0.0,
            "output_max": None,
            "monotonicity_pairs": [(1, 2)],
            "kernel_init": CategoricalCalibratorInit.CONSTANT,
        },
        {
            "num_categories": 5,
            "missing_input_value": 100.0,
            "output_min": 0.0,
            "output_max": None,
            "monotonicity_pairs": [(1, 2)],
            "kernel_init": CategoricalCalibratorInit.UNIFORM,
        },
        {
            "num_categories": 6,
            "missing_input_value": -10.0,
            "output_min": None,
            "output_max": 5.0,
            "monotonicity_pairs": [(2, 1), (3, 1)],
            "kernel_init": CategoricalCalibratorInit.CONSTANT,
        },
        {
            "num_categories": 6,
            "missing_input_value": -10.0,
            "output_min": None,
            "output_max": 5.0,
            "monotonicity_pairs": [(2, 1), (3, 1)],
            "kernel_init": CategoricalCalibratorInit.UNIFORM,
        },
        {
            "num_categories": 4,
            "missing_input_value": -1.0,
            "output_min": -1.0,
            "output_max": 2.0,
            "monotonicity_pairs": [(0, 1), (1, 2)],
            "kernel_init": CategoricalCalibratorInit.CONSTANT,
        },
        {
            "num_categories": 4,
            "missing_input_value": -1.0,
            "output_min": -1.0,
            "output_max": 2.0,
            "monotonicity_pairs": [(0, 1), (1, 2)],
            "kernel_init": CategoricalCalibratorInit.UNIFORM,
        },
    )
    def test_initialization(
        self,
        num_categories,
        missing_input_value,
        output_min,
        output_max,
        monotonicity_pairs,
        kernel_init,
    ):
        """Tests that CategoricalCalibrator initialization works properly."""
        calibrator = CategoricalCalibrator(
            num_categories,
            missing_input_value,
            output_min,
            output_max,
            monotonicity_pairs,
            kernel_init,
        )
        if missing_input_value is None:
            self.assertEqual(calibrator.num_categories, num_categories)
        else:
            self.assertEqual(calibrator.num_categories, num_categories + 1)
        self.assertEqual(calibrator.missing_input_value, missing_input_value)
        self.assertEqual(calibrator.output_min, output_min)
        self.assertEqual(calibrator.output_max, output_max)
        self.assertEqual(calibrator.monotonicity_pairs, monotonicity_pairs)
        self.assertEqual(calibrator.kernel_init, kernel_init)
        is_constant = torch.all(calibrator.kernel == calibrator.kernel[0])
        if kernel_init == CategoricalCalibratorInit.CONSTANT:
            self.assertTrue(is_constant)
        elif kernel_init == CategoricalCalibratorInit.UNIFORM:
            self.assertFalse(is_constant)
        if output_min is not None:
            self.assertTrue(torch.all(calibrator.kernel >= output_min))
        if output_max is not None:
            self.assertTrue(torch.all(calibrator.kernel <= output_max))

    @parameterized.parameters(
        {
            "missing_input_value": None,
            "kernel_data": torch.tensor([[1.0], [1.5], [2.0]]).double(),
            "inputs": torch.tensor([[0], [1], [2]]).long(),
            "expected_outputs": torch.tensor([[1.0], [1.5], [2.0]]).double(),
        },
        {
            "missing_input_value": None,
            "kernel_data": torch.tensor([[-1.0], [1.5], [2.0]]).double(),
            "inputs": torch.tensor([[0], [0], [2], [1]]).long(),
            "expected_outputs": torch.tensor([[-1.0], [-1.0], [2.0], [1.5]]).double(),
        },
        {
            "missing_input_value": -1.0,
            "kernel_data": torch.tensor([[1.0], [1.5], [0.5]]).double(),
            "inputs": torch.tensor([[-1], [0], [1], [-1]]).long(),
            "expected_outputs": torch.tensor([[0.5], [1.0], [1.5], [0.5]]).double(),
        },
    )
    def test_forward(self, missing_input_value, kernel_data, inputs, expected_outputs):
        """Tests that forward properly calibrated inputs."""
        num_categories = kernel_data.size()[0]
        if missing_input_value is not None:
            num_categories -= 1
        calibrator = CategoricalCalibrator(num_categories, missing_input_value)
        calibrator.kernel.data = kernel_data
        outputs = calibrator(inputs)
        self.assertTrue(torch.allclose(outputs, expected_outputs))

    def test_constrain_no_constraints(self):
        """Tests that constain does nothing when there are no costraints."""
        calibrator = CategoricalCalibrator(
            3, kernel_init=CategoricalCalibratorInit.CONSTANT
        )
        calibrator.constrain()
        expected_kernel_data = torch.tensor([[0.0], [0.0], [0.0]]).double()
        self.assertTrue(torch.allclose(calibrator.kernel.data, expected_kernel_data))

    @parameterized.parameters(
        {"output_min": 2.0, "kernel_data": torch.tensor([[1.0], [-2.0], [3.0]])},
        {"output_min": -2.0, "kernel_data": torch.tensor([[3.0], [-5.0]]).double()},
    )
    def test_constrain_only_output_min(self, output_min, kernel_data):
        """Tests that constrain properly projects kernel into output_min constraint."""
        calibrator = CategoricalCalibrator(kernel_data.size()[0], output_min=output_min)
        calibrator.kernel.data = kernel_data
        calibrator.constrain()
        self.assertTrue(torch.all(calibrator.keypoints_outputs() >= output_min))

    @parameterized.parameters(
        {"output_max": 2.0, "kernel_data": torch.tensor([[1.0], [-2.0], [3.0]])},
        {"output_max": -2.0, "kernel_data": torch.tensor([[3.0], [-5.0]]).double()},
    )
    def test_constrain_only_output_max(self, output_max, kernel_data):
        """Tests that constrain properly projects kernel into output_max constraint."""
        calibrator = CategoricalCalibrator(kernel_data.size()[0], output_max=output_max)
        calibrator.kernel.data = kernel_data
        calibrator.constrain()
        self.assertTrue(torch.all(calibrator.keypoints_outputs() <= output_max))

    @parameterized.parameters(
        {
            "output_min": 0.0,
            "output_max": 1.0,
            "kernel_data": torch.tensor([[-1.0], [0.0], [1.0]]).double(),
        },
        {
            "output_min": -2.0,
            "output_max": -1.0,
            "kernel_data": torch.tensor([[-1.0], [-3.0], [1.0]]).double(),
        },
        {
            "output_min": -1.0,
            "output_max": 1.0,
            "kernel_data": torch.tensor([[-2.0], [-1.0], [1.0], [2.0]]).double(),
        },
    )
    def test_constrain_bounds(self, output_min, output_max, kernel_data):
        """Tests that constrain properly projects kernel into output bounds."""
        calibrator = CategoricalCalibrator(
            kernel_data.size()[0], output_min=output_min, output_max=output_max
        )
        # pylint: disable=R0801
        calibrator.kernel.data = kernel_data
        calibrator.constrain()
        keypoints_outputs = calibrator.keypoints_outputs()
        self.assertTrue(torch.all(keypoints_outputs >= output_min))
        self.assertTrue(torch.all(keypoints_outputs <= output_max))
        # pylint: enable=R0801

    @parameterized.parameters(
        {
            "monotonicity_pairs": [(0, 1)],
            "kernel_data": torch.tensor([[1.0], [0.8]]).double(),
        },
        {
            "monotonicity_pairs": [(0, 1), (1, 2)],
            "kernel_data": torch.tensor([[1.0], [0.8], [0.6]]).double(),
        },
        {
            "monotonicity_pairs": [(0, 1), (0, 2)],
            "kernel_data": torch.tensor([[1.0], [0.8], [0.6]]).double(),
        },
        {
            "monotonicity_pairs": [(1, 0)],
            "kernel_data": torch.tensor([[0.8], [1.0]]).double(),
        },
        {
            "monotonicity_pairs": [(2, 1), (1, 0)],
            "kernel_data": torch.tensor([[0.6], [0.8], [1.0]]).double(),
        },
        {
            "monotonicity_pairs": [(2, 1), (2, 0)],
            "kernel_data": torch.tensor([[0.6], [0.8], [1.0]]).double(),
        },
    )
    def test_constrain_monotonicity_pairs(self, monotonicity_pairs, kernel_data):
        """Tests that contrain properly projects kernel to match monotonicity pairs."""
        calibrator = CategoricalCalibrator(
            kernel_data.size()[0], monotonicity_pairs=monotonicity_pairs
        )
        calibrator.kernel.data = kernel_data
        calibrator.constrain()
        keypoints_outputs = calibrator.keypoints_outputs()
        for i, j in monotonicity_pairs:
            self.assertLessEqual(keypoints_outputs[i], keypoints_outputs[j])

    @parameterized.parameters(
        {
            "output_min": -1.0,
            "monotonicity_pairs": [(0, 1)],
            "kernel_data": torch.tensor([[-1.5], [-1.8]]).double(),
        },
        {
            "output_min": 1.0,
            "monotonicity_pairs": [(0, 1), (0, 2)],
            "kernel_data": torch.tensor([[1.2], [1.0], [0.9]]).double(),
        },
        {
            "output_min": 0.0,
            "monotonicity_pairs": [(0, 1), (1, 2)],
            "kernel_data": torch.tensor([[1.0], [0.8], [0.6], [-1.0]]).double(),
        },
    )
    def test_constrain_output_min_with_monotonicity_pairs(
        self, output_min, monotonicity_pairs, kernel_data
    ):
        """Tests constaining output min with monotonicity pairs."""
        calibrator = CategoricalCalibrator(
            kernel_data.size()[0],
            output_min=output_min,
            monotonicity_pairs=monotonicity_pairs,
        )
        calibrator.kernel.data = kernel_data
        calibrator.constrain()
        keypoints_outputs = calibrator.keypoints_outputs()
        self.assertTrue(torch.all(keypoints_outputs >= output_min))
        for i, j in monotonicity_pairs:
            self.assertLessEqual(keypoints_outputs[i], keypoints_outputs[j])

    @parameterized.parameters(
        {
            "output_max": -1.0,
            "monotonicity_pairs": [(0, 1)],
            "kernel_data": torch.tensor([[-0.8], [-1.0]]).double(),
        },
        {
            "output_max": 1.0,
            "monotonicity_pairs": [(0, 1), (0, 2)],
            "kernel_data": torch.tensor([[1.2], [1.0], [0.9]]).double(),
        },
        {
            "output_max": 0.0,
            "monotonicity_pairs": [(0, 1), (1, 2)],
            "kernel_data": torch.tensor([[0.1], [0.0], [-0.1]]).double(),
        },
    )
    def test_constrain_output_max_with_monotonicity_pairs(
        self, output_max, monotonicity_pairs, kernel_data
    ):
        """Tests constaining output max with monotonicity pairs."""
        calibrator = CategoricalCalibrator(
            kernel_data.size()[0],
            output_max=output_max,
            monotonicity_pairs=monotonicity_pairs,
        )
        calibrator.kernel.data = kernel_data
        calibrator.constrain()
        keypoints_outputs = calibrator.keypoints_outputs()
        self.assertTrue(torch.all(keypoints_outputs <= output_max))
        for i, j in monotonicity_pairs:
            self.assertLessEqual(keypoints_outputs[i], keypoints_outputs[j])

    @parameterized.parameters(
        {
            "output_min": -1.0,
            "output_max": 1.0,
            "monotonicity_pairs": [(0, 1)],
            "kernel_data": torch.tensor([[-0.8], [-1.0], [2.0]]).double(),
        },
        {
            "output_min": 1.0,
            "output_max": 5.0,
            "monotonicity_pairs": [(0, 1), (0, 2)],
            "kernel_data": torch.tensor([[1.2], [1.1], [0.9], [6.0]]).double(),
        },
        {
            "output_min": -1.0,
            "output_max": 2.0,
            "monotonicity_pairs": [(0, 1), (1, 2)],
            "kernel_data": torch.tensor([[2.2], [1.8], [1.7], [-2.0]]).double(),
        },
    )
    def test_constrain_bounds_with_monotonicity_pairs(
        self, output_min, output_max, monotonicity_pairs, kernel_data
    ):
        """Tests constaining bounds with monotonicity pairs."""
        calibrator = CategoricalCalibrator(
            kernel_data.size()[0],
            output_min=output_min,
            output_max=output_max,
            monotonicity_pairs=monotonicity_pairs,
        )
        # pylint: disable=R0801
        calibrator.kernel.data = kernel_data
        calibrator.constrain()
        keypoints_outputs = calibrator.keypoints_outputs()
        self.assertTrue(torch.all(keypoints_outputs >= output_min))
        self.assertTrue(torch.all(keypoints_outputs <= output_max))
        for i, j in monotonicity_pairs:
            self.assertLessEqual(keypoints_outputs[i], keypoints_outputs[j])
        # pylint: enable=R0801

    @parameterized.parameters(
        {
            "num_categories": 3,
            "missing_input_value": None,
            "expected_keypoints_inputs": torch.tensor([0, 1, 2]).long(),
        },
        {
            "num_categories": 3,
            "missing_input_value": -1,
            "expected_keypoints_inputs": torch.tensor([0, 1, 2, -1]).long(),
        },
    )
    def test_keypoints_inputs(
        self, num_categories, missing_input_value, expected_keypoints_inputs
    ):
        """Tests that the correct keypoint inputs are returned."""
        calibrator = CategoricalCalibrator(num_categories, missing_input_value)
        self.assertTrue(
            torch.allclose(calibrator.keypoints_inputs(), expected_keypoints_inputs)
        )

    @parameterized.parameters(
        {
            "kernel_data": torch.tensor([[0.0], [1.0], [2.0]]).double(),
            "expected_keypoints_outputs": torch.tensor([0.0, 1.0, 2.0]).double(),
        },
        {
            "kernel_data": torch.tensor([[-1.0], [3.0], [0.5], [-4.2]]).double(),
            "expected_keypoints_outputs": torch.tensor([-1.0, 3.0, 0.5, -4.2]).double(),
        },
    )
    def test_keypoints_outputs(self, kernel_data, expected_keypoints_outputs):
        """Tests that the correct keypoint outputs are returned."""
        calibrator = CategoricalCalibrator(kernel_data.size()[0])
        calibrator.kernel.data = kernel_data
        self.assertTrue(
            torch.allclose(calibrator.keypoints_outputs(), expected_keypoints_outputs)
        )

    @parameterized.parameters(
        {
            "monotonicity_pairs": [(0, 1)],
            "kernel_data": torch.tensor([[1.0], [0.8]]).double(),
            "expected_projected_kernel_data": torch.tensor([[0.9], [0.9]]).double(),
        },
        {
            "monotonicity_pairs": [(0, 1), (0, 2)],
            "kernel_data": torch.tensor([[1.0], [0.8], [0.6]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[0.775], [0.85], [0.775]]
            ).double(),
        },
        {
            "monotonicity_pairs": [(0, 1), (1, 2)],
            "kernel_data": torch.tensor([[1.0], [0.8], [0.6]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[0.8], [0.8], [0.8]]
            ).double(),
        },
    )
    def test_approximately_project_monotonicity_pairs(
        self, monotonicity_pairs, kernel_data, expected_projected_kernel_data
    ):
        """Tests that kernel is properly projected to match monotonicity pairs."""
        calibrator = CategoricalCalibrator(
            kernel_data.size()[0], monotonicity_pairs=monotonicity_pairs
        )
        # pylint: disable=protected-access
        projected_kernel_data = calibrator._approximately_project_monotonicity_pairs(
            kernel_data
        )
        # pylint: enable=protected-access
        self.assertTrue(
            torch.allclose(projected_kernel_data, expected_projected_kernel_data)
        )

    def test_training(self):  # pylint: disable=too-many-locals
        """Tests that the `CategoricalCaclibrator` module can learn a mapping."""
        num_categories, num_examples_per_category = 5, 200
        training_examples = np.concatenate(
            [[c] * num_examples_per_category for c in range(num_categories)]
        )
        np.random.shuffle(training_examples)
        training_examples = torch.from_numpy(np.expand_dims(training_examples, 1))
        training_labels = training_examples.double()

        num_examples = num_categories * num_examples_per_category

        calibrator = CategoricalCalibrator(
            num_categories,
            output_min=0.0,
            output_max=num_categories - 1,
            monotonicity_pairs=[(i, i + 1) for i in range(num_categories - 1)],
        )

        # pylint: disable=R0801
        loss_fn = torch.nn.MSELoss()
        optimizer = torch.optim.Adam(calibrator.parameters(), lr=1e-2)

        train_calibrated_module(
            calibrator,
            training_examples,
            training_labels,
            loss_fn,
            optimizer,
            300,
            num_examples // 10,
        )

        keypoints_inputs = calibrator.keypoints_inputs()
        keypoints_outputs = calibrator.keypoints_outputs()
        self.assertTrue(
            torch.allclose(keypoints_inputs.double(), keypoints_outputs, atol=2e-2)
        )
        # pylint: enable=R0801
