# OpenAudit Visualizer - Full Stack Application

A comprehensive web application for exploring Philippine Commission on Audit (COA) reports data (2010-2020) with interactive visualizations and LLM integration capabilities.

## Quick Start (TL;DR)

```bash
# 1. Start Docker service
sudo systemctl start docker

# 2. Add yourself to docker group (first time only)
sudo usermod -aG docker $USER
newgrp docker

# 3. Run the application
./quick-start.sh

# 4. Open in browser
# http://localhost:5173
```

**That's it!** The application will start with all data loaded.

---

## Features

- **Interactive Dashboard**: Real-time statistics and visualizations of audit findings
- **Data Explorer**: Filter and search through 5,441+ unliquidated transaction records
- **Audit Topics**: Browse 25 audit finding themes identified through LDA topic modeling
- **PostgreSQL Database**: Structured storage for audit reports, LGUs, and findings
- **Python FastAPI Backend**: RESTful API with comprehensive endpoints
- **TypeScript React Frontend**: Modern, responsive UI with data visualization
- **LLM Integration Ready**: Infrastructure for AI-powered audit analysis
- **Docker Support**: One-command deployment with docker-compose

## Tech Stack

### Backend
- **Python 3.11** with FastAPI
- **PostgreSQL 15** database
- **SQLAlchemy** ORM
- **Pydantic** data validation
- Ready for **OpenAI** and **Anthropic** LLM APIs

### Frontend
- **TypeScript** with **React 18**
- **Vite** build tool
- **TailwindCSS** for styling
- **Recharts** for data visualization
- **TanStack Query** for data fetching

## Installation Guide for New Users

### System Requirements
- **Linux** (tested on Arch Linux, Ubuntu, Debian)
- **Docker** and **Docker Compose**
- **4GB RAM** minimum (8GB recommended)
- **2GB free disk space**

### Step 1: Install Prerequisites

**On Arch Linux:**
```bash
sudo pacman -S docker docker-compose
```

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install docker.io docker-compose
```

### Step 2: Set Up Docker Permissions

Add your user to the docker group (so you don't need sudo):
```bash
# Add yourself to docker group
sudo usermod -aG docker $USER

# Log out and log back in, OR run:
newgrp docker

# Verify it worked
groups
# You should see "docker" in the list
```

### Step 3: Start Docker Service

**On systems using systemd (most modern Linux):**
```bash
# Start Docker
sudo systemctl start docker

# Enable Docker to start on boot (optional)
sudo systemctl enable docker

# Check Docker is running
sudo systemctl status docker
```

**If you get kernel module errors**, you need to reboot:
```bash
# Check your kernel version
uname -r

# If modules are missing (common after kernel updates)
sudo reboot

# After reboot, start Docker again
sudo systemctl start docker
```

### Step 4: Download the Application

```bash
# Clone or navigate to the repository
cd /path/to/OpenAudit-Visualizer

# Make scripts executable
chmod +x quick-start.sh
```

### Step 5: Run the Application

**Quick Method (Automated):**
```bash
./quick-start.sh
```

**Manual Method (Step by Step):**
```bash
# 1. Start all services
docker-compose up -d

# 2. Wait for database to be ready (about 10 seconds)
sleep 10

# 3. Load the data into database
docker-compose exec backend python scripts/load_data.py

