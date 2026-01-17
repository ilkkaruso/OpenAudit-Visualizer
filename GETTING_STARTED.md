# Getting Started with OpenAudit Visualizer

This guide will help you set up and run the OpenAudit Visualizer in **5 minutes**.

## What You Need

- A Linux computer (Arch, Ubuntu, Debian, etc.)
- Docker installed
- Internet connection

## Installation Steps

### 1. Install Docker (if not already installed)

**Arch Linux:**
```bash
sudo pacman -S docker docker-compose
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install docker.io docker-compose
```

### 2. Set Up Docker

```bash
# Give yourself permission to use Docker
sudo usermod -aG docker $USER

# Apply the permission (choose one):
# Option A: Log out and log back in
# Option B: Run this command
newgrp docker

# Start Docker
sudo systemctl start docker

# Make Docker start on boot (optional)
sudo systemctl enable docker
```

### 3. Navigate to the Application

```bash
cd /path/to/OpenAudit-Visualizer
```

### 4. Run the Application

**Easy Way:**
```bash
chmod +x quick-start.sh
./quick-start.sh
```

**Manual Way:**
```bash
docker-compose up -d
sleep 10
docker-compose exec backend python scripts/load_data.py
```

### 5. Open in Your Browser

```
http://localhost:5173
```

You should see the OpenAudit dashboard!

## What You'll See

The application has 3 tabs:

### 📊 Dashboard
- Statistics showing total LGUs, reports, and unliquidated amounts
- Charts showing trends over time
- Table of top LGUs with the most issues

### 🔍 Data Explorer
- Filter transactions by:
  - Year (2010-2020)
  - Province
  - Amount range
- Search through 5,437+ audit transactions

### 📑 Audit Topics
- Browse 25 audit finding themes
- See which issues are most common
- Understand what auditors flag most often

## Common Issues & Fixes

### "Permission denied" when running Docker

**Fix:**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### "Cannot connect to Docker daemon"

**Fix:**
```bash
sudo systemctl start docker
```

### "Kernel modules not found"

**Fix:** Reboot your computer
```bash
sudo reboot
```

### Data not showing up

**Fix:**
```bash
docker-compose exec backend python scripts/load_data.py
```

## Stopping the Application

```bash
# Keep data
docker-compose down

# Remove everything (including data)
docker-compose down -v
```

## Next Steps

- Read the full [README_VISUALIZER.md](./README_VISUALIZER.md) for detailed information
- Check the [API documentation](http://localhost:8000/docs)
- Explore the [project background](./README.md)

## Need Help?

1. Check the logs: `docker-compose logs`
2. Verify services are running: `docker-compose ps`
3. Review the [Troubleshooting section](./README_VISUALIZER.md#troubleshooting) in the main README

## What This Application Does

OpenAudit Visualizer helps you explore Philippine government audit data from 2010-2020:

- **5,437 transactions** showing unliquidated funds
- **1,422 local government units** (municipalities and cities)
- **86 provinces** across the Philippines
- **25 audit themes** identified through machine learning

You can filter, search, and visualize corruption patterns, accountability issues, and fiscal management across Philippine local governments.

Enjoy exploring the data!
