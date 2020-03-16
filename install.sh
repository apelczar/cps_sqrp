#!/bin/bash 

# 1. First check to see if the correct version of Python is installed on the local machine 
echo "Checking for installed Python version in '/usr/local/bin/python3.8'"

REQ_PYTHON_V="381"
ACTUAL_PYTHON_V=$("/usr/local/bin/python3.8" -c 'import sys; version=sys.version_info[:3]; print("{0}{1}{2}".format(*version))')
ACTUAL_PYTHON3_V=$("/usr/local/bin/python3.8" -c 'import sys; version=sys.version_info[:3]; print("{0}{1}{2}".format(*version))')

if [[ $ACTUAL_PYTHON_V > $REQ_PYTHON_V ]] || [[ $ACTUAL_PYTHON_V == $REQ_PYTHON_V ]];  then 
    PYTHON="/usr/local/bin/python3.8"
elif [[ $ACTUAL_PYTHON3_V > $REQ_PYTHON_V ]] || [[ $ACTUAL_PYTHON3_V == $REQ_PYTHON_V ]]; then 
    PYTHON="/usr/local/bin/python3.8"
else
    echo -e "\tPython 3.8.1 is not installed in the expected folder on this machine. Please install Python 3.8.1 before continuing."
    exit 1
fi

echo -e "\t--Python 3.8.1 is installed"

# 2. Create Virtual environment 

# Remove the env directory if it exists 
if [[ -d env ]]; then 
    rm -rf env  
fi

echo -e "Creating virtual environment..."
$PYTHON -m venv env 
if [[ ! -d env ]]; then 
    echo -e "\t--Could not create virtual environment...Please make sure venv is installed"
    exit 1
fi

# 3. Install requirements 

echo -e "Installing Requirements"
if [[ ! -e "requirements.txt" ]]; then 
    echo -e "\t--Need to requirements.txt to install packages."
    exit 1
fi

source env/bin/activate
env/bin/pip install -r requirements.txt
deactivate 
echo -e "Done."
