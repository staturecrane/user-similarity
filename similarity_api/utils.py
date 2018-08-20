"""
Utility functions for Pluralsight similarity challenge
"""


def normalize(x, scoremin, scoremax):
    return (x - scoremin)/(scoremax - scoremin)