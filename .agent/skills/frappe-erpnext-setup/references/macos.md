# macOS Development Setup for Frappe / ERPNext (Native)

Complete guide for setting up a native development environment for Frappe and ERPNext on macOS, optimized for Apple Silicon (M1/M2/M3/M4) Macs.

---

## 1. Prerequisites

### Install Xcode CLI Tools
```bash
xcode-select --install
```

### Install Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
**Apple Silicon Note:** Ensure Homebrew is in your PATH:
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

---

## 2. System Dependencies

Install core dependencies via Homebrew:
```bash
brew install mariadb@10.6 redis git pkg-config mariadb-connector-c
```

### MariaDB Configuration
Frappe requires specific MariaDB settings (utf8mb4).

1. **Create/Update Config**: Create `/opt/homebrew/etc/my.cnf`:
```ini
[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[mysql]
default-character-set = utf8mb4
```

2. **Start & Service**:
```bash
brew services start mariadb@10.6
brew services start redis
```

3. **Set Root Password**:
Homebrew MariaDB often uses socket auth. Set a password for Frappe (e.g., `@SEcurePassword`):
```bash
sudo mariadb -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'YOUR_PASSWORD'; FLUSH PRIVILEGES;"
```

### wkhtmltopdf (PDF Generation)
```bash
curl -L https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-2/wkhtmltox-0.12.6-2.macos-cocoa.pkg -o /tmp/wkhtmltox.pkg
sudo installer -pkg /tmp/wkhtmltox.pkg -target /
```

---

## 3. Python & Node.js

### Python via uv (Recommended)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.zshrc

# Install Python 3.12 (For Frappe v15)
uv python install 3.12 --default
```

### Node.js & Yarn
```bash
# Install nvm if not present
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.zshrc

nvm install 24
npm install -g yarn
```

---

## 4. Bench CLI & Project Setup

### Install Bench
```bash
uv tool install frappe-bench
```

### Initialize Bench
```bash
bench init my-bench --frappe-branch version-15
cd my-bench
```

### Create Site & Install ERPNext
```bash
# Create site
bench new-site mysite.localhost --mariadb-root-password YOUR_PASSWORD --admin-password admin

# Enable Developer Mode
bench set-config -g developer_mode 1

# Get ERPNext
bench get-app erpnext --branch version-15

# Install ERPNext on site
bench --site mysite.localhost install-app erpnext
```

---

## 5. Troubleshooting (Native Mac Issues)

### `bench add-to-hosts` Failures
If `sudo bench add-to-hosts` fails with `KeyError: "getgrnam(): name not found"`, add it manually:
```bash
echo "127.0.0.1 mysite.localhost" | sudo tee -a /etc/hosts
```

### `ImportError` or Missing Modules during Install
If `install-app` fails with missing modules (e.g., `frappe.core.doctype.notification_recipient`):
1. **Ensure Services are running**: `bench start` should be active in a separate terminal so Redis is available.
2. **Reinstall Site**: Sometimes metadata gets corrupted during a failed partial install.
   ```bash
   bench --site mysite.localhost reinstall
   bench --site mysite.localhost install-app erpnext
   ```

### Redis Connection Issues
If `migrate` or `install-app` says "Service redis_cache is not running":
1. Check `brew services list`.
2. Ensure `bench start` is running in another tab.
3. Check `sites/common_site_config.json` ports match your Redis config.

### MariaDB in PATH
If `mariadb` command is not found, add it to your shell:
```bash
echo 'export PATH="/opt/homebrew/opt/mariadb@10.6/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```
