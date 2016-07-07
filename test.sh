#!/bin/bash
#
# why a bash script is doing my tests you ask?
#
# I want to follow good integration as here:
# http://pytest.org/latest/goodpractices.html
#
# But unfortunately, using like this gives me
# error with PyQt5 as below:
#
# $ python3 setup.py test
# running test
# Searching for pyqt5
# Reading https://pypi.python.org/simple/pyqt5/
# No local packages or download links found for pyqt5
# error: Could not find suitable distribution for Requirement.parse('pyqt5')
#
# Maybe in the future.

export PYTHONPATH=src/
py.test
