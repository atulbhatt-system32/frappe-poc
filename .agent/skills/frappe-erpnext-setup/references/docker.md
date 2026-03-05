# Docker Development Setup for Frappe / ERPNext

The Docker method provides the most consistent and reproducible development environment across all operating systems. It uses the official `frappe_docker` repository with VS Code Dev Containers for a seamless experience.

---

## Prerequisites

| Tool | Required | Install Guide |
|---|---|---|
| **Docker Desktop** | Yes | [docker.com/get-docker](https://docs.docker.com/get-docker/) |
| **VS Code** | Recommended | [code.visualstudio.com](https://code.visualstudio.com/) |
| **Dev Containers Extension** | Recommended | Install from VS Code Extensions marketplace |
| **Git** | Yes | `brew install git` / `apt install git` / [git-scm.com](https://git-scm.com/) |

**Docker Desktop Settings** (important):
- Allocate at least **4 GB RAM** (8 GB recommended)
- Enable Docker Compose V2

---

## Method 1: VS Code Dev Container (Recommended)

This method gives you a full development environment inside a container with VS Code as your editor.

### Step 1: Clone frappe_docker

```bash
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker
```

### Step 2: Copy Dev Container Config

```bash
# Copy the example devcontainer configuration
cp -R devcontainer-example .devcontainer

# Copy VS Code settings
cp -R development/vscode-example .vscode
```

### Step 3: Open in VS Code Dev Container

1. Open VS Code in the `frappe_docker` directory:
   ```bash
   code .
   ```
2. VS Code should detect the `.devcontainer` folder and prompt: **"Reopen in Container"** — click it
3. If no prompt appears: Press `Cmd/Ctrl + Shift + P` → **"Dev Containers: Reopen in Container"**
4. Wait for the container to build (first time takes 5–10 minutes)

### Step 4: Install Dependencies (Inside Container)

Once inside the container terminal in VS Code:

```bash
# Install Node.js (check version matrix in SKILL.md)
nvm install 18   # For Frappe v15
# OR
nvm install 24   # For Frappe v16

# Install Python (if not already available)
# The container usually has Python pre-installed
python3 --version
```

### Step 5: Initialize Bench

```bash
# Initialize bench
bench init --skip-redis-config-generation frappe-bench

cd frappe-bench
```

### Step 6: Configure for Container Environment

```bash
# Set Redis URLs for the Docker Redis services
bench set-config -g db_host mariadb
bench set-config -g redis_cache redis://redis-cache:6379
bench set-config -g redis_queue redis://redis-queue:6379
bench set-config -g redis_socketio redis://redis-queue:6379
```

### Step 7: Create Site and Install Apps

```bash
# Create a new site
bench new-site mysite.localhost \
  --mariadb-root-password 123 \
  --admin-password admin \
  --no-mariadb-socket

# Set as default
bench use mysite.localhost

# Get and install ERPNext
bench get-app erpnext --branch version-15
bench --site mysite.localhost install-app erpnext

# Enable developer mode
bench set-config -g developer_mode 1
```

### Step 8: Start Development Server

```bash
bench start
```

Access your site at `http://mysite.localhost:8000`

> **Note**: The default MariaDB root password in the Docker setup is `123`. This is fine for development.

---

## Method 2: Docker Compose (Without VS Code)

If you prefer to use your own editor and just need the services running:

### Step 1: Clone and Configure

```bash
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker
```

### Step 2: Create a Docker Compose Override

Create `docker-compose.override.yml`:

```yaml
version: "3"
services:
  frappe:
    build:
      context: .
      dockerfile: development/Dockerfile
    volumes:
      - ./development:/workspace/development
      - frappe-bench:/workspace/frappe-bench
    ports:
      - "8000:8000"
      - "9000:9000"
      - "6787:6787"
    stdin_open: true
    tty: true
    depends_on:
      - mariadb
      - redis-cache
      - redis-queue

  mariadb:
    image: mariadb:10.6
    environment:
      MYSQL_ROOT_PASSWORD: 123
      MYSQL_CHARACTER_SET_SERVER: utf8mb4
      MYSQL_COLLATION_SERVER: utf8mb4_unicode_ci
    volumes:
      - mariadb-data:/var/lib/mysql

  redis-cache:
    image: redis:alpine

  redis-queue:
    image: redis:alpine

volumes:
  frappe-bench:
  mariadb-data:
```

### Step 3: Start Services

```bash
docker compose up -d
```

### Step 4: Enter the Container

```bash
docker compose exec frappe bash
```

Then follow Steps 5–8 from Method 1 above.

---

## Working with Docker

### Common Docker Commands

```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# View logs
docker compose logs -f frappe

# Enter the container
docker compose exec frappe bash

# Rebuild the container (after Dockerfile changes)
docker compose build --no-cache

# Clean up everything (WARNING: deletes data)
docker compose down -v
```

### Persisting Data

Your site data (database, files) persists in Docker volumes. To back up:

```bash
# Inside the container
cd frappe-bench
bench backup --with-files
```

Backups are stored in `sites/mysite.localhost/private/backups/`.

### Multiple Sites

```bash
# Inside the container
bench new-site site2.localhost \
  --mariadb-root-password 123 \
  --admin-password admin \
  --no-mariadb-socket

bench --site site2.localhost install-app erpnext
```

### Custom App Development in Docker

```bash
# Inside the container
cd frappe-bench

# Create a new app
bench new-app my_custom_app

# The app source is at frappe-bench/apps/my_custom_app/
# If using Dev Container, this is accessible from VS Code file explorer

# Install on your site
bench --site mysite.localhost install-app my_custom_app
```

---

## Troubleshooting Docker Setup

**Container won't start / MariaDB errors:**
```bash
# Check logs
docker compose logs mariadb

# Reset MariaDB data
docker compose down
docker volume rm frappe_docker_mariadb-data
docker compose up -d
```

**Port 8000 already in use:**
```bash
# Find what's using the port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Or change the port mapping in docker-compose.override.yml
ports:
  - "8001:8000"
```

**Slow performance on macOS/Windows:**
- Increase Docker Desktop RAM allocation to 8 GB+
- On macOS: Enable VirtioFS in Docker Desktop → Settings → General
- On Windows: Use WSL2 backend (not Hyper-V)

**Dev Container extension not detected:**
- Ensure `.devcontainer/devcontainer.json` exists
- Restart VS Code
- Check that the Dev Containers extension is installed and enabled

**Redis connection errors inside container:**
```bash
# Verify Redis containers are running
docker compose ps

# Test connectivity
redis-cli -h redis-cache ping
redis-cli -h redis-queue ping
```
