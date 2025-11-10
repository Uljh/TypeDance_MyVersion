
import torch
import numpy as np
from PIL import Image
import os
import random
from bg_removal import bg_removal
import cv2
import os
import sys
from colorthief import ColorThief
from random import sample
from utils import *
from transformers import CLIPProcessor, CLIPModel
from clip_interrogator import Config, Interrogator
from diffusers import DiffusionPipeline,StableDiffusionDepth2ImgPipeline,StableDiffusionImg2ImgPipeline,StableDiffusionPipeline

### model_id = "C:/Users/user/.cache/huggingface/hub/models--runwayml--stable-diffusion-v1-5/snapshots/aa9ba505e1973ae5cd05f5aedd345178f52f8e6a"
model_path = "/root/autodl-tmp/TypeDance/models/huggingface/hub/models--runwayml--stable-diffusion-v1-5/snapshots/451f4fe16113bff5a5d2269ed5ad43b0592e9a14"
#model_path = "runwayml/stable-diffusion-v1-5"

# =================== 设备与模型加载 ===================
current_path = os.getcwd()
print("[INFO] 检测可用设备中...")

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

def load_pipeline_with_fallback():
    """加载 Stable Diffusion 模型，自动处理显存不足和加速问题"""
    try:
        print(f"[INFO] 尝试在 {device.upper()} 上加载模型 (dtype={dtype})")
        pipe_img2img_art = StableDiffusionImg2ImgPipeline.from_pretrained(
            model_path,
            torch_dtype=dtype,
            local_files_only=True,  # 若你没联网下载过模型，可改为 False
            safety_checker=None,  # 禁用 NSFW 检查器（可选，如果需要可以启用）
            requires_safety_checker=False  # 禁用安全检查器
        ).to(device)

        pipe_text2img = StableDiffusionPipeline.from_pretrained(
            model_path,
            torch_dtype=dtype,
            local_files_only=True,
            safety_checker=None,  # 禁用 NSFW 检查器（可选，如果需要可以启用）
            requires_safety_checker=False  # 禁用安全检查器
        ).to(device)

        # ✅ 在这里插入打印，确认模型在哪个设备上
        print(f"[INFO] pipe_img2img_art 运行于设备: {pipe_img2img_art.device}")
        print(f"[INFO] pipe_text2img 运行于设备: {pipe_text2img.device}")
        print(f"[INFO] 模型成功加载于 {device.upper()} 上 ✅")

        return pipe_img2img_art, pipe_text2img

    except RuntimeError as e:
        print("⚠️ [WARN] GPU 显存不足，自动切换到 CPU 模式运行...")
        pipe_img2img_art = StableDiffusionImg2ImgPipeline.from_pretrained(
            model_path,
            torch_dtype=torch.float32,
            local_files_only=False,
            safety_checker=None,  # 禁用 NSFW 检查器
            requires_safety_checker=False  # 禁用安全检查器
        ).to("cpu")

        pipe_text2img = StableDiffusionPipeline.from_pretrained(
            model_path,
            torch_dtype=torch.float32,
            local_files_only=True,
            safety_checker=None,  # 禁用 NSFW 检查器
            requires_safety_checker=False  # 禁用安全检查器
        ).to("cpu")

        # ✅ CPU fallback 分支同样打印
        print(f"[INFO] pipe_img2img_art 运行于设备: {pipe_img2img_art.device}")
        print(f"[INFO] pipe_text2img 运行于设备: {pipe_text2img.device}")
        print("[INFO] 模型已切换至 CPU 模式 ✅")

        return pipe_img2img_art, pipe_text2img

# 调用加载函数
pipe_img2img_art, pipe_text2img = load_pipeline_with_fallback()

#批量生成
def img2img(pipe_img2img, prompt, im_bg, num_images, s=0.9):
    # 随机生成一个种子
    seed = random.randint(0, 99999999)
    device_type = pipe_img2img.device.type  # 自动检测 pipeline 的设备
    generator = torch.Generator(device=device_type).manual_seed(seed)

    # 一次生成全部图片
    output = pipe_img2img(
        prompt=prompt,
        image=im_bg,
        strength=s,
        guidance_scale=7,
        num_images_per_prompt=num_images,
        generator=generator
    )

    # 过滤掉 NSFW 图片
    nfsw_checker = output.nsfw_content_detected
    if nfsw_checker is None:
        # 如果 NSFW 检查器被禁用，直接使用所有图像
        images = output.images
    else:
        images = [
            img for i, img in enumerate(output.images)
            if not nfsw_checker[i]
        ]

        # ✅ 如果全被过滤，就保留第一张作为兜底
        if len(images) == 0:
            print("[WARN] 所有生成图被 NSFW 过滤，自动保留第一张作为兜底。")
            images = [output.images[0]]

    return images


#逐一生成
# def img2img(pipe_img2img, prompt, im_bg, num_images, s=0.9):
#     # Generator = torch.Generator(device="cuda").manual_seed(220124)
#     images_img2img = []
#     while (len(images_img2img)<num_images):
#         seed = random.randint(0,99999999)
#         # 根据当前设备选择合适的生成器
#         device_type = pipe_img2img.device.type  # 自动检测 pipeline 的设备（cpu 或 cuda）
#         generator = torch.Generator(device=device_type).manual_seed(seed)
#         ### output = pipe_img2img(prompt = prompt, image=im_bg, strength=s, guidance_scale=7,
#         ###                     generator=Generator, num_images_per_prompt=1, return_dict=True)
#
#         output = pipe_img2img(
#             prompt=prompt,
#             image=im_bg,
#             strength=s,
#             guidance_scale=7,
#             num_images_per_prompt=1,# ✅ 每次只生成一张，避免逻辑重复
#             generator=generator
#         )
#
#         # images.insert(0, init_image)
#         images = output.images[0]
#         nfsw_checker = output.nsfw_content_detected
#         if not nfsw_checker[0]:
#             images_img2img.append(images)
#     return images_img2img

