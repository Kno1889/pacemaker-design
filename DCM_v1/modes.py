# Modes Module
#
# Version 0.2
# Created by: M. Lemcke
# Date Modified: Oct. 20, 2020
#
# Purpose: To store and edit parameter information for each operating mode on the pacemaker.
# This module interfaces with the GUI module by providing information on the current operating
# mode in use and the saved parameters of the other modes. The GUI module can also make requests
# to change the current operating mode on the pacemaker

import logging


all_modes = []      # List to hold all operating mode objects


# Range values of each parameter
# First digit in list is an identifier to determine how the list is read
# 0 = read following 2 numbers as the range (all values between are valid)
# 1 = read following entries as absolute values that are valid, if the entry is a list any number within the range is valid
ranges = {
    "upper_rate_limit": [0, 50, 175],
    "lower_rate_limit": [0, 30, 175],
    "ventricular_amplitude": [1, 0, [0.5, 3.2], [3.5, 7]],
    "ventricular_pulse_width": [1, 0.05, [0.1, 1.9]],
    "ventricular_sensitivity": [1, 0.25, 0.5, 0.75, [1, 10]],
    "ventricular_refactory_period": [0, 150, 500],
    "hysteresis": [1, True, False],
    "rate_smoothing": [1, 0, 3, 6, 9, 12, 15, 18, 21, 25],
    "atrial_amplitude": [1, 0, [0.5, 3.2], [3.5, 7]],
    "atrial_pulse_width": [1, 0.05, [0.1, 1.9]],
    "atrial_sensitivity": [1, 0.25, 0.5, 0.75, [1, 10]],
    "atrial_refactory_period": [0, 150, 500],
    "post_ventricular_atrial_refractory_period": [0, 150, 500]
}


class Mode():

    name = ''               # name code of the pacing module
    synch = False           # indicates if mode is synchronous
    currentMode = False     # indicates if the pacemaker is operating with the mode
    params = {}             # operation parameters and values

    # Initializes all variables from the given parameters
    def __init__(self, name, synch, params):
        self.name = name
        self.synch = synch
        self.params = params
        logger.info('Created %s mode', self.name)

    def invalidParams(self, params):
        global ranges
        invalid = []
        for p in params:
            validParam = False
            try:
                r = ranges[p]
            except KeyError:
                r = []
            if r[0] == 0 and params[p] >= r[1] and params[p] <= r[2]:
                validParam = True
            elif r[0] == 1:
                for i in range(1, len(r)):
                    if type(r[i]) == list and params[p] >= r[i][0] and params[p] <= r[i][1]:
                        validParam = True
                    elif r[i] == params[p]:
                        validParam = True
            if not validParam:
                invalid.append(p)
        return invalid


# Retrieves the list of modes for use outside of the module
def allModes():
    logger.debug('allModes() called')
    return all_modes


# Changes parameter values of the given mode if all parameter entries are valid, returns a list of the parameters that are not in the proper range
# Logs an error message if a parameter name doesn't match the parameters of the mode
# Returns error code 1 if the given mode is not valid, returns error code 2 if the parameters are of the wrong data type
def saveParamValues(modeEdit, parameterValues):
    if type(modeEdit) == Mode and type(parameterValues) == dict:
        logger.debug('saveParamValues() called for %s mode', modeEdit.name)
        invalid = modeEdit.invalidParams(parameterValues)
        if invalid == []:
            for mode in all_modes:
                if mode.name == modeEdit.name:
                    for param in parameterValues:
                        try:
                            mode.params[param]
                            mode.params[param] = parameterValues[param]
                        except KeyError:
                            logger.error(
                                '%s operating parameter does not exist in the %s mode', param, mode.name)
                    return invalid
            logger.warning('%s is not a valid mode', modeEdit.name)
            return 1
    else:
        logger.error('saveParamValues requires a Mode object and dictionary')
        return 2
    return invalid


# Makes the given mode as the current operating mode
def getCurrentMode():
    logger.debug('getCurrentMode() called')
    for mode in all_modes:
        if mode.currentMode == True:
            return mode


# sets the given mode as the current operating mode on the pacemaker
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
        {
            "upper_rate_limit": 120,
            "lower_rate_limit": 60,
            "ventricular_amplitude": 3.5,
            "ventricular_pulse_width": 0.4
        }
    )
    modes.append(voo)
    aoo = Mode(
        'aoo',
        False,
        {
            "upper_rate_limit": 120,
            "lower_rate_limit": 60,
            "atrial_amplitude": 3.5,
            "atrial_pulse_width": 0.4
        }
    )
    modes.append(aoo)
    vvi = Mode(
        'vvi',
        True,
        {
            "upper_rate_limit": 120,
            "lower_rate_limit": 60,
            "ventricular_amplitude": 3.5,
            "ventricular_pulse_width": 0.4,
            "ventricular_sensitivity": 2.5,
            "ventricular_refactory_period": 320,
            "hysteresis": False,
            "rate_smoothing": 0
        }
    )
    modes.append(vvi)
    aai = Mode(
        'aai',
        True,
        {
            "upper_rate_limit": 120,
            "lower_rate_limit": 60,
            "atrial_amplitude": 3.5,
            "atrial_pulse_width": 0.4,
            "atrial_sensitivity": 0.75,
            "atrial_refactory_period": 250,
            "post_ventricular_atrial_refractory_period": 250,
            "hysteresis": False,
            "rate_smoothing": 0
        }
    )
    modes.append(aai)
    return modes


# Starts the logging file
def _startLog():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARNING)

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
