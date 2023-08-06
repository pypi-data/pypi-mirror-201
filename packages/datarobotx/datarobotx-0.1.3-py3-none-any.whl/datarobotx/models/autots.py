#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd

from datarobotx.common import utils
from datarobotx.models.autopilot import AutopilotModel

logger = logging.getLogger("drx")


class AutoTSModel(AutopilotModel):
    """
    AutoTS orchestrator

    Applies automatic feature engineering and a model selection process
    optimized for the nuances of time-series modeling (e.g.
    automatic engineering of lag variables, handling of varying
    forecast horizons).

    Parameters
    ----------
    name : str, optional
        Name to use for the DataRobot project that will be created. Alias for the DR
        'project_name' configuration parameter.
    feature_window: tuple of int, optional
        Window of time relative to the forecast point over which to automatically
        derive features. Expected format is a tuple: (start, end) e.g. (-20, 0).
        Larger windows require more data for predictions. Window unit of time is
        automatically detected but can be explicitly specified separately.

        Alias for the DR 'feature_derivation_window_start' and
        'feature_derivation_window_end' configuration parameters.
    forecast_window: tuple of int, optional
        Window of time relative to the forecast point for which predictions
        are of interest. Expected format is a tuple: (start, end) e.g. (1, 5).
        Window unit of time is automatically detected but can be explicitly
        specified separately.

        Alias for the DR 'forecast_window_start' and 'forecast_window_end'
        configuration parameters.
    **kwargs
        Additional DataRobot configuration parameters for project creation and
        autopilot execution. See the DRConfig docs for usage examples.

    See Also
    --------
    DRConfig :
        Configuration object for DataRobot project and autopilot settings,
        also includes detailed examples of usage

    """

    def __init__(  # type: ignore[no-untyped-def]
        self,
        name: Optional[str] = None,
        feature_window: Optional[Tuple[int, int]] = None,
        forecast_window: Optional[Tuple[int, int]] = None,
        **kwargs,
    ):
        super().__init__(
            name=name,
            feature_window=feature_window,
            forecast_window=forecast_window,
            **kwargs,
        )

    def _prepare_params(self, **kwargs) -> Dict[str, Any]:  # type: ignore[no-untyped-def]
        """Translate parameter aliases, set required DR flags"""
        params = super()._prepare_params(**kwargs)
        if "feature_window" in params:
            feature_window = params.pop("feature_window")
            start, end = (None, None)
            if feature_window is not None:
                start, end = feature_window
            params["feature_derivation_window_start"] = start
            params["feature_derivation_window_end"] = end

        if "forecast_window" in params:
            forecast_window = params.pop("forecast_window")
            start, end = (None, None)
            if forecast_window is not None:
                start, end = forecast_window
            params["forecast_window_start"] = start
            params["forecast_window_end"] = end

        params["use_time_series"] = True
        params["cv_method"] = "datetime"
        return dict(params)

    def fit(  # type: ignore[no-untyped-def]
        self,
        X: Union[pd.DataFrame, str],
        datetime_partition_column: str,
        target: Optional[str] = None,
        multiseries_id_columns: Optional[Union[str, List[str]]] = None,
        segmentation_id_column: Optional[str] = None,
        **kwargs,
    ) -> AutoTSModel:
        """
        Fit time-series challenger models using DataRobot

        Automatically engineers temporally lagged features and establishes
        time-series champion models across a forecast horizon of interest.

        Parameters
        ----------
        X : pandas.DataFrame
            Training dataset for challenger models.
            If str, can be AI catalog dataset id or name (if unambiguous)
        target : str, default=None
            Column name from the dataset to be used as the target variable.
            If None, TS anomaly detection will be executed.
        datetime_partition_column : str
            Column name from the dataset containing the primary date/time feature to
            be used in partitioning, feature engineering, and establishing forecast
            horizons
        multiseries_id_columns : str or list of str, optional
            Column name from the dataset containing a series identifier for each row.
            If specified, DataRobot will treat this as a multiseries problem. Presently
            only a single series id column is supported.
        segmentation_id_column: str, optional
            Column name from the dataset containing a segmentation identifier for each row.
            If specified, DataRobot will perform segmented modeling to break the problem
            into multiple projects.
        **kwargs :
            Additional optional fit-time parameters to pass to DataRobot i.e. 'weights'

        See Also
        --------
        DRConfig :
            Configuration object for DataRobot project and autopilot settings,
            also includes detailed examples of usage.
        """
        utils.create_task_new_thread(
            self._fit(
                X,
                target=target,
                datetime_partition_column=datetime_partition_column,
                multiseries_id_columns=multiseries_id_columns,
                segmentation_id_column=segmentation_id_column,
                **kwargs,
            )
        )
        return self

    def _set_fit_params(self, **kwargs) -> None:  # type: ignore[no-untyped-def]
        """Handle time-series specific fit-time parameters"""
        if "multiseries_id_columns" in kwargs and isinstance(kwargs["multiseries_id_columns"], str):
            kwargs["multiseries_id_columns"] = [kwargs["multiseries_id_columns"]]

        segmentation_id_column = kwargs.pop("segmentation_id_column")
        if segmentation_id_column is not None:
            logger.info(
                "Segmentation values provided. Drx cannot make predictions until "
                "Autopilot is finished. These projects can take a while.."
            )
            self._segmentation_id_column = [segmentation_id_column]
        return super()._set_fit_params(**kwargs)
