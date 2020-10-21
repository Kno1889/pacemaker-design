# Modes Module
#
# Version 1.1
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
            logger.error('Keyword argument error creating %s', self.name)
        logger.info('Created %s mode', self.name)


# Retrieves the list of modes for use outside of the module
def allModes():
    logger.debug('allModes() called')
    return all_modes


# Changes parameter values of the given mode
# Logs an error message if a parameter name doesn't match the parameters of the mode
def saveParamValues(modeEdit, parameterValues):
    if type(modeEdit) == Mode and type(parameterValues) == dict:
        logger.debug('saveParamValues() called for %s mode', modeEdit.name)
        for mode in all_modes:
            if mode.name == modeEdit.name:
                for param in parameterValues:
                    try:
                        mode.params[param]
                        mode.params[param] = parameterValues[param]
                    except KeyError:
                        logger.error(
                            '%s operating parameter does not exist in the %s mode', param, mode.name)
                return None
        logger.warning('%s is not a valid mode', modeEdit.name)
    else:
        logger.error('saveParamValues requires a Mode object and dictionary')

# Makes the given mode as the current operating mode


def setCurrentMode(currMode):
    if type(currMode) == Mode:
        logger.debug('setCurrentMode() called for %s mode', currMode.name)
        for mode in all_modes:
            if mode.name == currMode.name:
                mode.currentMode = True
                logger.info('%s is the current mode', mode.name)
                return None
            else:
                mode.currentMode = False
        logger.warning('%s is not a valid mode', currMode.name)
    else:
        logger.error('setCurrentMode requires a Mode object')

# Defines all pacing modes and default values


def _createModes():
    logger.debug('_createModes() called')
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
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    f_handler = logging.FileHandler('DCM_v1/logs/file.log')
    l_handler = logging.FileHandler('DCM_v1/logs/modes.log')
    f_formatter = logging.Formatter(
        '[%(asctime)s] - %(name)s -  %(levelname)s: %(message)s')
    l_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s')
    f_handler.setFormatter(f_formatter)
    l_handler.setFormatter(l_formatter)
    logger.addHandler(f_handler)
    logger.addHandler(l_handler)
    return logger


# Run on import
logger = _startLog()
all_modes = _createModes()
