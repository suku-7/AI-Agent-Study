import os

class Config:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = "gpt-5-mini"
    MAX_TOKENS: int = 300

    ROOT_DIR: str = os.path.dirname(os.path.abspath(__file__))

    RSS_URL: str = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
    MAX_NEWS_COUNT: int = 60
    BATCH_SIZE: int = 10

    NEWS_CATEGORIES: list[str] = [
        "정치",
        "경제",
        "사회",
        "문화/연예",
        "IT/과학",
        "스포츠",
        "국제",
        "생활/건강",
        "기타",
    ]
    NEWS_PER_CATEGORY: int = 30

    OUTPUT_DIR: str = f"{ROOT_DIR}/outputs"

    @classmethod
    def validate(cls) -> bool:
        """설정 유효성 검사"""
        if not cls.OPENAI_API_KEY:
            print("OpenAI API 키가 설정되지 않았습니다.")
            print("환경 변수 OPENAI_API_KEY를 설정하거나 실행 시 입력하세요.")
            return False
        return True
    