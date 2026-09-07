from typing import Any
from sqlalchemy import select
from dataclasses import dataclass, field
from typing import Literal

from schema import OnomatopoeicTypes, Pos
from onomatopoeic import Onomatopoeic
from database import session_factory, EnglishWiktionary, RussianWiktionary
from settings import settings
from logger import logger

@dataclass
class Word:
    """Individual unit of the translation."""
    spelling: str
    transcription: str | None

@dataclass
class Translation:
    """Individual translation with its linguistic & phonosemantic properties."""
    words: list[Word]
    score: float | None = None
    phonotypes: tuple[str, ...] | None = None
    model: tuple[str, ...] | None = None

@dataclass
class Example:
    """Example sentence representing a specific meaning."""
    russian: str
    english: str

@dataclass
class Sense:
    """Meaning that can be translated in several ways."""
    translations: list[Translation]
    examples: list[Example]

@dataclass
class LexicalUnit:
    """Class reserved for operations on lexical units."""
    lemma: str
    pos: Pos
    onomatop_type: OnomatopoeicTypes | None = None
    senses: list[Sense] = field(default_factory=list)

    @classmethod
    def from_wiktionary(cls,
        lemma: str,
        pos: Pos,
    ):
        instance = cls(lemma=lemma, pos=pos)
        entry = instance._get_russian_wiktionary_entry()
        if entry: instance._set_wiktionary_translation(entry=entry)
        return instance

    def _get_russian_wiktionary_entry(self) -> dict[str, Any] | None:
        """Get wiktionary entry for this Russian word by its lemma and POS."""
        with session_factory() as session:
            stmt = select(RussianWiktionary.entry).where(RussianWiktionary.word == self.lemma)
            if self.pos: stmt.where(RussianWiktionary.pos == self.pos)
            return session.scalars(stmt).first()

    @staticmethod
    def _get_english_wiktionary_entry(lemma: str, pos: Pos | None = None) -> dict[str, Any] | None:
        """Get wiktionary entry for English word by lemma and POS."""
        with session_factory() as session:
            stmt = select(EnglishWiktionary.entry).where(EnglishWiktionary.word == lemma)
            if pos: stmt.where(EnglishWiktionary.pos == pos)
            return session.scalars(stmt).first()

    def _set_wiktionary_translation(self, entry: dict[str, Any]):
        """Get entry from wiktionary."""
        # Loop meanings
        for sense in entry['senses']:
            # Loop various translations of each meaning
            translations: list[Translation] = []
            for link in sense['links']:
                # Loop links(words) of each translation
                words: list[Word] = []
                # Skip link if its invalid (link consists of two elements)
                if len(link) < 2: continue
                for word in link[1].split(' '):
                    trascription = self._get_wiktionary_transcription(word)
                    words.append(Word(
                        spelling=word,
                        transcription=trascription,
                    ))
                translations.append(
                    Translation(
                        words=words,
                    )
                )
            # Find examples for each meaning
            examples: list[Example] = [
                Example(
                    russian=example.get('text', ''),
                    english=example.get('english', ''),
                )
                for example in sense.get('examples', [])
            ]
            self.senses.append(Sense(translations=translations, examples=examples))

    @staticmethod
    def _get_wiktionary_transcription(word: str) -> str | None:
        entry = LexicalUnit._get_english_wiktionary_entry(lemma=word)
        if not entry: return
        sounds: list[dict[str, Any]] = entry.get('sounds', [])
        
        # Try to find each pronunciation in a priority list
        for tag in settings.wiktionary_pronunciation_priority:
            for sound in sounds:
                if 'ipa' in sound and tag in sound.get('tags', []):
                    # Select phonemic
                    if '[' not in sound['ipa']: return sound['ipa']
        
        # Fallback 1: take untagged "default" pronounciation
        for sound in sounds:
            if 'ipa' in sound and not sound.get('tags'):
                # Select phonemic
                if '[' not in sound['ipa']: return sound['ipa']
        
        # Fallback 2: take the first ipa entry that was found
        for sound in sounds:
            if 'ipa' in sound:
                # Select phonemic
                if '[' not in sound['ipa']: return sound['ipa']

    def calculate_onomatopoeic_score(self, onomatop_type: OnomatopoeicTypes) -> None:
        """Perform phonosemantic processing of each translation."""
        self.onomatop_type = onomatop_type
        onomatopoeic_module = Onomatopoeic()
        for sense in self.senses:
            for translation in sense.translations:
                # Concat individual word transcriptions into one
                common_transcription = ''.join([word.transcription for word in translation.words if word.transcription])
                # Skip translation if there are no transcriptions
                if not common_transcription: continue
                # Perform phonosemantic processing
                score, phonotypes, model = onomatopoeic_module.weigh_transcription(
                    ipa=common_transcription,
                    type=onomatop_type,
                )
                # Set score, phonotypes models & chosen model
                translation.score = score
                translation.phonotypes = phonotypes
                translation.model = model