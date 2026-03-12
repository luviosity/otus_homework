#!/bin/sh

set -e

echo "Apply migrations.."
alembic upgrade head
echo "Migrations applied! Starting service..."

exec "$@"