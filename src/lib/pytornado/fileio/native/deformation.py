#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2017-2019 Airinnova AB and the PyTornado authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------

# Authors:
# * Aaron Dettmann

"""
Reading the aircraft deformation file.

Developed at Airinnova AB, Stockholm, Sweden.
"""

import os
import logging
import json

import numpy as np
from commonlibs.logger import truncate_filepath
from commonlibs.math.vectors import vector_projection
from aeroframe.fileio.serialise import load_json_def_field

import pytornado.objects.objecttools as ot

logger = logging.getLogger(__name__)


def load(aircraft, settings):
    """
    Loads the aircraft deformation file if it exitsts.

    Args:
        :aircraft: (obj) aircraft
        :settings: (obj) settings
    """

    filepath = settings.paths('f_deformation')
    logger.info(f"Reading deformation from file '{truncate_filepath(filepath)}'")

    if not os.path.exists(filepath):
        raise IOError(f"file '{filepath}' not found")

    # File is empty or as good as (this also catches empty JSON file: '{}')
    if os.stat(filepath).st_size < 10:
        logger.warning(f"Empty deformation file. No deformations are modelled.")
        return

    def_fields = load_json_def_field(filepath)
    for wing_uid, def_field in def_fields.items():
        aircraft.wings[wing_uid].def_field = def_field

        # TODO: handle exception
        # TODO: check deformation continuity
