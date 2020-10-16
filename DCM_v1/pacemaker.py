# Pacemaker Module
#
# Version 1.0
# Created by: M. Lemcke
# Date Modified: Oct. 16, 2020
#
# Purpose: To determine which pacemaker is currently connected to the DCM and store all
# information on past connected pacemakers and their users. The module will directly
# interface with the GUI when connecting new or existing pacemakers and the Users module
# when registering new users or storing information in the data module.

import logging
import data


all_pacemakers = []  # a list of all pacemaker objects storing information of all pacemakers that have been connected to the DCM


class Pacemaker():

    model = ''          # stores the model number/serial number/identifier of the pacemaker
    numUsers = 0        # stores the number of users registered on the pacemaker
    lastUsed = False    # determines if pacemaker was the last to be connected

    def __init__(self, model, numUsers, lastUsed):
        self.model = model
        self.numUsers = numUsers
        self.lastUsed = lastUsed


# connects to the given pacemaker. Returns true if the given pacemaker was the last to be connected
def connect(model):
    logger.debug('connect() called')
    global all_pacemakers
    lastConnected = False
    if _currentPacemaker() == model:
        lastConnected = True
        logger.info('Pacemaker %s is already connected', model)
    else:
        newPacer = True
        for p in all_pacemakers:
            if p.model == model:
                newPacer = False
                info = {
                    'model': p.model,
                    'numUsers': p.numUsers,
                    'lastUsed': p.lastUsed
                }
                data.setConnectedPacemaker(info)
                logger.info('Pacemaker %s is now connected', model)
        if newPacer:
            all_pacemakers.append(_addNewPacemaker(model))
            info = {
                'model': all_pacemakers[-1].model,
                'numUsers': all_pacemakers[-1].numUsers,
                'lastUsed': all_pacemakers[-1].lastUsed
            }
            data.setConnectedPacemaker(info)
            logger.info('Pacemaker %s is now connected', model)
    _getData()
    return lastConnected


# creates a new pacemaker with the given model number and returns the object
def _addNewPacemaker(model):
    logger.debug('_addNewPacemaker called')
    newP = Pacemaker(model, 0, False)
    logger.info('Pacemaker %s created', newP.model)
    return newP


# returns the model number of the connected pacemaker
def _currentPacemaker():
    logger.debug('_currentPacemaker() called')
    global all_pacemakers
    for p in all_pacemakers:
        if p.lastUsed:
            logger.info('Pacemaker %s is connected', p.model)
            return p.model
    return None


# Gets the data for all pacemakers that have been connected to the DCM and updates the all_pacemakers list
def _getData():
    logger.debug('_getData() called')
    global all_pacemakers
    info = data.getPacemakerInfo()
    all_pacemakers = []
    for i in info:
        newP = Pacemaker(i['model'], i['numUsers'], i['lastUsed'])
        all_pacemakers.append(newP)


# Sets up logging file used for debugging and reporting errors
def _startLog():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    f_handler = logging.FileHandler('DCM_v1/logs/file.log')
    l_handler = logging.FileHandler('DCM_v1/logs/pacemaker.log')
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
_getData()
