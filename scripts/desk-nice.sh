#!/bin/sh
# Document / apply one niced Ollama generate on myarch. Not Yes. Not the APK.
# Phone queue is the product truth; this keeps the desktop interactive.
set -eu
echo "OLLAMA_NUM_PARALLEL=1"
echo "systemd: Nice=10 on the ollama unit (operator ops, not git)"
echo "Never a second generate to feel faster. Never auto-Yes."
