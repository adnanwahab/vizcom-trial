def isolate_cup_from_image():
    from sam2.build_sam import build_sam2
    from sam2.sam2_image_predictor import SAM2ImagePredictor

    import numpy as np
    import torch
    from PIL import Image
    import matplotlib.pyplot as plt

    # 1. Load model and create predictor
    sam2_checkpoint = "./checkpoints/sam2.1_hiera_base_plus.pt"
    model_cfg = "configs/sam2.1/sam2.1_hiera_b+.yaml"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    sam2_model = build_sam2(model_cfg, sam2_checkpoint, device=device)
    predictor = SAM2ImagePredictor(sam2_model)

    # 2. Load your cup image
    image_path = "../public/cup.png"
    image_pil = Image.open(image_path).convert("RGB")
    image_np = np.array(image_pil)
    predictor.set_image(image_np)

    # 3. Provide point or box prompts to isolate the cup
    input_point = np.array([[450, 300]])  # example point on the cup
    input_label = np.array([1])           # 1 = foreground
    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=True
    )

    # 4. Pick the best mask
    best_idx = np.argmax(scores)
    cup_mask = masks[best_idx]  # shape [H, W]

    # (Optional) Show the mask
    plt.figure(figsize=(6,6))
    plt.imshow(image_np)
    plt.imshow(cup_mask, alpha=0.6) 
    plt.axis('off')
    plt.show()
    print("yay image saved")



def crop_image():
    import cv2

    # Convert True/False to 0/255
    mask_255 = (cup_mask * 255).astype(np.uint8)

    # Find bounding box of the mask
    y_idxs, x_idxs = np.where(mask_255 > 0)
    y_min, y_max = y_idxs.min(), y_idxs.max()
    x_min, x_max = x_idxs.min(), x_idxs.max()

    # Crop image to bounding box
    cropped_img = image_np[y_min:y_max, x_min:x_max]
    cropped_mask = mask_255[y_min:y_max, x_min:x_max]

    # Create RGBA version (with alpha = mask)
    rgba = np.dstack([cropped_img, cropped_mask])

    # Save final alpha image
    Image.fromarray(rgba).save("cup_cropped_rgba.png")


    contours, _ = cv2.findContours(mask_255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # pick the largest contour if multiple
    largest_contour = max(contours, key=cv2.contourArea)


def generate_three_dimensional_model():
    import trimesh
    import numpy as np

    # largest_contour is of shape (N, 1, 2)
    # We want something like (N, 2) in an (x, y) format for revolve
    outline_xy = largest_contour.squeeze(1)
    # e.g. rotate around the y-axis, so interpret 'outline_xy' as (r, z),
    # meaning the distance from the center to the boundary is "r", and vertical is "z".

    # Convert bounding-box-based coordinates to a centered coordinate system
    # so revolve is around the cup's vertical axis:
    cx = (x_min + x_max)/2
    cy = (y_min + y_max)/2
    outline_rz = []
    for (x, y) in outline_xy:
        # radius from horizontal center:
        radius = x - cx
        # z from vertical center (or invert y if you want y up):
        z = -(y - cy)
        outline_rz.append([radius, z])

    outline_rz = np.array(outline_rz)

    # revolve it using trimesh
    lathe = trimesh.creation.lathe(
        polygon=outline_rz, 
        angle=None,       # revolve full 360
        segments=64       # how many steps in the revolve
    )
    # Now lathe is a 3D mesh in trimesh
    lathe.export('cup_model.obj')


#if __name__ == "main":
print('cool beans')
isolate_cup_from_image()
print('cool bean 2')