def text2img(pipe_text2img, prompt, num_images):
    prompts = [prompt] * num_images
    image_text2img = pipe_text2img(prompt=prompts, width=512, height=512, guidance_scale=7.5).images
    return image_text2img

# def crop_element_from_RGBA(image, mask_single_FLAG= True):
#     img_removal = np.array(image)
#     imgray = cv2.cvtColor(img_removal, cv2.COLOR_BGR2GRAY)
#     ret, thresh = cv2.threshold(imgray, 30, 255, 0)
#     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     if len(contours) == 1 or mask_single_FLAG == False:
#         left, top, right, bottom = image.width, image.height, 0, 0 
#         for x in range(image.width): 
#             for y in range(image.height): 
#                 if image.getpixel((x, y))[3] != 0: 
#                     left = min(left, x) 
#                     top = min(top, y) 
#                     right = max(right, x) 
#                     bottom = max(bottom, y) 
#         image = image.crop((left, top, right, bottom))
#     else: #取一个contour并且裁剪
#         area_highest = 0
#         for cntr in contours:
#             x,y,w,h = cv2.boundingRect(cntr)
#             if w*h > area_highest:   # find the biggest area 
#                 x_gen, y_gen, w_gen, h_total = x,y,w,h
#                 area_highest = w*h
#         img_removal_correct = img_removal[y_gen:y_gen+h_total,x_gen:x_gen+w_gen]
#         image = Image.fromarray(img_removal_correct).convert("RGBA")
#     return image

