#!/bin/bash

set -euo pipefail

alembic -c /app/alembic/alembic.ini upgrade head

uvicorn app.core.api:create_app --host 0.0.0.0 --port 80 --factory