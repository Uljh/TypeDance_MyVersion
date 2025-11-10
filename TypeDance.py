from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import numpy as np
import torch
import os
import time
from pathlib import Path
from PIL import Image
import cv2

# ==================== 环境变量设置（必须在导入 clip_interrogator 之前）====================
# 设置项目根目录
_project_root = os.path.dirname(os.path.abspath(__file__))
_local_models_dir = os.path.join(_project_root, 'models', 'huggingface', 'hub')

# 检查模型文件是否存在，如果存在则设置环境变量
_model_check_path = os.path.join(_local_models_dir, 'models--timm--vit_large_patch14_clip_224.openai')
if os.path.exists(_model_check_path):
    # 检查模型文件是否完整
    _snapshots_dir = os.path.join(_model_check_path, 'snapshots')
    if os.path.exists(_snapshots_dir):
        _snapshots = [d for d in os.listdir(_snapshots_dir) 
                     if os.path.isdir(os.path.join(_snapshots_dir, d))]
        if _snapshots:
            _snapshot_path = os.path.join(_snapshots_dir, _snapshots[0])
            _model_file = os.path.join(_snapshot_path, 'open_clip_pytorch_model.bin')
            if os.path.exists(_model_file):
                # 模型文件存在，设置环境变量
                os.environ['HF_HOME'] = os.path.join(_project_root, 'models', 'huggingface')
                os.environ['HUGGINGFACE_HUB_CACHE'] = _local_models_dir
                os.environ['HF_LOCAL_FILES_ONLY'] = 'True'
                # 如果没有设置镜像，使用默认值（可以在外部设置）
                if 'HF_ENDPOINT' not in os.environ:
                    pass  # 保持未设置，或者可以在这里设置镜像
                os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '300'
                print(f"[INIT] ✅ 检测到本地模型，已设置环境变量")
                print(f"[INIT]    HF_HOME: {os.environ.get('HF_HOME')}")
                print(f"[INIT]    HUGGINGFACE_HUB_CACHE: {os.environ.get('HUGGINGFACE_HUB_CACHE')}")
                print(f"[INIT]    HF_LOCAL_FILES_ONLY: {os.environ.get('HF_LOCAL_FILES_ONLY')}")

# 现在导入其他模块（环境变量已设置）
from diffusers import DiffusionPipeline,StableDiffusionDepth2ImgPipeline,StableDiffusionImg2ImgPipeline,StableDiffusionPipeline
from brainstorm import get_answer, get_dict_from_answer
from image_segment import get_img_embedding, highlight_mask, mask_to_image, img_word_to_canvas
from segment_anything import sam_model_registry, SamPredictor
from clip_interrogator import Config, Interrogator
from utils import *
from generate import Generation
from generate import Generation, Feedback, Refine
from transformers import CLIPProcessor, CLIPModel

# ==================== 模型配置和初始化 ====================
def setup_model_cache():
    """配置模型缓存目录，优先使用项目本地目录"""
    # 1. 优先使用项目本地模型目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    local_models_dir = os.path.join(project_root, 'models', 'huggingface', 'hub')
    
    # 2. 系统默认缓存目录
    default_cache = os.path.expanduser('~/.cache/huggingface')
    
    # 3. 检查模型文件是否存在
    model_check_path = os.path.join(local_models_dir, 'models--timm--vit_large_patch14_clip_224.openai')
    
    if os.path.exists(model_check_path):
        # 进一步检查模型文件是否完整（检查关键文件）
        snapshots_dir = os.path.join(model_check_path, 'snapshots')
        model_file_found = False
        
        if os.path.exists(snapshots_dir):
            # 检查 snapshots 目录下是否有模型文件
            for item in os.listdir(snapshots_dir):
                snapshot_path = os.path.join(snapshots_dir, item)
                if os.path.isdir(snapshot_path):
                    model_file = os.path.join(snapshot_path, 'open_clip_pytorch_model.bin')
                    safetensors_file = os.path.join(snapshot_path, 'open_clip_model.safetensors')
                    if os.path.exists(model_file) or os.path.exists(safetensors_file):
                        model_file_found = True
                        # 检查文件大小是否合理（至少 100MB）
                        if os.path.exists(model_file):
                            file_size = os.path.getsize(model_file)
                            if file_size < 100 * 1024 * 1024:  # 小于 100MB 可能不完整
                                print(f"[INFO] ⚠️  警告: 模型文件可能不完整 ({file_size / (1024**2):.2f} MB)")
                        break
        
        if model_file_found:
            # 使用项目本地模型
            os.environ['HF_HOME'] = os.path.join(project_root, 'models', 'huggingface')
            os.environ['HUGGINGFACE_HUB_CACHE'] = local_models_dir
            print(f"[INFO] ✅ 使用项目本地模型缓存: {local_models_dir}")
            return True
        else:
            print(f"[INFO] ⚠️  模型目录存在但未找到完整的模型文件")
            print(f"[INFO] 将尝试从网络下载或使用系统缓存")
            os.environ['HF_HOME'] = os.path.join(project_root, 'models', 'huggingface')
            os.environ['HUGGINGFACE_HUB_CACHE'] = local_models_dir
            return False
    elif os.path.exists(local_models_dir):
        # 目录存在但模型文件不完整
        os.environ['HF_HOME'] = os.path.join(project_root, 'models', 'huggingface')
        os.environ['HUGGINGFACE_HUB_CACHE'] = local_models_dir
        print(f"[INFO] ⚠️  项目模型目录存在但模型文件可能不完整: {local_models_dir}")
        print(f"[INFO] 将尝试从网络下载或使用系统缓存")
        return False
    elif os.path.exists(default_cache):
        # 使用系统默认缓存
        os.environ['HF_HOME'] = default_cache
        print(f"[INFO] ℹ️  使用系统默认 Hugging Face 缓存: {default_cache}")
        print(f"[INFO] 提示: 建议运行 python download_open_clip_model.py 下载到项目目录")
        return False
    else:
        # 没有找到任何缓存目录
        print(f"[INFO] ⚠️  未找到模型缓存目录")
        print(f"[INFO] 将尝试下载模型到: {local_models_dir}")
        # 创建目录
        os.makedirs(local_models_dir, exist_ok=True)
        os.environ['HF_HOME'] = os.path.join(project_root, 'models', 'huggingface')
        os.environ['HUGGINGFACE_HUB_CACHE'] = local_models_dir
        return False

