from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import logging

app = FastAPI()
# Mount the static directory
app.mount("/public", StaticFiles(directory="public"), name="public")
logger = logging.getLogger("mylogger")
logger.setLevel(logging.INFO)

@app.get("/", response_class=HTMLResponse)
def home():
    # Check if the file exists
    image_path = "public/sticker.png"
    if not os.path.exists(image_path):
        logger.error(f"Image file not found at {image_path}")
    
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Segment-2-demo</title>
        </head>
        <body>
            <h1>Segment Anything</h1>
            <img src="/public/sticker.png">
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/test")
def test_route():
    """Simple test route to verify logging is working."""
    logger.info("Test route called!")
    return {"msg": "Hello"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