def crop_element_from_RGBA(image, crop = False):
    img_arr = np.array(image)
    img_removal = 255-np.array(image)
    imgray = cv2.cvtColor(img_removal, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 30, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if crop == False: #取一个contour并且不裁剪
        # area_highest = 0
        # for cntr in contours:
        #     x,y,w,h = cv2.boundingRect(cntr)
        #     if w*h > area_highest:   # find the biggest area 
        #         x_gen, y_gen, w_gen, h_total = x,y,w,h
        #         area_highest = w*h
        # img_removal_correct = img_arr[y_gen:y_gen+h_total,x_gen:x_gen+w_gen]
        # image = Image.fromarray(img_removal_correct).convert("RGBA")
        # bg = Image.new("RGBA", (512,512), "white")
        # bg.paste(image, (x_gen, y_gen)) # 左上角的坐标
        # image = add_bg_color(bg, color=[255, 255, 255])
        image = Image.fromarray(img_arr).convert("RGBA")
        bg = Image.new("RGBA", (512,512), "white")
        bg.paste(image, (0, 0)) # 左上角的坐标
        image = add_bg_color(bg, color=[255, 255, 255])
    else: #取一个contour并且裁剪
        area_highest = 0
        for cntr in contours:
            x,y,w,h = cv2.boundingRect(cntr)
            if w*h > area_highest:   # find the biggest area 
                x_gen, y_gen, w_gen, h_total = x,y,w,h
                area_highest = w*h
        img_removal_correct = img_arr[y_gen:y_gen+h_total,x_gen:x_gen+w_gen]
        image = Image.fromarray(img_removal_correct).convert("RGBA")
    return image

def image_grid(imgs, rows, cols, mode="RGB"):
    # imgs is a list containing several PIL objects
    assert len(imgs) == rows * cols

    w, h = imgs[0].size
    grid = Image.new(mode, size=(cols * w, rows * h))
    grid_w, grid_h = grid.size

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid

class Generation:
    def __init__(self):
        # 确保必要的目录存在
        os.makedirs("check/first_generation", exist_ok=True)
        os.makedirs("check/second_generation", exist_ok=True)
        os.makedirs("check/color_generation", exist_ok=True)
        os.makedirs("check/wrap", exist_ok=True)
        pass

    def compare_saliency_maps(self, imageA, imageB):
        """
        比较两个图像的显著图（saliency maps）
        如果 OpenCV saliency 模块不可用，使用替代方法
        """
        try:
            # 尝试使用 OpenCV saliency 模块
            if hasattr(cv2, 'saliency') and hasattr(cv2.saliency, 'StaticSaliencySpectralResidual_create'):
                saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
                (success, saliencyMapA) = saliency.computeSaliency(np.array(imageA))
                (success, saliencyMapB) = saliency.computeSaliency(np.array(imageB))
                if success:
                    saliencyMapA = (saliencyMapA * 255).astype("uint8")
                    saliencyMapB = (saliencyMapB * 255).astype("uint8")
                    mae = np.mean(np.abs(saliencyMapA - saliencyMapB))
                    return mae
        except (AttributeError, Exception) as e:
            # saliency 模块不可用，使用替代方法
            print(f"[INFO] OpenCV saliency 模块不可用，使用替代方法: {e}")
        
        # 替代方法：使用灰度图像和梯度计算相似度
        try:
            # 转换为 numpy 数组
            imgA = np.array(imageA)
            imgB = np.array(imageB)
            
            # 确保图像尺寸一致
            if imgA.shape != imgB.shape:
                # 调整图像B的尺寸以匹配图像A
                imgB = cv2.resize(imgB, (imgA.shape[1], imgA.shape[0]))
            
            # 转换为灰度图
            if len(imgA.shape) == 3:
                grayA = cv2.cvtColor(imgA, cv2.COLOR_RGB2GRAY)
            else:
                grayA = imgA
                
            if len(imgB.shape) == 3:
                grayB = cv2.cvtColor(imgB, cv2.COLOR_RGB2GRAY)
            else:
                grayB = imgB
            
            # 计算梯度（作为显著性的替代）
            # 使用 Sobel 算子计算梯度
            gradA_x = cv2.Sobel(grayA, cv2.CV_64F, 1, 0, ksize=3)
            gradA_y = cv2.Sobel(grayA, cv2.CV_64F, 0, 1, ksize=3)
            gradA = np.sqrt(gradA_x**2 + gradA_y**2)
            
            gradB_x = cv2.Sobel(grayB, cv2.CV_64F, 1, 0, ksize=3)
            gradB_y = cv2.Sobel(grayB, cv2.CV_64F, 0, 1, ksize=3)
            gradB = np.sqrt(gradB_x**2 + gradB_y**2)
            
            # 归一化
            gradA = (gradA / gradA.max() * 255).astype("uint8") if gradA.max() > 0 else gradA.astype("uint8")
            gradB = (gradB / gradB.max() * 255).astype("uint8") if gradB.max() > 0 else gradB.astype("uint8")
            
            # 计算 MAE
            mae = np.mean(np.abs(gradA.astype(float) - gradB.astype(float)))
            return mae
            
        except Exception as e:
            # 如果梯度方法也失败，使用简单的像素差异
            print(f"[WARN] 梯度计算失败，使用简单的像素差异: {e}")
            try:
                imgA = np.array(imageA)
                imgB = np.array(imageB)
                
                # 确保图像尺寸一致
                if imgA.shape != imgB.shape:
                    imgB = cv2.resize(imgB, (imgA.shape[1], imgA.shape[0]))
                
                # 转换为灰度图
                if len(imgA.shape) == 3:
                    grayA = cv2.cvtColor(imgA, cv2.COLOR_RGB2GRAY)
                else:
                    grayA = imgA
                    
                if len(imgB.shape) == 3:
                    grayB = cv2.cvtColor(imgB, cv2.COLOR_RGB2GRAY)
                else:
                    grayB = imgB
                
                # 计算简单的像素差异
                mae = np.mean(np.abs(grayA.astype(float) - grayB.astype(float)))
                return mae
            except Exception as e:
                # 最后的备用方案：返回一个默认值
                print(f"[WARN] 所有方法都失败，返回默认值: {e}")
                return 50.0  # 返回一个合理的默认值

    def first_generation(self, iter, prompts, n_propmts, init_image, strength, mae_dict, mode):
        # 确保目录存在
        os.makedirs("check/first_generation", exist_ok=True)
        
        images_img2img = []
        max_attempts = 20  # 最大尝试次数，避免无限循环
        attempts = 0
        
        while (len(images_img2img)<3) and attempts < max_attempts:
            attempts += 1
            seed = random.randint(0,99999999)
            Generator = torch.Generator(device="cuda").manual_seed(seed)
            output = pipe_img2img_art(prompt=prompts, negative_prompt=n_propmts, image=init_image, strength=strength, 
                                        guidance_scale=7.5, generator=Generator, return_dict=True)
            nfsw_checker = output.nsfw_content_detected
            images = output.images
            
            # 处理 NSFW 检查（如果检查器被禁用，nfsw_checker 可能是 None 或全 False）
            if nfsw_checker is None:
                # 如果 NSFW 检查器被禁用，直接使用所有图像
                images_output = images
            else:
                # 过滤 NSFW 内容
                images_output = [images[i] for i in range(len(nfsw_checker)) if not nfsw_checker[i]]
                
                # 如果所有图像都被标记为 NSFW，记录警告但继续使用
                if len(images_output) == 0 and len(images) > 0:
                    print(f"[WARN] 所有生成图被 NSFW 过滤，自动保留第一张作为兜底。")
                    images_output = [images[0]]  # 使用第一张作为兜底
            
            images_img2img.extend(images_output)
        
        # 如果仍然没有足够的图像，使用已有的图像
        if len(images_img2img) == 0:
            print(f"[WARN] 经过 {max_attempts} 次尝试后仍无法生成足够的图像，使用初始图像")
            images_img2img = [init_image] * 3
        
        # 确保至少有3张图像
        while len(images_img2img) < 3:
            images_img2img.append(images_img2img[-1] if images_img2img else init_image)
        
        for id, img in enumerate(images_img2img):
            img_path = "check/first_generation/"+mode+"img_generation_iter"+str(iter)+"_id"+str(id)+".png"
            img.save(img_path)
            mae = self.compare_saliency_maps(init_image, img)
            mae_float2 = float('%.2f' % mae)
            mae_dict[img_path] = mae_float2
        # images_r = image_grid(images_img2img, 1, len(images_img2img))
        # images_r.save("check/generation/img_generation_"+str(id)+".png")
        return images_img2img, seed, mae_dict

    def second_generation(self, mae_dict, prompt, n_propmt, user_prompt):
        # 确保目录存在
        os.makedirs("check/second_generation", exist_ok=True)
        
        # 取四个mae不错的，但不是最拔尖的
        sorted_mae_list_seleted = []
        conditions = [
            ("even", "iter0"),
            ("even", "iter1"),
            ("odd", "iter2"),
            ("odd", "iter3")
        ]
        FLAG_SAMPLE_2 = False
        for condition in conditions:
            filtered_dict = {key: value for key, value in mae_dict.items() if condition[0] in key and condition[1] in key}
            if not filtered_dict:
                FLAG_SAMPLE_2 = True
                continue
            selected_key = random.sample(list(filtered_dict.keys()), 2) if FLAG_SAMPLE_2 and len(filtered_dict)>=2 else random.sample(list(filtered_dict.keys()), 1)
            sorted_mae_list_seleted.extend(selected_key)

        # sorted_mae_list_all = sorted(mae_dict.items(), key=lambda x:x[1])
        # mae_dict_new = dict(sorted_mae_list_all)
        # sorted_mae_list_seleted = sample(list(mae_dict_new.keys())[2:8], 4)
        init_image_list = []
        mode_list = []
        img_list = []

        for id, img_path in enumerate(sorted_mae_list_seleted):
            try:
                init_image = Image.open(img_path).convert("RGB").resize((512, 512))
                print(img_path)
                if user_prompt!="":
                    final_prompt = ", ".join([user_prompt]*2) + ", " + prompt.split(",")[4] + "minimalistic logo, vectorised, minimal flat 2d vector. lineal color." 
                    has_nfsw_flag = True
                    max_nfsw_attempts = 10  # 最大尝试次数，避免无限循环
                    nfsw_attempts = 0
                    original_image = init_image  # 保存原始图像作为备用
                    
                    while (has_nfsw_flag) and nfsw_attempts < max_nfsw_attempts:
                        nfsw_attempts += 1
                        seed = random.randint(0,99999999)
                        Generator = torch.Generator(device="cuda").manual_seed(seed)
                        output = pipe_img2img_art(prompt=final_prompt, negative_prompt=n_propmt, image=init_image, strength=0.5, 
                                                    guidance_scale=7.5, generator=Generator, return_dict=True)
                        init_image = output.images[0]
                        nfsw_checker = output.nsfw_content_detected
                        print(nfsw_checker)
                        # 处理 NSFW 检查（如果检查器被禁用，nfsw_checker 可能是 None）
                        if nfsw_checker is None:
                            has_nfsw_flag = False  # 如果检查器被禁用，认为没有 NSFW 内容
                        else:
                            has_nfsw_flag = nfsw_checker[0] if len(nfsw_checker) > 0 else False
                    
                    # 如果达到最大尝试次数仍然被标记为 NSFW，使用最后一次生成的图像
                    if has_nfsw_flag and nfsw_attempts >= max_nfsw_attempts:
                        print(f"[WARN] 经过 {max_nfsw_attempts} 次尝试后图像仍被标记为 NSFW，使用生成的图像")
                        # 继续使用最后一次生成的图像
                
                mode = img_path.split("_")[0] if "_" in img_path else "unknown"
                mode_list.append(mode)
                
                # 确保保存路径的目录存在
                save_path = "check/second_generation/"+img_path.split("/")[-1]
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                init_image.save(save_path)
                img_list.append(init_image)
            except Exception as e:
                print(f"[ERROR] 处理图像 {img_path} 时出错: {e}")
                # 如果处理失败，跳过这个图像
                continue
        
        # 如果没有任何图像被处理，返回空列表
        if len(img_list) == 0:
            print("[WARN] second_generation 没有生成任何图像")
        
        return img_list, mode_list

    def color_generation(self, prompts, n_propmts, init_image, id, FLAG_shape):
        # 确保目录存在
        os.makedirs("check/color_generation", exist_ok=True)
        
        seed = random.randint(0,99999999)
        Generator = torch.Generator(device="cuda").manual_seed(seed)
        # 只生成一个
        # ⚠️ 重要：为了更好应用颜色，提高strength，让颜色更明显
        if FLAG_shape:
            # 对于形状模式，使用中等strength
            strength = random.random()*(0.50-0.35)+0.35  # 从0.16-0.30提高到0.35-0.50
        else:
            # 对于非形状模式，使用较高strength以更好应用颜色
            strength = random.random()*(0.75-0.60)+0.60  # 从0.45-0.60提高到0.60-0.75
        # ⚠️ 增强prompt，明确要求保留和应用颜色
        color_prompt = prompts if isinstance(prompts, str) else prompts[0] if isinstance(prompts, list) else str(prompts)
        # 如果prompt中没有明确的颜色相关词汇，添加颜色提示
        if "color" not in color_prompt.lower() and "colour" not in color_prompt.lower():
            color_prompt = color_prompt + ", vibrant colors, colorful, rich colors, detailed colors"
        print(f"[INFO] 🎨 颜色生成 - strength: {strength:.2f}, prompt: {color_prompt[:100]}...")
        images_img2img = pipe_img2img_art(prompt=color_prompt, negative_prompt=n_propmts, image=init_image, strength=strength, 
                                    guidance_scale=7.5, generator=Generator).images[0]
        # images_r = image_grid(images_img2img, 1, len(images_img2img))
        images_img2img.save("check/color_generation/img_generation_"+str(id)+".png")
        return images_img2img

    def scale_concept_img(self, img_RGBA, concept_image):
        (left, top, right, bottom) = get_rgba_border(img_RGBA)
        width_black_img = right - left
        height_black_img = bottom - top
        (left, top, right, bottom) = get_rgba_border(concept_image)
        concept_image_crop = concept_image.crop((left, top, right, bottom))
        concept_image_scale = concept_image_crop.resize((width_black_img, height_black_img))

        bg_rgba = Image.new("RGBA", (512, 512), (0,0,0,0))
        x = (bg_rgba.width - width_black_img) // 2
        y = (bg_rgba.height - height_black_img) // 2
        bg_rgba.paste(concept_image_scale , (x, y)) # 左上角的坐标
        return bg_rgba
 
    def add_alpha(self, img_RGBA, img_rgb):
        rgba_array = np.array(img_RGBA)
        rgb_array = np.array(img_rgb)
        alpha_channel = rgba_array[:, :, 3]
        new_array = np.dstack((rgb_array , alpha_channel))
        new_image = Image.fromarray((new_array).astype(np.uint8))
        return new_image
    
    # ======== wrap得到的svg转成png ========
    def svg_to_png(self, input_svg_path, output_png_path):
        convertapi.api_secret = 'o3hO1Ge75aGpzXWm'
        convertapi.convert('png', {
            'File': input_svg_path
        }, from_format = 'svg').save_files(output_png_path)

    # ======== 这个png是线条需要填充 ========
    def png_flood_filling(self, output_png_path):
        image = Image.open(output_png_path).convert("RGBA")
        image = add_bg_color(image, color=[255, 255, 255])
        image = np.array(image)
        ## 选一个边边角角做floodfilling => 背景涂黑
        mask = np.zeros((image.shape[0]+2, image.shape[1]+2), np.uint8) 
        seedPoint = (1, 1)
        newVal = (0, 0, 0)
        loDiff, upDiff = (30, 30, 30), (30, 30, 30)
        cv2.floodFill(image, mask, seedPoint, newVal, loDiff, upDiff)

        # ## 可以识别contour了
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(contours)):
            if hierarchy[0][i][3] == -1: # 外部轮廓
                cv2.drawContours(image, contours, i, (255, 255, 255), thickness=cv2.FILLED)
                cv2.drawContours(image, contours, i, (255, 255, 255), thickness=2)
        for i in range(len(contours)):
            if hierarchy[0][i][3] != -1: # 内部轮廓
                cv2.drawContours(image, contours, i, (0, 0, 0), thickness=cv2.FILLED)
                cv2.drawContours(image, contours, i, (0, 0, 0), thickness=2)
        img_r = Image.fromarray(image)
     
        # ## 黑白反转
        # # 将图像转换为灰度图像
        grayscale_image = img_r.convert("L")
        inverted_image = Image.eval(grayscale_image, lambda x: 255 - x)
        return inverted_image.convert("RGB").resize((512, 512))

    def __call__(self, img_word, img_mask, prompt, semantic_prompt, num_to_generate, strength, option_list):
        clear_folder()
        current_path = os.path.dirname(os.path.abspath(__file__)) #即 D:\TypeDance_Doc\TypeDance
        img_word_list = []
        FLAG_shape = False
        # ==================== shape ====================
        # 如果shape存在就要替换掉img_word,变成wrap版本
        if "shape" in option_list:
            FLAG_shape = True
            for i in [3]:
                self.svg_to_png('check/wrap/wrap_'+str(i)+'.svg', 'check/wrap/wrap_'+str(i)+'.png')
                img_word = self.png_flood_filling('check/wrap/wrap_'+str(i)+'.png')
                img_word.save('check/wrap/img_'+str(i)+'_filling.png')
                # img_word_list.append(img_word)
                img_word_list.extend([img_word]*4)
                option_list = [item for item in option_list if item != "shape"]
        else:
            img_word_list = [img_word]*4

        # ==================== semantic/base ==================== 
        images_rm_list = []
        mae_dict = {}
        # step1：生成，把结果都存下来看看
        alt = semantic_prompt.split(",")[0]
        alt = "_".join(alt.split(" "))
        prompt_even = semantic_prompt # concept
        # semantic_prompt = ','.join(semantic_prompt.split(",")[:2])
        # prompt_odd = ", ".join([prompt]*2) + ", " + semantic_prompt + ", stylized silhouette, minimalistic logo, vectorised, minimal flat 2d vector. lineal color. trending on artstation." # "stylized silhouette, text logo, " #+ "trending on artstation" #minimal flat 2d vector. lineal color.
        prompt_odd = ','.join(semantic_prompt.split(",")[:4]) + ", stylized silhouette, minimalistic logo, vectorised, minimal flat 2d vector. lineal color. trending on artstation." # "stylized silhouette, text logo, " #+ "trending on artstation" #minimal flat 2d vector. lineal color.
        n_propmt = "shadow, blurry, watermark, text, signature, frame, cg render, lights"

        n_propmts = [n_propmt] * 3

        # step3：循环。
        iter = 0
        while(iter<2):
            # step2：得到saliency map 算mae
            prompt_ = prompt_even if iter % 2 ==0 else prompt_odd
            mode = "even_" if prompt_ == prompt_even else "odd_"
            print("---- prompt: ", prompt_)
            prompts = [prompt_] * 3
            # normal:分奇偶处理
            if prompt_ == prompt_even: # augment performance
                print("---EVEN---")
                # 构建final_even_prompt（移到循环外部，避免重复构建）
                if prompt != "":
                    final_even_prompt = ", ".join([prompt]*3) + ", " + semantic_prompt.split(",")[0] + ", stylized silhouette, text logo, minimalistic logo, vectorised, minimal flat 2d vector. lineal color. trending on artstation, pinterest, drrrrible" 
                else:
                    final_even_prompt = "An illustration, " + semantic_prompt.split(",")[0]+ ", pinterest, drrrrible, stylized silhouette, text logo, minimalistic logo, vectorised, minimal flat 2d vector. lineal color. trending on artstation" 
                print("----------final_even_prompt: ", final_even_prompt)
                final_even_prompts = [final_even_prompt] * 3
                
                # 得到原材料
                if FLAG_shape == True:
                    bg_img_list = img2img(pipe_img2img_art, prompt_, img_word_list[iter], 2, s=strength+0.1)
                else:
                    bg_img_list = img2img(pipe_img2img_art, prompt_, img_word_list[iter], 2, s=0.96)
                # bg_img_list = text2img(pipe_text2img, prompt_, 2)
                for i, bg_img in enumerate(bg_img_list):
                    word_img_RGBA = bg_removal(img_word_list[i], current_path)
                    bg_img.save("check/first_generation/bg_img" + str(i) + ".png")
                    # 抠图 method1
                    # if FLAG_shape == True:
                    #     img_r = Image.blend(bg_img, img_word_list[i], 0.5) # bigger, mask 
                    img_r = self.add_alpha(word_img_RGBA, bg_img)
                    img_r = add_bg_color(img_r, color=[255, 255, 255])
                    # 抠图 method2
                    img_RGBA = bg_removal(bg_img, current_path)

                    temp_path = os.path.join(current_path, "check/temp_rgba.png")
                    img_RGBA.save(temp_path) #后续这个临时文件可以删除
                    color_thief = ColorThief(temp_path)

                    main_color = color_thief.get_color()
                    image_bg_color = add_bg_color(img_RGBA, main_color)
                    img_r = self.add_alpha(word_img_RGBA, image_bg_color)
                    img_r = add_bg_color(img_r, [255,255,255])
                    # img_r.save("check/first_generation/bg_img_cc" + str(i) + ".png")
                    # 图文结合
                    img_combine = img2img(pipe_img2img_art, prompt_, img_r, 1, s=0.65)[0]
                    # gray
                    gray_img = img_combine.convert("L").convert("RGB")
                    # generate (使用循环外部构建的final_even_prompts)
                    images_img2img, seed, mae_dict = self.first_generation(i, final_even_prompts, n_propmts, gray_img, strength=0.54, mae_dict=mae_dict, mode=mode)
            # step2：得到saliency map 算mae
            else:
                print("---ODD---")
                for i in range(2):
                    images_img2img, seed, mae_dict = self.first_generation(i+2, prompts, n_propmts, img_word_list[i+2], strength, mae_dict, mode)
            iter += 1

        # step4：refine/choose
        img_list, mode_list = self.second_generation(mae_dict, prompt_, n_propmt, prompt)

        if (len(option_list)==1 and option_list[0]=="semantic") or len(option_list)==0:
            # remove background
            for img in img_list:
                img_RGBA = bg_removal(img, current_path)
                element = crop_element_from_RGBA(img_RGBA, crop = False)
                images_rm_list.append(element)
            return images_rm_list, mode_list, alt

        # ==================== color ==================== 
        if "color" in option_list:
            print("[INFO] 🎨 开始颜色生成处理...")
            for i, word_copncept_image in enumerate(img_list):
                # load image
                concept_image = img_mask
                # processing: word_copncept_image -> removal, concept_img_scaled->scale
                img_RGBA = bg_removal(word_copncept_image, current_path)
                concept_img_scaled = self.scale_concept_img(img_RGBA, concept_image)
                # get color from concept_img
                # ColorThief 需要文件路径，不能直接使用 PIL Image 对象
                # 先将图像保存到临时文件
                temp_color_path = f"check/temp_color_refine_{i}.png"
                os.makedirs("check", exist_ok=True)
                concept_img_scaled.save(temp_color_path)
                try:
                    color_thief = ColorThief(temp_color_path)
                    main_color = color_thief.get_color()
                    print(f"[INFO] 🎨 从概念图像提取的主要颜色 (RGB): {main_color}")
                except Exception as e:
                    print(f"[WARN] ⚠️ 颜色提取失败: {e}，使用默认颜色")
                    main_color = (128, 128, 128)  # 默认灰色
                finally:
                    # 清理临时文件
                    if os.path.exists(temp_color_path):
                        try:
                            os.remove(temp_color_path)
                        except:
                            pass  # 忽略删除失败
                image_bg_color = add_bg_color(concept_img_scaled, main_color)
                img_r = self.add_alpha(img_RGBA, image_bg_color)
                image_color = add_bg_color(img_r, [255,255,255])
                image_color.save("check/img_color_grid.png")
                print(f"[INFO] 🎨 颜色参考图像已保存: check/img_color_grid.png")
                # word_copncept_image -- canny
                # image_arr = colorizer(word_copncept_image, image_color)
                # img_rgb = Image.fromarray(image_arr)
                # image = self.add_alpha(img_RGBA, img_rgb)
                # ⚠️ 重要：使用增强的prompt和更高的strength来应用颜色
                image_color = self.color_generation(prompt_, n_propmt, image_color, i, FLAG_shape)
                # img_RGBA = bg_removal(image_color, current_path)
                # element = crop_element_from_RGBA(img_RGBA)
                img_list[i] = image_color
                print(f"[INFO] ✅ 颜色生成完成 - 图像 {i+1}/{len(img_list)}")
            if len(option_list)==1 or (len(option_list)==2 and "semantic" in option_list):
                return img_list, mode_list, alt


