# Face Recognition Attendance System - Docker Guide

## Quick Start with Docker

Docker provides the easiest way to run the application on any platform (Windows, macOS, Linux) without worrying about dependencies.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- At least 4GB of free disk space

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

Access the application at: http://localhost:8181

### Option 2: Using Docker Commands

```bash
# Build the image
docker build -t face-attendance .

# Run the container
docker run -d \
  -p 8181:8181 \
  -v $(pwd)/student_images:/app/student_images \
  -v $(pwd)/exports:/app/exports \
  -v $(pwd)/attendance_system.db:/app/attendance_system.db \
  --name face-attendance \
  face-attendance

# View logs
docker logs -f face-attendance

# Stop the container
docker stop face-attendance
docker rm face-attendance
```

### Windows PowerShell

```powershell
# Run with PowerShell
docker run -d `
  -p 8181:8181 `
  -v ${PWD}/student_images:/app/student_images `
  -v ${PWD}/exports:/app/exports `
  -v ${PWD}/attendance_system.db:/app/attendance_system.db `
  --name face-attendance `
  face-attendance
```

### Windows Command Prompt

```cmd
# Run with Command Prompt
docker run -d ^
  -p 8181:8181 ^
  -v %CD%/student_images:/app/student_images ^
  -v %CD%/exports:/app/exports ^
  -v %CD%/attendance_system.db:/app/attendance_system.db ^
  --name face-attendance ^
  face-attendance
```

## Advantages of Docker

✅ No need to install Python or dependencies
✅ Consistent environment across all platforms
✅ Easy to deploy and share
✅ Isolated from your system
✅ Easy to update and rollback

## Updating the Application

```bash
# Stop and remove old container
docker-compose down

# Rebuild with latest changes
docker-compose up -d --build
```

## Accessing the Application

- **Home**: http://localhost:8181
- **Admin Login**: http://localhost:8181/admin/login
- **Mark Attendance**: http://localhost:8181/mark-attendance

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

## Webcam Access

**Note**: For face recognition to work, Docker needs access to your webcam.

### macOS
Docker Desktop should prompt for camera access. Grant it in System Preferences.

### Windows
Enable camera access in Docker Desktop settings and Windows Privacy settings.

### Linux
Use the `--device` flag:
```bash
docker run -d \
  --device=/dev/video0:/dev/video0 \
  -p 8181:8181 \
  face-attendance
```

## Data Persistence

The Docker setup persists:
- Student images in `./student_images`
- Export files in `./exports`
- Database in `./attendance_system.db`

These folders are mounted from your host system, so data persists even if you recreate containers.

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs

# Or for direct docker:
docker logs face-attendance
```

### Port already in use
Change the port mapping in `docker-compose.yml`:
```yaml
ports:
  - "8080:8181"  # Use 8080 instead
```

### Rebuild from scratch
```bash
docker-compose down
docker-compose up -d --build --force-recreate
```

## Production Deployment

For production, consider:
1. Using environment variables for secrets
2. Setting up HTTPS with a reverse proxy (nginx)
3. Using Docker secrets for sensitive data
4. Regular backups of the database

See `README.md` and `INSTALL.md` for more details.
