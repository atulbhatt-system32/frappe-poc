# Windows Development Setup for Frappe / ERPNext

Frappe Framework is designed for Unix-like systems and does **not** run natively on Windows. There are two recommended approaches:

1. **WSL2 + Ubuntu** (Recommended) — Run Ubuntu inside Windows seamlessly
2. **VirtualBox + Ubuntu VM** — Full virtual machine approach

---

## Method 1: WSL2 + Ubuntu (Recommended)

WSL2 (Windows Subsystem for Linux 2) lets you run a real Linux kernel inside Windows with near-native performance. This is the fastest and most convenient way to develop Frappe on Windows.

### Prerequisites

- Windows 10 version 2004+ or Windows 11
- At least 8 GB RAM (16 GB recommended)
- At least 50 GB free disk space

### Step 1: Enable WSL2

Open **PowerShell as Administrator** and run:

```powershell
wsl --install
```

This installs WSL2 with Ubuntu by default. Restart your computer when prompted.

If you need a specific Ubuntu version:
```powershell
wsl --install -d Ubuntu-24.04
```

### Step 2: Configure WSL2

After restarting, Ubuntu will open and ask you to create a username and password. Then:

```bash
# Update system
sudo apt update && sudo apt upgrade -y
```

### Step 3: Increase WSL2 Resources (Important)

Create or edit `%USERPROFILE%\.wslconfig` in Windows:

```ini
[wsl2]
memory=8GB
processors=4
swap=4GB
```

Restart WSL:
```powershell
wsl --shutdown
```

### Step 4: Follow the Linux Setup

From here, follow the **Linux (Ubuntu/Debian) setup guide** in `references/linux.md`. All the same commands work inside WSL2.

### Step 5: Access from Windows Browser

Frappe's development server in WSL2 is automatically accessible from your Windows browser at:
```
http://localhost:8000
```

If using a custom site name, add it to your Windows hosts file:
1. Open Notepad **as Administrator**
2. Open `C:\Windows\System32\drivers\etc\hosts`
3. Add: `127.0.0.1 mysite.localhost`

### WSL2 Tips

**File system performance**: Keep your Frappe project inside the Linux filesystem (`~/frappe/`), not in `/mnt/c/` (the Windows filesystem). Linux filesystem access is significantly faster.

**VS Code integration**: Install the [Remote - WSL extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) in VS Code:
```bash
# From inside WSL, open VS Code in the current directory
code .
```

**Auto-start services**: WSL doesn't run systemd by default. Start services manually:
```bash
sudo service mariadb start
sudo service redis-server start
```

Or enable systemd in WSL2 — add to `/etc/wsl.conf`:
```ini
[boot]
systemd=true
```

Then restart WSL: `wsl --shutdown` from PowerShell.

**Backup your WSL distribution**:
```powershell
wsl --export Ubuntu frappe-backup.tar
```

---

## Method 2: VirtualBox + Ubuntu VM

This method creates a full Ubuntu virtual machine. It's heavier than WSL2 but provides complete isolation.

### Prerequisites

- [VirtualBox](https://www.virtualbox.org/wiki/Downloads) installed
- [Ubuntu Server 24.04 LTS ISO](https://ubuntu.com/download/server) downloaded
- At least 8 GB RAM on host (allocate 4 GB+ to VM)
- At least 50 GB free disk space

### Step 1: Create the Virtual Machine

1. Open VirtualBox → **New**
2. Name: `FrappeERPNext`
3. Type: **Linux**, Version: **Ubuntu (64-bit)**
4. Memory: **4096 MB** minimum (8192 MB recommended)
5. Hard disk: **Create a virtual hard disk now** → **VDI** → **Dynamically allocated** → **50 GB+**

### Step 2: Configure VM Settings

Before starting the VM, adjust settings:

**System:**
- Processors: **2+**
- Enable PAE/NX

**Network:**
- Adapter 1: **NAT** (for internet access)
- Click **Advanced** → **Port Forwarding** → Add rule:
  - Name: `HTTP`
  - Host Port: `8000`
  - Guest Port: `8000`

**Storage:**
- Add the Ubuntu ISO to the optical drive

### Step 3: Install Ubuntu Server

1. Start the VM
2. Follow the Ubuntu Server installation wizard
3. Select **OpenSSH server** during installation
4. Set username and password

### Step 4: Follow the Linux Setup

Once Ubuntu is installed, follow the **Linux (Ubuntu/Debian) setup guide** in `references/linux.md`.

### Step 5: Access from Windows

After running `bench start` inside the VM, access from your Windows browser at:
```
http://localhost:8000
```

(Thanks to the port forwarding configured in Step 2)

### VirtualBox Tips

**SSH Access**: Instead of using the VirtualBox console, SSH into the VM for a better experience:
```powershell
ssh username@localhost -p 2222
```
(Add a port forwarding rule: Host 2222 → Guest 22)

**Shared Folders**: For sharing files between Windows and the VM:
1. Install VirtualBox Guest Additions inside the VM
2. Configure shared folders in VM settings
3. Mount inside VM:
   ```bash
   sudo mount -t vboxsf shared_folder /mnt/shared
   ```

**Snapshots**: Take snapshots before major changes so you can roll back if needed.

---

## Which Method Should You Choose?

| Feature | WSL2 | VirtualBox |
|---|---|---|
| Performance | Near-native | Good (some overhead) |
| Setup complexity | Easy | Moderate |
| RAM usage | Shared with Windows | Dedicated allocation |
| File system | Shared (with caveats) | Isolated |
| VS Code integration | Excellent | Good (via SSH) |
| Isolation | Moderate | Complete |
| Portability | Windows-only | Cross-platform |

**Recommendation**: Use **WSL2** for development. It's faster, easier, and integrates better with Windows tools. Use **VirtualBox** if you need complete isolation or want to closely replicate a production Linux environment.
