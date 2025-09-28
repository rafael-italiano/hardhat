podman run \
    -p 8000:8000 \
    -v ./src:/app \
    --env-file .env \
    localhost/hardhat-scraper-dev