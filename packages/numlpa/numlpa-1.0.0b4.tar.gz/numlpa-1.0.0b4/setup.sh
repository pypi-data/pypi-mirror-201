#!/bin/sh

: '
This shell script allows to initialize the environment needed to run
and develop the Python package. The installation of the package is done
in development mode in a virtual environment. The virtual environment
is created at the location defined by the variable $PATH_VENV. If the
path to the virtual environment does not suit you, you can redefine this
variable below. To access the shell commands defined below and activate
the virtual environment, run the command ". setup.sh".
'

# define the path to the project directory
export PATH_REPO="$(dirname "$BASH_SOURCE")"
export PATH_REPO="$(realpath "$PATH_REPO")"

# define the path to the development virtual environment
export BASE_NAME="$(basename "$PATH_REPO")"
export PATH_VENV=~/.venv/dev/$BASE_NAME

# define the path to the package sources
export PATH_PACK=$PATH_REPO/src/numlpa

# command to deactivate the (potential) current virtual environment
workoff()
{
    deactivate > /dev/null 2>&1 || true
}

# command to activate the development virtual environment
workon()
{
    . $PATH_VENV/bin/activate
}

# command to create and activate the development virtual environment
install()
{
    workoff
    if test -d "$PATH_VENV"
    then
        workon
    else
        echo "creating virtual environment $PATH_VENV"
        python3 -m venv $PATH_VENV
        workon
        python3 -m pip install --upgrade pip
        python3 -m pip install --upgrade build
        python3 -m pip install --upgrade twine
        python3 -m pip install --upgrade sphinx
        python3 -m pip install --upgrade sphinx-rtd-theme
        python3 -m pip install --upgrade myst-parser
        python3 -m pip install --upgrade pylint
        python3 -m pip install --upgrade flake8
        python3 -m pip install --editable $PATH_REPO
    fi
}

# command to deactivate and remove the development virtual environment
uninstall()
{
    workoff
    if [ -d "$PATH_VENV" ]
    then
        echo "deleting virtual environment $PATH_VENV"
        rm --recursive $PATH_VENV
    fi
}

# command to recreate and reactivate the development virtual environment
reinstall()
{
    uninstall
    install
}

# command to build the documentation of the package
makedocs()
{
    cleardocs
    sphinx-apidoc -o $PATH_REPO/docs/source/package $PATH_PACK -f -T -M -e -d 1
    make html -C $PATH_REPO/docs
}

# command to clean the documentation of the package
cleardocs()
{
    rm -rf $PATH_REPO/docs/source/package
    rm -rf $PATH_REPO/docs/build
}

# command to execute the tests
run()
{
    python3 --version
    python3 $PATH_REPO/tests/run.py
}

# command to identify bugs and stylistic errors in the code
lint()
{
    pylint $PATH_PACK $PATH_REPO/tests/run.py --rcfile $PATH_REPO/.pylintrc
    flake8 $PATH_PACK $PATH_REPO/tests/run.py
}

# command to upload the package to PyPI
upload()
{
    python3 -m build
    dist=$(find dist -name "*.tar.gz" -o -name "*-none-any.whl")
    python3 -m twine upload $dist --skip-existing
}

# install and activate the virtual environment
install