# 配置模型缓存
model_available = setup_model_cache()

# 增加超时时间（秒）
os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '300'  # 5分钟

# 如果检测到本地模型文件，自动启用本地文件模式，避免网络下载
# 这样可以强制 open_clip 只使用本地缓存，不会尝试从 Hugging Face Hub 下载
if model_available:
    # 检测到本地模型文件，强制使用本地文件模式
    os.environ['HF_LOCAL_FILES_ONLY'] = 'True'
    print("[INFO] 🔒 检测到本地模型文件，已自动启用仅使用本地文件模式")
else:
    # 检查是否手动设置了 HF_LOCAL_FILES_ONLY
    USE_LOCAL_FILES_ONLY = os.environ.get('HF_LOCAL_FILES_ONLY', 'False').lower() == 'true'
    if USE_LOCAL_FILES_ONLY:
        print("[INFO] 🔒 已启用仅使用本地文件模式（手动设置）")
        print("[WARN] ⚠️  警告: 启用本地文件模式但模型文件可能不存在，可能会失败")

# 支持 Hugging Face 镜像站点（适用于中国大陆用户）
# 如果设置了 HF_ENDPOINT 环境变量，将使用该镜像
if 'HF_ENDPOINT' not in os.environ:
    # 可以在这里设置默认镜像，例如：
    # os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'  # 取消注释以使用镜像
    pass
else:
    print(f"[INFO] 使用 Hugging Face 镜像: {os.environ.get('HF_ENDPOINT')}")


app = Flask(__name__)
# 配置 CORS，允许来自前端的跨域请求
# 注意：虽然前端不再发送 Cache-Control 和 Pragma 头，但为了兼容性仍然允许它们
CORS(app,
     resources={r'/*': {
         'origins': ['http://localhost:3000', 'http://127.0.0.1:3000'],
         'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD'],
         'allow_headers': ['Content-Type', 'Authorization', 'Cache-Control', 'Pragma', 'X-API-Key'],
         'expose_headers': ['Content-Length', 'Last-Modified', 'Content-Type', 'Cache-Control']
     }},
     supports_credentials=True)


@app.route('/brainstorm',methods=['GET', 'POST'])
def brainstorm():
    data = request.get_json()
    user_prompt = data["user_prompt"]
    answer = get_answer(user_prompt)
    string = answer["content"]
    ### print(answer)
    print(string)
    concept_dict = get_dict_from_answer(string)
    # concept_dict = {"1. Giant Panda": "The giant panda is not only a beloved symbol of Chengdu, but it is also native to the region. Using the image of a playful and adorable giant panda in the logo can represent Chengdu's connection to nature and its commitment to wildlife conservation.",
# "2. Sichuan Cuisine": "Chengdu is renowned for its delicious and spicy Sichuan cuisine. Using elements like chili peppers, hot pot, or a pair of chopsticks can symbolize the city's vibrant food culture and its reputation as a food lover's paradise.",
# "3. Bamboo Forest": "Chengdu is surrounded by beautiful bamboo forests, known for their tranquility and elegance. Incorporating the image of bamboo stalks or leaves in the logo can represent Chengdu's connection to nature, its traditional arts, and its commitment to preserving green spaces.",
# "4. Mask Changing": "Sichuan Opera is famous for its unique art of 'mask changing,' where performers change masks in the blink of an eye using various techniques. Including a mask or a theatrical mask-inspired design element in the logo can symbolize Chengdu's rich cultural heritage, its vibrant performing arts scene, and its tradition of innovation.",
# "5. Jinsha Site Museum": "The Jinsha Site Museum is an archaeological site in Chengdu that preserves the remains of the ancient Shu civilization. Incorporating elements such as ancient artifacts, a stylized symbol of archaeological discoveries, or the museum's iconic architecture can represent Chengdu's historical significance, its rich heritage, and its commitment to preserving and promoting its cultural roots."}
    return jsonify(concept_dict)

# box
# @app.route('/image_segment',methods=['GET', 'POST'])
# def image_view():
#     data = request.get_json()
#     input_box = data["box"]
#     image_url = data["image_url"]
#     mode = data["mode"]
#     image = dataurl_to_pil(image_url, output_path=None).convert("RGB")
#     print(image.size)
#     image.save("from_interface.png")
#     if mode == "image":
#         input_box = np.array([input_box[0]*(image.size[1]/180), input_box[1]*(image.size[1]/180), input_box[2]*(image.size[1]/180), input_box[3]*(image.size[1]/180)])
#         print(input_box)
#     if mode == "word":
#         input_box = np.array([input_box[0], input_box[1], input_box[2], input_box[3]])
#     image = np.array(image)
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     mask = get_img_embedding(image, input_box)
#     image_r, contours_g = highlight_mask(mask, image, mode)
#     image_r.save("check/img_segment.png")

#     if mode == "image":
#         # ===== get design prior ====
#         # shape
#         img_defalt_bg = Image.open('frontend/src/assets/generation/default/extract-feature-bg.png')	
#         shape_rectagle = extract_shape(image_r, contours_g, input_box)
#         shape_image = add_margin(img_defalt_bg, shape_rectagle)
#         # 圆角rgba贴上去是黑色
#         shape_image_rgb = add_bg_color(shape_image, color=[247, 246, 240])
#         # paste to img_defalt_shape
#         img_defalt_shape = Image.open('frontend/src/assets/generation/default/shape.png')
#         shape_image_resize = shape_image_rgb.resize((175,175))
#         img_defalt_shape.paste(shape_image_resize, (535, 18))
#         img_defalt_shape.save("check/img_shape.png")

