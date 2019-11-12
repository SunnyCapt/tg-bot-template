#!/usr/bin/env bash

source .venv/bin/activate
echo "enter bot token (like `14881488:jejrhrfuuh3493498r3iuh3iur`):"
read bot_token
python bot.py ${bot_token}
