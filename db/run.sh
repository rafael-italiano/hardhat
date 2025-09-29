podman run \
  --replace \
  --name supabase-postgres \
  --pod db-pod \
  --volume pgdata:/var/lib/postgresql/data:z \
  --env-file=.env \
  --health-cmd="pg_isready -U postgres -d postgres" \
  --health-interval=3s \
  --health-timeout=5s \
  --health-retries=10 \
  --restart=unless-stopped \
  docker.io/supabase/postgres:17.6.1.011
