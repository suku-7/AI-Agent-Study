# from langchain.prompts import PromptTemplate
# template = PromptTemplate.from_template(
#     "당신은 친절한 AI입니다.\n질문: {question}\n답변:"
# )
# print(template.format(question="랭체인이 뭐죠?"))

#---------------------------------------------------#

# from langchain.prompts import PromptTemplate

# template = PromptTemplate(
#     input_variables=["article", "style"],
#     template="다음 기사를 {style} 스타일로 요약하세요:\n\n{article}"
# )

# print(template.format(article="OpenAI가 GPT-5를 공개했다...", style="뉴스"))


#---------------------------------------------------#
from langchain.prompts import PromptTemplate

base_prompt = PromptTemplate.from_template("'{text}' 문장을 {lang}로 번역하세요.")
ko_prompt = base_prompt.partial(lang="Korean")
en_prompt = base_prompt.partial(lang="English")

print(ko_prompt.format(text="Hello"))
print(en_prompt.format(text="안녕하세요"))