# Quick Start Guide - All Platforms

Choose your platform and follow the instructions:

## 🪟 Windows

### Easiest: Using Docker
```cmd
docker-compose up -d
```
Then open: http://localhost:8181

### Easy: Using Python
```cmd
python start.py
```

### Alternative: Batch File
```cmd
start.bat
```
Or just double-click `start.bat`

---

## 🍎 macOS

### Easiest: Using Docker
```bash
docker-compose up -d
```
Then open: http://localhost:8181

### Easy: Using Python
```bash
python3 start.py
```

### Alternative: Shell Script
```bash
chmod +x start.sh  # First time only
./start.sh
```

---

## 🐧 Linux

### Easiest: Using Docker
```bash
docker-compose up -d
```
Then open: http://localhost:8181

### Easy: Using Python
```bash
python3 start.py
```

### Alternative: Shell Script
```bash
chmod +x start.sh  # First time only
./start.sh
```

---

## 📱 Default Login

- **URL**: http://localhost:8181/admin/login
- **Username**: `admin`
- **Password**: `admin123`

---

## 🆘 Need Help?

- **Installation issues**: See [INSTALL.md](INSTALL.md)
- **Docker issues**: See [DOCKER.md](DOCKER.md)
- **General usage**: See [README.md](README.md)

---

## 🛑 Stopping the Application

### If using Docker:
```bash
docker-compose down
```

### If using Python/scripts:
Press `Ctrl+C` in the terminal where it's running

---

That's it! Choose your method and get started in under 5 minutes! 🚀
