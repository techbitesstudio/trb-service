import asyncio
import logging
import sys
import tempfile
import os
from pyppeteer import launch

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Convert HTML to PDF
async def html_to_pdf(html_content: str) -> bytes:
    """
    Converts HTML content to PDF and returns the PDF content as bytes.

    Args:
        html_content (str): The HTML content to convert to PDF

    Returns:
        bytes: The generated PDF content as bytes, or empty bytes if conversion fails
    """
    if not html_content or not isinstance(html_content, str):
        logger.error("Invalid HTML content provided")
        return ''

    tmp_file_path = None
    browser = await launch()
    try:
        logger.info("Creating new page...")
        page = await browser.newPage()
        await page.setViewport({'width': 1200, 'height': 800})
        page.setDefaultNavigationTimeout(60000)  # 60 seconds

        # Create a temporary HTML file to handle content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8') as tmp_file:
            tmp_file.write(html_content)
            tmp_file_path = tmp_file.name

        file_url = f'file://{tmp_file_path}'
        logger.info(f"Navigating to temporary file: {file_url}")

        await page.goto(file_url, {'waitUntil': 'networkidle0'})

        # Additional wait to ensure rendering is complete
        await asyncio.sleep(2)

        logger.info("Generating PDF...")
        # Create a temporary file to save the PDF
        fd, temp_pdf_path = tempfile.mkstemp(suffix=".pdf")
        os.close(fd)

        # Generate PDF with more specific options
        pdf_options = {
            'path': temp_pdf_path,
            'format': 'A4',
            'printBackground': True,
            'margin': {
                'top': '20mm',
                'right': '20mm',
                'bottom': '20mm',
                'left': '20mm'
            },
            'preferCSSPageSize': True,
            'displayHeaderFooter': False,
            'scale': 0.8
        }
        
        # Generate the PDF directly to memory
        pdf_content = await page.pdf(pdf_options)
        
        # Verify the PDF content is not empty
        if not pdf_content:
            raise Exception("Generated PDF is empty")

        logger.info(f"Successfully generated PDF ({len(pdf_content)} bytes)")
        return pdf_content

    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}", exc_info=True)
        return b''  # Return empty bytes on error

    finally:
        if browser:
            try:
                await browser.close()
                logger.info("Browser closed successfully")
            except Exception as e:
                logger.error(f"Error closing browser: {str(e)}")

        # Clean up the temporary file
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
            logger.info(f"Removed temporary file: {tmp_file_path}")

        if temp_pdf_path and os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
            logger.info(f"Removed temporary PDF file: {temp_pdf_path}")
