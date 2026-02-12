# GitHub Activity Event Logger

A real-time GitHub webhook event logging application that captures and displays **PUSH**, **PULL REQUEST**, and **MERGE** events from connected repositories.


## Overview

This application listens for GitHub webhook events and stores them in MongoDB, providing a real-time dashboard to visualize all activity happening in your repositories. Events are automatically refreshed every 15 seconds.

### Event Types Captured

| Event Type | Description |
|------------|-------------|
| **PUSH** | Commits pushed to a branch |
| **PULL_REQUEST** | Pull requests opened |
| **MERGE** | Pull requests merged into target branch |

---

## Architecture

```
┌──────────────┐
│    GitHub    │
└──────┬───────┘
       │
       ▼
┌───────────────────────┐
│ Flask route           │
│ (HTTP only)           │
└──────┬────────────────┘
       │
       ▼
┌───────────────────────┐
│ Thread                │
│ (offload work)        │
└──────┬────────────────┘
       │
       ▼
┌───────────────────────────────────────┐
│ github_event_handler                  │
│ (business logic + Pydantic)           │
└──────┬────────────────────────────────┘
       │
       ▼
┌────────────────────────┐
│ Celery task            │
│ (async, retryable)     │
└──────┬─────────────────┘
       │
       ▼
┌────────────────────────┐
│ Redis                  │
│ (broker)               │
└──────┬─────────────────┘
       │
       ▼
┌────────────────────────┐
│ MongoDB                │
│ (persistence)          │
└────────────────────────┘
```

**Event Processing Flow:**
1. **GitHub** sends webhook events
2. **Flask route** receives HTTP request (HTTP only, fast response)
3. **Thread** offloads processing to avoid blocking
4. **github_event_handler** processes with business logic & Pydantic validation
5. **Celery task** queues for async processing with retry capabilities
6. **Redis** acts as message broker between Flask and Celery workers
7. **MongoDB** persists processed events for dashboard display


## 🛠️ Tech Stack

### Backend
- **Flask** - Python web framework
- **Celery** - Distributed task queue for async processing
- **Redis** - Message broker for Celery queue
- **Pydantic** - Data validation
- **PyMongo** - MongoDB driver
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **React 19** - UI library
- **Vite** - Build tool
- **Tailwind CSS v4** - Utility-first CSS
- **Axios** - HTTP client

### Database
- **MongoDB Atlas** - Cloud database

---

### Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB Atlas account for cloud connection string (or local MongoDB)
- ngrok/local-tunnel (for local webhook testing)

### 1. Clone the Repository

```bash
git clone https://github.com/rohitrath0d/webhook-repo.git
cd webhook-repo
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the backend directory:

```env
DATABASE_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority
DATABASE_NAME=webhook-data-receiver-app
ALLOWED_ORIGINS=http://localhost:5173
WEBHOOK_SECRET=your-webhook-secret-here
```

Start the backend server:

```bash
python run_server.py
```

The backend will run on `http://localhost:5000`

### 3. Redis Setup

Ensure Redis is running. You can use Docker:

```bash
# Run Redis in Docker
docker run -d -p 6379:6379 redis:latest
```

