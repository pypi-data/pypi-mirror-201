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
"""Tests for Linear module."""
import unittest

import numpy as np
import torch
from absl.testing import parameterized

from pytorch_calibrated.enums import Monotonicity
from pytorch_calibrated.layers.linear import Linear

from .utils import train_calibrated_module


# pylint: disable-next=missing-class-docstring
class TestLinear(parameterized.TestCase, unittest.TestCase):
    @parameterized.parameters(
        {
            "input_dim": 5,
            "monotonicities": None,
            "use_bias": True,
            "weighted_average": False,
        },
        {
            "input_dim": 5,
            "monotonicities": None,
            "use_bias": True,
            "weighted_average": True,
        },
    )
    def test_initialization(
        self, input_dim, monotonicities, use_bias, weighted_average
    ) -> None:
        """Tests that Linear initialization works properly"""
        linear = Linear(input_dim, monotonicities, use_bias, weighted_average)
        self.assertEqual(linear.input_dim, input_dim)
        self.assertEqual(
            linear.monotonicities,
            monotonicities
            if not weighted_average
            else [Monotonicity.INCREASING] * input_dim,
        )
        self.assertEqual(linear.use_bias, use_bias if not weighted_average else False)
        self.assertEqual(linear.weighted_average, weighted_average)
        self.assertTrue(
            torch.allclose(
                linear.kernel.data,
                torch.tensor([[1.0 / input_dim] * input_dim]).double(),
            )
        )
        if use_bias:
            self.assertTrue(linear.bias.data.size() == torch.Size([1]))
            self.assertTrue(torch.all(linear.bias.data == 0.0))

    @parameterized.parameters(
        {
            "kernel_data": torch.tensor([[1.0], [2.0], [3.0]]).double(),
            "bias_data": None,
            "inputs": torch.tensor(
                [[1.0, 1.0, 1.0], [3.0, 2.0, 1.0], [1.0, -2.0, 3.0]]
            ).double(),
            "expected_outputs": torch.tensor([[6.0], [10.0], [6.0]]).double(),
        },
        {
            "kernel_data": torch.tensor([[1.0], [2.0], [1.0]]).double(),
            "bias_data": torch.tensor([-1.0]).double(),
            "inputs": torch.tensor(
                [[1.0, 2.0, 3.0], [2.0, 3.0, 1.0], [4.0, -1.0, 2.0]]
            ).double(),
            "expected_outputs": torch.tensor([[7.0], [8.0], [3.0]]).double(),
        },
    )
    def test_forward(self, kernel_data, bias_data, inputs, expected_outputs) -> None:
        """Tests that forward properly combined inputs."""
        linear = Linear(kernel_data.size()[0], use_bias=bias_data is not None)
        linear.kernel.data = kernel_data
        if bias_data is not None:
            linear.bias.data = bias_data
        outputs = linear(inputs)
        self.assertTrue(torch.allclose(outputs, expected_outputs))

    @parameterized.parameters(
        {
            "monotonicities": None,
            "kernel_data": torch.tensor([[1.2], [2.5], [3.1]]).double(),
            "bias_data": None,
        },
        {
            "monotonicities": None,
            "kernel_data": torch.tensor([[1.2], [2.5], [3.1]]).double(),
            "bias_data": torch.tensor([1.0]).double(),
        },
        {
            "monotonicities": [Monotonicity.NONE, Monotonicity.NONE, Monotonicity.NONE],
            "kernel_data": torch.tensor([[1.2], [2.5], [3.1]]).double(),
            "bias_data": torch.tensor([1.0]).double(),
        },
        {
            "monotonicities": [Monotonicity.NONE, Monotonicity.NONE, Monotonicity.NONE],
            "kernel_data": torch.tensor([[1.2], [2.5], [3.1]]).double(),
            "bias_data": torch.tensor([1.0]).double(),
        },
    )
    def test_constrain_no_constraints(
        self, monotonicities, kernel_data, bias_data
    ) -> None:
        """Tests that constrain does nothing when there are no constraints."""
        linear = Linear(kernel_data.size()[0], monotonicities=monotonicities)
        linear.kernel.data = kernel_data
        if bias_data is not None:
            linear.bias.data = bias_data
        linear.constrain()
        self.assertTrue(torch.allclose(linear.kernel.data, kernel_data))
        if bias_data is not None:
            self.assertTrue(torch.allclose(linear.bias.data, bias_data))

    @parameterized.parameters(
        {
            "monotonicities": [
                Monotonicity.NONE,
                Monotonicity.INCREASING,
                Monotonicity.DECREASING,
            ],
            "kernel_data": torch.tensor([[1.0], [-0.2], [0.2]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[1.0], [0.0], [0.0]]
            ).double(),
        },
        {
            "monotonicities": [
                Monotonicity.NONE,
                Monotonicity.INCREASING,
                Monotonicity.NONE,
            ],
            "kernel_data": torch.tensor([[1.0], [0.2], [-2.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[1.0], [0.2], [-2.0]]
            ).double(),
        },
        {
            "monotonicities": [
                Monotonicity.DECREASING,
                Monotonicity.DECREASING,
            ],
            "kernel_data": torch.tensor([[-1.0], [0.2]]).double(),
            "expected_projected_kernel_data": torch.tensor([[-1.0], [0.0]]).double(),
        },
        {
            "monotonicities": [
                Monotonicity.INCREASING,
                Monotonicity.INCREASING,
            ],
            "kernel_data": torch.tensor([[-1.0], [1.0]]).double(),
            "expected_projected_kernel_data": torch.tensor([[0.0], [1.0]]).double(),
        },
    )
    def test_constrain_monotonicities(
        self, monotonicities, kernel_data, expected_projected_kernel_data
    ) -> None:
        """Tests that constrain properly projects kernel according to monotonicies."""
        linear = Linear(kernel_data.size()[0], monotonicities=monotonicities)
        linear.kernel.data = kernel_data
        linear.constrain()
        self.assertTrue(
            torch.allclose(linear.kernel.data, expected_projected_kernel_data)
        )

    @parameterized.parameters(
        {
            "kernel_data": torch.tensor([[1.0], [2.0], [3.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[1 / 6], [2 / 6], [0.5]]
            ).double(),
        },
        {
            "kernel_data": torch.tensor([[2.0], [-1.0], [1.0], [3.0]]).double(),
            "expected_projected_kernel_data": torch.tensor(
                [[2 / 6], [0.0], [1 / 6], [0.5]]
            ).double(),
        },
    )
    def test_constrain_weighted_average(
        self, kernel_data, expected_projected_kernel_data
    ) -> None:
        """Tests that constrain properly projects kernel to be a weighted average."""
        linear = Linear(kernel_data.size()[0], weighted_average=True)
        linear.kernel.data = kernel_data
        linear.constrain()
        self.assertTrue(
            torch.allclose(linear.kernel.data, expected_projected_kernel_data)
        )

    def test_training(self) -> None:
        """Tests that the `Linear` module can learn f(x_1,x_2) = 2x_1 + 3x_2"""
        num_examples = 1000
        input_min, input_max = 0.0, 10.0
        training_examples = torch.from_numpy(
            np.random.uniform(input_min, input_max, size=(1000, 2))
        )
        linear_coefficients = torch.tensor([2.0, 3.0]).double()
        training_labels = torch.sum(
            linear_coefficients * training_examples, dim=1, keepdim=True
        )

        linear = Linear(2, use_bias=False)
        loss_fn = torch.nn.MSELoss()
        optimizer = torch.optim.Adam(linear.parameters(), lr=1e-2)

        train_calibrated_module(
            linear,
            training_examples,
            training_labels,
            loss_fn,
            optimizer,
            300,
            num_examples // 10,
        )

        self.assertTrue(
            torch.allclose(torch.squeeze(linear.kernel.data), linear_coefficients)
        )
