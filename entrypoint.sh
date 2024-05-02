#!/bin/bash

# wait for the database to be ready
./wait-for-it.sh db:3606

# start main webapp
python main.py