Or install locally:
- **Windows**: Download from [Redis-Windows](https://github.com/microsoftarchive/redis/releases)
- **Linux/Mac**: `brew install redis` or use your package manager

### 4. Celery Worker Setup

Start the Celery worker in a separate terminal:

```bash
cd backend
# Activate virtual environment first (if not already active)
celery -A app.celery_app worker --loglevel=info --pool=solo (if you need more than one worker - exclude --polo=solo args)
```

This will start the Celery worker that processes async tasks queued by the Flask backend.

### 5. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:5000
```

Start the development server:

```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

---

## Running All Services Together

For a complete local setup, start these services in parallel (use separate terminals):

**Terminal 1 - Redis:**
```bash
# If using Docker
docker run -d -p 6379:6379 redis:latest

# Or if installed locally
redis-server
```

**Terminal 2 - Flask Backend:**
```bash
cd backend
# Activate virtual environment
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
python run_server.py
```

**Terminal 3 - Celery Worker:**
```bash
cd backend
# Activate virtual environment (if not already active)
celery -A app.celery_app worker --loglevel=info
```

**Terminal 4 - React Frontend:**
```bash
cd frontend
npm run dev
```

Access the application at `http://localhost:5173`

---

## Docker Setup

Run both services with Docker Compose:

```bash
docker-compose up --build
```

| Service | Port |
|---------|------|
| Backend | 4001 (maps to 5000) |
| Frontend | 3001 (maps to 3000) |

---

## Testing with ngrok

Since GitHub webhooks require a publicly accessible URL, use **ngrok** to expose your local server for testing.

### Step 1: Install ngrok

```bash
# Windows (with Chocolatey)
choco install ngrok

# Or download from https://ngrok.com/download
```

### Step 2: Start the Backend Server

```bash
cd backend
python run_server.py
```

### Step 3: Start ngrok Tunnel / Local Tunnel

Open a new terminal and run:

```bash
ngrok http 5000
```

You'll see output like:

```
Session Status                online
Forwarding                    https://abc123xyz.ngrok.io -> http://localhost:5000
```

Copy the **HTTPS forwarding URL** (e.g., `https://abc123xyz.ngrok.io`)

### Step 4: Configure GitHub Webhook

1. Go to your GitHub repository's **Settings** → **Webhooks** → **Add webhook**

2. Configure the webhook:

   | Field | Value |
   |-------|-------|
   | **Payload URL** | `https://abc123xyz.ngrok.io/webhook/receiver` |
   | **Content type** | `application/json` |
   | **Secret** | *(your WEBHOOK_SECRET from .env)* |
   | **SSL verification** | Enable |
   | **Events** | Select: `Pushes`, `Pull requests` |

3. Click **Add webhook**

4. GitHub will send a `ping` event - you should see the response in ngrok's web interface at `http://localhost:4040`

### Step 5: Test with Real Events

Perform actions in your repository:
- **Push a commit** → Triggers PUSH event
- **Open a pull request** → Triggers PULL_REQUEST event
- **Merge a pull request** → Triggers MERGE event

Check the frontend dashboard to see events appear in real-time!

---

## Dummy Actions Repository

For testing purposes, a separate repository is used to simulate GitHub events:

**Repository**: [https://github.com/rohitrath0d/actions-repo](https://github.com/rohitrath0d/actions-repo)

This repository is configured with the webhook pointing to this application. You can:

1. Push dummy commits to trigger **PUSH** events
2. Create pull requests to trigger **PULL_REQUEST** events  
3. Merge pull requests to trigger **MERGE** events

### How to Use

1. Clone the actions-repo:
   ```bash
   git clone https://github.com/rohitrath0d/actions-repo.git
   cd actions-repo
   ```

2. Make changes and push:
   ```bash
   echo "test change" >> demo-text.txt
   git add .
   git commit -m "Test push event"
   git push origin main
   ```

3. Watch the events appear on your dashboard!

---

## 📡 API Endpoints

### Health Check
```http
GET /
```
Response:
```json
{
  "status": "Webhook server running"
}
```

### Webhook Receiver
```http
POST /webhook/receiver
```
Receives GitHub webhook events and stores them in MongoDB.

**Headers Required:**
- `X-GitHub-Event`: Event type (push, pull_request)
- `Content-Type`: application/json

### Get Events
```http
GET /webhook/events
```
Returns the latest 50 events sorted by timestamp (newest first).

Response:
```json
[
  {
    "_id": "...",
    "request_id": "abc123",
    "author": "rohitrath0d",
    "action": "PUSH",
    "from_branch": null,
    "to_branch": "main",
    "timestamp": "2026-02-01T20:30:00Z"
  }
]
```
---

## 🔧 Environment Variables & Configuration

### Celery & Redis Configuration

The Celery task queue is configured to work with Redis as the message broker. You can customize these settings:

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_URL` | Redis connection URL | redis://localhost:6379/0 |
| `CELERY_BROKER_URL` | Celery broker URL | redis://localhost:6379/0 |
| `CELERY_RESULT_BACKEND` | Celery result backend | redis://localhost:6379/0 |

### Backend (.env)

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | MongoDB connection string |
| `DATABASE_NAME` | Database name |
| `ALLOWED_ORIGINS` | CORS allowed origins (comma-separated) |
| `WEBHOOK_SECRET` | GitHub webhook secret for verification |

### Frontend (.env)

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Backend API base URL |

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Author

**Rohit Rathod**  
GitHub: [@rohitrath0d](https://github.com/rohitrath0d)

