# Modes Module
#
# Version 1.0
# Created by: M. Lemcke
# Date Modified: Oct. 2, 2020
#
# Purpose: To store and edit parameter information for each operating mode on the pacemaker.
# This module interfaces with the GUI module by providing information on the current operating
# mode in use and the saved parameters of the other modes. The GUI module can also make requests
# to change the current operating mode on the pacemaker

import logging


all_modes = []      # List to hold all operating mode objects


class Mode():

    name = ''               # name code of the pacing module
    synch = False           # indicates if mode is synchronous
    currentMode = False     # indicates if the pacemaker is operating with the mode
    params = {}             # operation parameters and values

    # Initializes all variables from the given parameters
    def __init__(self, name, synch, **kwargs):
        self.name = name
        self.synch = synch
        try:
            for arg in kwargs:
                self.params[arg] = kwargs[arg]
        except:
            logging.error('Keyword argument error creating %s', self.name)
        logging.info('Created %s mode', self.name)


# Retrieves the list of modes for use outside of the module
def allModes():
    logging.debug('allModes() called')
    return all_modes


# Changes parameter values of the given mode
# Logs an error message if a parameter name doesn't match the parameters of the mode
def saveParamValues(modeEdit, parameterValues):
    logging.debug('saveParamValues() called for %s mode', modeEdit.name)
    for mode in all_modes:
        if mode.name == modeEdit.name:
            for param in parameterValues:
                try:
                    mode.params[param]
                    mode.params[param] = parameterValues[param]
                except KeyError:
                    logging.error(
                        '%s operating parameter does not exist in the %s mode', param, mode.name)


# Makes the given mode as the current operating mode
def setCurrentMode(currMode):
    logging.debug('setCurrentMode() called for %s mode', currMode.name)
    for mode in all_modes:
        if mode.name == currMode.name:
            mode.currentMode = True
            logging.info('%s is the current mode', mode.name)
        else:
            mode.currentMode = False

# Defines all pacing modes and default values


def _createModes():
    logging.debug('_createModes() called')
    modes = []
    voo = Mode(
        'voo',
        False,
        upper_rate_limit=80,
        lower_rate_limit=60,
        ventricular_amplitude=45,
        ventricular_pulse_width=30
    )
    modes.append(voo)
    aoo = Mode(
        'aoo',
        False,
        upper_rate_limit=80,
        lower_rate_limit=60,
        atrial_amplitude=45,
        atrial_pulse_width=30
    )
    modes.append(aoo)
    vvi = Mode(
        'vvi',
        True,
        upper_rate_limit=80,
        lower_rate_limit=60,
        ventricular_amplitude=45,
        ventricular_pulse_width=30,
        ventricular_sensitivity=10,
        ventricular_refactory_period=5,
        hysteresis=25,
        rate_smoothing=60
    )
    modes.append(vvi)
    aai = Mode(
        'aai',
        True,
        upper_rate_limit=80,
        lower_rate_limit=60,
        atrial_amplitude=45,
        atrial_pulse_width=30,
        atrial_sensitivity=10,
        atrial_refactory_period=5,
        post_ventricular_atrial_refractory_period=35,
        hysteresis=25,
        rate_smoothing=60
    )
    modes.append(aai)
    return modes


# Starts the logging file
def _startLog():
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s: %(message)s',
        filename='DCM_v1/logs/modes.log',
        level=logging.DEBUG
    )
    logging.info('Logging started')


# Run on import of module
_startLog()
all_modes = _createModes()
