import re


import re

def extract_non_special_characters(text):
    # 使用正则表达式提取字母和数字
    result = re.findall(r'[a-zA-Z0-9]+', text)
    # 将结果列表连接成字符串
    return '-'.join(result)

# 示例文本
text = "Hello, World! 123"
clean_text = extract_non_special_characters(text)
print(clean_text)  # 输出 "HelloWorld123"