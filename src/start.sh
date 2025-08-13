#!/bin/bash

source ~/.venv/bin/activate
source .env

# python -m pip install --upgrade pip
# python -m pip install -r requirements.txt

python main.py hellogithub_collect_repo
python main.py gitstar_collect_repo
python main.py gitstar_collect_user
python main.py github_collect_repo
