# Installation Guide - Face Recognition Attendance System

## Cross-Platform Quick Start

**The easiest way to start the application on any OS (Windows, macOS, Linux):**

```bash
# Run the cross-platform startup script
python start.py
# or on Unix systems:
python3 start.py
```

This script automatically:
- Checks for Python installation
- Creates a virtual environment
- Installs dependencies
- Initializes the database
- Starts the Flask application

---

## Platform-Specific Installation

The face recognition library requires `dlib`, which can be tricky to install. Choose the method for your operating system:

### Windows Installation

#### Method 1: Using the Startup Script (Easiest)

```cmd
# Run the Python startup script
python start.py
```

#### Method 2: Using the Batch File

```cmd
# Double-click start.bat or run:
start.bat
```

#### Method 3: Manual Installation

```cmd
# Step 1: Create and activate virtual environment
python -m venv venv
venv\Scripts\activate.bat

# Step 2: Install core dependencies
pip install -r requirements.txt

# Step 3: Install dlib (may require Visual Studio Build Tools)
# Download Visual Studio Build Tools from:
# https://visualstudio.microsoft.com/visual-cpp-build-tools/
pip install dlib
pip install face_recognition
```

**Windows Troubleshooting:**
- If dlib installation fails, install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Select "Desktop development with C++" workload
- Or use pre-built wheels from [Christoph Gohlke's collection](https://www.lfd.uci.edu/~gohlke/pythonlibs/)

### macOS Installation

#### Method 1: Using the Startup Script (Easiest)

```bash
# Run the Python startup script
python3 start.py
```

#### Method 2: Using Homebrew (Recommended)

```bash
# Step 1: Install Homebrew dependencies
brew install cmake
brew install dlib

# Step 2: Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Step 3: Install core dependencies first
pip install -r requirements.txt

# Step 4: Install dlib and face_recognition
pip install dlib
pip install face_recognition
```

#### Method 3: Using the Shell Script

```bash
# Make the script executable (first time only)
chmod +x start.sh

# Run the script
./start.sh
```

### Linux Installation

#### Method 1: Using the Startup Script (Easiest)

```bash
# Run the Python startup script
python3 start.py
```

#### Method 2: Manual Installation (Ubuntu/Debian)

```bash
# Step 1: Install system dependencies
sudo apt-get update
sudo apt-get install -y build-essential cmake
sudo apt-get install -y libopenblas-dev liblapack-dev
sudo apt-get install -y libx11-dev libgtk-3-dev

# Step 2: Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Step 3: Install dependencies
pip install -r requirements.txt
pip install dlib
pip install face_recognition
```

---

## Alternative Installation Methods

## Alternative Installation Methods

### Method A: Alternative Face Recognition Library

If dlib continues to fail, you can use an alternative approach with `deepface`:

```bash
# Install core dependencies
pip install -r requirements.txt

# Install deepface (alternative to face_recognition)
pip install deepface
pip install tf-keras
```

Then update the code to use deepface (I'll provide an alternative module).

### Method C: Pre-built Wheels

```bash
# Install core dependencies
pip install -r requirements.txt

# Install cmake first
pip install cmake

# Try installing dlib with verbose output
pip install --verbose dlib

# Then install face_recognition
pip install face_recognition
```

### Method B: Using Conda (Cross-Platform)

```bash
# If you have conda installed
conda create -n attendance python=3.10
conda activate attendance

# Install dlib via conda (pre-built)
conda install -c conda-forge dlib

# Install other dependencies
pip install flask opencv-python numpy pandas openpyxl pillow
pip install face_recognition
```

## Current Issue Resolution

You're getting a CMake version compatibility error. Here's the fix:

### Option A: Update CMake

```bash
# Upgrade cmake via brew
brew upgrade cmake

# Verify version (should be 3.5+)
cmake --version

# Then retry installation
pip install dlib
pip install face_recognition
```

### Option B: Install without face_recognition (Testing Mode)

For now, you can run the system without face recognition to test other features:

```bash
# Install only the core dependencies (already done)
pip install -r requirements.txt

# The system will work for database, admin panel, etc.
# Face recognition features will need to be added later
```

## Running the Application

After installation, you can start the application using any of these methods:

### Option 1: Cross-Platform Python Script (Recommended)

```bash
python start.py
# or on Unix systems:
python3 start.py
```

### Option 2: Platform-Specific Scripts

**Windows:**
```cmd
start.bat
```

**macOS/Linux:**
```bash
chmod +x start.sh  # First time only
./start.sh
```

### Option 3: Manual Start

```bash
# Activate virtual environment first
# Windows:
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Then run the app
python app.py
```

---

## Troubleshooting

### All Platforms

#### Issue: Virtual environment not activating
**Solution:**
- Windows: Use `venv\Scripts\activate.bat` or run `start.py`
- macOS/Linux: Use `source venv/bin/activate` or run `start.py`

#### Issue: Python not found
**Solution:**
- Install Python 3.8+ from [python.org](https://www.python.org/)
- Make sure to check "Add Python to PATH" during Windows installation
- Verify with `python --version` or `python3 --version`

### Windows-Specific

#### Issue: CMake not found or Visual C++ errors
**Solution:**
```cmd
# Install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Select "Desktop development with C++" workload
```

#### Issue: Permission denied errors
**Solution:**
```cmd
# Run Command Prompt or PowerShell as Administrator
```

### macOS-Specific

### Issue: CMake not found
```bash
brew install cmake
export PATH="/usr/local/bin:$PATH"
```

### Issue: Homebrew not installed
**Solution:**
```bash
# Install Homebrew first
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Linux-Specific

#### Issue: Missing system libraries
**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y build-essential cmake libopenblas-dev liblapack-dev

# Fedora/RHEL
sudo dnf install gcc gcc-c++ cmake openblas-devel lapack-devel

# Arch Linux
sudo pacman -S base-devel cmake openblas lapack
```

---

## Testing Installation

After installation, verify all components:

```bash
# Activate virtual environment first (if not already active)
# Then run:
python verify_installation.py
```

This will check if all components are properly installed.

---

## Next Steps After Successful Installation

1. **Start the application** (choose one):
   ```bash
   python start.py
   # or use platform-specific scripts (start.bat on Windows, start.sh on Unix)
   ```

2. **Run the initial setup** (optional, for sample data):
   ```bash
   # Activate virtual environment first
   python setup.py
   ```

3. **Access the application**:
   - Home: http://localhost:8181
   - Admin: http://localhost:8181/admin/login
   - Mark Attendance: http://localhost:8181/mark-attendance

4. **Default credentials**:
   - Username: admin
   - Password: admin123

---

## For Production Deployment

### Docker (Recommended for Production)

Create a `Dockerfile` for easier deployment across all platforms:

```dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopencv-dev \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir dlib face_recognition
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p student_images exports

# Initialize database
RUN python database.py

EXPOSE 8181

CMD ["python", "app.py"]
```

**Build and run:**
```bash
docker build -t face-attendance .
docker run -p 8181:8181 -v $(pwd)/student_images:/app/student_images face-attendance
```

---

## Platform Notes

### Windows Notes
- If you see "execution of scripts is disabled" in PowerShell, run:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- Or use Command Prompt (cmd) instead of PowerShell

### macOS Notes
- On Apple Silicon (M1/M2), you may need to install Rosetta 2:
  ```bash
  softwareupdate --install-rosetta
  ```

### Linux Notes
- Ensure Python 3.8+ is installed (some distributions default to Python 2.7)
- Use `python3` instead of `python` if needed

---

## Getting Help

If you encounter issues not covered here:
1. Check the error message carefully
2. Ensure Python 3.8+ is installed
3. Try the cross-platform `start.py` script
4. Check the GitHub issues or create a new one

For detailed usage instructions, see [README.md](README.md).
