# import torch

# def main():
#     print("Hello from vizcom-demo!")



# def run_sam():
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     sam2_checkpoint = "sam2/checkpoints/sam2.1_hiera_large.pt"
#     model_cfg = "sam2/configs/sam2.1/sam2.1_hiera_l.yaml"

#     sam2_model = build_sam2(model_cfg, sam2_checkpoint, device=device)
#     predictor = SAM2ImagePredictor(sam2_model)
#     print('hi')


# if __name__ == "__main__":
#     main()
#     run_sam()


from replicate.client import Client

#token = 

replicate = Client(
    api_token='r8_4APDh27ImSprdIvbprIGCBdKwbkl5az0YwSaf',#os.environ["SOME_OTHER_REPLICATE_API_TOKEN"]
    headers={
        "User-Agent": "my-app/1.0"
    }
)

output = replicate.run(
    "lucataco/segment-anything-2:be7cbde9fdf0eecdc8b20ffec9dd0d1cfeace0832d4d0b58a071d993182e1be0",
    input={
        "image": "https://replicate.delivery/pbxt/LMUHQoCnNzN15MpwWLPJUVF96g3zxer6p3dNTHtVrNxqMMe0/socer.png",
        "mask_limit": 2,
        "mask_2_mask": True,
        "crop_n_layers": 1,
        "box_nms_thresh": 0.7,
        "points_per_side": 64,
        "pred_iou_thresh": 0.7,
        "multimask_output": False,
        "points_per_batch": 128,
        "min_mask_region_area": 25,
        "stability_score_offset": 0.7,
        "stability_score_thresh": 0.92,
        "crop_n_points_downscale_factor": 2
    }
)
print(output)