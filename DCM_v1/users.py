# Users Module
#
# Version 2.1
# Created by: M. Lemcke
# Date Modified: Oct. 8, 2020
#
# Purpose: To register and store new user information and verify user credentials to access to the
# pacemaker application

import json
import logging
import data


all_users = []      # a list of objects of all registered users


class User():

    name = ''               # user's name
    password = ''           # user's password
    currentUser = False     # true if the current signed in user, false by default

    def __init__(self, name, password):
        self.name = name
        self.password = password
        logger.info('Created user object for %s', self.name)


# registers new user information. Returns true if action was successful
def makeNewUser(name, password):
    logger.debug('makeNewUser() called for %s', name)
    if type(name) == type('string') and type(password) == type('string'):
        global all_users
        all_users = _getInfo()
        if len(all_users) < 10:
            newUser = User(name.lstrip().rstrip(), password.lstrip().rstrip())
            all_users.append(newUser)
            _saveInfo()
            return True
    logger.info('user was not make for %s')
    return False


# deletes the given user and the corresponding saved info if they are signed in. Returns true if the user was deleted successfully
def deleteUser(name):
    logger.debug('deleteUser() called for %s', name)
    global all_users
    for user in all_users:
        if user.currentUser and user.name == name:
            all_users.pop(all_users.index(user))
            logger.info('%s deleted', name)
            _saveInfo()
            return True
    return False


# signs in the given user if the password is correct. Returns true if sign in was successful
def signInUser(name, password):
    logger.debug(
        'signInUser() called for %s', name)
    if type(name) == type('string') and type(password) == type('string'):
        global all_users
        all_users = _getInfo()
        validatedUser = _validateUser(name, password)
        if (validatedUser):
            for user in all_users:
                if user == validatedUser:
                    user.currentUser = True
                    logger.info('%s is signed in', name)
                    return True
    logger.info('%s could not be verified', name)
    return False


# Signs out the given user if they were logged in
def signOutUser(name):
    logger.debug('signOutUser() called')
    for user in all_users:
        if user.name == name and user.currentUser:
            user.currentUser = False
            logger.info('%s has been logged out', user.name)


# Returns the information of the current user signed into the application
def currentUserInfo():
    logger.debug('currentUserInfo() called')
    for user in all_users:
        if user.currentUser:
            logger.info('%s is logged in', user.name)
            return [user.name]
    logger.info('No user logged in')
    return []


# gets all user data registered with the connected pacemaker and returns a list of user objects
def _getInfo():
    logger.debug('_getInfo() called')
    info = data.getUserInfo()
    users = []
    for i in info:
        newUser = User(i['name'], i['password'])
        users.append(newUser)
    return users


# sends all user and pacemaker data to the data module and updates information within the module
def _saveInfo():
    logger.debug('_saveInfo() called')
    global all_users
    userInfo = []
    for u in all_users:
        info = {
            'name': u.name,
            'password': u.password
        }
        userInfo.append(info)
    data.changeUserInfo(userInfo)
    all_users = _getInfo()


# Determines if the credentials given are valid and returns the user object of the validated user
def _validateUser(name, password):
    logger.debug('_validateUser() called for %s', name)
    nameEdit = name.rstrip().lstrip()
    passEdit = password.rstrip().lstrip()
    for user in all_users:
        if user.name == nameEdit and user.password == passEdit:
            logger.info('%s was validated', name)
            return user
    logger.info('%s was not validated', name)
    return None


# Starts the logging file
def _startLog():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    f_handler = logging.FileHandler('DCM_v1/logs/file.log')
    l_handler = logging.FileHandler('DCM_v1/logs/users.log')
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
all_users = _getInfo()
