from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from settings import settings
from database import SessionDep
from lexical import LexicalUnit, Sense, Example, Translation, Word
from schema import TranslatePayload

# Mount app
app = FastAPI(
    # App name
    title=settings.app_name,
    # App version
    version=settings.version,
    # Debug switch
    debug=settings.debug,
    # All requests to api start with /api
    root_path="/api",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test routers (temporary)
@app.get('/health', tags=["test"])
def check_api_health():
    """Simpliest api health check."""
    return {
        'status': 'healthy'
    }

@app.post('/onomatopoeic/translate')
def translate_onomatop(session: SessionDep, payload: TranslatePayload) -> LexicalUnit:
    """Perform translation of russian onomatop into english."""
    original = LexicalUnit.from_wiktionary(payload.text, payload.pos)
    original.calculate_onomatopoeic_score(payload.type)
    return original


    # return LexicalUnit(
    #     lemma='бить',
    #     pos='verb',
    #     onomatop_type='I',
    #     senses=[
    #         Sense(
    #             translations=[
    #                 Translation(
    #                     words=[Word(spelling='beat', transcription='/biːt/')],
    #                     score=0.67, phonotypes=('PLOS▼', 'VOC_h_s', 'PLOS▲'),
    #                     model=('PLOS▼', 'VOC_h_w', 'PLOS▲')
    #                 )
    #             ],
    #             examples=[
    #                 Example(russian='В на́ше вре́мя учи́тель никогда́ не бьёт ученика́.', english='In our time the teacher never beats the student.'),
    #                 Example(russian='Ты ду́маешь, меня́ не би́ли? Меня́, Олё́ша, так би́ли, что ты э́того и в стра́шном сне не уви́дишь.', english='Do you think I was never thrashed? I got such beatings, the like you’d never see even in a nightmare.')]),
    #         Sense(
    #             translations=[
    #                 Translation(
    #                     words=[Word(spelling='chime', transcription='/tʃaɪm/')],
    #                     score=0.33,
    #                     phonotypes=('AFFR▲', 'VOC_l_s', 'SON_lab'),
    #                     model=('AFFR▲', 'VOC_h_w', 'PLOS▲')
    #                 )
    #             ],
    #             examples=[
    #                 Example(russian='бить в ладо́ши', english='to clap (palms), causing applause'),
    #                 Example(russian='Режиссёр име́ет привы́чку бить в ладо́ши что́бы привле́чь внима́ние.', english='The producer has the habit of clapping to attract attention.'),
    #                 Example(russian='Часы́ бьют на ба́шне.', english='The clock chimes on the top of the tower.')]),
    #         Sense(
    #             translations=[
    #                 Translation(
    #                     words=[Word(spelling='churn', transcription='/t͡ʃɝn/')],
    #                     score=0.33, phonotypes=('AFFR▲', 'VOC_l_s', 'SON_nas'),
    #                     model=('AFFR▲', 'VOC_h_w', 'PLOS▲')
    #                 )
    #             ],
    #             examples=[]
    #         )
    #     ]
    # )