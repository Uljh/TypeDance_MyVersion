import os
import numpy as np
import cv2
from PIL import Image
import torch
from segment_anything import sam_model_registry, SamPredictor

# =========== 模型初始化 ===========

# 使用更大的模型 vit_h（更好的分割效果）
sam_checkpoint = "models/sam_vit_h_4b8939.pth"
model_type = "vit_h"

# 自动选择设备（若有 GPU 用 GPU，否则用 CPU）
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[INFO] Using device: {device}")

# 加载模型并迁移到设备
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)

predictor = SamPredictor(sam)

# =========== 工具函数 ===========

def safe_save(image: Image.Image, path: str):
    """确保目录存在后再保存图片文件。"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    image.save(path)

def resize_with_aspect(image: np.ndarray, max_side: int):
    """将 image 缩放，使其最长边为 max_side，返回缩放后的图像与缩放比例"""
    h, w = image.shape[:2]
    max_current = max(h, w)
    if max_current <= max_side:
        return image, 1.0
    scale = max_side / max_current
    new_w = int(w * scale)
    new_h = int(h * scale)
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return resized, scale

#主函数，根据点或框生成 mask。
def get_img_embedding(image, input, mode):
    """
    获取 mask（布尔数组）。支持自动降分辨率策略，避免显存不足。
    `image` 可为 numpy 数组或 PIL 图像。
    `input` 为点 coords 或 box，按缩放比例做对应变换。
    `mode` 为 "image" 或 "word"（不同分割模式）。
    """
    # 如果是 PIL 图像，转成 numpy
    if isinstance(image, Image.Image):
        image = np.array(image)

    # 自动缩放
    max_allowed = 800  # 你可以根据显存情况调整这个阈值
    image_resized, scale = resize_with_aspect(image, max_allowed)

    # 缩放 input 坐标（如果 input 是 box 或点）
    input_scaled = np.array(input) * scale

    # 清理显存
    if device == "cuda":
        torch.cuda.empty_cache()

    predictor.set_image(image_resized)

    if mode == "word":
        masks, _, _ = predictor.predict(
            point_coords=None,
            point_labels=None,
            box=input_scaled[None, :],
            multimask_output=False
        )
    elif mode == "image":
        if len(input_scaled) == 1:
            # 单点
            input_label = np.array([1])
            masks, _, _ = predictor.predict(
                point_coords=input_scaled,
                point_labels=input_label,
                multimask_output=False
            )
        else:
            input_first = np.array([input_scaled[0]])
            input_label = np.array([1])
            masks, scores, logits = predictor.predict(
                point_coords=input_first,
                point_labels=input_label,
                multimask_output=False
            )
            input_label = np.array([1] * len(input_scaled))
            mask_input = logits[np.argmax(scores), :, :]
            masks, _, _ = predictor.predict(
                point_coords=input_scaled,
                point_labels=input_label,
                mask_input=mask_input[None, :, :],
                multimask_output=False
            )
    mask = masks[0]

    # 如果做了缩放，需要把 mask 放大回原图尺寸
    if scale != 1.0:
        mask_img = Image.fromarray((mask.astype(np.uint8) * 255))
        # 放大时用 NEAREST 保留二值特性
        mask_img = mask_img.resize((image.shape[1], image.shape[0]), resample=Image.NEAREST)
        mask = np.array(mask_img) > 0

    return mask

#在原图上叠加半透明遮罩与轮廓高亮。
def highlight_mask(mask, image, mode):
    """将 mask 区域高亮叠在 image 上，返回 RGBA 图像 + 轮廓列表"""
    mask = mask.astype(np.uint8)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if mode == "image":
        cv2.drawContours(image, contours, -1, (255, 255, 255), thickness=5)
    image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    image_rgba[:, :, 3] = np.where(mask == 1, 255, 75)
    image_r = Image.fromarray(image_rgba)
    print("高亮完成")
    return image_r, contours

#将 mask 区域映射到画布上。
def img_word_to_canvas(mask, image, mode):
    """mask -> RGBA image + contours"""
    mask = mask.astype(np.uint8)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    image_rgba[:, :, 3] = np.where(mask == 1, 0, 255)
    image_r = Image.fromarray(image_rgba)
    print("映射完成")
    return image_r, contours

#输出透明背景的分割结果。
def mask_to_image(mask, image):
    """mask -> RGBA 图像，透明背景 + mask 区域不透明"""
    mask = mask.astype(np.uint8)
    image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
    image_rgba[:, :, 3] = np.where(mask == 1, 255, 0)
    image_r = Image.fromarray(image_rgba)
    print("选中字体部分已完成")
    return image_r


# =========== try it ===========
# image_path = 'truck.jpg'
# image = cv2.imread(image_path)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# input_box = np.array([425, 600, 700, 875])
# mask = get_img_embedding(image, input_box)
# image_r = highlight_mask(mask, image)
# image_r.save("see.png")
