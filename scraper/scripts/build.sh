#!/usr/bin/env bash

podman build -t hardhat-scraper -f Containerfile
podman build -t hardhat-scraper-dev -f Containerfile.dev
