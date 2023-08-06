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
"""Tests for NumericalCalibrator module."""
import unittest

import numpy as np
import torch
from absl.testing import parameterized

from pytorch_calibrated.enums import Monotonicity, NumericalCalibratorInit
from pytorch_calibrated.layers.numerical_calibrator import NumericalCalibrator

from .utils import train_calibrated_module


# pylint: disable-next=missing-class-docstring
class TestNumericalCalibrator(parameterized.TestCase, unittest.TestCase):
    # pylint: disable=too-many-arguments
    @parameterized.parameters(
        {
            "input_keypoints": np.linspace(1.0, 4.0, num=5),
            "missing_input_value": None,
            "output_min": None,
            "output_max": None,
            "monotonicity": Monotonicity.NONE,
            "kernel_init": NumericalCalibratorInit.EQUAL_HEIGHTS,
            "projection_iterations": 10,
            "expected_kernel": torch.tensor([[[-2.0]] + ([[1.0]] * 4)]).double(),
        },
        {
            "input_keypoints": np.linspace(-2.0, 8.0, num=11),
            "missing_input_value": -1.0,
            "output_min": -1.0,
            "output_max": 1.0,
            "monotonicity": Monotonicity.INCREASING,
            "kernel_init": NumericalCalibratorInit.EQUAL_SLOPES,
            "projection_iterations": 4,
            "expected_kernel": torch.tensor([[-1.0]] + ([[0.2]] * 10)).double(),
        },
        {
            "input_keypoints": np.linspace(-2.0, 8.0, num=17),
            "missing_input_value": 20,
            "output_min": 2.0,
            "output_max": None,
            "monotonicity": Monotonicity.DECREASING,
            "kernel_init": NumericalCalibratorInit.EQUAL_HEIGHTS,
            "projection_iterations": 1,
            "expected_kernel": torch.tensor([[6.0]] + ([[-0.25]] * 16)).double(),
        },
    )
    def test_initialization(
        self,
        input_keypoints,
        missing_input_value,
        output_min,
        output_max,
        monotonicity,
        kernel_init,
        projection_iterations,
        expected_kernel,
    ) -> None:
        """Tests that NumericalCalibrator class initialization works properly."""
        calibrator = NumericalCalibrator(
            input_keypoints,
            missing_input_value,
            output_min,
            output_max,
            monotonicity,
            kernel_init,
            projection_iterations,
        )
        self.assertTrue(torch.allclose(calibrator.kernel.data, expected_kernel))
        self.assertTrue((calibrator.input_keypoints == input_keypoints).all())
        self.assertEqual(calibrator.missing_input_value, missing_input_value)
        self.assertEqual(calibrator.output_min, output_min)
        self.assertEqual(calibrator.output_max, output_max)
        self.assertEqual(calibrator.monotonicity, monotonicity)
        self.assertEqual(calibrator.kernel_init, kernel_init)
        self.assertEqual(calibrator.projection_iterations, projection_iterations)

    @parameterized.parameters(
        {
            "input_keypoints": np.linspace(1.0, 5.0, num=5),
            "kernel_init": NumericalCalibratorInit.EQUAL_HEIGHTS,
            "kernel_data": None,
            "inputs": torch.tensor(
                [
                    [0.5],
                    [1.0],
                    [2.0],
                    [3.0],
                    [4.0],
                    [5.0],
                    [5.5],
                ]
            ).double(),
            "expected_outputs": torch.tensor(
                [
                    [-2.0],
                    [-2.0],
                    [-1.0],
                    [0.0],
                    [1.0],
                    [2.0],
                    [2.0],
                ]
            ).double(),
        },
        {
            "input_keypoints": np.linspace(1.0, 5.0, num=5),
            "kernel_init": NumericalCalibratorInit.EQUAL_HEIGHTS,
            "kernel_data": torch.tensor([[2.0], [-4.0], [2.0], [-1.0], [2.0]]).double(),
            "inputs": torch.tensor([[1.5], [2.5], [3.5], [4.5]]).double(),
            "expected_outputs": torch.tensor([[0.0], [-1.0], [-0.5], [0.0]]).double(),
        },
        {
            "input_keypoints": np.array([1.0, 3.0, 4.0, 5.0, 7.0, 9.0]),
            "kernel_init": NumericalCalibratorInit.EQUAL_SLOPES,
            "kernel_data": None,
            "inputs": torch.tensor(
                [
                    [1.0],
                    [1.5],
                    [2.0],
                    [2.5],
                    [3.0],
                    [3.5],
                    [4.0],
                    [4.5],
                    [5.0],
                    [5.5],
                    [6.0],
                    [6.5],
                    [7.0],
                    [7.5],
                    [8.0],
                    [8.5],
                    [9.0],
                ]
            ).double(),
            "expected_outputs": torch.tensor(
                [
                    [-2.0],
                    [-1.75],
                    [-1.5],
                    [-1.25],
                    [-1.0],
                    [-0.75],
                    [-0.5],
                    [-0.25],
                    [0.0],
                    [0.25],
                    [0.5],
                    [0.75],
                    [1.0],
                    [1.25],
                    [1.5],
                    [1.75],
                    [2.0],
                ]
            ).double(),
        },
    )
    def test_forward(
        self, input_keypoints, kernel_init, kernel_data, inputs, expected_outputs
    ) -> None:
        """Tests that forward properly calibrated inputs."""
        calibrator = NumericalCalibrator(input_keypoints, kernel_init=kernel_init)
        if kernel_data is not None:
            calibrator.kernel.data = kernel_data
        outputs = calibrator.forward(inputs)
        self.assertTrue(torch.allclose(outputs, expected_outputs))

    def test_constrain_no_constraints(self) -> None:
        """Tests that constrain does nothing when there are no constraints."""
        calibrator = NumericalCalibrator(np.linspace(1.0, 5.0, num=5))
        calibrator.constrain()
        expected_kernel_data = torch.tensor(
            [[-2.0], [1.0], [1.0], [1.0], [1.0]]
        ).double()
        self.assertTrue(torch.allclose(calibrator.kernel.data, expected_kernel_data))

    @parameterized.parameters(
        {
            "output_min": 2.0,
            "kernel_data": torch.tensor([[-3.0], [1.0], [1.0], [1.0], [1.0]]).double(),
        },
        {
            "output_min": -3.0,
            "kernel_data": torch.tensor(
                [[-3.0], [1.0], [-12.0], [8.0], [-1.0]]
            ).double(),
        },
    )
    def test_constrain_only_output_min(self, output_min, kernel_data) -> None:
        """Tests that constrain properly projects kernel into output_min constraint."""
        calibrator = NumericalCalibrator(
            np.linspace(1.0, 5.0, num=5), output_min=output_min
        )
        calibrator.kernel.data = kernel_data
        calibrator.constrain()
        self.assertTrue(torch.all(calibrator.keypoints_outputs() >= output_min))

    @parameterized.parameters(
        {
            "output_max": -2.0,
            "kernel_data": torch.tensor([[-3.0], [1.0], [1.0], [1.0], [1.0]]).double(),
        },
        {
            "output_max": 5.0,
            "kernel_data": torch.tensor(
                [[-3.0], [1.0], [6.0], [9.0], [-11.0]]
            ).double(),
        },
    )
    def test_constrain_only_output_max(self, output_max, kernel_data) -> None:
        """Tests that constrain properly projects kernel into output_max constraint."""
        calibrator = NumericalCalibrator(
            np.linspace(1.0, 5.0, num=5), output_max=output_max
        )
        calibrator.kernel.data = kernel_data
        calibrator.constrain()
        self.assertTrue(torch.all(calibrator.keypoints_outputs() <= output_max))

    @parameterized.parameters(
        {
            "output_min": 1.0,
            "output_max": 5.0,
            "kernel_data": torch.tensor(
                [[-2.0], [1.0], [1.0], [1.0], [1.0], [3.0]]
            ).double(),
        },
        {
            "output_min": -5.0,
            "output_max": 0.0,
            "kernel_data": torch.tensor(
                [[-2.0], [-8.0], [12.0], [3.0], [-30.0], [3.0]]
            ).double(),
        },
    )
    def test_constrain_bounds(self, output_min, output_max, kernel_data) -> None:
        """Tests that constrain properly projects kernel into output bounds."""
        calibrator = NumericalCalibrator(
            np.linspace(1.0, 5.0, num=6), output_min=output_min, output_max=output_max
        )
        # pylint: disable=R0801
        calibrator.kernel.data = kernel_data
        calibrator.constrain()
        keypoints_outputs = calibrator.keypoints_outputs()
        self.assertTrue(torch.all(keypoints_outputs >= output_min))
        self.assertTrue(torch.all(keypoints_outputs <= output_max))
        # pylint: enable=R0801

    @parameterized.parameters(
        {"kernel_data": torch.tensor([[0.0], [1.0], [-2.0], [3.0], [1.0]]).double()},
        {"kernel_data": torch.tensor([[-2.0], [-2.0], [1.0], [-3.0], [-4.0]]).double()},
    )
    def test_constrain_increasing_monotonicity(self, kernel_data) -> None:
        """Tests that contrain properly projects kernel to be increasingly monotonic."""
        calibrator = NumericalCalibrator(
            np.linspace(1.0, 5.0, num=5), monotonicity=Monotonicity.INCREASING
        )
        calibrator.kernel.data = kernel_data
        calibrator.constrain()
        heights = calibrator.kernel.data[1:]
        self.assertTrue(torch.all(heights >= 0))

    @parameterized.parameters(
        {"kernel_data": torch.tensor([[0.0], [1.0], [-2.0], [3.0]]).double()},
        {"kernel_data": torch.tensor([[-2.0], [-2.0], [1.0], [-3.0]]).double()},
    )
    def test_constrain_decreasing_monotonicity(self, kernel_data) -> None:
        """Tests that contrain properly projects kernel to be decreasingly monotonic."""
        calibrator = NumericalCalibrator(
            np.linspace(1.0, 5.0, num=4), monotonicity=Monotonicity.DECREASING
        )
        calibrator.kernel.data = kernel_data
        calibrator.constrain()
        heights = calibrator.kernel.data[1:]
        self.assertTrue(torch.all(heights <= 0))

    @parameterized.parameters(
        {
            "output_min": -2.0,
            "monotonicity": Monotonicity.INCREASING,
            "kernel_data": torch.tensor([[-3.0], [1.0], [-2.5], [2.0]]).double(),
        },
        {
            "output_min": 3.0,
            "monotonicity": Monotonicity.INCREASING,
            "kernel_data": torch.tensor([[-3.0], [-1.0], [4.0], [-2.0]]).double(),
        },
        {
            "output_min": -3.0,
            "monotonicity": Monotonicity.DECREASING,
            "kernel_data": torch.tensor([[-3.0], [-1.0], [4.0], [-2.0]]).double(),
        },
        {
            "output_min": 2.0,
            "monotonicity": Monotonicity.DECREASING,
            "kernel_data": torch.tensor([[-1.0], [-2.0], [-4.0], [2.0]]).double(),
        },
    )
    def test_constrain_output_min_monotonicity(
        self, output_min, monotonicity, kernel_data
    ) -> None:
        """Tests contraining output min with monotonicity constraints."""
        calibrator = NumericalCalibrator(
            np.linspace(1.0, 5.0, num=4),
            output_min=output_min,
            monotonicity=monotonicity,
        )
        calibrator.kernel.data = kernel_data
        calibrator.constrain()
        keypoints_outputs = calibrator.keypoints_outputs()
        self.assertTrue(torch.all(keypoints_outputs >= output_min))
        heights = calibrator.kernel.data[1:]
        if monotonicity == Monotonicity.INCREASING:
            self.assertTrue(torch.all(heights >= 0))
        else:
            self.assertTrue(torch.all(heights <= 0))

    @parameterized.parameters(
        {
            "output_max": -2.0,
            "monotonicity": Monotonicity.INCREASING,
            "kernel_data": torch.tensor([[-1.0], [1.0], [-2.5], [2.0]]).double(),
        },
        {
            "output_max": 3.0,
            "monotonicity": Monotonicity.INCREASING,
            "kernel_data": torch.tensor([[4.0], [-1.0], [4.0], [-2.0]]).double(),
        },
        {
            "output_max": 3.0,
            "monotonicity": Monotonicity.DECREASING,
            "kernel_data": torch.tensor([[4.0], [-1.0], [4.0], [-2.0]]).double(),
        },
        {
            "output_max": -2.0,
            "monotonicity": Monotonicity.DECREASING,
            "kernel_data": torch.tensor([[3.0], [-2.0], [3.0], [-4.0]]).double(),
        },
    )
    def test_constrain_output_max_with_monotonicity(
        self, output_max, monotonicity, kernel_data
    ) -> None:
        """Tests contraining output max with monotonicity constraints."""
        calibrator = NumericalCalibrator(
            np.linspace(1.0, 5.0, num=4),
            output_max=output_max,
            monotonicity=monotonicity,
        )
        calibrator.kernel.data = kernel_data
        calibrator.constrain()
        keypoints_outputs = calibrator.keypoints_outputs()
        self.assertTrue(torch.all(keypoints_outputs <= output_max))
        heights = calibrator.kernel.data[1:]
        if monotonicity == Monotonicity.INCREASING:
            self.assertTrue(torch.all(heights >= 0))
        else:
            self.assertTrue(torch.all(heights <= 0))

    @parameterized.parameters(
        {
            "output_min": -1.0,
            "output_max": 1.0,
            "monotonicity": Monotonicity.INCREASING,
            "kernel_data": torch.tensor([[-1.5], [1.5], [1.5], [-1.0]]).double(),
        },
        {
            "output_min": -1.0,
            "output_max": 1.0,
            "monotonicity": Monotonicity.DECREASING,
            "kernel_data": torch.tensor([[1.5], [-1.5], [-1.5], [1.0]]).double(),
        },
    )
    def test_constrain_bounds_with_monotonicity(
        self, output_min, output_max, monotonicity, kernel_data
    ) -> None:
        """Tests constraining output bounds with monotonicity constraints."""
        calibrator = NumericalCalibrator(
            np.linspace(1.0, 5.0, num=4),
            output_min=output_min,
            output_max=output_max,
            monotonicity=monotonicity,
        )
        # pylint: disable=R0801
        calibrator.kernel.data = kernel_data
        calibrator.constrain()
        keypoints_outputs = calibrator.keypoints_outputs()
        self.assertTrue(torch.all(keypoints_outputs >= output_min))
        self.assertTrue(torch.all(keypoints_outputs <= output_max))
        # pylint: enable=R0801
        heights = calibrator.kernel.data[1:]
        if monotonicity == Monotonicity.INCREASING:
            self.assertTrue(torch.all(heights >= 0))
        else:
            self.assertTrue(torch.all(heights <= 0))

    @parameterized.parameters(
        {"input_keypoints": np.linspace(1.0, 5.0, num=5)},
        {"input_keypoints": np.linspace(1.0, 10.0, num=34)},
    )
    def test_keypoints_inputs(self, input_keypoints) -> None:
        """Tests that the correct keypoint inputs are returned."""
        calibrator = NumericalCalibrator(input_keypoints)
        self.assertTrue(
            torch.allclose(calibrator.keypoints_inputs(), torch.tensor(input_keypoints))
        )

    @parameterized.parameters(
        {
            "num_keypoints": 5,
            "kernel_data": torch.tensor([[0.0], [0.2], [0.7], [1.5], [4.8]]).double(),
            "expected_keypoints_outputs": torch.tensor(
                [0.0, 0.2, 0.9, 2.4, 7.2]
            ).double(),
        },
        {
            "num_keypoints": 6,
            "kernel_data": torch.tensor(
                [[-2.0], [4.0], [-2.0], [0.5], [-1.7], [3.4]]
            ).double(),
            "expected_keypoints_outputs": torch.tensor(
                [-2.0, 2.0, 0.0, 0.5, -1.2, 2.2]
            ).double(),
        },
    )
    def test_keypoints_outputs(
        self, num_keypoints, kernel_data, expected_keypoints_outputs
    ) -> None:
        """Tests that the correct keypoint outputs are returned."""
        calibrator = NumericalCalibrator(np.linspace(1.0, 5.0, num=num_keypoints))
        calibrator.kernel.data = kernel_data
        self.assertTrue(
            torch.allclose(calibrator.keypoints_outputs(), expected_keypoints_outputs)
        )

    @parameterized.parameters(
        {
            "input_keypoints": np.linspace(1.0, 4.0, num=4),
            "output_min": None,
            "output_max": None,
            "monotonicity": Monotonicity.INCREASING,
            "kernel_data": torch.tensor([[0.0], [1.0], [1.0], [1.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[0.0], [1.0], [1.0], [1.0]]
            ).double(),
        },
        {
            "input_keypoints": np.linspace(1.0, 4.0, num=4),
            "output_min": 1.0,
            "output_max": None,
            "monotonicity": Monotonicity.INCREASING,
            "kernel_data": torch.tensor([[1.0], [1.0], [2.0], [3.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[1.0], [1.0], [2.0], [3.0]]
            ).double(),
        },
        {
            "input_keypoints": np.linspace(1.0, 4.0, num=4),
            "output_min": 1.0,
            "output_max": None,
            "monotonicity": Monotonicity.INCREASING,
            "kernel_data": torch.tensor([[0.0], [1.0], [1.0], [1.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[1.0], [1.0], [1.0], [1.0]]
            ).double(),
        },
        {
            "input_keypoints": np.linspace(1.0, 4.0, num=4),
            "output_min": None,
            "output_max": 5.0,
            "monotonicity": Monotonicity.INCREASING,
            "kernel_data": torch.tensor([[0.0], [1.0], [1.0], [1.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[0.0], [1.0], [1.0], [1.0]]
            ).double(),
        },
        {
            "input_keypoints": np.linspace(1.0, 4.0, num=4),
            "output_min": None,
            "output_max": 5.0,
            "monotonicity": Monotonicity.INCREASING,
            "kernel_data": torch.tensor([[3.0], [1.0], [2.0], [2.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[2.25], [0.25], [1.25], [1.25]]
            ).double(),
        },
        {
            "input_keypoints": np.linspace(1.0, 4.0, num=4),
            "output_min": 3.0,
            "output_max": 5.0,
            "monotonicity": Monotonicity.INCREASING,
            "kernel_data": torch.tensor([[3.0], [1.0], [2.0], [2.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[3.0], [0.0], [1.0], [1.0]]
            ).double(),
        },
        {
            "input_keypoints": np.linspace(1.0, 4.0, num=4),
            "output_min": None,
            "output_max": None,
            "monotonicity": Monotonicity.DECREASING,
            "kernel_data": torch.tensor([[0.0], [-1.0], [-1.0], [-1.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[0.0], [-1.0], [-1.0], [-1.0]]
            ).double(),
        },
        {
            "input_keypoints": np.linspace(1.0, 4.0, num=4),
            "output_min": -5.0,
            "output_max": None,
            "monotonicity": Monotonicity.DECREASING,
            "kernel_data": torch.tensor([[0.0], [-1.0], [-1.0], [-1.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[0.0], [-1.0], [-1.0], [-1.0]]
            ).double(),
        },
        {
            "input_keypoints": np.linspace(1.0, 4.0, num=4),
            "output_min": -5.0,
            "output_max": None,
            "monotonicity": Monotonicity.DECREASING,
            "kernel_data": torch.tensor([[-3.0], [-1.0], [-2.0], [-2.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[-2.25], [-0.25], [-1.25], [-1.25]]
            ).double(),
        },
        {
            "input_keypoints": np.linspace(1.0, 4.0, num=4),
            "output_min": None,
            "output_max": -1.0,
            "monotonicity": Monotonicity.DECREASING,
            "kernel_data": torch.tensor([[1.0], [-1.0], [-2.0], [-3.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[-1.0], [-1.0], [-2.0], [-3.0]]
            ).double(),
        },
        {
            "input_keypoints": np.linspace(1.0, 4.0, num=4),
            "output_min": None,
            "output_max": -1.0,
            "monotonicity": Monotonicity.DECREASING,
            "kernel_data": torch.tensor([[0.0], [-1.0], [-1.0], [-1.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[-1.0], [-1.0], [-1.0], [-1.0]]
            ).double(),
        },
        {
            "input_keypoints": np.linspace(1.0, 4.0, num=4),
            "output_min": -5.0,
            "output_max": -3.0,
            "monotonicity": Monotonicity.DECREASING,
            "kernel_data": torch.tensor([[-3.0], [-1.0], [-2.0], [-2.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[-3.0], [0.0], [-1.0], [-1.0]]
            ).double(),
        },
    )
    def test_project_monotonic_bounds(
        self,
        input_keypoints,
        output_min,
        output_max,
        monotonicity,
        kernel_data,
        expected_projected_kernel_data,
    ) -> None:
        """Tests that kernel is properly projected into bounds with monotonicity."""
        calibrator = NumericalCalibrator(
            input_keypoints,
            output_min=output_min,
            output_max=output_max,
            monotonicity=monotonicity,
        )
        bias, heights = kernel_data[0:1], kernel_data[1:]
        # pylint: disable=protected-access
        (
            projected_bias,
            projected_heights,
        ) = calibrator._project_monotonic_bounds(bias, heights)
        # pylint: enable=protected-access
        projected_kernel_data = torch.cat((projected_bias, projected_heights), 0)
        self.assertTrue(
            torch.allclose(projected_kernel_data, expected_projected_kernel_data)
        )

    @parameterized.parameters(
        {
            "output_min": None,
            "output_max": None,
            "kernel_data": torch.tensor([[0.0], [1.0], [1.0], [1.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[0.0], [1.0], [1.0], [1.0]]
            ).double(),
        },
        {
            "output_min": 1.0,
            "output_max": None,
            "kernel_data": torch.tensor([[1.0], [1.0], [2.0], [3.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[1.0], [1.0], [2.0], [3.0]]
            ).double(),
        },
        {
            "output_min": 1.0,
            "output_max": None,
            "kernel_data": torch.tensor([[0.0], [1.0], [1.0], [1.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[1.0], [0.0], [1.0], [1.0]]
            ).double(),
        },
        {
            "output_min": None,
            "output_max": 5.0,
            "kernel_data": torch.tensor([[0.0], [1.0], [1.0], [1.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[0.0], [1.0], [1.0], [1.0]]
            ).double(),
        },
        {
            "output_min": None,
            "output_max": 5.0,
            "kernel_data": torch.tensor([[4.0], [1.0], [2.0], [1.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[4.0], [1.0], [0.0], [0.0]]
            ).double(),
        },
        {
            "output_min": 3.0,
            "output_max": 5.0,
            "kernel_data": torch.tensor([[4.0], [1.0], [-3.0], [1.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[4.0], [1.0], [-2.0], [0.0]]
            ).double(),
        },
    )
    def test_approximately_project_bounds_only(
        self,
        output_min,
        output_max,
        kernel_data,
        expected_projected_kernel_data,
    ) -> None:
        """Tests that bounds are properly projected when monotonicity is NONE."""
        calibrator = NumericalCalibrator(
            np.linspace(1.0, 4.0, num=4),
            output_min=output_min,
            output_max=output_max,
            monotonicity=Monotonicity.NONE,
        )
        bias, heights = kernel_data[0:1], kernel_data[1:]
        # pylint: disable=protected-access
        (
            projected_bias,
            projected_heights,
        ) = calibrator._approximately_project_bounds_only(bias, heights)
        # pylint: enable=protected-access
        projected_kernel_data = torch.cat((projected_bias, projected_heights), 0)
        self.assertTrue(
            torch.allclose(projected_kernel_data, expected_projected_kernel_data)
        )

    @parameterized.parameters(
        {
            "monotonicity": Monotonicity.INCREASING,
            "heights": torch.tensor([[1.0], [-2.0], [3.0], [-1.0], [0.5]]).double(),
            "expected_projected_heights": torch.tensor(
                [[1.0], [0.0], [3.0], [0.0], [0.5]]
            ).double(),
        },
        {
            "monotonicity": Monotonicity.DECREASING,
            "heights": torch.tensor([[-1.0], [2.0], [-3.0], [1.0], [-0.5]]).double(),
            "expected_projected_heights": torch.tensor(
                [[-1.0], [0.0], [-3.0], [0.0], [-0.5]]
            ).double(),
        },
    )
    def test_project_monotonicity(
        self,
        monotonicity,
        heights,
        expected_projected_heights,
    ) -> None:
        """Tests that monotonicity is properly projected"""
        calibrator = NumericalCalibrator(
            np.linspace(1.0, 4.0, num=4), monotonicity=monotonicity
        )
        # pylint: disable=protected-access
        projected_heights = calibrator._project_monotonicity(heights)
        # pylint: enable=protected-access
        self.assertTrue(torch.allclose(projected_heights, expected_projected_heights))

    @parameterized.parameters(
        {
            "monotonicity": Monotonicity.INCREASING,
            "output_min": None,
            "output_max": None,
            "kernel_data": torch.tensor([[0.0], [1.0], [1.0], [1.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[0.0], [1.0], [1.0], [1.0]]
            ).double(),
        },
        {
            "monotonicity": Monotonicity.INCREASING,
            "output_min": 1.0,
            "output_max": None,
            "kernel_data": torch.tensor([[1.0], [1.0], [2.0], [3.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[1.0], [1.0], [2.0], [3.0]]
            ).double(),
        },
        {
            "monotonicity": Monotonicity.INCREASING,
            "output_min": None,
            "output_max": 5.0,
            "kernel_data": torch.tensor([[1.0], [1.0], [2.0], [3.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[1.0], [0.6666666666666666], [1.3333333333333333], [2.0]]
            ).double(),
        },
        {
            "monotonicity": Monotonicity.DECREASING,
            "output_min": None,
            "output_max": -1.0,
            "kernel_data": torch.tensor([[-1.0], [-1.0], [-2.0], [-3.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[-1.0], [-1.0], [-2.0], [-3.0]]
            ).double(),
        },
        {
            "monotonicity": Monotonicity.DECREASING,
            "output_min": -5.0,
            "output_max": None,
            "kernel_data": torch.tensor([[-1.0], [-1.0], [-2.0], [-3.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[-1.0], [-0.6666666666666666], [-1.3333333333333333], [-2.0]]
            ).double(),
        },
    )
    def test_squeeze_by_scaling(
        self,
        monotonicity,
        output_min,
        output_max,
        kernel_data,
        expected_projected_kernel_data,
    ) -> None:
        """Tests that kernel is scaled into bound constraints properly."""
        calibrator = NumericalCalibrator(
            np.linspace(1.0, 4.0, num=4),
            output_min=output_min,
            output_max=output_max,
            monotonicity=monotonicity,
        )
        bias, heights = kernel_data[0:1], kernel_data[1:]
        # pylint: disable=protected-access
        projected_bias, projected_heights = calibrator._squeeze_by_scaling(
            bias, heights
        )
        # pylint: enable=protected-access
        projected_kernel_data = torch.cat((projected_bias, projected_heights), 0)
        self.assertTrue(
            torch.allclose(projected_kernel_data, expected_projected_kernel_data)
        )

    def test_training(self) -> None:  # pylint: disable=too-many-locals
        """Tests that the `NumericalCalibrator` module can learn f(x) = |x|."""
        num_examples = 1000
        output_min, output_max = 0.0, 2.0
        training_examples = torch.from_numpy(
            np.random.uniform(-output_max, output_max, size=num_examples)
        )[:, None]
        training_labels = torch.absolute(training_examples)

        calibrator = NumericalCalibrator(
            np.linspace(-2.0, 2.0, num=21),
            output_min=output_min,
            output_max=output_max,
            monotonicity=Monotonicity.NONE,
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
            torch.allclose(
                torch.absolute(keypoints_inputs), keypoints_outputs, atol=2e-2
            )
        )
        # pylint: enable=R0801
