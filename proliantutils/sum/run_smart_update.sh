#!/bin/bash

set -e

FILE_PATH="$1"
COMPONENTS="$2"

cd $FILE_PATH
./hpsum --s --romonly $COMPONENTS
