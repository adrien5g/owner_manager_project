class EmailAlreadyInUse(Exception):
    '''
    Email already in use
    '''

class InvalidEmail(Exception):
    '''
    Invalid email
    '''

class InvalidName(Exception):
    '''
    Invalid name
    '''

class EmptyData(Exception):
    '''
    Empty data
    '''

class CarColorNotFound(Exception):
    '''
    Car color not found
    '''

class CarTypeNotFound(Exception):
    '''
    Car type not found
    '''

class OwnerNotFound(Exception):
    '''
    Owner not found
    '''

class CarLimitPerOwnerReached(Exception):
    '''
    Car limit per owner reached
    '''

class CarNotFound(Exception):
    '''
    Car not found
    '''