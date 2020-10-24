# Data Module
#
# Version 0.1
# Created by: M. Lemcke
# Date Modified: Oct. 15, 2020
#
# Purpose: To read and write data to be stored locally in a JSON file.
# The pacemaker and users module will directly interface with the module to
# request information and to send information to be updated on the JSON file.

import json
import logging

# stores the data read from the JSON file
all_data = {}

# stores the data of the previously or currently connected pacemaker, including the user information
current_data = {}


# disconnects the previously connected pacemaker and sets the given one as connected
def setConnectedPacemaker(newInfo):
    logger.debug('setConnectedPacemaker() called')
    global current_data
    global all_data
    current_data['lastUsed'] = False
    makeNewPacemaker = 0
    if bool(all_data):
        for i in range(len(all_data['pacemakers'])):
            if all_data['pacemakers'][i]['model'] == newInfo['model']:
                makeNewPacemaker = i+1
            if all_data['pacemakers'][i]['model'] == current_data['model']:
                del all_data['pacemakers'][i]
                all_data['pacemakers'].append(current_data)
                logger.info('Pacemaker %s disconnected',
                            current_data['model'])
                break
    else:
        logger.info('No existing pacemakers')
    if makeNewPacemaker:
        current_data = all_data['pacemakers'][makeNewPacemaker-1]
    else:
        current_data = newInfo
        try:
            current_data['users']
        except KeyError:
            current_data['users'] = []

    current_data['lastUsed'] = True
    _writeData()


# Returns a list of dictionaries of information for each pacemaker except the user information
def getPacemakerInfo():
    logger.debug('getPacemakerInfo() called')
    global all_data
    info = []
    if bool(all_data):
        for p in all_data['pacemakers']:
            paceInfo = {}
            paceInfo['model'] = p['model']
            paceInfo['numUsers'] = p['numUsers']
            paceInfo['lastUsed'] = p['lastUsed']
            info.append(paceInfo)
    return info


# Returns a list of dictionaries of the user information stored on the connected pacemaker
def getUserInfo():
    logger.debug('getUserInfo() called')
    global current_data
    info = []
    if bool(all_data):
        for u in current_data['users']:
            userInfo = {
                'name': u['name'],
                'password': u['password']
            }
            info.append(userInfo)
    return info


# Changes all stored user information on the connected pacemaker and saves the information
def changeUserInfo(newInfo):
    logger.debug('changeUserInfo() called')
    global current_data
    if bool(current_data):
        current_data['users'] = []
        for user in newInfo:
            current_data['users'].append(user)
        _writeData()


# Read the JSON file and returns a list of 2 dictionaries to store as all_data and current_data, respectively
def _readData():
    logger.debug('_readData() called')
    rawData = {}
    currentData = {}
    try:
        with open('DCM_v1/data/data.json') as infile:
            rawData = json.load(infile)
            for p in rawData['pacemakers']:
                logger.debug('Pacemaker %s data read', p['model'])
                if p['lastUsed']:
                    currentData = p
                    logger.info('Pacemaker %s is/was connected', p['model'])
    except:
        logger.warning('JSON file could not be opened')
    return rawData, currentData


# Merges the current_data and all_data dictionaries and writes to the JSON file
def _writeData():
    logger.debug('_writeData() called')
    global current_data
    global all_data
    newPacemaker = True
    current_data['numUsers'] = 0
    for u in current_data['users']:
        current_data['numUsers'] += 1
    if bool(all_data):
        for i in range(len(all_data['pacemakers'])):
            if all_data['pacemakers'][i]['model'] == current_data['model']:
                del all_data['pacemakers'][i]
                all_data['pacemakers'].append(current_data)
                newPacemaker = False
                logger.info('Pacemaker %s updated', current_data['model'])
                break
        if newPacemaker:
            all_data['pacemakers'].append(current_data)
            logger.info('Pacemaker %s added to list', current_data['model'])
    else:
        all_data = {'pacemakers': []}
        all_data['pacemakers'].append(current_data)
        logger.info('First pacemaker added')
    try:
        with open('DCM_v1/data/data.json', 'w') as outfile:
            json.dump(all_data, outfile)
            logger.info('Data written to JSON file')
    except:
        logger.warning('JSON file could not be opened')

    all_data, current_data = _readData()


# Sets up logging file used for debugging and reporting errors
def _startLog():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARNING)

    f_handler = logging.FileHandler('DCM_v1/logs/file.log')
    l_handler = logging.FileHandler('DCM_v1/logs/data.log')
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
all_data, current_data = _readData()
