"""
PDF Converter Tool - FastAPI Main Application
"""

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import API routes
from .api import convert

# 创建应用实例
app = FastAPI(
    title="PDF Converter API",
    description="Free online PDF converter tools - Convert PDF to Word, Excel, and PowerPoint",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS (生产环境应该限制具体域名)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend path
frontend_path = Path(__file__).parent.parent.parent / "frontend"
index_html = None
if frontend_path.exists():
    index_path = frontend_path / "index.html"
    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            index_html = f.read()
        logger.info(f"Loaded frontend from: {frontend_path}")

# Include API routers FIRST
app.include_router(convert.router)


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "pdf-converter-api",
        "version": "1.0.0"
    }


@app.get("/api/info")
async def api_info():
    """API信息端点"""
    return {
        "name": "PDF Converter API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "api_info": "/api/info",
            "convert_pdf_to_word": "/api/convert/pdf-to-word",
            "validate_pdf": "/api/convert/validate-pdf"
        },
        "features": [
            "PDF to Word conversion",
            "File validation",
            "Size limits (10MB)",
            "Auto-cleanup"
        ]
    }


@app.get("/{path:path}")
async def serve_frontend(path: str):
    """Serve frontend SPA - return index.html for all non-API routes"""
    # Check if it's requesting a static asset
    if path and "." in path:
        asset_path = frontend_path / path
        if asset_path.exists() and asset_path.is_file():
            with open(asset_path, "rb") as f:
                content = f.read()
            # Determine content type
            if path.endswith(".css"):
                return Response(content, media_type="text/css")
            elif path.endswith(".js"):
                return Response(content, media_type="application/javascript")
            elif path.endswith(".png"):
                return Response(content, media_type="image/png")
            elif path.endswith(".jpg") or path.endswith(".jpeg"):
                return Response(content, media_type="image/jpeg")
            elif path.endswith(".svg"):
                return Response(content, media_type="image/svg+xml")
            elif path.endswith(".ico"):
                return Response(content, media_type="image/x-icon")
            else:
                return Response(content)
    # Return index.html for all other routes (SPA)
    if index_html:
        return Response(content=index_html, media_type="text/html")
    return Response(content="Frontend not found", status_code=404)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
