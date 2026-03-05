# Linux (Ubuntu / Debian) Development Setup for Frappe / ERPNext

Complete guide for setting up Frappe Framework and ERPNext on Linux. Tested on Ubuntu 24.04+ and Debian 13+.

---

## Prerequisites

### 1. Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Create a Dedicated User (Recommended for Production)

For development, you can use your regular user. For production or shared environments:

```bash
sudo adduser frappe
sudo usermod -aG sudo frappe
su - frappe
```

---

## Install System Dependencies

### Essential Packages

```bash
sudo apt install -y \
  git \
  python3-dev \
  python3-pip \
  python3-venv \
  build-essential \
  curl \
  wget \
  software-properties-common \
  pkg-config \
  libffi-dev \
  libssl-dev
```

### MariaDB

```bash
# Install MariaDB server and client
sudo apt install -y mariadb-server mariadb-client libmariadb-dev

# Start and enable
sudo systemctl start mariadb
sudo systemctl enable mariadb

# Secure the installation
sudo mariadb-secure-installation
```

During secure installation:
1. Enter current root password → **Press Enter** (blank by default)
2. Switch to unix_socket authentication → **No**
3. Set root password → **Yes** (remember this password!)
4. Remove anonymous users → **Yes**
5. Disallow root login remotely → **Yes**
6. Remove test database → **Yes**
7. Reload privilege tables → **Yes**

### Configure MariaDB for Frappe

Edit the MariaDB config:
```bash
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```

Add/modify under `[mysqld]`:
```ini
[mysqld]
innodb-file-format=barracuda
innodb-file-per-table=1
innodb-large-prefix=1
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[mysql]
default-character-set = utf8mb4
```

Restart MariaDB:
```bash
sudo systemctl restart mariadb
```

### Redis

```bash
sudo apt install -y redis-server

# Start and enable
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Verify
redis-cli ping
# Should respond: PONG
```

### wkhtmltopdf

```bash
# Install dependencies
sudo apt install -y xvfb libfontconfig

# Download wkhtmltopdf (check https://wkhtmltopdf.org/downloads.html for latest)
# For Ubuntu 24.04 (amd64):
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.jammy_amd64.deb

sudo dpkg -i wkhtmltox_0.12.6.1-3.jammy_amd64.deb
sudo apt install -f  # Fix any dependency issues

# Verify
wkhtmltopdf --version
```

---

## Install Python

### Using uv (Recommended)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # or restart terminal

# For Frappe v15
uv python install 3.12 --default

# For Frappe v16
uv python install 3.14 --default
```

### Using System Python (Alternative)

```bash
sudo apt install -y python3.12 python3.12-venv python3.12-dev
# OR for v16:
sudo apt install -y python3.14 python3.14-venv python3.14-dev
```

Verify:
```bash
python3 --version
```

---

## Install Node.js

### Using nvm (Recommended)

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.bashrc  # or restart terminal

# For Frappe v15
nvm install 18

# For Frappe v16
nvm install 24
```

### Install Yarn

```bash
npm install -g yarn
```

---

## Install Bench CLI & Create Bench

```bash
# Install bench
uv tool install frappe-bench

# Verify
bench --version

# Create bench directory
mkdir ~/frappe && cd ~/frappe

# Initialize bench
bench init my-bench --frappe-branch version-15

# Create a site
cd my-bench
bench new-site mysite.localhost \
  --mariadb-root-password YOUR_PASSWORD \
  --admin-password admin

# Start development server
bench start
```

---

## Production Setup (Optional)

For running Frappe/ERPNext in production on Linux:

### Install Nginx and Supervisor

```bash
sudo apt install -y nginx supervisor
```

### Setup Production Config

```bash
cd ~/frappe/my-bench

# Run production setup (creates nginx & supervisor configs)
sudo bench setup production $USER

# Enable scheduler
bench --site mysite.localhost enable-scheduler

# Setup multitenant (multiple sites on one bench)
bench config dns_multitenant on
```

### SSL with Let's Encrypt

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### Manage Production Services

```bash
# Restart all services
sudo supervisorctl restart all

# Check status
sudo supervisorctl status

# Reload nginx
sudo nginx -t && sudo systemctl reload nginx
```

---

## Firewall Configuration

```bash
# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# For development (port 8000)
sudo ufw allow 8000/tcp

# Enable firewall
sudo ufw enable
```

---

## Systemd Service Management

```bash
# MariaDB
sudo systemctl status mariadb
sudo systemctl restart mariadb

# Redis
sudo systemctl status redis-server
sudo systemctl restart redis-server

# Nginx (production)
sudo systemctl status nginx
sudo systemctl restart nginx

# Supervisor (production)
sudo systemctl status supervisor
sudo systemctl restart supervisor
```
