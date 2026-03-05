---
name: frappe-erpnext-setup
description: How to set up a Frappe Framework and ERPNext development environment, and create/manage custom applications. Use this skill whenever someone asks about installing Frappe, setting up ERPNext, configuring bench, creating a new Frappe site, or developing custom Frappe apps. Covers both setup and app lifecycle management.
---

# Frappe / ERPNext Development Setup

This skill covers end-to-end development environment setup for the **Frappe Framework** and **ERPNext** across every supported platform. Frappe is a full-stack Python web framework, and ERPNext is the flagship ERP application built on top of it.

## Quick Platform Selection

| Platform | Recommended Method | Complexity | Reference File |
|---|---|---|---|
| **macOS** (Intel & Apple Silicon) | Native via Homebrew | Medium | `references/macos.md` |
| **Linux** (Ubuntu 24.04+ / Debian 13+) | Native install | Medium | `references/linux.md` |
| **Windows** | WSL2 + Ubuntu | Medium | `references/windows.md` |
| **Any OS** (Cross-platform) | Docker + VS Code DevContainer | Low | `references/docker.md` |

> **Recommendation**: For the smoothest experience, use the **Docker + DevContainer** method regardless of your OS. It's the most reproducible and requires the fewest system-level changes. For production-like environments or maximum performance, use the native install for your OS.

---

## Architecture Overview

Before diving into setup, understand the Frappe stack:

```
┌──────────────────────────────────────┐
│           Frappe Bench               │  ← CLI tool managing everything
├──────────────────────────────────────┤
│  Sites       │  Apps                 │
│  (databases) │  (frappe, erpnext,    │
│              │   custom apps)        │
├──────────────────────────────────────┤
│  Python 3.12+ │ Node.js 18+/24      │
│  MariaDB 10.6+│ Redis               │
│  wkhtmltopdf  │ Yarn                │
└──────────────────────────────────────┘
```

**Key concepts:**
- **Bench**: A directory structure + CLI tool that manages Frappe deployments. One bench can host multiple sites.
- **Site**: A tenant with its own database and configuration. Accessed via hostname.
- **App**: A Python/JS module installed on a site. Frappe itself is an app. ERPNext is another app.

---

## Version Compatibility Matrix

| Component | Frappe v15 (LTS) | Frappe v16 (develop) |
|---|---|---|
| Python | 3.10 – 3.13 | 3.14+ |
| Node.js | 18+ | 24+ |
| MariaDB | 10.6+ | 11.8+ |
| Redis | 6+ | 6+ |
| wkhtmltopdf | 0.12.6 (patched qt) | 0.12.6 (patched qt) |

---

## Universal Setup Steps (All Platforms)

Regardless of platform, the final steps are always the same once prerequisites are installed:

### 1. Install Bench CLI

```bash
# Using uv (recommended)
uv tool install frappe-bench

# Or using pip
pip install frappe-bench
```

Verify installation:
```bash
bench --version
```

### 2. Initialize a Frappe Bench

```bash
mkdir ~/frappe && cd ~/frappe

# For Frappe v15 (stable/LTS)
bench init my-bench --frappe-branch version-15

# For Frappe v16 (latest development)
bench init my-bench
```

### 3. Create a New Site

```bash
cd my-bench

# Create site (you'll be prompted for MariaDB root password)
bench new-site mysite.localhost \
  --mariadb-root-password <your-mysql-root-password> \
  --admin-password admin

# Set as default site
bench use mysite.localhost
```

### 4. Install ERPNext

```bash
# Get the ERPNext app
bench get-app erpnext --branch version-15   # or just: bench get-app erpnext

# Install on your site
bench --site mysite.localhost install-app erpnext
```

### 5. Start Development Server

```bash
bench start
```

Access your site at `http://mysite.localhost:8000`
- Default login: `Administrator` / `admin`

> If `mysite.localhost` doesn't resolve, add it to your hosts file:
> ```bash
> bench --site mysite.localhost add-to-hosts
> ```

---

## Essential Bench Commands

These are the commands you'll use daily during Frappe/ERPNext development:

### Site Management
```bash
bench new-site <sitename>              # Create a new site
bench use <sitename>                   # Set default site
bench --site <name> set-admin-password <pw>  # Reset admin password
bench drop-site <sitename>             # Delete a site
bench backup                           # Backup default site
bench restore <path/to/backup.sql.gz>  # Restore from backup
```

