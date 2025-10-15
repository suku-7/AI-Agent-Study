from langchain_core.runnables import RunnableBranch
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-5-mini")
parser = StrOutputParser()

def is_english(x: dict) -> bool:
    """ 입력 딕셔너리의 'word' 키에 해당하는 값이 영어인지 확인합니다."""
    return all(ord(char) < 128 for char in x["word"])

english_prompt = ChatPromptTemplate.from_template(
    "Give me 3 synonyms for {word}. Only list the words"
)

korean_prompt = ChatPromptTemplate.from_template(
    "주어진 '{word}'와 유사한 단어 3가지를 나열해주세요. 단어만 나열합니다."
)

language_aware_chain = RunnableBranch(
    (is_english, english_prompt | model | parser),
    korean_prompt | model | parser,
)

english_word = {"word": "happy"}
english_result = language_aware_chain.invoke(english_word)
print(f"Synonyms for '{english_word['word']}' : \n{english_result}\n")

korean_word = {"word": "행복"}
korean_result = language_aware_chain.invoke(korean_word)
print(f"'{korean_word['word']}'의 동의어: \n{korean_result}\n")