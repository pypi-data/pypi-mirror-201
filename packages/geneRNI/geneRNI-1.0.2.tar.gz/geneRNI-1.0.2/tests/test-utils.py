# -*- coding: utf-8 -*-
#
#  test-utils.py
#
#  Copyright 2023 Antoine Passemiers <antoine.passemiers@gmail.com>
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

import math

from geneRNI.utils import is_lambda_function


def test_lambda_function():
    assert is_lambda_function(lambda x: 2 * x + 1)
    assert not is_lambda_function(is_lambda_function)
    assert not is_lambda_function(math.exp)
    assert not is_lambda_function(26.92)
    assert not is_lambda_function('Hello world')
    assert True
