# Docling Backend API

FastAPI backend for document conversion using Docling.

## Setup

### Windows

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

### macOS/Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /convert` - Convert uploaded file
- `POST /convert-url` - Convert document from URL

## Configuration

The server runs on `http://localhost:8000` by default.
CORS is configured to allow requests from `http://localhost:3000`.