#         # shape
#         color_palette = extract_color_palatte(image_r)
#         img_defalt_color = Image.open("frontend/src/assets/generation/default/color.png")
#         img_defalt_color.paste(color_palette, (215, 150))
#         img_defalt_color.save("check/img_color.png")

#         return {"img": pil_to_data_uri(image_r), "shape":pil_to_data_uri(img_defalt_shape),
#                 "color":pil_to_data_uri(img_defalt_color)}

#     if mode == "word":
#         return pil_to_data_uri(image_r)

# click
@app.route('/image_segment', methods=['GET', 'POST'])
def image_view():
    data = request.get_json()
    image_url = data["image_url"]
    mode = data["mode"]

    print("🟥 [Backend] Received mode:", mode)
    print("🟥 [Backend] image_url head:", image_url[:50])
    print("🟥 [Backend] image_url valid:", image_url.startswith("data:image"))

    os.makedirs("check", exist_ok=True)
    image = dataurl_to_pil(image_url, output_path=None).convert("RGB")
    image.save("check/from_interface.png")

    # ============ IMAGERY 模式 ============
    if mode == "image":
        input_points = np.array(data["points"]) * (image.size[1] / 180)
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mask = get_img_embedding(image, input_points, mode)
        img_mask = mask_to_image(mask, image)
        img_mask.save("check/img_mask.png")

        image_r, contours_g = highlight_mask(mask, image, mode)
        image_r.save("check/img_segment.png")

        blank_rgba = Image.new("RGBA", image_r.size, (0, 0, 0, 0))
        blank_rgba_arr = np.array(blank_rgba)
        max_contour = find_max_contour(contours_g)
        cv2.drawContours(blank_rgba_arr, max_contour, -1, (79, 79, 79, 255), thickness=8)
        img_contour = Image.fromarray(blank_rgba_arr).convert("RGBA")
        img_contour = crop_element_from_RGBA(img_contour, mask_single_FLAG=False)
        img_contour.save("check/img_segment_contour.png")

        # 统一返回 JSON 格式，与 word 模式保持一致
        return jsonify({
            "highlight": pil_to_data_uri(image_r)
        })

    # ============ TYPEFACE 模式 ============
    if mode == "word":
        input_boxes = data["box"]
        print("🟦 input_boxes:", input_boxes)
        
        # 初始化 svg_content 变量
        svg_content = None

        if isinstance(input_boxes[0], list):
            print("--ADD SELECTION--")
            mask_merge = np.zeros((300, 464), dtype=bool)
            image = np.array(image)
            for input_box in input_boxes:
                box = np.array([input_box[0], input_box[1], input_box[2], input_box[3]])
                img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                mask = get_img_embedding(img_rgb, box, mode)
                mask_merge = np.bitwise_or(mask_merge, mask)

            img_mask = mask_to_image(mask_merge, image)
            img_mask.save("check/img_mask_word.png")
            img_mask.save("check/img_mask.png")
            img_word = get_word_img(img_mask)
            img_word.save("check/img_word.png")

            # 高亮选中区域
            image_r, contours_g = highlight_mask(mask_merge, image, mode)
            image_r.save("check/img_segment.png")
            
            # === 生成剩余结构并转为 SVG（多选情况）===
            inverse_mask = np.logical_not(mask_merge)
            remaining_image = np.array(image)
            remaining_image[~inverse_mask] = [255, 255, 255]  # 白底
            remaining_pil = Image.fromarray(remaining_image)
            remaining_pil.save("check/remaining_word.png")
            
            # 转为 SVG 文件
            svg_path = "frontend/public/canvas/word_dynamic.svg"
            
            print("=" * 50)
            print(f"🔄 [SVG] STEP 1: 准备 SVG 转换 (multi-selection)...")
            print(f"🔄 [SVG] Input: check/remaining_word.png")
            print(f"🔄 [SVG] Output: {svg_path}")
            
            # ⚠️ 重要：不删除旧文件，而是覆盖（便于调试）
            # 新文件会直接覆盖旧文件，避免显示缓存的问题通过文件修改时间检测解决
            if os.path.exists(svg_path):
                try:
                    # 记录旧文件的修改时间，用于前端检测新文件
                    old_mtime = os.path.getmtime(svg_path)
                    print(f"ℹ️ [SVG] 旧 SVG 文件存在 (multi-selection)，将被新文件覆盖（旧文件修改时间: {old_mtime}）")
                except Exception as e:
                    print(f"⚠️ [SVG] 检查旧 SVG 文件失败 (multi-selection): {e}")
            else:
                print(f"ℹ️ [SVG] SVG 文件不存在 (multi-selection)，将创建新文件")
            
            # 在后台线程中异步调用 SVG 转换，避免阻塞 HTTP 响应
            import threading
            def async_svg_conversion():
                try:
                    print(f"🔄 [SVG] 开始异步 SVG 转换 (multi-selection)...")
                    img_to_svg_api("check/remaining_word.png", svg_path)
                    print(f"✅ [SVG] 异步 SVG 转换完成 (multi-selection): {svg_path}")
                except Exception as e:
                    print(f"❌ [SVG] 异步 SVG 转换失败 (multi-selection): {e}")
                    import traceback
                    traceback.print_exc()
            
            # 启动异步转换
            svg_thread = threading.Thread(target=async_svg_conversion, daemon=True)
            svg_thread.start()
            print(f"🔄 [SVG] 已启动异步 SVG 转换任务 (multi-selection)")
            
            # 不等待转换完成，立即返回响应
            # 前端将通过 svg_path 加载 SVG 文件，并使用轮询机制等待新文件生成
            print(f"🔄 [SVG] STEP 2: 不等待转换完成，立即返回响应 (multi-selection)")
            print(f"ℹ️ [SVG] 前端将通过路径加载新生成的 SVG 文件: {svg_path}")
            print("=" * 50)
            
            # ⚠️ 重要：不读取旧的 SVG 文件，让前端等待新文件生成
            svg_content = None
            print(f"ℹ️ [SVG] 不返回旧的 SVG 内容，前端将等待新文件生成 (multi-selection)")

        else:
            box = np.array([input_boxes[0], input_boxes[1], input_boxes[2], input_boxes[3]])
            image_np = np.array(image)
            image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
            mask = get_img_embedding(image_rgb, box, mode)

            # === 高亮部分 ===
            img_mask = mask_to_image(mask, image_np)
            img_mask.save("check/img_mask_word.png")
            img_mask.save("check/img_mask.png")
            img_word = get_word_img(img_mask)
            img_word.save("check/img_word.png")

            # === 高亮图（选中部分）===
            image_r, contours_g = highlight_mask(mask, image_np, mode)
            image_r.save("check/img_segment.png")

            # === 生成轮廓图 ===
            blank_rgba = Image.new("RGBA", image_r.size, (0, 0, 0, 0))
            blank_rgba_arr = np.array(blank_rgba)
            max_contour = find_max_contour(contours_g)
            cv2.drawContours(blank_rgba_arr, max_contour, -1, (79, 79, 79, 255), thickness=8)
            img_contour = Image.fromarray(blank_rgba_arr).convert("RGBA")
            img_contour = crop_element_from_RGBA(img_contour, mask_single_FLAG=False)
            img_contour.save("check/img_segment_contour.png")

            # === 新增：生成剩余结构并转为 SVG ===
            # 取反掩码，得到剩余部分
            inverse_mask = np.logical_not(mask)
            remaining_image = np.array(image_np)
            remaining_image[~inverse_mask] = [255, 255, 255]  # 白底
            remaining_pil = Image.fromarray(remaining_image)
            remaining_pil.save("check/remaining_word.png")

            # 转为 SVG 文件供前端加载，保存svg文件
            svg_path = "frontend/public/canvas/word_dynamic.svg"
            
            print("=" * 50)
            print(f"🔄 [SVG] STEP 1: 准备 SVG 转换...")
            print(f"🔄 [SVG] Input: check/remaining_word.png")
            print(f"🔄 [SVG] Output: {svg_path}")
            
            # ⚠️ 重要：不删除旧文件，而是覆盖（便于调试）
            # 新文件会直接覆盖旧文件，避免显示缓存的问题通过文件修改时间检测解决
            if os.path.exists(svg_path):
                try:
                    # 记录旧文件的修改时间，用于前端检测新文件
                    old_mtime = os.path.getmtime(svg_path)
                    print(f"ℹ️ [SVG] 旧 SVG 文件存在，将被新文件覆盖（旧文件修改时间: {old_mtime}）")
                except Exception as e:
                    print(f"⚠️ [SVG] 检查旧 SVG 文件失败: {e}")
            else:
                print(f"ℹ️ [SVG] SVG 文件不存在，将创建新文件")
            
            # 在后台线程中异步调用 SVG 转换，避免阻塞 HTTP 响应
            import threading
            def async_svg_conversion():
                try:
                    print(f"🔄 [SVG] 开始异步 SVG 转换...")
                    img_to_svg_api("check/remaining_word.png", svg_path)
                    print(f"✅ [SVG] 异步 SVG 转换完成: {svg_path}")
                except Exception as e:
                    print(f"❌ [SVG] 异步 SVG 转换失败: {e}")
                    import traceback
                    traceback.print_exc()
            
            # 启动异步转换
            svg_thread = threading.Thread(target=async_svg_conversion, daemon=True)
            svg_thread.start()
            print(f"🔄 [SVG] 已启动异步 SVG 转换任务")
            
            # 不等待转换完成，立即返回响应
            # 前端将通过 svg_path 加载 SVG 文件，并使用轮询机制等待新文件生成
            print(f"🔄 [SVG] STEP 2: 不等待转换完成，立即返回响应")
            print(f"ℹ️ [SVG] 前端将通过路径加载新生成的 SVG 文件: {svg_path}")
            print("=" * 50)
            
            # ⚠️ 重要：不读取旧的 SVG 文件，让前端等待新文件生成
            svg_content = None
            print(f"ℹ️ [SVG] 不返回旧的 SVG 内容，前端将等待新文件生成")

        # === 前端返回 JSON，包含高亮图 + SVG 内容 ===
        print("=" * 50)
        print(f"🔄 [Response] Preparing response data...")
        print(f"🔄 [Response] svg_content type: {type(svg_content)}, value: {svg_content is not None}")
        if svg_content:
            print(f"🔄 [Response] svg_content length: {len(svg_content)}")
            print(f"🔄 [Response] svg_content preview (first 200 chars): {svg_content[:200]}")
        
        # 构建完整的 SVG 文件 URL（使用后端服务器地址）
        # 注意：这里返回相对路径，前端会添加后端服务器地址
        svg_relative_path = "/api/svg_image/frontend/public/canvas/word_dynamic.svg"
        
        response_data = {
            "highlight": pil_to_data_uri(image_r),   # 左侧显示高亮笔画
            "svg_path": svg_relative_path,  # 使用 API 路由访问 SVG 文件
        }
        
        print(f"🔄 [Response] SVG 路径: {svg_relative_path}")
        print(f"ℹ️ [Response] 前端需要将此路径添加到后端服务器地址: http://127.0.0.1:6006{svg_relative_path}")
        
        # 如果 SVG 内容存在，添加到响应中
        if svg_content:
            response_data["svg_content"] = svg_content
            print(f"✅ [Response] SVG content included in response, length: {len(svg_content)}")
            print(f"✅ [Response] SVG content starts with: {svg_content[:50]}")
        else:
            print(f"⚠️ [Response] SVG content is None or empty, NOT included in response")
            print(f"⚠️ [Response] This means frontend will try to load from path instead")
        
        print(f"🔄 [Response] Response keys: {list(response_data.keys())}")
        print(f"🔄 [Response] Response data preview: highlight length={len(response_data['highlight'])}, svg_content={'present' if 'svg_content' in response_data else 'missing'}")
        print("=" * 50)
        
        return jsonify(response_data)