class Feedback(Generation):
    def __init__(self):
        super().__init__()

    def get_previous_img_prompt(self, ci, img_list):
        result_prompt_list = []
        for img in img_list:
            prompt = ci.interrogate_fast(img)
            result_prompt_list.append(prompt)
        return result_prompt_list
    
    def get_feedback_mode(self, previous_mode):
        if len(previous_mode)==1:
            current_mode = previous_mode*3
        if len(previous_mode)==2:
            current_mode = previous_mode
        if len(previous_mode)==3:
            current_mode = [sample(previous_mode, 1)[0]]
        return current_mode
    
    def get_feedback_img(self, current_mode, previous_img_list):
        if len(current_mode)==1:
            feedback_refer_list = [sample(previous_img_list, 1)[0]]
        if len(current_mode)==2:
            feedback_refer_list = previous_img_list
        if len(current_mode)==3:
            feedback_refer_list = [sample(previous_img_list, 1)[0]]*3
        return feedback_refer_list

    def second_generation(self, mae_dict, prompt, n_propmt, num_to_generate):
        # 确保目录存在
        os.makedirs("check/second_generation", exist_ok=True)
        
        sorted_mae_list_seleted = sample(list(mae_dict.keys()), num_to_generate)

        init_image_list = []
        mode_list = []
        img_list = []
        for id, img_path in enumerate(sorted_mae_list_seleted):
            try:
                init_image = Image.open(img_path).convert("RGB").resize((512, 512))
                print(img_path)
                mode = img_path.split("_")[0] if "_" in img_path else "unknown"
                mode_list.append(mode)
                
                # 确保保存路径的目录存在
                save_path = "check/second_generation/"+img_path.split("/")[-1]
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                init_image.save(save_path)
                img_list.append(init_image)
            except Exception as e:
                print(f"[ERROR] 处理图像 {img_path} 时出错: {e}")
                # 如果处理失败，跳过这个图像
                continue
        
        # 如果没有任何图像被处理，返回空列表
        if len(img_list) == 0:
            print("[WARN] second_generation 没有生成任何图像")
        
        return img_list, mode_list

     
    def __call__(self, img_word, img_mask, prompt, semantic_prompt, num_to_generate, strength, option_list, previous_mode, previous_img_list):
        # 1. 原图prompt
        # 2. feedback prompt
        # 3. mode
        clear_folder()


        # ============== step 1: get feedback objects ==============
        current_mode = self.get_feedback_mode(previous_mode)

        # ============== step 2: get feedback prompt ==============
        feedback_refer_list = self.get_feedback_img(current_mode, previous_img_list)
        config = Config(clip_model_name="ViT-L-14/openai")
        ci = Interrogator(config)
        refer_prompt_list = self.get_previous_img_prompt(ci, feedback_refer_list)

        # ==================== step 3: regeneration based on feedback ====================
        # 前台evalute需要alt
        alt = semantic_prompt.split(",")[0]
        alt = "_".join(alt.split(" "))

        mae_dict = {}
        for idx, mode in enumerate(current_mode):
            if mode == "even":
                print("---EVEN---")
                prompt_even = prompt + ", " + semantic_prompt.split(",")[0] + ", " + refer_prompt_list[idx] # concept
                n_propmt = "shadow, blurry, watermark, text, signature, frame, cg render, lights"
                n_propmts = [n_propmt] * 4
                final_even_prompts = [prompt_even] * 4
                # 得到原材料
                word_img_RGBA = bg_removal(img_word, current_path)
                bg_img = img2img(pipe_img2img_art, prompt_even, img_word, 1, s=0.9)[0]
                bg_img.save("check/first_generation/bg_img" + str(idx) + ".png")
                # 抠图
                img_r = self.add_alpha(word_img_RGBA, bg_img)
                img_r = add_bg_color(img_r, color=[255, 255, 255])
                # 图文结合
                img_combine = img2img(pipe_img2img_art, prompt_even, img_r, 1, s=0.6)[0]
                # gray
                gray_img = img_combine.convert("L").convert("RGB")
                # generate
                if prompt != "":
                    final_even_prompt = ", ".join([prompt]*3) + ", " + semantic_prompt.split(",")[0] + ", stylized silhouette, text logo, minimalistic logo, vectorised, minimal flat 2d vector. lineal color. trending on artstation, pinterest, drrrrible" 
                else:
                    final_even_prompt = "An illustration, " + semantic_prompt.split(",")[0]+ ", pinterest, drrrrible, stylized silhouette, text logo, minimalistic logo, vectorised, minimal flat 2d vector. lineal color. trending on artstation" 
                print("----------final_even_prompt: ", final_even_prompt)
                final_prompts = [final_even_prompt] * 4
                images_img2img, seed, mae_dict = self.first_generation(i, final_prompts, n_propmts, gray_img, strength=0.54, mae_dict=mae_dict, mode=mode)
            if mode == "odd":
                print("---ODD---")
                prompt_odd = prompt + ", " + semantic_prompt.split(",")[0] + ", " + refer_prompt_list[idx]
                n_propmt = "shadow, blurry, watermark, text, signature, frame, cg render, lights"
                n_propmts = [n_propmt] * 4
                final_prompts = [prompt_odd] * 4
                images_img2img, seed, mae_dict = self.first_generation(idx, final_prompts, n_propmts, img_word, strength=strength, mae_dict=mae_dict, mode=mode)

        # ==================== step 3: regeneration based on feedback ====================
        images_rm_list = []
        # step4：refine
        img_list, mode_list = self.second_generation(mae_dict, semantic_prompt, n_propmt, num_to_generate)

        if (len(option_list)==1 and option_list[0]=="semantic") or len(option_list)==0:
            # remove background
            for img in img_list:
                img_RGBA = bg_removal(img, current_path)
                element = crop_element_from_RGBA(img_RGBA, crop = False)
                images_rm_list.append(element)
            return images_rm_list, mode_list, alt

        # ==================== color ==================== 
        if "color" in option_list:
            print("[INFO] 🎨 开始颜色生成处理 (Feedback模式)...")
            for i, word_copncept_image in enumerate(img_list):
                # load image
                concept_image = img_mask
                # processing: word_copncept_image -> removal, concept_img_scaled->scale
                img_RGBA = bg_removal(word_copncept_image, current_path)
                concept_img_scaled = self.scale_concept_img(img_RGBA, concept_image)
                # get color from concept_img
                # ColorThief 需要文件路径，不能直接使用 PIL Image 对象
                # 先将图像保存到临时文件
                temp_color_path = f"check/temp_color_feedback_{i}.png"
                os.makedirs("check", exist_ok=True)
                concept_img_scaled.save(temp_color_path)
                try:
                    color_thief = ColorThief(temp_color_path)
                    main_color = color_thief.get_color()
                    print(f"[INFO] 🎨 从概念图像提取的主要颜色 (RGB): {main_color}")
                except Exception as e:
                    print(f"[WARN] ⚠️ 颜色提取失败: {e}，使用默认颜色")
                    main_color = (128, 128, 128)  # 默认灰色
                finally:
                    # 清理临时文件
                    if os.path.exists(temp_color_path):
                        try:
                            os.remove(temp_color_path)
                        except:
                            pass  # 忽略删除失败
                image_bg_color = add_bg_color(concept_img_scaled, main_color)
                img_r = self.add_alpha(img_RGBA, image_bg_color)
                image_color = add_bg_color(img_r, [255,255,255])
                image_color.save("check/img_color_grid.png")
                print(f"[INFO] 🎨 颜色参考图像已保存 (Feedback): check/img_color_grid.png")
                # word_copncept_image -- canny
                # image_arr = colorizer(word_copncept_image, image_color)
                # img_rgb = Image.fromarray(image_arr)
                # image = self.add_alpha(img_RGBA, img_rgb)
                # ⚠️ 重要：使用增强的prompt和更高的strength来应用颜色
                image_color = self.color_generation(final_prompts[0], n_propmt, image_color, i, FLAG_shape=False)
                img_RGBA = bg_removal(image_color, current_path)
                element = crop_element_from_RGBA(img_RGBA, crop = False)
                images_rm_list.append(element)
                print(f"[INFO] ✅ 颜色生成完成 (Feedback) - 图像 {i+1}/{len(img_list)}")
            if len(option_list)==1 or (len(option_list)==2 and "semantic" in option_list):
                return img_list, mode_list, alt




