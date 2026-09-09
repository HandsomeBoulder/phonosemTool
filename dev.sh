#!/bin/bash
set -e

PROJECT_DIR="/www/phonosemTool"

cd "$PROJECT_DIR"

SESSION="phonosemSession"

tmux new-session -d -s "$SESSION" -c "$PROJECT_DIR/backend" "source venv/bin/activate; python3 run.py"

tmux split-window -h -t "$SESSION" -c "$PROJECT_DIR/frontend" "quasar dev"

tmux attach-session -t "$SESSION"