#!/bin/sh

set -e

# -----------------------------
# Safe defaults (VERY IMPORTANT for teams)
# -----------------------------
POSTGRES_HOST=${POSTGRES_HOST:-db}
POSTGRES_PORT=${POSTGRES_PORT:-5432}

echo "======================================"
echo "🚀 ENTRYPOINT STARTING"
echo "======================================"

echo "POSTGRES_HOST=$POSTGRES_HOST"
echo "POSTGRES_PORT=$POSTGRES_PORT"

# -----------------------------
# Wait for PostgreSQL safely
# -----------------------------
echo "⏳ Waiting for PostgreSQL..."

# Prevent infinite silent failure loops (team-safe improvement)
MAX_RETRIES=60
COUNT=0

until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  COUNT=$((COUNT + 1))

  if [ "$COUNT" -ge "$MAX_RETRIES" ]; then
    echo "❌ PostgreSQL did not become ready after $MAX_RETRIES attempts"
    exit 1
  fi

  sleep 1
done

echo "✅ PostgreSQL is ready"



# -----------------------------
# Start application
# -----------------------------
echo "🚀 Starting process..."

exec "$@"





