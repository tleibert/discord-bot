#! /bin/bash

source .venv/bin/activate
nohup python3 bin/bot.py > bot.log &
