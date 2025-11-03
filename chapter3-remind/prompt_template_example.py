import os
from langchain.prompts import load_prompt

current_dir_path = os.path.dirname(os.path.abspath(__file__))

file_prompt = load_prompt(f"{current_dir_path}/template_example.yaml", encoding="utf-8")
print(file_prompt.format(context="서울은 한국 수도이다.", question="수도는?"))