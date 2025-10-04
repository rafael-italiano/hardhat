#!/usr/bin/env bash

podman run \
  --pod hardhat-scraper \
  -v ./src:/app \
  --env-file .env \
  localhost/hardhat-scraper-dev