# 4. Verify everything is running
docker-compose ps
```

### Step 6: Access the Application

Open your web browser and go to:

**Main Application:**
```
http://localhost:5173
```

**API Documentation:**
```
http://localhost:8000/docs
```

**Health Check:**
```bash
curl http://localhost:8000/health
```

## Using the Application

### Dashboard Tab
- View **4 key statistics** at the top:
  - Total LGUs (Local Government Units)
  - Total audit reports in database
  - Number of provinces covered
  - Total unliquidated funds (in millions of pesos)

- **Yearly Trends Chart**: Line graph showing unliquidated amounts from 2010-2020
- **Top 10 LGUs Bar Chart**: Which municipalities have the highest unliquidated amounts
- **Detailed Table**: Full list of top 20 LGUs with province and transaction counts

### Data Explorer Tab
Use the filter controls to search through 5,437+ transactions:

1. **Year Filter**: Select specific year (2010-2020) or "All Years"
2. **Province Filter**: Filter by province or "All Provinces"
3. **Amount Filters**: Set minimum and maximum transaction amounts
4. Click "Search" or filters apply automatically
5. Results show in the table below with LGU name, province, year, and amount

**Example Queries:**
- "Show me all transactions in Cebu in 2015"
- "Find all transactions over ₱10 million"
- "What did Manila report between 2018-2020?"

### Audit Topics Tab
Browse the 25 audit finding themes identified through machine learning:

- Each card shows:
  - **Topic Number** (1-25)
  - **Description** (e.g., "Unliquidated Cash Advances Issues")
  - **Key Terms** from the topic model
  - **Prevalence Bar** showing how common this issue is

These topics come from analyzing 17,392 audit reports using LDA topic modeling.

## Troubleshooting

### Docker Permission Denied
**Error:** `permission denied while trying to connect to the Docker daemon socket`

**Solution:**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Docker Service Won't Start
**Error:** `Failed to start Docker Application Container Engine`

**Solution:** Reboot your system to load updated kernel modules
```bash
sudo reboot
```

### Port Already in Use
**Error:** `port 5432: address already in use`

**Solution:** The application uses port 5433 for PostgreSQL to avoid conflicts. If you still get errors:
```bash
# Check what's using the ports
sudo netstat -tulpn | grep -E '5432|5433|8000|5173'

# Stop the conflicting service or change ports in docker-compose.yml
```

### Data Not Loading
**Error:** `CSV file not found` or `No data showing in frontend`

**Solution:**
```bash
# Re-run the data loading script
docker-compose exec backend python scripts/load_data.py

# Verify data loaded
docker-compose exec postgres psql -U openaudit_user -d openaudit -c "SELECT COUNT(*) FROM unliquidated_transactions;"
```

### Frontend Won't Load
**Error:** Blank page or connection refused

**Solution:**
```bash
# Check frontend logs
docker-compose logs frontend

# Restart frontend
docker-compose restart frontend

# Clear browser cache and refresh
```

### Can't Access Application
**Error:** `curl: (7) Failed to connect`

**Solution:**
```bash
# Check all services are running
docker-compose ps

# Check logs for errors
docker-compose logs

# Restart all services
docker-compose down
docker-compose up -d
```

## Stopping the Application

```bash
# Stop all services (keeps data)
docker-compose down

# Stop and remove all data
docker-compose down -v
```

## Updating the Application

```bash
# Pull latest changes
git pull

# Rebuild containers
docker-compose down
docker-compose build
docker-compose up -d

# Reload data if needed
docker-compose exec backend python scripts/load_data.py
```

## Common Commands

```bash
# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Restart a service
docker-compose restart backend

# Access database directly
docker-compose exec postgres psql -U openaudit_user -d openaudit

# Run backend shell
docker-compose exec backend bash

