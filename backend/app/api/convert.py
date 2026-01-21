"""
PDF Conversion API Routes
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse, Response
from pathlib import Path
import logging
import tempfile
from urllib.parse import quote

from ..core.pdf_converter import PDFToWordConverter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/convert", tags=["conversion"])

# Initialize converter
temp_dir = Path(tempfile.gettempdir()) / "pdf_converter"
converter = PDFToWordConverter(temp_dir)


@router.post("/pdf-to-word")
async def pdf_to_word(file: UploadFile = File(...)):
    """
    Convert PDF to Word document

    Args:
        file: Uploaded PDF file

    Returns:
        JSON response with conversion result or download URL
    """
    temp_file_path = None
    output_file_path = None

    try:
        # Validate file type
        if not file.filename or not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        # Read file content
        content = await file.read()

        # Validate file size (10MB limit)
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")

        logger.info(f"Received PDF file: {file.filename}, size: {len(content)} bytes")

        # Save uploaded file
        temp_file_path = await converter.save_uploaded_file(content, file.filename)

        # Validate PDF
        validation = converter.validate_pdf(temp_file_path)
        if not validation["valid"]:
            raise HTTPException(status_code=400, detail=f"Invalid PDF: {validation.get('error')}")

        logger.info(f"PDF validated: {validation['pages']} pages")

        # Convert PDF to Word
        output_file_path = await converter.convert_pdf_to_word(
            temp_file_path,
            output_filename=file.filename.replace('.pdf', '.docx')
        )

        # Get file info
        file_info = converter.get_file_info(output_file_path)

        logger.info(f"Conversion successful: {output_file_path}")

        # Read file content
        with open(output_file_path, 'rb') as f:
            file_content = f.read()

        # Encode filename for Content-Disposition header
        # Use RFC 2231/5987 format for UTF-8 encoded filenames
        safe_filename = file_info["filename"]
        encoded_filename = quote(safe_filename, safe='')

        return Response(
            content=file_content,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Conversion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

    finally:
        # Cleanup: Always clean up the uploaded file
        if temp_file_path and temp_file_path.exists():
            await converter.cleanup_file(temp_file_path)

        # Note: Don't clean up output file immediately if user needs to download
        # In production, implement a cleanup job that runs after 1 hour


@router.get("/pdf-to-word")
async def pdf_to_word_info():
    """Get information about the PDF to Word conversion endpoint"""
    return {
        "endpoint": "/api/convert/pdf-to-word",
        "method": "POST",
        "description": "Convert PDF document to editable Word file",
        "parameters": {
            "file": {
                "type": "PDF file",
                "format": "multipart/form-data",
                "max_size": "10MB",
                "required": True
            }
        },
        "response": {
            "format": "Word document (.docx)",
            "media_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        },
        "features": [
            "Preserves text formatting",
            "Extracts images",
            "Maintains table structure",
            "Supports multi-page PDFs"
        ],
        "status": "Active"
    }


@router.post("/validate-pdf")
async def validate_pdf(file: UploadFile = File(...)):
    """
    Validate PDF file without converting

    Args:
        file: Uploaded PDF file

    Returns:
        PDF validation results
    """
    try:
        # Read file content
        content = await file.read()

        # Save temporarily
        temp_file_path = await converter.save_uploaded_file(content, file.filename)

        # Validate
        validation = converter.validate_pdf(temp_file_path)

        # Get file info
        file_info = converter.get_file_info(temp_file_path)

        # Clean up
        await converter.cleanup_file(temp_file_path)

        return {
            "valid": validation["valid"],
            "filename": file.filename,
            "size": file_info["size"],
            "size_mb": file_info["size_mb"],
            "pages": validation.get("pages", 0),
            "encrypted": validation.get("encrypted", False),
            "has_images": validation.get("has_images", False)
        }

    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@router.post("/pdf-to-excel")
async def pdf_to_excel(file: UploadFile = File(...)):
    """
    Convert PDF to Excel document
    Extracts tables from PDF and saves to Excel format

    Args:
        file: Uploaded PDF file

    Returns:
        Excel document (.xlsx)
    """
    temp_file_path = None
    output_file_path = None

    try:
        # Validate file type
        if not file.filename or not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        # Read file content
        content = await file.read()

        # Validate file size (10MB limit)
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")

        logger.info(f"Received PDF file for Excel conversion: {file.filename}, size: {len(content)} bytes")

        # Save uploaded file
        temp_file_path = await converter.save_uploaded_file(content, file.filename)

        # Validate PDF
        validation = converter.validate_pdf(temp_file_path)
        if not validation["valid"]:
            raise HTTPException(status_code=400, detail=f"Invalid PDF: {validation.get('error')}")

        # Convert PDF to Excel
        output_file_path = await converter.convert_pdf_to_excel(
            temp_file_path,
            output_filename=file.filename.replace('.pdf', '.xlsx')
        )

        # Get file info
        file_info = converter.get_file_info(output_file_path)
        logger.info(f"Excel conversion successful: {output_file_path}")

        # Read file content
        with open(output_file_path, 'rb') as f:
            file_content = f.read()

        # Encode filename for Content-Disposition header
        safe_filename = file_info["filename"]
        encoded_filename = quote(safe_filename, safe='')

        return Response(
            content=file_content,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Excel conversion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Excel conversion failed: {str(e)}")

    finally:
        # Cleanup uploaded file
        if temp_file_path and temp_file_path.exists():
            await converter.cleanup_file(temp_file_path)


@router.post("/pdf-to-ppt")
async def pdf_to_ppt(file: UploadFile = File(...)):
    """
    Convert PDF to PowerPoint presentation
    Each PDF page becomes a PPT slide

    Args:
        file: Uploaded PDF file

    Returns:
        PowerPoint presentation (.pptx)
    """
    temp_file_path = None
    output_file_path = None

    try:
        # Validate file type
        if not file.filename or not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        # Read file content
        content = await file.read()

        # Validate file size (10MB limit)
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")

        logger.info(f"Received PDF file for PPT conversion: {file.filename}, size: {len(content)} bytes")

        # Save uploaded file
        temp_file_path = await converter.save_uploaded_file(content, file.filename)

        # Validate PDF
        validation = converter.validate_pdf(temp_file_path)
        if not validation["valid"]:
            raise HTTPException(status_code=400, detail=f"Invalid PDF: {validation.get('error')}")

        # Convert PDF to PPT
        output_file_path = await converter.convert_pdf_to_ppt(
            temp_file_path,
            output_filename=file.filename.replace('.pdf', '.pptx')
        )

        # Get file info
        file_info = converter.get_file_info(output_file_path)
        logger.info(f"PPT conversion successful: {output_file_path}")

        # Read file content
        with open(output_file_path, 'rb') as f:
            file_content = f.read()

        # Encode filename for Content-Disposition header
        safe_filename = file_info["filename"]
        encoded_filename = quote(safe_filename, safe='')

        return Response(
            content=file_content,
            media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation',
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PPT conversion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PPT conversion failed: {str(e)}")

    finally:
        # Cleanup uploaded file
        if temp_file_path and temp_file_path.exists():
            await converter.cleanup_file(temp_file_path)
