#!/bin/bash

set -e  # Exit on error

echo "========================================="
echo "OpenAudit Visualizer - Quick Start"
echo "========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed."
    echo ""
    echo "Install Docker with:"
    echo "  Arch Linux: sudo pacman -S docker docker-compose"
    echo "  Ubuntu/Debian: sudo apt install docker.io docker-compose"
    echo ""
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed."
    echo ""
    echo "Install Docker Compose with:"
    echo "  Arch Linux: sudo pacman -S docker-compose"
    echo "  Ubuntu/Debian: sudo apt install docker-compose"
    echo ""
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Error: Docker daemon is not running."
    echo ""
    echo "Start Docker with:"
    echo "  sudo systemctl start docker"
    echo ""
    echo "If you get 'permission denied' errors:"
    echo "  sudo usermod -aG docker \$USER"
    echo "  newgrp docker"
    echo ""
    exit 1
fi

# Check if user can run docker without sudo
if ! docker ps &> /dev/null; then
    echo "⚠️  Warning: You may need to add yourself to the docker group."
    echo ""
    echo "Run these commands:"
    echo "  sudo usermod -aG docker \$USER"
    echo "  newgrp docker"
    echo ""
    echo "Then run this script again."
    echo ""
    exit 1
fi

echo "✓ Docker is installed and running"

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "Creating backend/.env file..."
    cp backend/.env.example backend/.env
    echo "✓ Environment file created"
else
    echo "✓ Environment file already exists"
fi

# Build and start services
echo ""
echo "Building and starting Docker services..."
if ! docker-compose up -d --build; then
    echo ""
    echo "❌ Error: Failed to start services."
    echo ""
    echo "Common fixes:"
    echo "  - Port conflict: Check if ports 5173, 8000, or 5433 are in use"
    echo "  - Disk space: Ensure you have at least 2GB free"
    echo "  - Permissions: Make sure you can run docker without sudo"
    echo ""
    echo "Check logs with: docker-compose logs"
    exit 1
fi

echo "✓ Services started"

# Wait for database to be ready
echo ""
echo "Waiting for database to be ready..."
for i in {1..30}; do
    if docker-compose exec -T postgres pg_isready -U openaudit_user &> /dev/null; then
        echo "✓ Database is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Error: Database did not become ready in time"
        echo ""
        echo "Check database logs with: docker-compose logs postgres"
        exit 1
    fi
    sleep 1
done

# Load data
echo ""
echo "Loading data into database..."
if docker-compose exec -T backend python scripts/load_data.py 2>&1 | grep -q "Data loading complete"; then
    echo "✓ Data loaded successfully"
else
    # Try loading anyway, it might succeed
    docker-compose exec -T backend python scripts/load_data.py > /dev/null 2>&1 || true

    # Verify data was loaded
    COUNT=$(docker-compose exec -T postgres psql -U openaudit_user -d openaudit -t -c "SELECT COUNT(*) FROM unliquidated_transactions;" 2>/dev/null | tr -d ' ')
    if [ "$COUNT" -gt 0 ] 2>/dev/null; then
        echo "✓ Data loaded successfully ($COUNT transactions)"
    else
        echo "⚠️  Warning: Data may not have loaded properly"
        echo ""
        echo "You can try loading data manually with:"
        echo "  docker-compose exec backend python scripts/load_data.py"
    fi
fi

# Verify services are running
echo ""
echo "Verifying services..."

if curl -s http://localhost:8000/health &> /dev/null; then
    echo "✓ Backend API is running"
else
    echo "⚠️  Backend may still be starting up..."
fi

if curl -s http://localhost:5173 &> /dev/null; then
    echo "✓ Frontend is running"
else
    echo "⚠️  Frontend may still be starting up..."
fi

echo ""
echo "========================================="
echo "✅ Setup Complete!"
echo "========================================="
echo ""
echo "📊 Access the application:"
echo "  Frontend:  http://localhost:5173"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/docs"
echo ""
echo "📚 Documentation:"
echo "  Getting Started: ./GETTING_STARTED.md"
echo "  Full Guide:      ./README_VISUALIZER.md"
echo ""
echo "🛠️  Useful commands:"
echo "  View logs:       docker-compose logs -f"
echo "  Stop services:   docker-compose down"
echo "  Restart:         docker-compose restart"
echo "  Load data again: docker-compose exec backend python scripts/load_data.py"
echo ""
echo "🎉 Happy exploring!"
echo ""
