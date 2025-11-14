import io
from io import BytesIO
import base64
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import cairosvg
from colorthief import ColorThief
import openai
from keybert import KeyBERT
import svgtrace
from pathlib import Path
import convertapi
import requests
import yaml
import os
import shutil
with open('my_key.yaml', 'r') as file:
    data = yaml.safe_load(file)

key = data.get('openai_api_key', None)
openai.api_key = key

# 全局任务存储（用于存储任务 ID 和对应的输出路径、结果）
_svg_conversion_tasks = {}
_svg_conversion_lock = None

def _init_svg_tasks_lock():
    """初始化任务锁（线程安全）"""
    global _svg_conversion_lock
    if _svg_conversion_lock is None:
        import threading
        _svg_conversion_lock = threading.Lock()

def img_to_svg_api(img_path, output_path, callback_base_url=None):
    """
    将输入图片转换为 SVG 矢量图（使用 ai-gs.cn API）。
    支持异步任务：上传图片 URL -> 创建任务 -> 等待回调 -> 下载 SVG
    
    参数:
        img_path: 图片文件路径或 URL
        output_path: 输出 SVG 文件路径
        callback_base_url: 回调 URL 的基础地址（例如：http://your-server.com）
                          如果为 None，将尝试从环境变量或 Flask 应用获取
    
    ✅ 无需修改调用处参数（callback_base_url 为可选参数）。
    """
    import requests
    import time
    import urllib3
    import threading
    import socket
    
    # 初始化锁
    _init_svg_tasks_lock()
    
    # 禁用 SSL 警告（如果禁用 SSL 验证）
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # API 配置
    api_key = "8ERzVP4vElaPkyzcG1Zj4qHcw5ur2IkCoFrg"
    api_url = "https://imageapi.ai-gs.cn/v1/vector"
    
    # 创建输出目录
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # 检查输入文件是否存在
    if not img_path.startswith('http://') and not img_path.startswith('https://'):
        if not os.path.exists(img_path):
            print(f"❌ 图片文件不存在: {img_path}")
            return
    
    # 检查文件大小（API 限制 10MB，仅对本地文件）
    if not img_path.startswith('http://') and not img_path.startswith('https://'):
        file_size = os.path.getsize(img_path)
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            print(f"❌ 文件大小 {file_size} 字节超过最大限制 {max_size} 字节（10MB）")
            return
    
    # ==================== 步骤 1: 准备回调基础 URL ====================
    # 获取回调基础 URL（用于构建图片 URL 和回调 URL）
    
    # 调试：打印环境变量
    env_callback_url = os.environ.get('SVG_CALLBACK_BASE_URL')
    print(f"[SVG] 调试信息:")
    print(f"  - 环境变量 SVG_CALLBACK_BASE_URL: {env_callback_url}")
    print(f"  - 传入的 callback_base_url 参数: {callback_base_url}")
    
    if callback_base_url is None:
        # 尝试从环境变量获取
        callback_base_url = env_callback_url
        if callback_base_url is None:
            # 使用默认值（Flask 应用的默认地址）
            callback_base_url = "http://127.0.0.1:6006"  # 默认 Flask 端口
            print(f"[SVG] ⚠️ 环境变量未设置，使用默认值: {callback_base_url}")
        else:
            print(f"[SVG] ✅ 从环境变量读取: {callback_base_url}")
    else:
        print(f"[SVG] ✅ 使用传入的参数: {callback_base_url}")
    
    print(f"[SVG] 最终使用回调基础 URL: {callback_base_url}")
    
    # ==================== 步骤 2: 准备图片 URL ====================
    image_url = img_path
    
    # 如果输入是本地文件，我们需要提供一个可访问的 URL
    if not img_path.startswith('http://') and not img_path.startswith('https://'):
        # 使用 Flask 应用提供的图片服务
        # 获取项目根目录
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 计算相对于项目根目录的文件路径
        try:
            rel_path = os.path.relpath(img_path, current_file_dir)
            # 将路径中的反斜杠转换为正斜杠（Windows 兼容）
            rel_path = rel_path.replace('\\', '/')
        except ValueError:
            # 如果文件不在项目目录内，使用绝对路径的最后一个部分
            rel_path = os.path.basename(img_path)
            print(f"[WARN] 文件不在项目目录内，使用文件名: {rel_path}")
        
        # 构建图片 URL（使用 Flask 应用的图片服务）
        image_url = f"{callback_base_url}/api/svg_image/{rel_path}"
        print(f"[SVG] 本地文件转换为 URL: {image_url}")
        
        # 检查是否是本地地址
        if "127.0.0.1" in callback_base_url or "localhost" in callback_base_url:
            print(f"[SVG] ⚠️ 警告：使用本地地址，API 服务器可能无法访问")
            print(f"[SVG]   建议设置环境变量 SVG_CALLBACK_BASE_URL 为公网可访问的地址")
            print(f"[SVG]   例如：export SVG_CALLBACK_BASE_URL=https://your-public-url.com")
        else:
            print(f"[SVG] ✅ 使用公网地址，API 服务器应该可以访问")
    
    # ==================== 步骤 3: 准备回调 URL ====================
    callback_url = f"{callback_base_url}/api/svg_callback"
    print(f"[SVG] 回调 URL: {callback_url}")
    
    # ==================== 步骤 4: 创建转换任务 ====================
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # 构建请求体
    payload = {
        "format": "svg",
        "image_url": image_url,
        "callback": callback_url
    }
    
    # 构建请求 URL（token 作为查询参数）
    request_url = f"{api_url}?token={api_key}"
    
    try:
        print(f"[SVG] 正在创建转换任务...")
        print(f"[SVG] API URL: {api_url}")
        print(f"[SVG] 图片 URL: {image_url}")
        print(f"[SVG] 输出路径: {output_path}")
        
        response = requests.post(
            request_url,
            headers=headers,
            json=payload,
            timeout=30,
            verify=False  # 禁用 SSL 验证（如果需要）
        )
        
        print(f"[SVG] 响应状态码: {response.status_code}")
        print(f"[SVG] 响应内容: {response.text}")
        
        if response.status_code != 200:
            error_msg = f"请求失败 [{response.status_code}]: {response.text}"
            print(f"❌ {error_msg}")
            
            # 处理不同的错误码
            try:
                error_data = response.json()
                error_code = error_data.get("code", "")
                error_detail = error_data.get("detail", "")
                
                if error_code == "no_token":
                    print(f"[DEBUG] API Key 未提供或无效")
                elif error_code == "invalid_post":
                    print(f"[DEBUG] 请求参数错误: {error_detail}")
                    if "image_url" in error_detail.lower():
                        print(f"[DEBUG] 图片 URL 可能无法访问，请确保图片可以从公网访问")
                elif error_code == "used_up":
                    print(f"[DEBUG] API 套餐已用完，需要充值")
                elif error_code == "invalid_api_key":
                    print(f"[DEBUG] API Key 错误")
                elif response.status_code == 402:
                    print(f"[DEBUG] 图片处理错误: {error_detail}")
            except:
                pass
            
            return
        
        # 解析响应
        try:
            result = response.json()
        except ValueError:
            print(f"❌ 响应不是有效的 JSON: {response.text}")
            return
        
        task_id = result.get("taskId")
        code = result.get("code")
        
        if not task_id:
            print(f"❌ 未获取到任务 ID: {result}")
            return
        
        if code != "processing":
            print(f"⚠️ 任务状态异常: {code}")
        
        print(f"✅ SVG 转换任务已创建（任务 ID: {task_id}）")
        
        # ==================== 步骤 5: 注册任务并等待回调 ====================
        # 将任务信息存储到全局字典中
        with _svg_conversion_lock:
            _svg_conversion_tasks[task_id] = {
                "output_path": output_path,
                "status": "pending",
                "result_url": None,
                "error": None,
                "created_at": time.time()
            }
        
        # 等待回调结果（最多等待 5 分钟）
        max_wait_time = 300  # 5 分钟
        check_interval = 2  # 每 2 秒检查一次
        elapsed_time = 0
        
        print(f"[SVG] 等待转换完成（最多等待 {max_wait_time} 秒）...")
        
        while elapsed_time < max_wait_time:
            time.sleep(check_interval)
            elapsed_time += check_interval
            
            # 检查任务状态
            with _svg_conversion_lock:
                task_info = _svg_conversion_tasks.get(task_id)
                if task_info:
                    if task_info["status"] == "completed":
                        # 任务完成，下载 SVG 文件
                        result_url = task_info["result_url"]
                        if result_url:
                            print(f"[SVG] 转换完成，正在下载 SVG 文件...")
                            try:
                                svg_response = requests.get(result_url, timeout=60, verify=False)
                                if svg_response.status_code == 200:
                                    with open(output_path, "wb") as f:
                                        f.write(svg_response.content)
                                    file_size = os.path.getsize(output_path)
                                    print(f"✅ SVG 文件已保存到: {output_path} ({file_size} 字节)")
                                    
                                    # 清理任务信息
                                    with _svg_conversion_lock:
                                        _svg_conversion_tasks.pop(task_id, None)
                                    return
                                else:
                                    print(f"❌ 下载 SVG 文件失败 [{svg_response.status_code}]: {svg_response.text}")
                            except Exception as e:
                                print(f"❌ 下载 SVG 文件时出现错误: {e}")
                        else:
                            print(f"❌ 任务完成但未提供下载 URL")
                        
                        # 清理任务信息
                        with _svg_conversion_lock:
                            _svg_conversion_tasks.pop(task_id, None)
                        return
                    
                    elif task_info["status"] == "failed":
                        # 任务失败
                        error = task_info.get("error", "未知错误")
                        print(f"❌ 转换任务失败: {error}")
                        
                        # 清理任务信息
                        with _svg_conversion_lock:
                            _svg_conversion_tasks.pop(task_id, None)
                        return
            
            # 每 10 秒打印一次进度
            if elapsed_time % 10 == 0:
                print(f"[SVG] 等待中... ({elapsed_time}/{max_wait_time} 秒)")
        
        # 超时
        print(f"❌ 转换任务超时（已等待 {max_wait_time} 秒）")
        print(f"   任务 ID: {task_id}")
        print(f"   回调 URL: {callback_url}")
        print(f"")
        print(f"⚠️ 问题诊断:")
        print(f"   1. 回调 URL 可能无法从公网访问（当前: {callback_base_url}）")
        print(f"   2. API 服务器无法访问本地地址（如 127.0.0.1）")
        print(f"")
        print(f"💡 解决方案:")
        print(f"   方案 1: 使用 ngrok 暴露本地服务器（推荐用于开发）")
        print(f"      - 安装 ngrok: https://ngrok.com/download")
        print(f"      - 运行: ngrok http 6006")
        print(f"      - 设置环境变量: export SVG_CALLBACK_BASE_URL=https://xxxx.ngrok-free.app")
        print(f"      - 重启 Flask 应用")
        print(f"")
        print(f"   方案 2: 部署到公网服务器（推荐用于生产）")
        print(f"      - 确保服务器有公网 IP 或域名")
        print(f"      - 设置环境变量: export SVG_CALLBACK_BASE_URL=http://your-server-ip:6006")
        print(f"      - 确保防火墙开放端口 6006")
        print(f"")
        print(f"   方案 3: 使用 AutoDL 公网访问（如果可用）")
        print(f"      - 在 AutoDL 控制台查看\"自定义服务\"或\"SSH 隧道\"")
        print(f"      - 获取公网访问地址（通常格式: https://xxxx-xxxx.gradio.live）")
        print(f"      - 设置环境变量: export SVG_CALLBACK_BASE_URL=https://xxxx-xxxx.gradio.live")
        print(f"")
        print(f"   详细说明请查看: SVG_API_SETUP.md")
        print(f"")
        print(f"   测试回调 URL 是否可访问:")
        print(f"     python test_callback_url.py {callback_base_url}")
        
        # 清理任务信息
        with _svg_conversion_lock:
            _svg_conversion_tasks.pop(task_id, None)
        return
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {type(e).__name__}: {e}")
        return
    except Exception as e:
        print(f"❌ 转换过程中出现错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return

def handle_svg_callback(callback_data):
    """
    处理 SVG 转换回调（由 Flask 路由调用）
    
    参数:
        callback_data: 回调数据（字典）
    
    返回:
        bool: 是否处理成功
    """
    _init_svg_tasks_lock()
    
    try:
        code = callback_data.get("code")
        task_id = callback_data.get("taskId")
        
        if not task_id:
            print(f"[SVG] 回调数据中缺少 taskId: {callback_data}")
            return False
        
        with _svg_conversion_lock:
            task_info = _svg_conversion_tasks.get(task_id)
            if not task_info:
                print(f"[SVG] 未找到任务 ID: {task_id}")
                return False
            
            if code == "success":
                # 转换成功
                imgurl = callback_data.get("imgurl")
                if imgurl:
                    task_info["status"] = "completed"
                    task_info["result_url"] = imgurl
                    print(f"[SVG] 任务 {task_id} 转换成功，结果 URL: {imgurl}")
                    return True
                else:
                    print(f"[SVG] 回调数据中缺少 imgurl: {callback_data}")
                    task_info["status"] = "failed"
                    task_info["error"] = "回调数据中缺少 imgurl"
                    return False
            else:
                # 转换失败
                error_detail = callback_data.get("detail", "未知错误")
                task_info["status"] = "failed"
                task_info["error"] = error_detail
                print(f"[SVG] 任务 {task_id} 转换失败: {error_detail}")
                return False
                
    except Exception as e:
        print(f"[SVG] 处理回调时出现错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False
# def img_to_svg_api(img_path, output_path):
#     """
#     将输入图片转换为 SVG 矢量图（使用 libolibo API）。
#     支持异步任务：上传 -> 查询状态 -> 下载结果
#     ✅ 无需修改调用处参数。
#     """
#     import requests
#     import time
#     import urllib3
#
#     # 禁用 SSL 警告（如果禁用 SSL 验证）
#     urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#
#     # 从 my_key.yaml 读取 API Key（推荐方式）
#     # 使用绝对路径，确保能找到配置文件
#     api_key = None
#     key_file_path = None
#     try:
#         # 获取当前文件所在目录，然后查找项目根目录
#         current_file_dir = os.path.dirname(os.path.abspath(__file__))
#         key_file_path = os.path.join(current_file_dir, 'my_key.yaml')
#
#         # 如果当前目录没有，尝试使用工作目录
#         if not os.path.exists(key_file_path):
#             key_file_path = 'my_key.yaml'
#             if not os.path.exists(key_file_path):
#                 # 再次尝试使用工作目录的绝对路径
#                 key_file_path = os.path.join(os.getcwd(), 'my_key.yaml')
#
#         if os.path.exists(key_file_path):
#             with open(key_file_path, 'r', encoding='utf-8') as file:
#                 data = yaml.safe_load(file)
#                 if data:
#                     # 获取 API key
#                     api_key = data.get('libolibo_api_key')
#                     # 如果还是 None，打印调试信息
#                     if not api_key:
#                         print(f"[DEBUG] YAML 文件内容: {data}")
#                         print(f"[DEBUG] 所有键: {list(data.keys()) if data else 'None'}")
#                         # 尝试所有键，看是否有类似的键名
#                         for key in data.keys():
#                             if 'libolibo' in key.lower() or 'api' in key.lower():
#                                 print(f"[DEBUG] 找到可能的键: {key} = {data[key]}")
#                     else:
#                         # 确保 api_key 是字符串类型，去除可能的引号
#                         if isinstance(api_key, str):
#                             api_key = api_key.strip().strip("'").strip('"')
#                         print(f"[DEBUG] ✅ 成功读取 libolibo_api_key，长度: {len(api_key) if api_key else 0}")
#         else:
#             print(f"⚠️ my_key.yaml 文件不存在")
#             print(f"   尝试的路径: {key_file_path}")
#             print(f"   当前工作目录: {os.getcwd()}")
#             print(f"   当前文件目录: {os.path.dirname(os.path.abspath(__file__))}")
#     except FileNotFoundError:
#         print(f"⚠️ my_key.yaml 文件不存在")
#         print(f"   尝试的路径: {key_file_path if key_file_path else 'my_key.yaml'}")
#         print(f"   当前工作目录: {os.getcwd()}")
#         print(f"   当前文件目录: {os.path.dirname(os.path.abspath(__file__))}")
#     except yaml.YAMLError as e:
#         print(f"⚠️ YAML 解析错误: {e}")
#         import traceback
#         traceback.print_exc()
#     except Exception as e:
#         print(f"⚠️ 无法读取 my_key.yaml: {type(e).__name__}: {e}")
#         import traceback
#         traceback.print_exc()
#
#     if not api_key:
#         print("❌ 未找到 libolibo_api_key，请在 my_key.yaml 中添加：libolibo_api_key: 'your_api_key'")
#         return
#
#     # 检查输入文件是否存在
#     if not os.path.exists(img_path):
#         print(f"❌ 图片文件不存在: {img_path}")
#         return
#
#     # 创建输出目录
#     output_dir = os.path.dirname(output_path)
#     if output_dir:
#         os.makedirs(output_dir, exist_ok=True)
#
#     # ==================== 步骤 1: 上传并创建转换任务 ====================
#     url_convert = "https://admin.libolibo.cn/api/v1/convert"
#     headers = {
#         "X-API-Key": api_key
#     }
#
#     try:
#         # 检查文件是否存在和大小
#         if not os.path.exists(img_path):
#             print(f"❌ 图片文件不存在: {img_path}")
#             return
#
#         file_size = os.path.getsize(img_path)
#         print(f"[SVG] 正在上传图片: {img_path} (大小: {file_size} 字节)")
#         print(f"[SVG] API URL: {url_convert}")
#         print(f"[SVG] API Key: {api_key[:10]}...{api_key[-10:]} (长度: {len(api_key)})")
#
#         # 检查文件大小（文档要求最大2MB）
#         max_size = 2 * 1024 * 1024  # 2MB
#         if file_size > max_size:
#             print(f"⚠️ 文件大小 {file_size} 字节超过最大限制 {max_size} 字节（2MB）")
#             print(f"   建议压缩图片或减小尺寸")
#
#         # 准备文件上传 - 使用文件对象而不是读取内容
#         # 根据文档，应该使用 multipart/form-data 格式
#         try:
#             with open(img_path, "rb") as f:
#                 files = {
#                     "file": (os.path.basename(img_path), f, "image/png")
#                 }
#                 data = {
#                     "vectorFormat": ".svg"
#                 }
#
#                 print(f"[SVG] 请求参数:")
#                 print(f"  - files: file={os.path.basename(img_path)}, size={file_size} bytes")
#                 print(f"  - data: vectorFormat=.svg")
#
#                 # 尝试正常请求，如果 SSL 验证失败，则禁用验证
#                 try:
#                     response = requests.post(
#                         url_convert,
#                         headers=headers,
#                         files=files,
#                         data=data,
#                         timeout=30,
#                         verify=True
#                     )
#                 except requests.exceptions.SSLError as ssl_error:
#                     print(f"[WARN] SSL 证书验证失败，尝试禁用 SSL 验证")
#                     # 重新打开文件（因为之前的文件对象可能已经关闭）
#                     with open(img_path, "rb") as f2:
#                         files = {
#                             "file": (os.path.basename(img_path), f2, "image/png")
#                         }
#                         response = requests.post(
#                             url_convert,
#                             headers=headers,
#                             files=files,
#                             data=data,
#                             timeout=30,
#                             verify=False
#                         )
#         except Exception as e:
#             print(f"❌ 文件读取错误: {type(e).__name__}: {e}")
#             return
#
#         # 检查响应
#         print(f"[SVG] 响应状态码: {response.status_code}")
#         print(f"[SVG] 响应头: {dict(response.headers)}")
#
#         if response.status_code != 200:
#             print(f"❌ 上传失败 [{response.status_code}]: {response.text}")
#             print(f"[DEBUG] 请求 URL: {url_convert}")
#             print(f"[DEBUG] 请求头: {headers}")
#             print(f"[DEBUG] 响应内容: {response.text}")
#
#             # 根据文档，检查不同的错误码
#             if response.status_code == 401:
#                 print(f"[DEBUG] 401 错误：API Key 可能无效或未提供")
#                 print(f"  解决方案：检查 my_key.yaml 中的 libolibo_api_key 是否正确")
#             elif response.status_code == 403:
#                 print(f"[DEBUG] 403 错误：API Key 可能已禁用/过期/次数用完")
#                 print(f"  解决方案：联系服务提供商检查 API Key 状态")
#             elif response.status_code == 404:
#                 print(f"[DEBUG] 404 错误：请求的资源不存在")
#                 print(f"  可能的原因：")
#                 print(f"  1. API 端点路径可能已更改")
#                 print(f"  2. API 服务暂时不可用")
#                 print(f"  3. 服务器路由配置问题")
#                 print(f"  建议：联系服务提供商确认 API 端点是否正确")
#             elif response.status_code == 400:
#                 print(f"[DEBUG] 400 错误：请求参数错误")
#                 print(f"  请检查文件格式和参数是否正确")
#             elif response.status_code == 429:
#                 print(f"[DEBUG] 429 错误：请求过于频繁")
#                 print(f"  建议：降低请求频率，等待后重试")
#             elif response.status_code == 500:
#                 print(f"[DEBUG] 500 错误：服务器内部错误")
#                 print(f"  建议：稍后重试或联系技术支持")
#             return
#
#         try:
#             result = response.json()
#         except ValueError:
#             print(f"❌ 响应不是有效的 JSON: {response.text}")
#             return
#
#         if not result.get("success"):
#             error_msg = result.get("message", "未知错误")
#             print(f"⚠️ 转换任务创建失败: {error_msg}")
#             return
#
#         bianhao = result.get("data", {}).get("bianhao")
#         if not bianhao:
#             print(f"⚠️ 未获取到任务编号: {result}")
#             return
#
#         print(f"✅ SVG 转换任务已创建（编号: {bianhao}）")
#
#         # 检查是否立即返回了下载链接（同步情况）
#         download_url = result.get("data", {}).get("downloadUrl")
#         if download_url:
#             print(f"[SVG] 检测到直接下载链接，正在下载...")
#             try:
#                 # 尝试正常请求，如果 SSL 验证失败，则禁用验证
#                 try:
#                     svg_response = requests.get(download_url, timeout=60, verify=True)
#                 except requests.exceptions.SSLError:
#                     svg_response = requests.get(download_url, timeout=60, verify=False)
#
#                 if svg_response.status_code == 200:
#                     with open(output_path, "wb") as f:
#                         f.write(svg_response.content)
#                     file_size = os.path.getsize(output_path)
#                     print(f"✅ SVG 文件已保存到: {output_path} ({file_size} 字节)")
#                     return
#                 else:
#                     print(f"❌ 下载失败 [{svg_response.status_code}]: {svg_response.text}")
#                     # 如果直接下载失败，继续使用轮询方式
#             except Exception as e:
#                 print(f"⚠️ 直接下载失败，将使用轮询方式: {e}")
#                 # 继续使用轮询方式
#
#         # ==================== 步骤 2: 查询任务状态（异步任务）====================
#         url_status = f"https://admin.libolibo.cn/api/v1/status/{bianhao}"
#         max_attempts = 120  # 最大尝试次数（10分钟，每5秒一次）
#         attempt = 0
#         last_status = None
#
#         print(f"[SVG] 开始查询任务状态，最多等待 {max_attempts * 5} 秒...")
#
#         while attempt < max_attempts:
#             attempt += 1
#             time.sleep(5)  # 等待5秒后查询状态
#
#             try:
#                 # 尝试正常请求，如果 SSL 验证失败，则禁用验证
#                 try:
#                     status_response = requests.get(url_status, headers=headers, timeout=30, verify=True)
#                 except requests.exceptions.SSLError:
#                     status_response = requests.get(url_status, headers=headers, timeout=30, verify=False)
#
#                 if status_response.status_code != 200:
#                     print(f"⚠️ 查询状态失败 [{status_response.status_code}]: {status_response.text}")
#                     # 继续重试，不立即失败
#                     continue
#
#                 try:
#                     status_result = status_response.json()
#                 except ValueError:
#                     print(f"⚠️ 状态响应不是有效的 JSON: {status_response.text}")
#                     continue
#
#                 if not status_result.get("success"):
#                     error_msg = status_result.get("message", "未知错误")
#                     print(f"⚠️ 状态查询返回错误: {error_msg}")
#                     continue
#
#                 status_data = status_result.get("data", {})
#                 status = status_data.get("status")  # 可能的值: "pending", "processing", "completed", "failed"
#
#                 # 只在状态变化时打印
#                 if status != last_status:
#                     print(f"[SVG] 任务状态 ({attempt}/{max_attempts}): {status}")
#                     last_status = status
#
#                 if status == "completed":
#                     # 任务完成，获取下载链接
#                     download_url = status_data.get("downloadUrl")
#                     if download_url:
#                         print(f"[SVG] 任务完成，正在下载 SVG 文件...")
#                         try:
#                             # 尝试正常请求，如果 SSL 验证失败，则禁用验证
#                             try:
#                                 svg_response = requests.get(download_url, timeout=60, verify=True)
#                             except requests.exceptions.SSLError:
#                                 svg_response = requests.get(download_url, timeout=60, verify=False)
#
#                             if svg_response.status_code == 200:
#                                 with open(output_path, "wb") as f:
#                                     f.write(svg_response.content)
#                                 file_size = os.path.getsize(output_path)
#                                 print(f"✅ SVG 文件已保存到: {output_path} ({file_size} 字节)")
#                                 return
#                             else:
#                                 print(f"❌ 下载失败 [{svg_response.status_code}]: {svg_response.text}")
#                                 return
#                         except requests.exceptions.RequestException as e:
#                             print(f"❌ 下载文件时出现网络错误: {e}")
#                             return
#                     else:
#                         print(f"⚠️ 任务完成但未提供下载链接: {status_data}")
#                         return
#
#                 elif status == "failed":
#                     error_msg = status_data.get("error", status_data.get("message", "未知错误"))
#                     print(f"❌ 转换任务失败: {error_msg}")
#                     return
#
#                 # 如果状态是 "pending" 或 "processing"，继续等待
#                 # 每10次查询打印一次进度（减少日志输出）
#                 if attempt % 10 == 0:
#                     print(f"[SVG] 任务处理中... ({attempt}/{max_attempts}, 状态: {status})")
#
#             except requests.exceptions.Timeout:
#                 print(f"⚠️ 查询状态超时，继续重试... ({attempt}/{max_attempts})")
#                 continue
#             except requests.exceptions.RequestException as e:
#                 print(f"⚠️ 查询状态时出现网络错误: {e}，继续重试... ({attempt}/{max_attempts})")
#                 continue
#             except Exception as e:
#                 print(f"⚠️ 查询状态时出现未知错误: {type(e).__name__}: {e}")
#                 continue
#
#         # 超时
#         print(f"❌ 转换任务超时（已等待 {max_attempts * 5} 秒）")
#         print(f"   任务编号: {bianhao}")
#         print(f"   可以稍后手动查询状态: GET https://admin.libolibo.cn/api/v1/status/{bianhao}")
#         return
#
#     except FileNotFoundError:
#         print(f"❌ 图片文件不存在: {img_path}")
#         return
#     except requests.exceptions.RequestException as e:
#         print(f"❌ 网络请求失败: {type(e).__name__}: {e}")
#         return
#     except Exception as e:
#         print(f"❌ 转换过程中出现错误: {type(e).__name__}: {e}")
#         import traceback
#         traceback.print_exc()
#         return


def dataurl_to_pil(dataurl, output_path=None):
    image_data = dataurl.replace("data:image/png;base64,", '')
    if(len(image_data)%3 == 1): 
        image_data += "=="
    elif(len(image_data)%3 == 2): 
        image_data += "=" 
    binary_data = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(binary_data))
    return image

def pil_to_data_uri(pil_img):
    # Convert PIL image to bytes
    img_bytes = BytesIO()
    pil_img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()

    # Encode bytes as base64 string
    img_base64 = base64.b64encode(img_bytes).decode()

    # Create data URI
    data_uri = 'data:image/png;base64,' + img_base64

    # Create HTML string with image tag
    # html_str = f'<img src="{data_uri}">'

    return data_uri

def crop_element_from_RGBA(image, mask_single_FLAG= True):
    img_removal = np.array(image)
    imgray = cv2.cvtColor(img_removal, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 30, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 像素的边界
    if len(contours) == 1 or mask_single_FLAG == False:
        left, top, right, bottom = image.width, image.height, 0, 0 
        for x in range(image.width): 
            for y in range(image.height): 
                if image.getpixel((x, y))[3] != 0: 
                    left = min(left, x) 
                    top = min(top, y) 
                    right = max(right, x) 
                    bottom = max(bottom, y) 
        image = image.crop((left, top, right, bottom))
    else: # 最大的contour
        area_highest = 0
        for cntr in contours:
            x,y,w,h = cv2.boundingRect(cntr)
            if w*h > area_highest:   # find the biggest area 
                x_gen, y_gen, w_gen, h_total = x,y,w,h
                area_highest = w*h
        img_removal_correct = img_removal[y_gen:y_gen+h_total,x_gen:x_gen+w_gen]
        image = Image.fromarray(img_removal_correct).convert("RGBA")
    return image

def add_bg_color(img_rgba, color=[247, 246, 240]):
    image_array = np.array(img_rgba)
    alpha = image_array[:, :, 3]
    # white_array = np.ones_like(image_array) * color
    color_array = np.full_like(image_array[:, :, :3], color)

    image_array = np.where(np.expand_dims(alpha, axis=2) == 0, color_array, image_array[:, :, :3])

    # 打印处理后的数组
    image_rgb_r = Image.fromarray(image_array).convert("RGB")
    return image_rgb_r

def add_margin(background, img):
    
    w, h = img.size
    bg_wh, _ = background.size
    # print(h, w)
    max_value = max(h,w)
    if max_value-bg_wh>-10 or bg_wh - max_value > 100:
        if h>=w:
            ideal_h = bg_wh*0.9
            ideal_w = ideal_h * (w/h)
        if w>h:
            ideal_w = bg_wh*0.9
            ideal_h = ideal_w * (h/w)

    # if bg_wh - max_value > 100:
    #     # print("bg_wh - max_value > 100")
    #     if h>=w:
    #         ideal_h = bg_wh*0.9
    #         ideal_w = ideal_h * (w/h)
    #     if w>h:
    #         ideal_w = bg_wh*0.9
    #         ideal_h = ideal_w * (h/w)
        img = img.resize((int(ideal_w), int(ideal_h)))

    # print(ideal_w, ideal_h)
    # 计算居中位置
    x = (background.width - img.width) // 2
    y = (background.height - img.height) // 2

    # 将您的PIL对象居中粘贴到背景图像上
    background.paste(img, (x, y)) # 左上角的坐标
    return background

def add_margin_for_word(background, img):
    
    w, h = img.size
    bg_wh, _ = background.size
    # print(h, w)
    max_value = max(h,w)
    if max_value-bg_wh>-10 or bg_wh - max_value > 100:
        if h>=w:
            ideal_h = bg_wh*0.7
            ideal_w = ideal_h * (w/h)
        if w>h:
            ideal_w = bg_wh*0.7
            ideal_h = ideal_w * (h/w)
        img = img.resize((int(ideal_w), int(ideal_h)))

    # if bg_wh - max_value > 100:
    #     # print("bg_wh - max_value > 100")
    #     if h>=w:
    #         ideal_h = bg_wh*0.7
    #         ideal_w = ideal_h * (w/h)
    #     if w>h:
    #         ideal_w = bg_wh*0.7
    #         ideal_h = ideal_w * (h/w)

    # print(ideal_w, ideal_h)
    # 计算居中位置
    x = (background.width - img.width) // 2
    y = (background.height - img.height) // 2

    # 将您的PIL对象居中粘贴到背景图像上
    background.paste(img, (x, y)) # 左上角的坐标
    return background

def extract_shape(image_r, img_contour):
    # 得到边界 (left, top, right, bottom)
    border_tuple = get_rgba_border(img_contour) 
    # 新建画布 和边界一样大小
    bg = Image.new("RGBA", (border_tuple[2]-border_tuple[0], border_tuple[3]-border_tuple[1]),  "#D7D8C9")
    # 贴合上去 alpha
    # blank_rgba_arr = np.array(blank_rgba)
    # cv2.drawContours(blank_rgba_arr, contours_g, -1, (79, 79, 79), thickness=8)
    # blank_rgba_r = Image.fromarray(blank_rgba_arr).convert("RGB")
    # image_r = blank_rgba_r.crop(input_box)
    img_contour_border = img_contour.crop((border_tuple[0], border_tuple[1], border_tuple[2], border_tuple[3]))
    image_r = Image.alpha_composite(bg, img_contour_border) # color_bar 放上面
    return image_r

def rgb_to_hex(rgb):
    hex_value = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
    return hex_value

def extract_color_palatte(image_test):
    """
    从输入的 PIL.Image 图像中提取主色调调色板。
    使用 ColorThief 提取 dominant colors，并叠加默认的 color_bar 样式。
    """

    # ✅ 新增：如果输入是 PIL.Image，就先保存为临时文件供 ColorThief 读取
    if isinstance(image_test, Image.Image):
        tmp_path = "check/tmp_color_extract.png"
        image_test.save(tmp_path)
        color_thief = ColorThief(tmp_path)
    else:
        # 否则说明传入的是路径字符串
        color_thief = ColorThief(image_test)

    color_count = 5
    palette = color_thief.get_palette(color_count=color_count)

    # 载入默认色条背景
    color_bar = Image.open("frontend/src/assets/generation/default/color_bar.png").convert("RGBA")
    color_bar_w, color_bar_h = color_bar.size
    gap_length = color_bar_w // color_count

    # 绘制颜色矩形条
    bg = Image.new("RGBA", color_bar.size, "white")
    brush = ImageDraw.Draw(bg)
    for i in range(color_count):
        hex_value = rgb_to_hex(palette[i])
        brush.rectangle(
            [(i * gap_length, 0), ((i + 1) * gap_length, color_bar_h)],
            fill=hex_value
        )

    # ✅ 将颜色条叠加到默认模板
    final_palette = Image.alpha_composite(bg, color_bar)

    return final_palette


def extract_keyword(prompt):
    kw_model = KeyBERT(model='all-mpnet-base-v2')
    keywords = kw_model.extract_keywords(prompt,
                                        keyphrase_ngram_range=(1,1),
                                        stop_words='english',
                                        highlight=False,
                                        top_n=3)
    keywords_list = list(dict(keywords).keys())
    return keywords_list[0]

def add_text_to_img(keyword):
    # 加载字体和图像
    mf = ImageFont.truetype('frontend/src/assets/fonts/en/IBMPlexSans.ttf', 80)
    img_defalt_semantic = Image.open("frontend/src/assets/generation/default/semantic.png").convert("RGBA")
    brush = ImageDraw.Draw(img_defalt_semantic)

    # ✅ 新API：textbbox，取文字的边界盒
    bbox = brush.textbbox((0, 0), keyword, font=mf)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # 计算文字位置（右对齐，保留 30px 边距）
    text_x = img_defalt_semantic.width - text_width - 30
    text_y = (img_defalt_semantic.height - text_height) // 2  # 垂直居中

    # 绘制文本
    brush.text((text_x, text_y), keyword, fill=(70, 70, 70), font=mf)
    return img_defalt_semantic


def get_rgba_border(img_rgba):
    # ⚠️ 处理不同格式的图像
    original_mode = img_rgba.mode
    
    # 对于RGB图像，先检查是否需要转换为RGBA
    # 但如果原始是RGB，我们需要特殊处理（检查非白色区域）
    if img_rgba.mode == "RGB":
        # RGB图像：检查非白色区域（假设白色是背景）
        left, top, right, bottom = img_rgba.width, img_rgba.height, 0, 0 
        for x in range(img_rgba.width): 
            for y in range(img_rgba.height): 
                pixel = img_rgba.getpixel((x, y))
                # RGB像素是 (r, g, b) 元组
                if len(pixel) >= 3:
                    r, g, b = pixel[0], pixel[1], pixel[2]
                    # 如果不是白色背景（允许一些容差，处理接近白色的情况）
                    if not (r > 250 and g > 250 and b > 250):
                        left = min(left, x) 
                        top = min(top, y) 
                        right = max(right, x) 
                        bottom = max(bottom, y)
        
        # 如果所有像素都是背景（无效），返回整个图像的边界
        if left >= right or top >= bottom:
            return (0, 0, img_rgba.width, img_rgba.height)
        
        return (left, top, right, bottom)
    
    # 对于非RGB图像，转换为RGBA格式
    if img_rgba.mode != "RGBA":
        # 其他格式，先转换为 RGB，再转换为 RGBA
        img_rgba = img_rgba.convert("RGB").convert("RGBA")
    
    # RGBA图像：检查alpha通道
    left, top, right, bottom = img_rgba.width, img_rgba.height, 0, 0 
    for x in range(img_rgba.width): 
        for y in range(img_rgba.height): 
            pixel = img_rgba.getpixel((x, y))
            # 确保像素值有 alpha 通道
            if len(pixel) >= 4 and pixel[3] != 0: 
                left = min(left, x) 
                top = min(top, y) 
                right = max(right, x) 
                bottom = max(bottom, y)
    
    # 如果所有像素都是背景（无效），返回整个图像的边界
    if left >= right or top >= bottom:
        return (0, 0, img_rgba.width, img_rgba.height)
    
    return (left, top, right, bottom)

def get_rgb_border(img_rgb): 
    # 只能处理word，假设背景全白哦
    left, top, right, bottom = img_rgb.width, img_rgb.height, 0, 0  
    for x in range(img_rgb.width):  
        for y in range(img_rgb.height):  
            if img_rgb.getpixel((x, y)) != (255, 255, 255):  
                left = min(left, x)  
                top = min(top, y)  
                right = max(right, x)  
                bottom = max(bottom, y)  
    return (left, top, right, bottom)

# 得到image_word
def get_word_img(image):
    border_tuple = get_rgba_border(image)
    image_white = add_bg_color(image, [255,255,255])
    image_white = image_white.crop((border_tuple[0], border_tuple[1], border_tuple[2], border_tuple[3])).convert("RGB")
    bg = Image.new("RGB", (512, 512), "white")
    image_word = add_margin_for_word(bg, image_white)
    return image_word

# 横轴拉伸，最后还是512，512
def scale_image(init_image):
    # init_image = Image.open("check/img_word.png").convert("RGB").resize((512, 512))
    border_tuple = get_rgb_border(init_image)
    width = border_tuple[2] - border_tuple[0]
    height = border_tuple[3] - border_tuple[1]
    if width < 250: 
        scale = 300/width
        target_width = int(512*scale)
        scale_img = init_image.resize((target_width, 512))
        scale_img_r = scale_img.crop(((target_width/2-256), 0, (target_width/2+256), 512))
        return scale_img_r, target_width
    else:
        return scale_img_r

def clear_folder():
    main_folder = "check/"
    folder_path = ["first_generation", "final_generation"]

    for sub in folder_path:
        folder = os.path.join(main_folder, sub)
        os.makedirs(folder, exist_ok=True)  # ✅ 若不存在则自动创建

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")


def find_max_contour(contours):
    if len(contours)>1:
            max_area = 0
            max_contour = None
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    max_contour = contour
    else:
        max_contour = contours[0]
    return max_contour

# ======== 要处理的word转成svg ========
def word_to_svg(image_pil):
	# 这里的svg只是string
	# step1： 截取一下word，不能边框太大了
	(left, top, right, bottom) = get_rgb_border(image_pil)
	image_pil = image_pil.crop((left-10, top-10, right+10, bottom+10)).resize((512,512))
    # image_pil = image_pil.crop((left, top, right, bottom)).resize((512,512))

	# # step2： word_pil->svg
	svg_path = svgtrace.skimageTrace(image_pil)
	space_index = svg_path.find(" ")
	svg_path = svg_path[:space_index] + ' ' + 'id="svg-element"' + svg_path[space_index:]
	Path(f"svgTry.svg").write_text(
			svg_path, encoding="utf-8"
		)
	return svg_path

# ======== 找到contour ========
def find_continuous_contour(image_pil):
    # step1: 给img_mask换背景
    image_pil = add_bg_color(image_pil, color=[0, 0, 0])
    # step2: 找最大的contour
    image = np.array(image_pil)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = find_max_contour(contours)
    # step3: crop iamge
    x, y, w, h = cv2.boundingRect(max_contour)
    image = image[y:y+h, x:x+w]
    image_pil = Image.fromarray(image)
    bg = Image.new("RGB", (512, 512), "black")
    image_pil = add_margin(bg, image_pil)
    # step2: 在crop之后的ima|ge上找最大的contour
    image = np.array(image_pil)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = find_max_contour(contours)
    # step3: 近似contour（保证了只有一根contour）
    epsilon = 0.005 * cv2.arcLength(max_contour, True)
    contours = [cv2.approxPolyDP(max_contour, epsilon, True)]

    # # 绘制并显示结果
    # cv2.drawContours(image, contours, -1, (0, 255, 0), thickness=5)
    # # cv2.drawContours(image, max_contour, -1, (0, 0, 255), thickness=10)
    # img_r = Image.fromarray(image)
    # img_r
    return contours

# ======== 在contour上sample出点来 ========
def sample_from_contours(contours):
    # step1：预处理contours数组
    contours_array = [np.array(contour) for contour in contours]
    result = np.vstack(contours_array)
    reshaped_array = result.reshape(result.shape[0], 2)

    # step2：生成等间距的索引
    indices = np.linspace(0, reshaped_array.shape[0] - 1, num=18, dtype=int)
    indices = indices[:-1]

    # step3：通过索引获取相应的点
    sampled_points = reshaped_array[indices]

    # # step4：可视化
    # for point in sampled_points:
    #     cv2.circle(image, point, 3, (255, 0, 0), -1)
    # img_r = Image.fromarray(image)

    # step5：找到最左边的点（x最小）的位置，之前的都往后排，像队列一样
    # 为了保证第一个字母在左边，且没有旋转太多
    min_x = np.min(sampled_points[:,0])
    min_x_idx = np.argmin(sampled_points[:,0])
    sample_list = []
    for i in range(4):
        if i==0:
            new_sampled_points = np.vstack([sampled_points[min_x_idx:], sampled_points[:min_x_idx]])
        if i==1:
            new_sampled_points = np.vstack([sampled_points[min_x_idx-1:], sampled_points[:min_x_idx+i]])
        if i==2:
            new_sampled_points = np.vstack([sampled_points[min_x_idx+1:], sampled_points[:min_x_idx-1]])
        if i==3:
            new_sampled_points = np.vstack([sampled_points[min_x_idx-2:], sampled_points[:min_x_idx-2]])
        sampled_result = str(new_sampled_points.tolist())
        sample_list.append(sampled_result)
    return sample_list