### App Management
```bash
bench new-app <app-name>               # Scaffold a new custom app
bench get-app <git-url-or-name>        # Install app from git/registry
bench --site <name> install-app <app>  # Install app on a site
bench --site <name> list-apps          # List installed apps
bench remove-app <app-name>            # Remove app from bench

> **For detailed app creation and configuration workflow, see [references/app-creation.md](file:///Users/atulbhatt/Documents/Projects/Frappe-Erpnext/.agent/skills/frappe-erpnext-setup/references/app-creation.md)**
```

### Development
```bash
bench start                            # Start dev server (web + workers + redis)
bench build                            # Build JS/CSS assets
bench migrate                          # Run patches + sync schema
bench update                           # Pull + patch + build + migrate
bench console                          # Python REPL with Frappe loaded
bench mariadb                          # MariaDB shell for current site
bench clear-cache                      # Clear site cache
bench clear-website-cache              # Clear website cache
```

### Custom App Development
```bash
# Create a new Frappe app
bench new-app my_custom_app

# The app scaffolds at: apps/my_custom_app/
# Structure:
# my_custom_app/
# ├── my_custom_app/
# │   ├── __init__.py
# │   ├── hooks.py          ← App lifecycle hooks
# │   ├── modules.txt       ← List of modules
# │   └── my_module/
# │       ├── doctype/      ← DocType definitions
# │       └── ...
# ├── setup.py
# └── requirements.txt

# Install your app on the site
bench --site mysite.localhost install-app my_custom_app

# Enable developer mode (critical for writing schema changes to files)
bench set-config -g developer_mode 1

> **Deep Dive**: Learn about app structure, hooks, and fixtures in [references/app-creation.md](file:///Users/atulbhatt/Documents/Projects/Frappe-Erpnext/.agent/skills/frappe-erpnext-setup/references/app-creation.md).
```

---

## Platform-Specific Setup

Read the appropriate reference file for detailed, step-by-step instructions specific to your platform:

- **macOS**: Read `references/macos.md` — covers Homebrew, Apple Silicon considerations, and native setup
- **Linux (Ubuntu/Debian)**: Read `references/linux.md` — covers system packages, dedicated user creation, and production setup
- **Windows**: Read `references/windows.md` — covers WSL2 setup, VirtualBox VM alternative, and port forwarding
- **Docker**: Read `references/docker.md` — covers VS Code DevContainer, Docker Compose, and containerized workflow

---

## Troubleshooting

### Common Issues

**MariaDB won't start:**
```bash
# macOS
brew services restart mariadb@11.8

# Linux
sudo systemctl restart mariadb
```

**Redis connection refused:**
```bash
# macOS
brew services restart redis

# Linux
sudo systemctl restart redis-server
```

**`bench start` fails with socket errors:**
```bash
# Kill orphan processes
bench set-config -g developer_mode 1
redis-cli shutdown
# Restart
bench start
```

**Permission denied errors on Linux:**
```bash
# Make sure you're running as the correct user (not root)
sudo chown -R $USER:$USER ~/frappe
```

**Python version mismatch:**
```bash
# Check which Python bench is using
bench --python /path/to/correct/python init my-bench

# Or with uv
uv python install 3.14 --default
```

**Node.js version issues:**
```bash
# List installed versions
nvm ls

# Switch to correct version
nvm use 18  # for v15
nvm use 24  # for v16
```

**wkhtmltopdf PDF generation fails:**
```bash
# Verify installation
which wkhtmltopdf
wkhtmltopdf --version
# Should show 0.12.6 with patched qt
```

**Site not accessible in browser:**
```bash
# Add site to /etc/hosts
bench --site mysite.localhost add-to-hosts

# Or manually
echo "127.0.0.1 mysite.localhost" | sudo tee -a /etc/hosts
```

---

## Quick Reference Links

- [Frappe Framework Documentation](https://frappeframework.com/docs)
- [ERPNext Documentation](https://docs.erpnext.com)
- [Frappe GitHub](https://github.com/frappe/frappe)
- [ERPNext GitHub](https://github.com/frappe/erpnext)
- [Frappe Docker GitHub](https://github.com/frappe/frappe_docker)
- [Bench CLI Reference](https://frappeframework.com/docs/user/en/bench/resources/bench-commands-cheatsheet)
