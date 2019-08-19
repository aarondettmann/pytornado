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
# * Alessandro Gastaldi
# * Aaron Dettmann

"""
Data structure for aircraft flight state.

Developed for Airinnova AB, Stockholm, Sweden.
"""


import logging

import numpy as np
from numpy import cos, sin, deg2rad
from ambiance import Atmosphere

from pytornado.objects.utils import FixedNamespace, FixedOrderedDict

logger = logging.getLogger(__name__)


# Fundamental parameters used to define a flight state
STATE_BASE_PARAMS = ['airspeed', 'density', 'alpha', 'beta', 'rate_P', 'rate_Q', 'rate_R']


class StateDefinitionError(Exception):
    """Raised when properties of FLIGHTSTATE are ill-defined."""

    pass


class FlightState:
    """
    Data structure for the PyTornado flight conditions

    Attributes:
        :aero: (dict) aerodynamic operating parameters
        :refs: (dict) reference values (from AIRCRAFT)
        :state: (bool) FLIGHTSTATE definition status

    Note:
        * The angles 'alpha' and 'beta' are assumed to be given in DEGREES!
          Alpha and beta are user input. The angles stored in this state class
          will not be changed during runtime.
    """

    def __init__(self):
        """
        Initialise instance of FLIGHTSTATE.

            * FLIGHTSTATE inherits from FIXEDNAMESPACE.
            * Upon initialisation, attributes of FLIGHTSTATE are created and fixed.
            * Only existing attributes may be modified afterward.
        """

        self.aero = FixedOrderedDict()
        self.aero['alpha'] = None
        self.aero['beta'] = None
        self.aero['rate_P'] = None
        self.aero['rate_Q'] = None
        self.aero['rate_R'] = None
        self.aero['mach'] = None
        self.aero['altitude'] = None
        self.aero['airspeed'] = None
        self.aero['density'] = None
        self.aero._freeze()

        # Number of values in the aeroperformance map
        self.num_apm_values = 0
        self.idx_current_state = 0

    @property
    def free_stream_velocity_vector(self):
        """Return the free stream velocity vector (incoming flow)"""

        alpha = deg2rad(self.aero['alpha'])
        beta = deg2rad(self.aero['beta'])
        airspeed = self.aero['airspeed']

        # if None in [alpha, beta, airspeed]:
        #     raise RuntimeError("'alpha', 'beta' and 'airspeed' must be set")
        ###########################
        airspeed = 100
        alpha = deg2rad(3)
        beta = 0
        ###########################

        free_stream_vel = airspeed*np.array([cos(alpha)*cos(beta),
                                             -sin(beta),
                                             sin(alpha)*cos(beta)])
        return free_stream_vel

    def update_from_dict(self, aero):
        """Update state"""

        array_lenghts = set()
        for key, value in aero.items():
            if not isinstance(value, list):
                value = [value]

            array_lenghts.add(len(value))
            self.aero[key] = value

        if len(array_lenghts) > 1:
            msg = "State arrays have different lenghts!"
            raise ValueError(msg)

        self.num_apm_values = int(list(array_lenghts)[0])

#####################################################
        # UPDATE!!!
#####################################################
        # # We can allow either "airspeed and density" or "mach number and altitude"
        # all_values = {'airspeed', 'mach', 'density', 'altitude'}
        # pairs = [
        #     {'airspeed', 'density'},
        #     {'airspeed', 'altitude'},
        #     {'mach', 'altitude'},
        # ]

        # err_msg = """
        # Invalid combination: You may set:
        # (1) 'airspeed' and 'density' or
        # (2) 'airspeed' and 'altitude' or
        # (3) 'mach' and 'altitude'
        # Make sure the remaining values are all set to 'None'.
        # """

        # for pair in pairs:
        #     pair_values = [self.aero.get(v, None) for v in pair]
        #     other_values = [self.aero.get(v, None) for v in all_values.difference(pair)]

        #     if all(v is not None for v in pair_values):
        #         if any(v is not None for v in other_values):
        #             raise ValueError(err_msg)

        # # Compute airspeed and density if necessary
        # density = None
        # speed_of_sound = None
        # if self.aero['altitude'] is not None:
        #     atmosphere = Atmosphere(self.aero['altitude'])
        #     density = float(atmosphere.density)
        #     speed_of_sound = float(atmosphere.speed_of_sound)

        # if self.aero['density'] is None:
        #     self.aero['density'] = density

        # if self.aero['mach'] is not None:
        #     self.aero['airspeed'] = self.aero['mach']*speed_of_sound
