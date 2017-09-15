#!/usr/bin/env bash
cd $RB_TUTORIAL_REPO

# Cleans out everything.
clean_rb_tutorial () {
    echo "Cleaning out old data"
    find . -depth \( -name "*.py[cod]" -or -name "__pycache__" \) -exec /bin/rm -rf {} \;
    rm -rf $RB_TUTORIAL_REPO/{MANIFEST,build,_build,debian,dist,wheelhouse,*.egg-info,*.eggs,.cache,.eggs,.tox,htmlcov,.coverage.*,RB_TUTORIAL.log.*}
    vex $RB_TUTORIAL_VENV_NAME coverage erase
}

# Does a basic install after a clean for RB_TUTORIAL and installs using
# the development/editable version
install_rb_tutorial () {
    clean_rb_tutorial
    echo "Installing rb_tutorial dependencies"
    vex $RB_TUTORIAL_VENV_NAME pip install -q -U -r requirements_test.txt
    echo "Installing rb_tutorial in development mode"
    vex $RB_TUTORIAL_VENV_NAME pip install -q -e .
}

# Login for no arguments provided
# A quick mechanism to jump into the virtual environment (just type dd)
if [[ $# -eq 0 ]]; then
    vex $RB_TUTORIAL_VENV_NAME /bin/bash -l

# jump into a bash script outside of the venv
elif [[ "$@" == "bash" ]]; then
    /bin/bash -l

# build docs
elif [[ "$@" == doc* ]]; then
    install_RB_TUTORIAL
    vex $RB_TUTORIAL_VENV_NAME python setup.py build_sphinx

# Builds a debian package
elif [[ "$@" == build* ]]; then
    clean_rb_tutorial
    # Creates a debian package.
    vex $RB_TUTORIAL_VENV_NAME make-deb
    vex $RB_TUTORIAL_VENV_NAME dpkg-buildpackage -us -uc
    vex $RB_TUTORIAL_VENV_NAME /bin/bash -l

# Quick clean
elif [[ "$@" == "clean" ]]; then
    # Cleanup repo to reduce conflicts with host
    clean_rb_tutorial

# Quick install
elif [[ "$@" == "install" ]]; then
    install_rb_tutorial

# Run tests
elif [[ "$@" == test* ]]; then
    shift;
    install_rb_tutorial
    echo "Running tests"
    vex $RB_TUTORIAL_VENV_NAME pytest --cache-clear --cov=sm --all --cov-report=term:skip-covered --cov-report=term-missing --ignore=test $@

# Or something else
else
    vex $RB_TUTORIAL_VENV_NAME "$@" || /bin/bash -c "$@"
fi