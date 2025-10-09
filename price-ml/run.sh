#!/usr/bin/env bash
set -e  # Exit immediately on errors
POD_NAME=hardhat-ml
IMAGE="hardhat-ml"
CONTAINERFILE="Containerfile"

# Check if the image exists locally
if ! podman image exists "$IMAGE"; then
  echo "⚙️  Image not found locally. Building from $CONTAINERFILE..."
  podman build -t "$IMAGE" -f "$CONTAINERFILE" .
else
  echo "✅ Image $IMAGE already exists locally."
fi

podman pod create \
    --replace \
    --network podman-default-kube-network \
    $POD_NAME

podman run \
  --pod $POD_NAME \
  --volume ./src:/app \
  --env-file .env \
  $IMAGE