#!/bin/bash


if [ -z $1 ]; then
    envdir="env"
else
    envdir=$1
fi

if ! [ -d $envdir ]; then
    virtualenv $envdir --distribute --no-site-packages
    echo "Installed virtualenv to ./${envdir}"
fi

pip install -r requirements.txt
