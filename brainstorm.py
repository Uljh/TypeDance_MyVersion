import openai
from openai_compat import chat_completion
import os
import yaml
with open('my_key.yaml', 'r') as file:
    data = yaml.safe_load(file)

key = data.get('openai_api_key', None)
openai.api_key = key

def get_answer(user_prompt):
    # 构建消息列表
    messages = [
        {"role": "user", "content": user_prompt},
        {"role": "system", "content": "You are a mature logo designer. Your mission is to come up with concepts that are appropriate for symbol according to user's description. For example, given 'what can represent Chongqing', you can say the 'hot-pot' because it is the famous food in Chongqing, and you also can say 'Jie fang bei', since it is the famous landmark. Please give me five symbolize concepts and explaination, follow the format, 'xx:xx'. One concept is limited whithin one word. Using one short sententce for explanation is enough, please don't say other redundunt sentence"}  # 您的system prompt
    ]
    # 使用兼容函数
    answer_content = chat_completion(messages=messages, model="gpt-3.5-turbo")
    # 注意：由于兼容函数返回的是字符串，您可能需要根据原代码的返回格式进行调整
    # 例如，如果原代码期望返回一个对象，您可能需要构建一个类似的对象
    # 这里假设返回内容即可
    ### return answer_content
    return {"content": answer_content}

    ### 下面是原版的，但是API不知道咋了调用不了，改成上面的了
    # completion = openai.ChatCompletion.create(
    # model="gpt-3.5-turbo",
    # messages=[
    #     {"role": "user", "content": user_prompt},
    # {"role": "system", "content": "You are a mature logo designer. Your mission is to come up with concepts that are appropriate for symbol according to user's description. For example, given 'what can represent Chongqing', you can say the 'hot-pot' because it is the famous food in Chongqing, and you also can say 'Jie fang bei', since it is the famous landmark. Please give me five symbolize concepts and explaination, follow the format, 'xx:xx'. One concept is limited whithin one word. Using one short sententce for explanation is enough, please don't say other redundunt sentence"},
    # ]
    # )
    # return completion.choices[0].message


# def get_dict_from_answer(answer_str):
#     concept_dict = {}
#     lines = answer_str.strip().split("\n")
#     for line in lines:
#         if ":" in line:
#             parts = line.split(":", 1)
#             key = parts[0].strip()
#             # 防止越界
#             value = parts[1].strip() if len(parts) > 1 else ""
#             concept_dict[key] = value
#     return concept_dict

# def get_dict_from_answer(string):
#     concepts_and_explanations = string.split("\n")[:5]
#
#     concept_dict = {}
#
#     for concept in concepts_and_explanations:
#         parts = concept.split(": ")
#         concept_name = parts[0].split(". ")[1]
#         explanation = parts[1]
#
#         concept_dict[concept_name] = explanation
#
#     return concept_dict

def get_dict_from_answer(answer_str):
    """
    将 LLM 返回的字符串解析为字典：
    - 如果某行包含 “: ”，则按 “key: value” 形式拆分
    - 否则，用 “Concept_<行号>” 作为 key，整行作为 value
    """
    concept_dict = {}
    # 按行拆分，去除空行及开头的 ‘- ’（如果有）
    lines = [line.strip().lstrip("- ").strip()
             for line in answer_str.split("\n")
             if line.strip()]

    for idx, line in enumerate(lines, start=1):
        if ": " in line:
            key, value = line.split(": ", 1)
            key = key.strip()
            value = value.strip()
        else:
            key = f"Concept_{idx}"
            value = line
        concept_dict[key] = value
    return concept_dict

# user_prompt = "Give some ideas about representing Chengdu"
# answer = get_answer(user_prompt)
# print(answer)
# string = answer["content"]
# concept_dict = get_dict_from_answer(string)
# print(concept_dict)