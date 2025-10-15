from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template(
    "주어진 '{word}'와 유사한 단어 3가지를 나열해주세요. 단어만 나열합니다. "
)
model = ChatOpenAI(model="gpt-5-mini")
parser = StrOutputParser()

chain = RunnableParallel(
    {
        "original": RunnablePassthrough(),
        "processed": prompt | model | parser,
    }
)

result = chain.invoke({"word": "행복"})
print(result)