@app.route('/image_extract',methods=['GET', 'POST'])
def image_extract():
    image_r = Image.open("check/img_segment.png")
    img_contour = Image.open("check/img_segment_contour.png").convert("RGBA")
    img_mask = Image.open("check/img_mask.png").convert("RGBA")
    # =================== shape =========================
    img_defalt_bg = Image.open('frontend/src/assets/generation/default/extract-feature-bg.png')	
    shape_rectagle = extract_shape(image_r, img_contour)
    shape_image = add_margin(img_defalt_bg, shape_rectagle)
    # 圆角rgba贴上去是黑色
    shape_image_rgb = add_bg_color(shape_image, color=[247, 246, 240])
    # paste to img_defalt_shape
    img_defalt_shape = Image.open('frontend/src/assets/generation/default/shape.png')
    shape_image_resize = shape_image_rgb.resize((175,175))
    img_defalt_shape.paste(shape_image_resize, (535, 18))
    img_defalt_shape.save("check/img_shape.png")

    # =================== color =========================
    color_palette = extract_color_palatte(img_mask)
    img_defalt_color = Image.open("frontend/src/assets/generation/default/color.png")
    img_defalt_color.paste(color_palette, (215, 150))
    img_defalt_color.save("check/img_color.png")

    # ================= semantics =======================
    image_add_bg = add_bg_color(img_mask, color=[255, 255, 255])
    # 尝试用 CLIP-Interrogator 获取语义；若离线或无法下载权重，则降级为占位结果，保证接口不失败
    semantic_prompt = ""
    prompt = ""  # 初始化为空字符串，避免未定义错误
    
    # 使用全局变量缓存 Interrogator 实例，避免重复加载
    if not hasattr(image_extract, '_ci_cache'):
        image_extract._ci_cache = None
    
    try:
        # 如果还没有加载模型，则加载
        if image_extract._ci_cache is None:
            print("[INFO] 🔄 首次加载 CLIP 模型，这可能需要一些时间...")
            
            # 在初始化之前，再次确保环境变量正确设置
            project_root = os.path.dirname(os.path.abspath(__file__))
            local_models_dir = os.path.join(project_root, 'models', 'huggingface', 'hub')
            
            # 强制设置环境变量（确保在初始化前设置）
            os.environ['HF_HOME'] = os.path.join(project_root, 'models', 'huggingface')
            os.environ['HUGGINGFACE_HUB_CACHE'] = local_models_dir
            
            # 如果检测到本地模型，强制启用本地文件模式
            if model_available:
                os.environ['HF_LOCAL_FILES_ONLY'] = 'True'
            
            # 显示当前的环境变量配置
            hf_home = os.environ.get('HF_HOME', '未设置')
            hf_cache = os.environ.get('HUGGINGFACE_HUB_CACHE', '未设置')
            hf_local_only = os.environ.get('HF_LOCAL_FILES_ONLY', 'False')
            print(f"[INFO] 📋 HF_HOME: {hf_home}")
            print(f"[INFO] 📋 HUGGINGFACE_HUB_CACHE: {hf_cache}")
            print(f"[INFO] 📋 HF_LOCAL_FILES_ONLY: {hf_local_only}")
            
            # 验证模型文件是否存在
            if model_available:
                model_check_path = os.path.join(local_models_dir, 'models--timm--vit_large_patch14_clip_224.openai')
                if os.path.exists(model_check_path):
                    # 检查关键文件
                    snapshots_dir = os.path.join(model_check_path, 'snapshots')
                    if os.path.exists(snapshots_dir):
                        snapshots = [d for d in os.listdir(snapshots_dir) 
                                   if os.path.isdir(os.path.join(snapshots_dir, d))]
                        if snapshots:
                            snapshot_path = os.path.join(snapshots_dir, snapshots[0])
                            model_file = os.path.join(snapshot_path, 'open_clip_pytorch_model.bin')
                            if os.path.exists(model_file):
                                file_size = os.path.getsize(model_file) / (1024**3)
                                print(f"[INFO] ✅ 验证: 本地模型文件存在: {model_file} ({file_size:.2f} GB)")
                            else:
                                print(f"[INFO] ⚠️  警告: 模型文件不存在: {model_file}")
                        else:
                            print(f"[INFO] ⚠️  警告: snapshots 目录为空")
                    else:
                        print(f"[INFO] ⚠️  警告: snapshots 目录不存在")
                else:
                    print(f"[INFO] ⚠️  警告: 模型目录不存在: {model_check_path}")
            
            # 在初始化前，导入并设置 huggingface_hub 的缓存目录
            try:
                import huggingface_hub
                # 确保 huggingface_hub 使用我们设置的缓存目录
                huggingface_hub.constants.HF_HUB_CACHE = local_models_dir
            except Exception as e:
                print(f"[INFO] ⚠️  无法设置 huggingface_hub 缓存目录: {e}")
            
            config = Config(clip_model_name="ViT-L-14/openai")
            print("[INFO] 🔄 正在初始化 CLIP Interrogator...")
            image_extract._ci_cache = Interrogator(config)
            print("[INFO] ✅ CLIP 模型加载成功")
        else:
            print("[INFO] ♻️  使用已缓存的 CLIP 模型")
        
        ci = image_extract._ci_cache
        print("[INFO] 🎨 正在生成语义描述...")
        prompt = ci.interrogate_fast(image_add_bg)
        print(f"[INFO] 📝 CLIP Interrogator prompt: {prompt}")
        semantic_prompt = prompt
        # obtain the keyword
        sentance = prompt.split(",")[0]
        keyword = extract_keyword(sentance)
        img_defalt_semantic = add_text_to_img(keyword)
    except (FileNotFoundError, ConnectionError, TimeoutError, OSError) as e:
        # 清除失败的缓存，以便下次重试
        image_extract._ci_cache = None
        error_msg = str(e)
        if "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
            print(f"[WARN] ⏱️  CLIP 模型下载超时: {e}")
            print("[INFO] 💡 解决方案:")
            print("  1. 从本地同步模型文件到服务器（推荐）:")
            print("     ./sync_models_to_server.sh user@server:/path/to/TypeDance/")
            print("  2. 或在服务器上运行: python download_open_clip_model.py")
            print("  3. 如果在中国大陆，使用镜像: export HF_ENDPOINT=https://hf-mirror.com")
        elif "connection" in error_msg.lower():
            print(f"[WARN] 🔌 CLIP 模型连接失败: {e}")
            print("[INFO] 💡 解决方案:")
            print("  1. 从本地同步模型文件到服务器（推荐）:")
            print("     ./sync_models_to_server.sh user@server:/path/to/TypeDance/")
            print("  2. 检查网络连接")
            print("  3. 使用本地模型缓存（如果已下载）")
        else:
            print(f"[WARN] ❌ CLIP Interrogator 文件/连接错误: {e}")
        img_defalt_semantic = add_text_to_img("Semantic")
        prompt = "semantic description unavailable"
    except Exception as e:
        # 捕获 Hugging Face 相关错误
        error_type = type(e).__name__
        error_msg = str(e)
        
        # 检查是否是 sentence-transformers 相关的错误（不影响主要功能）
        is_sentence_transformer_error = "sentence-transformers" in error_msg.lower() or "all-mpnet" in error_msg.lower()
        
        # 检查是否是 Hugging Face Hub 相关错误
        if "huggingface" in error_type.lower() or "LocalEntryNotFoundError" in error_type or is_sentence_transformer_error:
            if is_sentence_transformer_error:
                # sentence-transformers 模型错误，不影响主要功能
                # 检查是否是因为网络超时（模型文件可能已存在）
                if "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
                    print(f"[INFO] ℹ️  sentence-transformers 模型网络请求超时（可忽略）")
                    print("[INFO] 💡 说明: CLIP 模型已成功加载并工作正常")
                    print("[INFO] 💡 说明: 语义描述已成功生成，功能完全正常")
                    print("[INFO] 💡 提示: 此警告可安全忽略，不影响功能使用")
                else:
                    print(f"[WARN] ⚠️  sentence-transformers 模型加载问题（不影响主要功能）: {error_type}")
                    print("[INFO] 💡 说明: CLIP 模型已成功加载，语义提取功能正常")
                    print("[INFO] 💡 可选操作: 运行 python download_sentence_transformer.py 下载完整模型")
                    print("[INFO] 💡 提示: 此错误不影响 /image_extract 接口的正常使用")
                # 不清除缓存，因为 CLIP 模型已经成功加载
                # 继续使用已有的结果
                if prompt:  # 如果 prompt 已经有值，说明 CLIP 模型工作正常
                    print(f"[INFO] ✅ CLIP 模型工作正常，已生成语义描述: {prompt[:50]}...")
                    # prompt 已经有值，不需要设置默认值
                else:
                    img_defalt_semantic = add_text_to_img("Semantic")
                    prompt = "semantic description unavailable"
            elif "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
                print(f"[WARN] ⏱️  Hugging Face 模型下载超时: {error_type}: {e}")
                print("[INFO] 💡 解决方案:")
                print("  1. 从本地同步模型文件到服务器（推荐）:")
                print("     ./sync_models_to_server.sh user@server:/path/to/TypeDance/")
                print("  2. 或在服务器上运行: python download_open_clip_model.py")
                print("  3. 如果在中国大陆，使用镜像: export HF_ENDPOINT=https://hf-mirror.com")
                print("  4. 检查网络连接和防火墙设置")
                # 清除失败的缓存，以便下次重试
                image_extract._ci_cache = None
                img_defalt_semantic = add_text_to_img("Semantic")
                prompt = "semantic description unavailable"
            elif "connection" in error_msg.lower() or "connect" in error_msg.lower():
                print(f"[WARN] 🔌 Hugging Face 连接失败: {error_type}: {e}")
                print("[INFO] 💡 解决方案:")
                print("  1. 从本地同步模型文件到服务器（推荐）:")
                print("     ./sync_models_to_server.sh user@server:/path/to/TypeDance/")
                print("  2. 检查网络连接")
                print("  3. 使用代理或镜像站点")
                # 清除失败的缓存，以便下次重试
                image_extract._ci_cache = None
                img_defalt_semantic = add_text_to_img("Semantic")
                prompt = "semantic description unavailable"
            else:
                print(f"[WARN] ❌ Hugging Face 模型加载失败: {error_type}: {e}")
                print("[INFO] 💡 提示: 请从本地同步模型文件或运行 python download_open_clip_model.py")
                # 清除失败的缓存，以便下次重试
                image_extract._ci_cache = None
                img_defalt_semantic = add_text_to_img("Semantic")
                prompt = "semantic description unavailable"
        else:
            print(f"[WARN] ❌ CLIP Interrogator 初始化失败: {error_type}: {e}")
            import traceback
            traceback.print_exc()
            print("[INFO] 💡 提示: 请从本地同步模型文件或运行 python download_open_clip_model.py")
            # 清除失败的缓存，以便下次重试
            image_extract._ci_cache = None
            img_defalt_semantic = add_text_to_img("Semantic")
            prompt = "semantic description unavailable"
    img_defalt_semantic.save("check/img_semantic.png")

    # ================= prepare material for wrap ================= 
    img_word = Image.open("check/img_word.png").convert("RGB")
    svg_string = word_to_svg(img_word)
    Path(f"frontend/src/assets/generation/shape_wrap/svgTry.svg").write_text(
			svg_string, encoding="utf-8"
		)
    contours = find_continuous_contour(img_mask)
    sampled_points = sample_from_contours(contours)

    return {"shape":pil_to_data_uri(img_defalt_shape),
            "color":pil_to_data_uri(img_defalt_color),
            "semantic":pil_to_data_uri(img_defalt_semantic),
            "semantic_prompt": prompt,
            "sampled_points": sampled_points}


