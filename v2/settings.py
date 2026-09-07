from pydantic import BaseModel

class Settings(BaseModel):
    database_name: str
    english_wiktionary: str
    russian_wiktionary: str
    wiktionary_pronunciation_priority: list[str]
    # Fastapi setting
    app_name: str
    version: str
    host: str
    port: int
    workers: int
    debug: bool
    cors_origins: list[str] | str

settings = Settings(
    database_name='dictionary',
    # Phonosemantic settings
    english_wiktionary='kaikki.org-dictionary-English.jsonl',
    russian_wiktionary='kaikki.org-dictionary-Russian.jsonl',
    wiktionary_pronunciation_priority = ['General-American', 'US', 'America'],
    # Fastapi setting
    app_name="Phonosemantic Tool",
    version="0.1.0",
    host="127.0.0.1",
    port=8000,
    workers=1,
    debug=True,
    cors_origins = [
        "http://localhost:9000",
        "http://localhost:3000",
        "http://127.0.0.1:9000",
        "http://127.0.0.1:3000",
    ],
)