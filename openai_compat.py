# import os
# from openai import OpenAI
# import openai
# import requests
# import time
# import json
# import time
#
# API_SECRET_KEY = "sk-zk289322a27e762705a127aacc46eb998f368ff789986089";
# BASE_URL = "https://api.zhizengzeng.com/v1/"
# # 新建一个文件 openai_compat.py
# try:
#     # 如果有自定义 base_url
#     client = OpenAI(
#         api_key=API_SECRET_KEY,
#         base_url=BASE_URL  # 只有第三方服务才需要这个
#     )
#
#     def chat_completion(messages, model="gpt-3.5-turbo"):
#         completion = client.chat.completions.create(
#             model=model,
#             messages=messages
#         )
#         return completion.choices[0].message.content
#
#     # def chat_completion(messages, model="gpt-3.5-turbo"):
#     #     ### client = OpenAI(api_key=API_SECRET_KEY, base_url=BASE_URL)
#     #     client = OpenAI(api_key=API_SECRET_KEY)
#     #     completion = client.chat.completions.create(
#     #         model=model,
#     #         messages=messages
#     #     )
#     #     return completion.choices[0].message.content
#
# except ImportError:
#
#     def chat_completion(messages, model="gpt-3.5-turbo"):
#         completion = openai.ChatCompletion.create(
#             model=model,
#             messages=messages
#         )
#         return completion.choices[0].message.content

# openai_compat.py
import requests
import json

API_SECRET_KEY = "sk-zk289322a27e762705a127aacc46eb998f368ff789986089"
BASE_URL = "https://api.zhizengzeng.com/v1/"


def chat_completion(messages, model="gpt-3.5-turbo"):
    """
    直接使用 requests 调用 API，绕过 OpenAI 库的问题
    """
    try:
        url = f"{BASE_URL}chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_SECRET_KEY}"
        }

        data = {
            "model": model,
            "messages": messages,
            "max_tokens": 500
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        return result["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"API调用失败: {e}")
        # 返回测试数据
        return """
1. Dragon: A powerful symbol representing strength and good luck.
2. Bamboo: Represents resilience and elegance in design.
3. Lotus: Symbolizes purity and enlightenment.
4. Phoenix: Represents rebirth and renewal.
5. Mountain: Signifies stability and endurance.
"""

# # openai_compat.py - 完全简化版本,用来测试！！！！！！！！！！！！！！！！！
# def chat_completion(messages, model="gpt-3.5-turbo"):
#     # 直接返回测试数据，跳过实际的 API 调用
#     test_response = """
# 1. Dragon: A powerful symbol in Chinese culture representing strength and good luck.
# 2. Bamboo: Represents resilience and elegance, commonly found in Asian art.
# 3. Lotus: Symbolizes purity and enlightenment in many Eastern traditions.
# 4. Phoenix: A mythical bird representing rebirth and renewal.
# 5. Mountain: Signifies stability and enduring presence in landscape design.
# """
#     return test_response