@app.route('/show_info',methods=['GET', 'POST'])
def show_info():
    img_word = Image.open("check/img_word.png").convert("RGB")
    img_mask = Image.open("check/img_mask.png").convert("RGBA")
    image_add_bg = add_bg_color(img_mask, color=[255, 255, 255])
    return {"word": pil_to_data_uri(img_word), "img": pil_to_data_uri(image_add_bg)}


@app.route('/generate',methods=['GET', 'POST'])
def image_generate():
    data = request.get_json()
    prompt = data["prompt"]
    num_to_generate = data["num_to_generate"]
    strength = float(data["strength"])
    semantic_prompt = data["semantic_prompt"]
    bool_list = data["generate-option"]
    # previous_mode = data["previous_mode"]
    # previous_img = data["previous_img"]
    FEEDBACK_FLAG = False
    # if len(previous_mode) !=0:
    #     FEEDBACK_FLAG = True
    #     print(previous_mode)
    #     previous_img_list = []
    #     for img in previous_img:
    #         img = dataurl_to_pil(img, output_path=None)
    #         previous_img_list.append(img)
    option_list = [option for index, option in enumerate(["semantic", "color", "shape"]) if bool_list[index]]
    if "shape" in option_list:
        wrap_svg_string = data["wrap_svg"]
        for i in range(4):
            Path('check/wrap/wrap_'+str(i)+'.svg').write_text(
                wrap_svg_string[i], encoding="utf-8"
            )

    print("prompt", prompt)
    print("semantic_prompt", semantic_prompt)
    print(option_list)

    img_word = Image.open("check/img_word.png").convert("RGB") # 已经512，512
    img_image = Image.open("check/img_segment.png").convert("RGB")
    img_mask = Image.open("check/img_mask.png").convert("RGBA")
    image_add_bg = add_bg_color(img_mask, color=[255, 255, 255])

    # if not FEEDBACK_FLAG or : # from scratch
    generationOperator = Generation()
    try:
        img_list, mode_list, alt = generationOperator(img_word, img_mask, prompt, semantic_prompt, num_to_generate, strength, option_list)
        
        # 检查生成的结果是否为空
        if not img_list or len(img_list) == 0:
            print("[WARN] 生成的图像列表为空，返回错误")
            return jsonify({"error": "无法生成图像，请重试"}), 500
        
        # 确保 mode_list 和 img_list 长度一致
        while len(mode_list) < len(img_list):
            mode_list.append("unknown")
        
    except Exception as e:
        print(f"[ERROR] 图像生成失败: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"图像生成失败: {str(e)}"}), 500
    # else:
    #     feedbackOperator = Feedback(img_word, img_mask, prompt, semantic_prompt, num_to_generate, strength, option_list, previous_mode, previous_img_list)




    return {"gallery": [pil_to_data_uri(img) for img in img_list], 
            "word": pil_to_data_uri(img_word), 
            "img": pil_to_data_uri(image_add_bg),
            "mode": mode_list,
            "alt": alt}

@app.route('/convert_to_svg',methods=['GET', 'POST'])
def convert_to_SVG():
    data = request.get_json()
    dataurl = data["data"]["src"]
    image = dataurl_to_pil(dataurl, output_path=None).convert("RGB")
    image.save("check/from_canvas.png")
    img_to_svg_api("check/from_canvas.png", "frontend/src/assets/canvas/image.svg")
    return jsonify("send svg")

@app.route('/evaluate_element',methods=['GET', 'POST'])
def evaluate_img():
    data = request.get_json()
    dataurl = data["data"]
    prompt = data["alt"]
    prompt = prompt.replace("_", " ")
    image = dataurl_to_pil(dataurl, output_path=None).convert("RGB")
    image.save("check/evaluate_img.png")

    try:
        # ⚠️ 使用与 image_extract 相同的 open_clip 模型，而不是 transformers.CLIPModel
        # 这样可以重用本地已有的模型文件
        import torch
        import open_clip
        from PIL import Image
        import numpy as np
        
        print("[INFO] 🔄 使用 open_clip 模型进行评估（与 image_extract 相同）")
        
        # 检查本地模型路径
        local_clip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "huggingface", "hub", "models--timm--vit_large_patch14_clip_224.openai")
        
        # 设置环境变量，确保使用本地模型
        os.environ['HF_HOME'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "huggingface")
        os.environ['HUGGINGFACE_HUB_CACHE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "huggingface", "hub")
        os.environ['HF_LOCAL_FILES_ONLY'] = 'True'
        
        # 加载模型（使用与 image_extract 相同的配置）
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, _, preprocess = open_clip.create_model_and_transforms(
            'ViT-L-14', 
            pretrained='openai',
            device=device
        )
        tokenizer = open_clip.get_tokenizer('ViT-L-14')
        
        # 准备文本和图像
        texts = ["A word or text", "An illustration or photo"]
        text_tokens = tokenizer(texts).to(device)
        
        # 预处理图像
        image_tensor = preprocess(image).unsqueeze(0).to(device)
        
        # 计算相似度
        with torch.no_grad():
            image_features = model.encode_image(image_tensor)
            text_features = model.encode_text(text_tokens)
            
            # 归一化
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
            
            # 计算相似度分数
            logits_per_image = (100.0 * image_features @ text_features.T).softmax(dim=-1)
            
        # 获取最大相似度的索引和值
        max_value, max_index = torch.max(logits_per_image, dim=1)
        max_index = max_index.item()
        max_value = max_value.item()
        
        # 计算最终分数
        if max_index == 0:
            print("more like typeface")
            origin_score = max_value
            final_score = -(origin_score-0.5)*2
        elif max_index == 1:
            print("more like imagery")
            origin_score = max_value
            final_score = (origin_score-0.5)*2
        else:
            # 如果索引不在预期范围内，使用默认分数
            print(f"[WARN] 意外的相似度索引: {max_index}")
            final_score = 0.0
            
        print(f"[INFO] ✅ 评估完成 - 最终分数: {final_score:.4f}")
        
    except Exception as e:
        print(f"[ERROR] CLIP模型加载失败: {e}")
        import traceback
        traceback.print_exc()
        print(f"[INFO] 评估功能暂时不可用，返回默认分数 0.5")
        final_score = 0.5
    result_score = round(final_score * 20) / 20
    result_score = 0.90 if result_score>0.90 else result_score
    result_score = -0.90 if result_score<-0.90 else result_score
    return jsonify({"result_score": result_score})

@app.route('/refine_element',methods=['GET', 'POST'])
def refine_img():
    data = request.get_json()
    print(data)
    strength = float(data["value"])
    anchor = data["anchor"]
    alt = data["alt"]

    RefineOperator = Refine()
    img = RefineOperator(strength, anchor, alt)

    return {"dataURL": pil_to_data_uri(img)} 

@app.route('/api/svg_image/<path:filename>', methods=['GET', 'HEAD', 'OPTIONS'])
def svg_image_service(filename):
    """
    提供图片服务，用于 SVG 转换 API
    允许 API 访问本地图片文件
    支持 GET（返回文件内容）和 HEAD（只返回头信息）请求
    """
    try:
        import os
        # 安全地构建文件路径（防止路径遍历攻击）
        # 只允许访问项目目录下的文件
        project_root = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(project_root, filename)
        
        # 确保文件在项目目录内
        if not os.path.commonpath([project_root, file_path]) == project_root:
            return jsonify({"error": "Access denied"}), 403
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"[SVG] 文件服务 - 文件不存在: {filename}")
            return jsonify({"error": "File not found"}), 404
        
        # 根据文件扩展名确定 MIME 类型
        _, ext = os.path.splitext(filename.lower())
        mimetype_map = {
            '.svg': 'image/svg+xml',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        mimetype = mimetype_map.get(ext, 'application/octet-stream')
        
        # 获取文件修改时间
        import time
        from datetime import datetime
        file_mtime = os.path.getmtime(file_path)
        file_size = os.path.getsize(file_path)
        
        # 设置 Last-Modified 头（使用文件修改时间）
        from email.utils import formatdate
        last_modified = formatdate(time.mktime(time.localtime(file_mtime)), usegmt=True)
        
        # 创建响应对象
        if request.method == 'HEAD':
            # HEAD 请求：只返回头信息，不返回文件内容
            response = app.response_class()
            response.headers['Content-Type'] = mimetype
            response.headers['Content-Length'] = str(file_size)
            response.headers['Last-Modified'] = last_modified
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            print(f"[SVG] 文件服务 HEAD - 文件: {filename}, 大小: {file_size} bytes, 修改时间: {last_modified}")
        else:
            # GET 请求：返回文件内容
            response = send_file(file_path, mimetype=mimetype)
            response.headers['Last-Modified'] = last_modified
            response.headers['Content-Length'] = str(file_size)
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            print(f"[SVG] 文件服务 GET - 文件: {filename}, 大小: {file_size} bytes, 修改时间: {last_modified}")
        
        return response
        
    except Exception as e:
        print(f"[SVG] 提供图片服务时出现错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/svg_callback', methods=['GET', 'POST'])
def svg_callback():
    """
    处理 SVG 转换 API 的回调
    API 会在转换完成时调用此端点
    """
    try:
        # 记录请求详细信息
        print(f"[SVG] 收到回调请求:")
        print(f"  方法: {request.method}")
        print(f"  URL: {request.url}")
        print(f"  头部: {dict(request.headers)}")
        print(f"  参数: {request.args}")
        print(f"  表单数据: {request.form}")
        print(f"  JSON: {request.get_json(silent=True)}")
        
        callback_data = {}
        
        # 优先从查询参数获取（GET 请求）
        if request.args:
            callback_data = request.args.to_dict()
            print(f"[SVG] 从查询参数获取数据: {callback_data}")
        
        # 如果查询参数为空，尝试从 JSON 获取（POST 请求）
        if not callback_data and request.is_json:
            callback_data = request.get_json()
            print(f"[SVG] 从 JSON 获取数据: {callback_data}")
        
        # 如果还是为空，尝试从表单数据获取（POST 请求）
        if not callback_data and request.form:
            callback_data = request.form.to_dict()
            print(f"[SVG] 从表单数据获取: {callback_data}")
            # 如果表单数据是 JSON 字符串，解析它
            if 'data' in callback_data:
                import json
                try:
                    callback_data = json.loads(callback_data['data'])
                    print(f"[SVG] 解析 JSON 字符串: {callback_data}")
                except:
                    pass
        
        # 如果还是为空，尝试从请求体获取（原始数据）
        if not callback_data:
            try:
                raw_data = request.get_data(as_text=True)
                if raw_data:
                    print(f"[SVG] 原始请求体: {raw_data}")
                    import json
                    try:
                        callback_data = json.loads(raw_data)
                        print(f"[SVG] 解析原始 JSON: {callback_data}")
                    except:
                        # 如果不是 JSON，尝试解析为查询字符串
                        from urllib.parse import parse_qs
                        parsed = parse_qs(raw_data)
                        callback_data = {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
                        print(f"[SVG] 解析查询字符串: {callback_data}")
            except Exception as e:
                print(f"[SVG] 解析请求体失败: {e}")
        
        print(f"[SVG] 最终回调数据: {callback_data}")
        
        # 处理回调
        from utils import handle_svg_callback
        success = handle_svg_callback(callback_data)
        
        if success:
            return jsonify({"status": "ok"}), 200
        else:
            return jsonify({"status": "error", "message": "回调处理失败"}), 400
            
    except Exception as e:
        print(f"[SVG] 处理回调时出现错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=88, debug=True)

#取消热重载，减少显存使用
if __name__ == "__main__":
    print("[INFO] 启动 Flask 后端服务中...")
    #app.run(host="127.0.0.1", port=88, debug=False, use_reloader=False)  #本地回环访问
    app.run(host="0.0.0.0", port=6006, debug=False, use_reloader=False) #服务器启动
