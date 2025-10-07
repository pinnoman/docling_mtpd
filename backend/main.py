from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from typing import List
import tempfile
import os
import json
import logging
import traceback
from pathlib import Path
import torch

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

# Detect CUDA availability and configure device
def get_device():
    """Detect if CUDA is available and return appropriate device."""
    if torch.cuda.is_available():
        device = "cuda"
        logger.info(f"CUDA is available! Using GPU: {torch.cuda.get_device_name(0)}")
        logger.info(f"CUDA Version: {torch.version.cuda}")
        logger.info(f"Number of GPUs: {torch.cuda.device_count()}")
    else:
        device = "cpu"
        logger.info("CUDA not available. Using CPU for processing.")
    return device

# Get device
device = get_device()

# Configure pipeline options for GPU acceleration
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
pipeline_options.do_table_structure = True

# Configure format options with device
format_options = {
    InputFormat.PDF: PdfFormatOption(
        pipeline_options=pipeline_options
    )
}

# Initialize the document converter with GPU support
converter = DocumentConverter(
    format_options=format_options
)

logger.info(f"DocumentConverter initialized with device: {device}")

@app.get("/")
async def root():
    return {"message": "Docling API is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint with device information."""
    health_info = {
        "status": "healthy",
        "device": device,
        "cuda_available": torch.cuda.is_available()
    }
    
    if torch.cuda.is_available():
        health_info["gpu_name"] = torch.cuda.get_device_name(0)
        health_info["gpu_count"] = torch.cuda.device_count()
        health_info["cuda_version"] = torch.version.cuda
    
    return health_info

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
                output = json.dumps(result.document.export_to_dict(), indent=2)
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
            output = json.dumps(result.document.export_to_dict(), indent=2)
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

@app.post("/convert-batch")
async def convert_batch_documents(
    files: List[UploadFile] = File(...),
    output_format: str = Form("markdown")
):
    """
    Convert multiple uploaded documents to specified format.
    Returns results for all files, including any errors.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    results = []
    allowed_extensions = {
        '.pdf', '.docx', '.pptx', '.xlsx', '.html', 
        '.png', '.jpg', '.jpeg', '.tiff', '.wav', '.mp3'
    }
    
    for file in files:
        file_result = {
            "filename": file.filename,
            "success": False,
            "format": output_format,
            "content": None,
            "error": None
        }
        
        try:
            # Validate file extension
            file_ext = Path(file.filename).suffix.lower()
            
            if file_ext not in allowed_extensions:
                file_result["error"] = f"Unsupported file type: {file_ext}"
                results.append(file_result)
                continue
            
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
                    output = json.dumps(result.document.export_to_dict(), indent=2)
                else:
                    file_result["error"] = f"Unsupported output format: {output_format}"
                    results.append(file_result)
                    continue
                
                file_result["success"] = True
                file_result["content"] = output
                
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
        
        except Exception as e:
            logger.error(f"Error converting {file.filename}: {str(e)}")
            file_result["error"] = str(e)
        
        results.append(file_result)
    
    # Calculate summary statistics
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    
    return JSONResponse(content={
        "success": True,
        "total": len(results),
        "successful": successful,
        "failed": failed,
        "results": results
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