class Refine:
    def __init__(self):
        pass

    def img2img(self, pipe_img2img, prompt, im_bg, num_images, s=0.9):
        generator = torch.Generator(device="cuda").manual_seed(220124) 
        output = pipe_img2img(prompt = prompt, image=im_bg, strength=s, guidance_scale=7, 
                            generator=generator, num_images_per_prompt=num_images, return_dict=True)
        # images.insert(0, init_image)
        images = output.images
        nfsw_checker = output.nsfw_content_detected
        # 处理 NSFW 检查（如果检查器被禁用，nfsw_checker 可能是 None）
        if nfsw_checker is None:
            # 如果 NSFW 检查器被禁用，直接使用所有图像
            images_img2img = images
        else:
            images_img2img = [images[i] for i in range(len(nfsw_checker)) if not nfsw_checker[i]]
            # 如果全被过滤，保留第一张作为兜底
            if len(images_img2img) == 0 and len(images) > 0:
                print("[WARN] 所有生成图被 NSFW 过滤，自动保留第一张作为兜底。")
                images_img2img = [images[0]]
        return images_img2img

    def __call__(self, strength, anchor, alt):
        bg_img = Image.open("check/evaluate_img.png").convert("RGB").resize((512,512))
        word_image = Image.open("check/img_word.png").convert("RGB").resize((512,512))
        if strength < anchor: 
            print("become more word")
            # 找合适的strength
            steps = int((anchor+1)//0.05) + 1
            print(steps)
            strength_arr = np.linspace(0, 1, steps)
            count = round((anchor-strength)//0.05)
            final_strength = strength_arr[count]
            print(final_strength)
            img_blend = Image.blend(bg_img, word_image, final_strength) # bigger, mask 
            # # 生成
            images_img2img = self.img2img(pipe_img2img_art, alt+"an illustration, art, logo", img_blend, 1, s=0.54)[0]
            img_RGBA = bg_removal(images_img2img, current_path)
            element = crop_element_from_RGBA(img_RGBA, crop = False)
            # 找合适的strength
            # if strength > 0.05:
            #     strength_arr = np.linspace(0, 1, 17)
            #     count = round((anchor-0.05)//0.05)
            #     step = len(strength_arr) // count
            #     final_strength_arr = strength_arr[::step][:count]
            #     current_idx = round((anchor-strength)//0.05)
            #     final_strength = final_strength_arr[current_idx-1]
            #     img_blend = Image.blend(bg_img, word_image, final_strength) # bigger, mask 
            # # 生成
            #     images_img2img = self.img2img(pipe_img2img_art, alt, img_blend, 1, s=0.54)[0]
            #     img_RGBA = bg_removal(images_img2img, current_path)
            #     element = crop_element_from_RGBA(img_RGBA, crop = False)
            # if strength == -0.95:
            #     images_img2img = self.img2img(pipe_img2img_art, alt, word_image, 1, s=0.54)[0]
            #     img_RGBA = bg_removal(images_img2img, current_path)
            #     element = crop_element_from_RGBA(img_RGBA, crop = False)
            if strength == -1:
                element = word_image
        if strength > anchor:
            print("become more concept")
            # 找合适的strength
            steps = int((1-anchor)//0.05) + 1
            print(steps)
            strength_arr = np.linspace(0.45, 0.85, steps)
            count = round((strength-anchor)//0.05)
            final_strength = strength_arr[count]
            print(final_strength)
            # 生成
            images_img2img = self.img2img(pipe_img2img_art, alt+"an illustration, art, logo", bg_img, 1, s=final_strength)[0]
            img_RGBA = bg_removal(images_img2img, current_path)
            element = crop_element_from_RGBA(img_RGBA, crop = False)
        return element