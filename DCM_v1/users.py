# Users Module
#
# Version 1.1
# Created by: M. Lemcke
# Date Modified: Oct. 8, 2020
#
# Purpose: To register and store new user information and verify user credentials to access to the
# pacemaker application

import json
import logging


all_users = []      # a list of objects of all registered users


class User():

    name = ''               # user's name
    password = ''           # user's password
    currentUser = False     # true if the current signed in user, false by default

    def __init__(self, name, password):
        self.name = name
        self.password = password
        logging.info('Created user object for %s', self.name)


# Registers new user information
def makeNewUser(name, password):
    logging.debug('makeNewUser() called for %s', name)
    newUser = User(name.lstrip().rstrip(), password.lstrip().rstrip())
    all_users.append(newUser)
    _writeFile()


# Deletes the given user and the corresponding saved info if they are signed in
def deleteUser(name):
    logging.debug('deleteUser() called for %s', name)
    for user in all_users:
        if user.currentUser and user.name == name:
            all_users.pop(all_users.index(user))
            logging.info('%s deleted', name)
            _writeFile()


# Signs in the given user if the password is correct
def signInUser(name, password):
    logging.debug(
        'signInUser() called for %s', name)
    validatedUser = _validateUser(name, password)
    if (validatedUser):
        for user in all_users:
            if user == validatedUser:
                user.currentUser = True
                logging.info('%s is signed in', name)
                return True

    logging.info('%s could not be verified', name)
    return False


# Signs out the given user if they were logged in
def signOutUser(name):
    logging.debug('signOutUser() called for %s', name)
    for user in all_users:
        if user.name == name and user.currentUser:
            user.currentUser = False
            logging.info('%s has been logged out', user.name)


# Returns the information of the current user signed into the application
def currentUserInfo():
    logging.debug('currentUserInfo() called')
    for user in all_users:
        if user.currentUser:
            logging.info('%s is logged in', user.name)
            return [user.name]
    logging.info('No user logged in')

    return []


# Retrives user information from JSON file
def _readFile():
    logging.debug('_readfile() called')
    userList = []
    try:
        with open('DCM_v1/data/userData.txt') as infile:
            userData = json.load(infile)
            for d in userData['users']:
                logging.debug('User data read')
                user = User(d['name'], d['password'])
                userList.append(user)
            logging.info('User objects created from file')
    except:
        logging.error('JSON file could not be opened')
    return userList


# Stores all current user information in JSON file
def _writeFile():
    logging.debug('_writefile() called')
    userData = {}
    userData['users'] = []
    for user in all_users:
        userData['users'].append({
            'name': user.name,
            'password': user.password
        })
        logging.info('User data stored for %s', user.name)
    try:
        with open('DCM_v1/data/userData.txt', 'w') as outfile:
            json.dump(userData, outfile)
            logging.info('User data written to JSON file')
    except:
        logging.error('JSON file could not be opened')


# Determines if the credentials given are valid and returns the user object of the validated user
def _validateUser(name, password):
    logging.debug('_validateUser() called for %s', name)
    nameEdit = name.rstrip().lstrip()
    passEdit = password.rstrip().lstrip()
    for user in all_users:
        if user.name == nameEdit and user.password == passEdit:
            logging.info('%s was validated', name)
            return user
    logging.info('%s was not validated', name)
    return None


# Starts the logging file
def _startLog():
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s: %(message)s',
        filename='DCM_v1/logs/users.log',
        level=logging.DEBUG
    )
    logging.info('Logging started')


# Run on import of module
_startLog()
all_users = _readFile()
