from typing import Literal
from pydantic import BaseModel

# Avaliable onomatopoeic types
OnomatopoeicTypes = Literal['I', 'TC', 'NC', 'TNC', 'F']

# Avaliable parts of speech
Pos = Literal['verb', 'noun']

class TranslatePayload(BaseModel):
    text: str
    pos: Pos
    type: OnomatopoeicTypes