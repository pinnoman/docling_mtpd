# Quick Start Guide

Get Docling Web UI up and running in minutes!

## Prerequisites

- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Python 3.9+** - [Download here](https://www.python.org/downloads/)

## Quick Start (Windows)

### Option 1: Using Batch Scripts (Easiest)

1. **Start the Backend** (in one terminal):
   ```bash
   start-backend.bat
   ```
   Wait for "Application startup complete" message.

2. **Start the Frontend** (in another terminal):
   ```bash
   start-frontend.bat
   ```
   Wait for the server to start.

3. **Open your browser** to `http://localhost:3000`

### Option 2: Manual Setup

#### Terminal 1 - Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### Terminal 2 - Frontend

```bash
cd docling-ui
npm install
npm run dev
```

## Quick Start (macOS/Linux)

#### Terminal 1 - Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

#### Terminal 2 - Frontend

```bash
cd docling-ui
npm install
npm run dev
```

## First Conversion

1. Go to `http://localhost:3000`
2. Click on "From URL" tab
3. Click on "Docling Technical Report (PDF)" example link
4. Click "Convert from URL"
5. Wait a few seconds and see the result!

## Troubleshooting

### Backend won't start
- Make sure Python 3.9+ is installed: `python --version`
- Try: `pip install --upgrade pip`
- Check if port 8000 is available

### Frontend won't start
- Make sure Node.js 18+ is installed: `node --version`
- Try: `npm cache clean --force`
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is available

### Conversion fails
- Make sure both backend AND frontend are running
- Check browser console for errors (F12)
- Verify backend is accessible at `http://localhost:8000/health`

### CORS errors
- Make sure you're accessing the frontend at `http://localhost:3000` (not 127.0.0.1)
- Check that backend CORS settings allow `http://localhost:3000`

## Next Steps

- Read the full [README.md](README.md) for detailed information
- Try uploading your own documents
- Experiment with different output formats (Markdown, HTML, JSON)
- Check out the [Docling documentation](https://docling-project.github.io/docling/)

## Need Help?

- Check the [Docling GitHub Issues](https://github.com/docling-project/docling/issues)
- Review the [Docling Documentation](https://docling-project.github.io/docling/)
- Open an issue in this repository
