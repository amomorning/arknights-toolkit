#!/bin/bash

set -xeu

trap 'kill $(jobs -p)' EXIT

WORKING_DIR=$(cd "$(dirname "$0")";pwd)

${WORKING_DIR}/arknights.sh >/dev/null 2>&1 &
${WORKING_DIR}/controller.py >/dev/null 2>&1 &
htop -F emulator
