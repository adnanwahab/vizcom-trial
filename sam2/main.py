from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
import os
import logging
import torch
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
from PIL import Image
import io
import numpy as np

app = FastAPI()
# Mount the static directory
app.mount("/public", StaticFiles(directory="public"), name="public")
logger = logging.getLogger("mylogger")
logger.setLevel(logging.INFO)

# Initialize SAM2 model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Device type is ", device)

sam2_checkpoint = "./checkpoints/sam2.1_hiera_large.pt"
model_cfg = "configs/sam2.1/sam2.1_hiera_l.yaml"

sam2_model = build_sam2(model_cfg, sam2_checkpoint, device=device)
predictor = SAM2ImagePredictor(sam2_model)

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
            <img src="https://github.com/adnanwahab/vizcom-trial/blob/main/public/vase.png?raw=true">

                        <img src="https://github.com/adnanwahab/vizcom-trial/blob/main/public/sticker.png?raw=true">

        <canvas id="canvas"></canvas>

        <script>
        

        
        </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/test")
def test_route():
    """Simple test route to verify logging is working."""
    logger.info("Test route called!")
    return {"msg": "Hello"}

@app.post("/segment")
async def segment_image(image: UploadFile = File(...)):
    """
    Endpoint to perform image segmentation using SAM2
    """
    try:
        # Read the image file
        contents = await image.read()
        pil_image = Image.open(io.BytesIO(contents))
        
        # Convert PIL image to numpy array
        image_array = np.array(pil_image)
        
        # Set image in predictor
        predictor.set_image(image_array)
        
        # Get segmentation (using point prompt at center of image for this example)
        h, w = image_array.shape[:2]
        point_coords = np.array([[w//2, h//2]])  # Center point
        point_labels = np.array([1])  # 1 indicates foreground point
        
        masks, scores, logits = predictor.predict(
            point_coords=point_coords,
            point_labels=point_labels
        )
        
        # Convert the first mask to a binary image
        mask = masks[0].astype(np.uint8) * 255
        mask_image = Image.fromarray(mask)
        
        # Save to bytes
        img_byte_arr = io.BytesIO()
        mask_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        return Response(content=img_byte_arr, media_type="image/png")
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
