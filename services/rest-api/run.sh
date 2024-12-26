#!/bin/bash

docker build -t rest-api .

docker run --env-file .env -p 8000:5000 rest-api --stats
