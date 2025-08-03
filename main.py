import os
import logging
import tempfile
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from pydantic import BaseModel
import logging
import os
import html
from typing import Optional
from src.service.html_to_pdf import html_to_pdf

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TRB Service",
    description="A template for a production-ready FastAPI service.",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def unescape_html_content(html_content: str) -> str:
    """
    Unescape HTML entities in the provided HTML content.
    
    Args:
        html_content: The HTML content with potential escaped characters
        
    Returns:
        str: The unescaped HTML content
    """
    return html.unescape(html_content)


class PDFRequest(BaseModel):
    html_content: str

@app.get("/")
def read_root():
    """A simple hello world endpoint."""
    return {"Hello": "World"}


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint to ensure the service is running."""
    return {"status": "ok"}


@app.post("/generate-pdf", response_class=Response, tags=["PDF Generation"])
async def generate_pdf(request: PDFRequest):
    """
    Generate a PDF from HTML content and return it as a downloadable file.

    Args:
        request (PDFRequest): The request containing the HTML content to convert to PDF.

    Returns:
        Response: A response containing the PDF file with appropriate headers
                for file download, or a JSONResponse with an error message.
    """
    try:
        logger.info("Starting PDF generation...")
        # Unescape HTML content before processing
        unescaped_html = unescape_html_content(request.html_content)
        logger.info(f"HTML content length after unescaping: {len(unescaped_html)} characters")
        
        pdf_content = await html_to_pdf(unescaped_html)

        if not pdf_content:
            error_msg = "Failed to generate PDF: The conversion resulted in empty content."
            logger.error(error_msg)
            return JSONResponse(status_code=500, content={"error": error_msg})
        
        logger.info(f"PDF generated successfully. Size: {len(pdf_content)} bytes")
        
        # Create a streaming response for better memory efficiency
        from starlette.responses import StreamingResponse
        from io import BytesIO
        
        return StreamingResponse(
            iter([pdf_content]),
            media_type="application/pdf",
            headers={
                'Content-Disposition': 'attachment; filename="resume.pdf"',
                'Content-Length': str(len(pdf_content)),
                'Content-Type': 'application/pdf',
                'Access-Control-Expose-Headers': 'Content-Disposition',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            }
        )

    except Exception as e:
        import traceback
        error_msg = f"Error generating PDF: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=500, 
            content={"error": error_msg},
            headers={"Content-Type": "application/json"}
        )
