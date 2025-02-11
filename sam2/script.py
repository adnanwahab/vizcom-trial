import torch
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
from PIL import Image

checkpoint = "./checkpoints/sam2.1_hiera_large.pt"
model_cfg = "configs/sam2.1/sam2.1_hiera_l.yaml"
predictor = SAM2ImagePredictor(build_sam2(model_cfg, checkpoint))



image = Image.open('../public/vase.png')

with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
    predictor.set_image(image)
    masks, score, logits = predictor.predict(
        point_coords=None,
        point_labels=None,
        box=input_box[None, :],
        multimask_output=False
    )
    print(masks, _, logits)






# import io
# import numpy as np
# from fastapi import FastAPI, File, UploadFile, Request
# from fastapi.responses import HTMLResponse
# from typing import List
# from PIL import Image

# # If using the official Segment Anything
# # pip install git+https://github.com/facebookresearch/segment-anything.git
# from segment_anything import sam_model_registry, SamPredictor

# app = FastAPI()

# # -----------------------------------------------------------------------------
# # Initialize your SAM model
# # -----------------------------------------------------------------------------
# MODEL_TYPE = "vit_h"  # or "vit_b", "vit_l", etc.
# CHECKPOINT_PATH = "./checkpoints/sam2.1_hiera_tiny.pt"  # update with your checkpoint

# sam_model = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH)
# predictor = SamPredictor(sam_model)


# # -----------------------------------------------------------------------------
# # 1) The root endpoint: returns a basic HTML form with a file input
# # -----------------------------------------------------------------------------
# @app.get("/", response_class=HTMLResponse)
# def read_form():
#     """
#     Return a simple HTML form that uploads a file to /predict.
#     """
#     return """
#     <!DOCTYPE html>
#     <html>
#     <head>
#       <title>Segment Anything Demo</title>
#     </head>
#     <body>
#       <h1>Segment Anything Demo</h1>
#       <form action="/predict" method="post" enctype="multipart/form-data">
#         <label for="file">Select an image:</label>
#         <input type="file" id="file" name="file" accept="image/*" required>
#         <button type="submit">Upload & Predict</button>
#       </form>
#     </body>
#     </html>
#     """


# # -----------------------------------------------------------------------------
# # 2) The /predict endpoint: handles the uploaded file & runs SAM
# # -----------------------------------------------------------------------------
# @app.post("/predict")
# async def predict_image(file: UploadFile = File(...)):
#     """
#     Accepts an image file and returns Segment Anything prediction data.
#     """
#     # Read the uploaded file into memory
#     contents = await file.read()

#     # Open with PIL, convert to NumPy array
#     image = Image.open(io.BytesIO(contents)).convert("RGB")
#     np_image = np.array(image)

#     # Setup the predictor
#     predictor.set_image(np_image)

#     # Example: define a single prompt point at (100, 100), label=1
#     input_point = np.array([[100, 100]])
#     input_label = np.array([1])

#     # Run prediction
#     masks, scores, logits = predictor.predict(
#         point_coords=input_point,
#         point_labels=input_label,
#         multimask_output=True
#     )

#     return {
#         "message": "Prediction complete!",
#         "scores": scores.tolist(),
#         "num_masks": len(masks)
#     }
