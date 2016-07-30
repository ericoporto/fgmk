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
#py.test
if hash py.test-3 2>/dev/null; then
    py.test-3
elif hash py.test 2>/dev/null; then
    py.test
else
    echo "install pytest. ex:"
    echo " $   sudo apt install python3-pytest"
    echo "or"
    echo " $   sudo pip3 install pytest"
fi