# Check service status
docker-compose ps
```

### Option 2: Manual Setup

#### Backend Setup

1. Create Python virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

4. Initialize database:
```bash
psql -U postgres -c "CREATE DATABASE openaudit;"
psql -U openaudit_user -d openaudit -f database/schema.sql
```

5. Load data:
```bash
python scripts/load_data.py
```

6. Start backend:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Create environment file:
```bash
echo "VITE_API_URL=http://localhost:8000" > .env
```

3. Start development server:
```bash
npm run dev
```

## Project Structure

```
OpenAudit-Visualizer/
├── backend/
│   ├── app/
│   │   ├── routers/          # API endpoint routers
│   │   │   ├── topics.py     # Audit topics endpoints
│   │   │   ├── lgus.py       # Local government endpoints
│   │   │   ├── transactions.py # Transaction endpoints
│   │   │   ├── analytics.py  # Analytics endpoints
│   │   │   └── llm.py        # LLM integration endpoints
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── database.py       # Database connection
│   │   ├── config.py         # Configuration
│   │   └── main.py           # FastAPI application
│   ├── database/
│   │   └── schema.sql        # Database schema
│   ├── scripts/
│   │   └── load_data.py      # Data loading script
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── Dashboard.tsx # Main dashboard
│   │   │   ├── Explorer.tsx  # Data explorer
│   │   │   └── Topics.tsx    # Topics viewer
│   │   ├── services/
│   │   │   └── api.ts        # API client
│   │   ├── types/
│   │   │   └── index.ts      # TypeScript types
│   │   ├── App.tsx           # Main app component
│   │   ├── main.tsx          # Entry point
│   │   └── index.css         # Global styles
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker-compose.yml
├── unliquidata1024.csv       # Source data
├── Topicmodel1.R             # Topic modeling script
├── extraction1.R             # Data extraction script
└── README_VISUALIZER.md      # This file
```

## API Endpoints

### Topics
- `GET /topics` - List all audit topics
- `GET /topics/{id}` - Get topic details
- `GET /topics/{id}/analysis` - Get topic analysis

### Local Governments
- `GET /lgus` - List LGUs (with filters)
- `GET /lgus/provinces` - List provinces
- `GET /lgus/{id}` - Get LGU details
- `GET /lgus/search/by-name` - Search LGUs

### Transactions
- `GET /transactions` - List transactions (with filters)
- `GET /transactions/years` - Get available years
- `GET /transactions/aggregate/by-year` - Yearly aggregates
- `GET /transactions/aggregate/by-province` - Province aggregates
- `GET /transactions/top-lgus` - Top LGUs by amount

### Analytics
- `GET /analytics/stats` - Overall statistics
- `GET /analytics/trends/yearly` - Yearly trends
- `GET /analytics/distribution/amount-ranges` - Amount distribution
- `GET /analytics/heatmap/province-year` - Province-year heatmap

### LLM Integration
- `POST /llm/analyze` - Analyze with LLM
- `GET /llm/analyses` - List analyses
- `GET /llm/analyses/{id}` - Get analysis

## Database Schema

The database consists of 7 main tables:

1. **audit_topics** - 25 audit finding themes from topic modeling
2. **local_governments** - LGU information (municipalities, cities)
3. **audit_reports** - Audit report metadata
4. **unliquidated_transactions** - Extracted transaction data
5. **report_topics** - Topic-report associations
6. **llm_analysis** - LLM-generated insights

## LLM Integration

The application is ready for LLM integration. To enable:

1. Add API keys to `.env`:
```env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

2. Use the LLM endpoints to:
   - Analyze individual reports
   - Generate summaries for LGUs
   - Identify patterns and anomalies
   - Generate recommendations

Example LLM request:
```json
{
  "lgu_id": 123,
  "analysis_type": "risk_assessment",
  "model": "claude-sonnet-4"
}
```

## Data Source

Based on Philippine Commission on Audit (COA) executive summaries:
- **Period**: 2010-2020
- **Coverage**: 17,392 audit reports across Philippine local governments
- **Focus**: "Audit Findings and Recommendations" sections
- **Methodology**: LDA topic modeling (k=25) + manual extraction

## Development

### Backend Development
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Running Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## Production Deployment

1. Update environment variables for production
2. Build frontend:
```bash
cd frontend
npm run build
```

3. Use production docker-compose:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

4. Set up reverse proxy (nginx/traefik)
5. Configure SSL certificates
6. Set up database backups

## Contributing

This application is built on the OpenAudit initiative. See the main README.md for project background and research context.

## License

Creative Commons Attribution 4.0 International (CC BY 4.0)

## Acknowledgments

- Philippine Commission on Audit (COA) for providing the audit reports
- MIT GOV/LAB for financial support
- MIT Political Methodology Lab for support
- Original OpenAudit team: Jerik Cruz, Philip Arnold Tuaño, Heidi Mendoza, Rainier Mora

## Support

For issues or questions:
1. Check API documentation: http://localhost:8000/docs
2. Review logs: `docker-compose logs -f`
3. Verify database: `docker-compose exec postgres psql -U openaudit_user -d openaudit`