####################################################
        # UPDATE!!!
#####################################################

    def check(self):
        pass
    #     """Check properties of state settings"""

    #     logger.info("Checking aerodynamic settings...")

    #     # Airspeed
    #     if self.aero['airspeed'] is None:
    #         raise StateDefinitionError("'aero.airspeed' is not defined.")
    #     elif not isinstance(self.aero['airspeed'], (float, int)):
    #         raise TypeError("'aero.airspeed' must be FLOAT [m/s].")
    #     else:
    #         self.aero['airspeed'] = float(self.aero['airspeed'])
    #     # ------------------------------------------------------------

    #     # angle of attack
    #     if self.aero['alpha'] is None:
    #         raise StateDefinitionError("'aero.alpha' is not defined.")
    #     elif not isinstance(self.aero['alpha'], (float, int)):
    #         raise TypeError("'aero.alpha' must be FLOAT [deg].")
    #     elif not -90.0 <= self.aero['alpha'] <= +90.0:
    #         raise ValueError("'aero.alpha' too large.")
    #     else:
    #         self.aero['alpha'] = float(self.aero['alpha'])

    #     # sideslip angle
    #     if self.aero['beta'] is None:
    #         raise StateDefinitionError("'aero.beta' is not defined.")
    #     elif not isinstance(self.aero['beta'], (float, int)):
    #         raise TypeError("'aero.beta' must be FLOAT [deg].")
    #     elif not -90.0 <= self.aero['beta'] <= +90.0:
    #         raise ValueError("'aero.beta' too large.")
    #     else:
    #         self.aero['beta'] = float(self.aero['beta'])

    #     # x-rotation rate
    #     if self.aero['rate_P'] is None:
    #         raise StateDefinitionError("'aero.rate_P' is not defined.")
    #     elif not isinstance(self.aero['rate_P'], (float, int)):
    #         raise TypeError("'aero.rate_P' must be FLOAT [rad/s].")
    #     else:
    #         self.aero['rate_P'] = float(self.aero['rate_P'])

    #     # y-rotation rate
    #     if self.aero['rate_Q'] is None:
    #         raise StateDefinitionError("'aero.rate_Q' is not defined.")
    #     elif not isinstance(self.aero['rate_Q'], (float, int)):
    #         raise TypeError("'aero.rate_Q' must be FLOAT [rad/s].")
    #     else:
    #         self.aero['rate_Q'] = float(self.aero['rate_Q'])

    #     # z-rotation rate
    #     if self.aero['rate_R'] is None:
    #         raise StateDefinitionError("'aero.rate_R' is not defined.")
    #     elif not isinstance(self.aero['rate_R'], (float, int)):
    #         raise TypeError("'aero.rate_R' must be FLOAT [rad/s].")
    #     else:
    #         self.aero['rate_R'] = float(self.aero['rate_R'])

    #     # density
    #     if self.aero['density'] is None:
    #         raise StateDefinitionError("'aero.density' is not defined.")
    #     elif not isinstance(self.aero['density'], (float, int)):
    #         raise TypeError("'aero.density' must be positive FLOAT [kgm-3].")
    #     elif not self.aero['density'] >= 0.0:
    #         raise ValueError("'aero.density' must be positive.")
    #     else:
    #         self.aero['density'] = float(self.aero['density'])

    #     # 2. SET STATE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    #     self.state = True

    def iter_aero_states(self):
        """
        Iterator which yields a dictionary for each flight state
        """

        for i in range(0, self.num_apm_values):
            current_state = FixedOrderedDict()
            for param in STATE_BASE_PARAMS:
                current_state[param] = float(self.aero[param][i])

            current_state._freeze()
            yield current_state
