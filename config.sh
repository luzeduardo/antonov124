#!/bin/bash
set -e

pip install pytest selenium virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements