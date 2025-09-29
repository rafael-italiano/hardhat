#!/usr/bin/env bash
set -euo pipefail

# --- Config ---
NETWORK_NAME="hardhat-net"
SERVICES=("db" "scraper")
IMAGE="localhost/hardhat-scraper-dev:latest"
POD_FILE="pods.yaml"

if ! podman image exists "$IMAGE"; then
    echo "🛠 Building scraper image: $IMAGE"
    podman build -t "$IMAGE" -f ./scraper/Containerfile.dev
else
    echo "ℹ️ Scraper image already exists: $IMAGE"
fi

for service in "${SERVICES[@]}"; do

    env_file="./${service}/secrets.yaml"
    if [[ ! -f "$env_file" ]]; then
        echo "❌ Env file for service '$service' not found: $env_file"
        echo "❌ Please refer to secrets.yaml.template and rename a copy to secrets.yaml"
        exit 1
    fi

    secret="${service}-env"
    if podman secret exists "$secret"; then
        echo "🔄 Secret $secret exists, deleting it"
        podman secret rm $secret
    fi
    echo "🔑 Creating secret $secret from $env_file"
    podman secret create "$secret" "$env_file"
done

# --- Ensure network exists ---
if ! podman network exists "$NETWORK_NAME"; then
    echo "🌐 Creating network $NETWORK_NAME"
    podman network create "$NETWORK_NAME"
else
    echo "ℹ️ Network $NETWORK_NAME already exists"
fi

echo "🚀 Deploying pods from $POD_FILE"
podman play kube "$POD_FILE" --replace

echo "🎉 Done! Use 'podman pod ps' to check running pods."
echo "Use"
echo "podman logs -f db-pod-supabase-postgres to see the logs of the database."
echo "podman logs -f scraper-pod-scraper-dev to see the logs of the app."