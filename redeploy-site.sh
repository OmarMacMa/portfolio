#!/bin/bash

tmux kill-server
cd ~/portfolio/
git fetch && git reset origin/main --hard
source ./venv/bin/activate
pip install -r requirements.txt
tmux new-session -d -s flasksession
tmux send-keys -t flasksession "cd ~/portfolio/" C-m
tmux send-keys -t flasksession "source ./venv/bin/activate" C-m
tmux send-keys -t flasksession "flask run --host=0.0.0.0"  C-m
