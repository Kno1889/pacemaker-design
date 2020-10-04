# Users Module
#
# Version 1.0
# Created by: M. Lemcke
# Date Modified: Oct. 4, 2020
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
    newUser = User(name, password)
    all_users.append(newUser)
    _writeFile()


# Verifies that the given user exists and the password is correct
def signInUser(name, password):
    for user in all_users:
        if user.name == name and user.password == password:
            user.currentUser = True
            logging.debug(
                'signInUser() called for %s', user.name)
            logging.info('%s was verified', user.name)
            return True
    logging.debug(
        'signInUser() called for %s', name)
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
