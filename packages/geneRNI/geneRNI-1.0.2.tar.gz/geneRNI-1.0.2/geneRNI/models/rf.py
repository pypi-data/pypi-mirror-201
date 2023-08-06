# -*- coding: utf-8 -*-
#
#  rf.py
#
#  Copyright 2022 Antoine Passemiers <antoine.passemiers@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

from typing import Dict, Any

import numpy as np
from sklearn.ensemble import RandomForestRegressor

from geneRNI.models import BaseWrapper


class RFWrapper(BaseWrapper):

    @staticmethod
    def new_estimator(**kwargs) -> RandomForestRegressor:
        return RandomForestRegressor(oob_score=True, **kwargs)

    @staticmethod
    def compute_feature_importances(estimator: RandomForestRegressor) -> np.array:
        # return np.array([e.tree_.compute_feature_importances(normalize=False)
        #                         for e in estimator.estimators_])
        return estimator.feature_importances_

    @staticmethod
    def get_default_parameters() -> Dict[str, Any]:
        return dict(
            estimator_t='RF',
            min_samples_leaf=1,
            # criterion = 'absolute_error',
            n_estimators=200,
            decay_coeff=.9,
            n_jobs=10
        )

    @staticmethod
    def get_grid_parameters() -> Dict[str, Any]:
        return dict(
            min_samples_leaf=np.arange(1, 10, 1),
            max_depth=np.arange(10, 50, 5),
            decay_coeff=np.arange(0, 1, .1),
        )
