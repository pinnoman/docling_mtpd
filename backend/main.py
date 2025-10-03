from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from docling.document_converter import DocumentConverter
import tempfile
import os
import logging
import traceback
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Docling API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the document converter
converter = DocumentConverter()

@app.get("/")
async def root():
    return {"message": "Docling API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/convert")
async def convert_document(
    file: UploadFile = File(...),
    output_format: str = "markdown"
):
    """
    Convert uploaded document to specified format.
    Supported formats: markdown, html, json
    """
    try:
        # Validate file extension
        allowed_extensions = {
            '.pdf', '.docx', '.pptx', '.xlsx', '.html', 
            '.png', '.jpg', '.jpeg', '.tiff', '.wav', '.mp3'
        }
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Supported types: {', '.join(allowed_extensions)}"
            )
        
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Convert the document
            result = converter.convert(tmp_file_path)
            
            # Export based on requested format
            if output_format == "markdown":
                output = result.document.export_to_markdown()
            elif output_format == "html":
                output = result.document.export_to_html()
            elif output_format == "json":
                output = result.document.export_to_dict()
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported output format: {output_format}"
                )
            
            return JSONResponse(content={
                "success": True,
                "filename": file.filename,
                "format": output_format,
                "content": output
            })
        
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error converting document: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")

@app.post("/convert-url")
async def convert_from_url(url: str, output_format: str = "markdown"):
    """
    Convert document from URL to specified format.
    """
    try:
        # Convert the document from URL
        result = converter.convert(url)
        
        # Export based on requested format
        if output_format == "markdown":
            output = result.document.export_to_markdown()
        elif output_format == "html":
            output = result.document.export_to_html()
        elif output_format == "json":
            output = result.document.export_to_dict()
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported output format: {output_format}"
            )
        
        return JSONResponse(content={
            "success": True,
            "url": url,
            "format": output_format,
            "content": output
        })
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error converting document from URL: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Conversion error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
