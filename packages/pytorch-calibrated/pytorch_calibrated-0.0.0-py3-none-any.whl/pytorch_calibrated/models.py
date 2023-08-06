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
"""PyTorch Calibrated Models to easily implement common calibrated model architectures.

PyTorch Calibrated Models make it easy to construct common calibrated model
architectures. To construct a PyTorch Calibrated Model, pass a calibrated modeling
config to the corresponding calibrated model.
"""
from typing import List, Optional, Union

import numpy as np
import torch

from .configs import CategoricalFeatureConfig, NumericalFeatureConfig
from .enums import (
    CategoricalCalibratorInit,
    FeatureType,
    Monotonicity,
    NumericalCalibratorInit,
)
from .layers.categorical_calibrator import CategoricalCalibrator
from .layers.linear import Linear
from .layers.numerical_calibrator import NumericalCalibrator


# pylint: disable-next=too-many-instance-attributes
class CalibratedLinear(torch.nn.Module):
    """PyTorch Calibrated Linear Model.

    Creates a `torch.nn.Module` representing a calibrated linear model, which will be
    constructed using the provided model configuration. Note that the model inputs
    should match the order in which they are defined in the `feature_configs`.

    Attributes:
        - All `__init__` arguments.
        calibrators: A dictionary that maps feature names to their calibrators.
        linear: The `Linear` layer of the model.
        output_calibrator: The output `NumericalCalibrator` calibration layer. This
            will be `None` if no output calibration is desired.

    Example:

    ```python
    csv_data = CSVData(...)

    feature_configs = [...]
    calibrated_model = CalibratedLinear(feature_configs, ...)

    loss_fn = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(calibrated_model.parameters(recurse=True), lr=1e-1)

    csv_data.prepare(feature_configs, "target", ...)
    for epoch in range(100):
        for examples, targets in csv_data.batch(64):
            optimizer.zero_grad()
            outputs = calibrated_model(inputs)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()
            calibrated_model.constrain()
    ```
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        feature_configs: List[Union[NumericalFeatureConfig, CategoricalFeatureConfig]],
        output_min: Optional[float] = None,
        output_max: Optional[float] = None,
        use_bias: bool = True,
        output_calibration_num_keypoints: Optional[int] = None,
    ) -> None:
        """Initializes an instance of `CalibratedLinear`.

        Args:
            feature_configs: A list of numerical and/or categorical feature configs.
            output_min: The minimum output value for the model. If `None`, the minimum
                output value will be unbounded.
            output_max: The maximum output value for the model. If `None`, the maximum
                output value will be unbounded.
            use_bias: Whether to use a bias term for the linear combination. If any of
                `output_min`, `output_max`, or `output_calibration_num_keypoints` are
                set, a bias term will not be used regardless of the setting here.
            output_calibration_num_keypoints: The number of keypoints to use for the
                output calibrator. If `None`, no output calibration will be used.

        Raises:
            ValueError: If any feature configs are not `NUMERICAL` or `CATEGORICAL`.
        """
        super().__init__()

        self.feature_configs = feature_configs
        self.output_min = output_min
        self.output_max = output_max
        self.use_bias = use_bias
        self.output_calibration_num_keypoints = output_calibration_num_keypoints

        linear_monotonicities = []
        self.calibrators = torch.nn.ModuleDict()
        for feature_config in feature_configs:
            if feature_config.feature_type == FeatureType.NUMERICAL:
                self.calibrators[feature_config.feature_name] = NumericalCalibrator(
                    input_keypoints=feature_config.input_keypoints,
                    missing_input_value=feature_config.missing_input_value,
                    output_min=output_min,
                    output_max=output_max,
                    monotonicity=feature_config.monotonicity,
                    kernel_init=NumericalCalibratorInit.EQUAL_SLOPES,
                )
                if feature_config.monotonicity == Monotonicity.NONE:
                    linear_monotonicities.append(Monotonicity.NONE)
                else:
                    linear_monotonicities.append(Monotonicity.INCREASING)
            elif feature_config.feature_type == FeatureType.CATEGORICAL:
                self.calibrators[feature_config.feature_name] = CategoricalCalibrator(
                    num_categories=len(feature_config.categories),
                    missing_input_value=feature_config.missing_input_value,
                    output_min=output_min,
                    output_max=output_max,
                    monotonicity_pairs=feature_config.monotonicity_index_pairs,
                    kernel_init=CategoricalCalibratorInit.UNIFORM,
                )
                if not feature_config.monotonicity_pairs:
                    linear_monotonicities.append(Monotonicity.NONE)
                else:
                    linear_monotonicities.append(Monotonicity.INCREASING)
            else:
                raise ValueError(
                    f"Unknown feature type {feature_config.feature_type} for feature "
                    f"{feature_config.feature_name}"
                )

        self.linear = Linear(
            input_dim=len(feature_configs),
            monotonicities=linear_monotonicities,
            use_bias=use_bias,
            weighted_average=(
                output_min is not None
                or output_max is not None
                or output_calibration_num_keypoints
            ),
        )

        self.output_calibrator = None
        if output_calibration_num_keypoints:
            non_monotonic = all(m == Monotonicity.NONE for m in linear_monotonicities)
            self.output_calibrator = NumericalCalibrator(
                input_keypoints=np.linspace(
                    0.0, 1.0, num=output_calibration_num_keypoints
                ),
                missing_input_value=None,
                output_min=output_min,
                output_max=output_max,
                monotonicity=Monotonicity.NONE
                if non_monotonic
                else Monotonicity.INCREASING,
                kernel_init=NumericalCalibratorInit.EQUAL_HEIGHTS,
            )

    def forward(self, x: torch.Tensor) -> torch.Tensor:  # pylint: disable=invalid-name
        """Runs an input through the network to produce a calibrated linear output.

        Args:
            x: The input tensor of feature values of shape `(batch_size, num_features)`.

        Returns:
            torch.Tensor of shape `(batch_size, 1)` containing the model output result.
        """
        result = torch.column_stack(
            tuple(
                calibrator(x[:, i, None])
                for i, calibrator in enumerate(self.calibrators.values())
            )
        )
        result = self.linear(result)
        if self.output_calibrator is not None:
            result = self.output_calibrator(result)
        return result

    @torch.no_grad()
    def constrain(self) -> None:
        """Constrains the model into desired constraints specified by the config."""
        for calibrator in self.calibrators.values():
            calibrator.constrain()
        self.linear.constrain()
        if self.output_calibrator:
            self.output_calibrator.constrain()
