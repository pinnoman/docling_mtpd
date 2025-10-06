# Docling Web UI

A beautiful and intuitive web interface for [Docling](https://github.com/docling-project/docling) - an AI-powered document processing tool that converts various document formats (PDF, DOCX, PPTX, XLSX, HTML, images, etc.) into structured formats like Markdown, HTML, and JSON.

## Features

- 🎨 **Beautiful UI** - Modern, responsive interface built with Next.js, React, TypeScript, shadcn/ui, and Tailwind CSS
- 📤 **File Upload** - Drag-and-drop or browse to upload documents
- 🔗 **URL Support** - Convert documents directly from URLs
- 🔄 **Multiple Formats** - Export to Markdown, HTML, or JSON
- 👁️ **Live Preview** - View converted documents with syntax highlighting
- 📋 **Copy & Download** - Easy export options for converted content
- 🌓 **Dark Mode** - Full dark mode support

## Supported Document Types

- PDF
- DOCX (Microsoft Word)
- PPTX (Microsoft PowerPoint)
- XLSX (Microsoft Excel)
- HTML
- Images (PNG, JPEG, TIFF)
- Audio (WAV, MP3)

## Prerequisites

- **Node.js** 18+ (for frontend)
- **Python** 3.9+ (for backend)
- **pip** (Python package manager)

## Installation & Setup

### 1. Backend Setup (Python + Docling)

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python main.py
```

The backend API will run on `http://localhost:8001`

### 2. Frontend Setup (Next.js)

```bash
# Navigate to frontend directory
cd docling-ui

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage

1. **Start both servers** (backend on port 8001, frontend on port 3000)
2. **Open your browser** and navigate to `http://localhost:3000`
3. **Choose your input method**:
   - **Upload File**: Drag and drop or browse to select a document
   - **From URL**: Enter a direct link to a document
4. **Select output format**: Choose between Markdown, HTML, or JSON
5. **Click Convert**: Wait for the conversion to complete
6. **View results**: Preview the converted document or view the raw output
7. **Export**: Copy to clipboard or download the converted file

## Example URLs to Try

- Docling Technical Report: `https://arxiv.org/pdf/2408.09869`
- Sample Research Paper: `https://arxiv.org/pdf/2206.01062`

## Project Structure

```
docling1/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # FastAPI server with Docling integration
│   └── requirements.txt    # Python dependencies
├── docling-ui/             # Next.js frontend
│   ├── app/                # Next.js app directory
│   │   ├── page.tsx        # Main page
│   │   ├── layout.tsx      # Root layout
│   │   └── globals.css     # Global styles
│   ├── components/         # React components
│   │   ├── DocumentConverter.tsx  # Main converter component
│   │   ├── FileUpload.tsx         # File upload component
│   │   ├── UrlInput.tsx           # URL input component
│   │   ├── ConversionResult.tsx   # Result display component
│   │   └── ui/                    # shadcn/ui components
│   ├── lib/                # Utility functions
│   └── package.json        # Node.js dependencies
└── README.md               # This file
```

## API Endpoints

### Backend (FastAPI)

- `GET /` - Health check
- `GET /health` - Health status
- `POST /convert` - Convert uploaded file
  - Body: `multipart/form-data` with `file` and `output_format`
- `POST /convert-url` - Convert document from URL
  - Query params: `url`, `output_format`

## Technologies Used

### Frontend
- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI components
- **Lucide React** - Icons
- **React Markdown** - Markdown rendering

### Backend
- **FastAPI** - Python web framework
- **Docling** - Document conversion engine
- **Uvicorn** - ASGI server

## Development

### Frontend Development
```bash
cd docling-ui
npm run dev      # Start dev server
npm run build    # Build for production
npm run start    # Start production server
```

### Backend Development
```bash
cd backend
python main.py   # Start with auto-reload
```

## Environment Configuration

The application uses the following default ports:
- Frontend: `3000`
- Backend: `8001`

To change these, modify:
- Frontend API calls in components (currently hardcoded to `http://localhost:8001`)
- Backend port in `main.py` (uvicorn.run parameters)

### GPU Acceleration (CUDA)

The backend automatically detects and uses CUDA-enabled GPUs when available:

- **With CUDA**: Significantly faster processing, especially for large PDFs and OCR tasks
- **Without CUDA**: Falls back to CPU processing automatically

**To check if GPU is being used:**
1. Start the backend server
2. Check the startup logs for "CUDA is available!" message
3. Visit `http://localhost:8001/health` to see device information

**Requirements for GPU acceleration:**
- NVIDIA GPU with CUDA support
- CUDA Toolkit installed
- PyTorch with CUDA support (`pip install torch --index-url https://download.pytorch.org/whl/cu118`)

## Troubleshooting

### Backend Issues
- **Import errors**: Make sure you've activated the virtual environment and installed all dependencies
- **Port already in use**: Change the port in `main.py`

### Frontend Issues
- **API connection errors**: Ensure the backend is running on port 8001
- **CORS errors**: Check CORS configuration in `backend/main.py`

### Conversion Issues
- **Large files**: May take longer to process
- **Unsupported formats**: Check the supported file types list
- **URL access**: Ensure the URL is publicly accessible

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is built on top of [Docling](https://github.com/docling-project/docling), which is licensed under MIT.

## Acknowledgments

- [Docling Project](https://github.com/docling-project/docling) - The amazing document processing engine
- [shadcn/ui](https://ui.shadcn.com/) - Beautiful UI components
- [Next.js](https://nextjs.org/) - The React framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
