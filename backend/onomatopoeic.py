import re
import itertools
from rapidfuzz.distance import Levenshtein
from collections import defaultdict

from logger import logger
from schema import OnomatopoeicTypes

class Onomatopoeic:
    """This is a class reserved for onomatopoeic operations."""

    CONS = {
        'PLOS▼', 'PLOS▲', 'FRIC▼', 'FRIC▲',
        'AFFR▼', 'AFFR▲', 'SON_lat', 'SON_lab',
        'SON_nas', 'SON_med', 'SON_gutt', 'R',
    }
    PLOS = {'PLOS▼', 'PLOS▲'}
    AFFR = {'AFFR▼', 'AFFR▲'}
    R = {'R'}

    VOC_SHORT = {'VOC_l_w', 'VOC_h_w'}
    VOC_LONG = {'VOC_l_s', 'VOC_h_s'}

    EMPTY = {None}
    
    # Dictionary of all onomatopoeic models by class
    onomatopoeic_models = {
        # Instant
        "I": (
            # P.47
            (
                PLOS | AFFR,
                VOC_SHORT,
                PLOS,
            ),
            # P.48
            (
                PLOS | AFFR,
                VOC_SHORT,
            ),
        ),
        # TODO: Уточнить, что именно у Воронина долгий, а что короткий
        # Tonal Continuant
        "TC": (
            # TODO: В тексте написано, что VOC_LONG. Выглядит как VOC_SHORT. Выяснить причину
            # P.49 (53)
            (
                CONS,
                {'SON_lat', 'SON_lab', None},
                VOC_LONG,
                PLOS | EMPTY,
            ),
            # P.49 (53) NOTE: Variation of the above
            (
                CONS | EMPTY,
                VOC_LONG,
                PLOS | EMPTY,
            ),
        ),
        # Noisy Continuant
        "NC": (
            # P.52 (56)
            (
                {'FRIC▲'},
                VOC_SHORT,
                CONS | EMPTY,
            ),
            # P.52 (56) NOTE: variation of the above
            (
                CONS | EMPTY,
                VOC_SHORT,
                {'FRIC▲'},
            ),
        ),
        # Tonal Noisy Continuant
        "TNC": (
            # P.53 (57)
            (
                CONS,
                VOC_SHORT,
                {'FRIC▼'},
            ),
        ),
        # Frecventatives
        "F": (
            # P.54 (58) TODO: Непонятные стрелочки на схеме
            (
                CONS | EMPTY,
                R,
                VOC_SHORT,
                PLOS,
            ),
            # P.56 (60)
            (
                CONS,
                VOC_SHORT,
                R,
            ),
            # P.57 (61)
            (
                CONS,
                VOC_SHORT,
                R,
            ),
            # P.57 (61)
            (
                CONS,
                R,
                VOC_LONG,
                CONS | EMPTY,
            ),
            # P.58 (62) NOTE: Included in #56
            # (
            #     {'FRIC▲'},
            #     VOC_SHORT,
            #     R,
            # ),
            # P.58 (62)
            (
                R,
                VOC_SHORT,
                {'FRIC▲'},
            ),
            # P.59 (62) TODO: Непоняные стрелочки на схеме
            (
                {'FRIC▲', None},
                R,
                VOC_SHORT,
                {'FRIC▼'},
            ),
        ),
        # "": (

        # )
    }

    phonotypes = {
        # 24 сonsonant phonemes
        # PLOS (6)
        'PLOS▼' : ('b', 'd', 'g') + ('ɡ',),
        'PLOS▲' : ('t', 'p', 'k'),
        # FRIC (8) (sib▲▼?)
        'FRIC▼': ('v', 'z', 'ð', 'ʒ'),
        'FRIC▲': ('f', 's', 'θ', 'ʃ', 'h',),
        # AFFR (2)
        'AFFR▼': ('d͡ʒ',) + ('dʒ',),
        'AFFR▲': ('t͡ʃ',) + ('tʃ',),
        # SON (7)
        'SON_lat': ('l',),  # боковые
        'SON_lab': ('m', 'w',),  # губные
        'SON_nas': ('m', 'n', 'ŋ',), # назальные
        'SON_med': ('j',),  # среднеязычные
        'SON_gutt': ('ŋ',),  # заднеязычные и фарингальные
        # R (1)
        'R': ('r',) + ('ɹ',),  # вибрант

        # 12(+1) monophthongs, 8(+1) diphthongs vowel phonemes (N.B. /ɛ/ & /oʊ/ not by Bondarko)
        'VOC_h_w': ('ɪ', 'ʊ', 'ə', 'e', 'ɛ'),
        'VOC_h_s': ('i', 'u', 'ɪə', 'ʊə', 'eɪ','əʊ', 'oʊ'),
        'VOC_l_w': ('æ', 'ʌ'),
        'VOC_l_s': ('ɑ', 'ɒ', 'ɔ', 'ɜ', 'aʊ', 'aɪ', 'ɔɪ', 'ɛə') + ('ɝ',),
    }

    # Reverse dict[phoneme, list[phonotype]] for tokenization
    phonotype_dict: dict[str, list[str]]
    # Sorted phonemes for maximal munch (complex phonemes first)
    sorted_phonemes: list[str]

    def __init__(self):
        # Create a dict of phonemes
        self.phonotype_dict = Onomatopoeic._collect_phonotypes_by_phoneme()
        # Sort phonemes: complex phonemes come first (maximal munch)
        self.sorted_phonemes = sorted(
            Onomatopoeic._collect_phonotypes_by_phoneme(), key=len, reverse=True
        )

    @classmethod
    def _model_variations(cls, type: OnomatopoeicTypes) -> tuple[tuple[str, ...], ...]:
        """Get all possible canonical model variations for input onomatopoeic class."""
        return tuple(
            tuple(elem for elem in variant if elem is not None)
            for model in cls.onomatopoeic_models[type]
            for variant in itertools.product(*(sorted(s, key=lambda x: (x is None, x)) for s in model))
        )

    @classmethod
    def _collect_phonotypes_by_phoneme(cls) -> dict[str, list[str]]:
        """Make a dict where keys are phonemes & values are their phonotypes."""
        phoneme_dict = defaultdict(list)
        for group, phonemes in cls.phonotypes.items():
            for phoneme in phonemes:
                phoneme_dict[phoneme].append(group)
        return phoneme_dict

    def _transcription_to_phonemes(self, ipa: str) -> list[str]:
        """Turn input transcription into a list of verified phonemes."""
        # Normalize transcription
        ipa = re.sub(r'[/\[\]\',ːˈ:. ̩  ̯ ()]', '', ipa)
        # Verify phonemes
        tokens: list[str] = []
        i = 0
        while i < len(ipa):
            matched = next((ph for ph in self.sorted_phonemes if ipa.startswith(ph, i)), None)
            if matched:
                tokens.append(matched)
                i += len(matched)
            else:
                logger.error(f'Unknown token found: {ipa[i]} in {ipa}')
                i += 1
        return tokens

    def _transcription_to_phonotypes(self, ipa: str, ) -> list[tuple[str, ...]]:
        """Find every way to describe phonemic transcription with phonotypes."""
        phonemes = self._transcription_to_phonemes(ipa)
        phonotype_groups = [
            self.phonotype_dict[phoneme]
            for phoneme in phonemes
        ]
        # Find all possible ways to tokenize transcription
        return list(itertools.product(*phonotype_groups))

    def weigh_transcription(self,
            ipa: str,
            type: OnomatopoeicTypes,
        ) -> tuple[float, tuple | None, tuple | None]:
        """Calculate phonosemantic score of ipa transcription for this onomatopoeic type.
        returns:
            phonosemantic_score -- from 0 to 1.
            ipa_phonotypes -- list of phonotypes that ipa string was converted to.
            selected_model -- onomatopoeic model with the highest similarity.
        """
        best_score = 0.0
        best_phonotypes_variant = None
        best_model_variant = None
        for phonotypes_variant in self._transcription_to_phonotypes(ipa):
            for model_variant in Onomatopoeic._model_variations(type):
                score = Levenshtein.normalized_similarity(model_variant, phonotypes_variant)
                # print(f'{model_variant} <-> {phonotypes_variant}: {score}')
                if score > best_score:
                    best_score = score
                    best_phonotypes_variant = phonotypes_variant
                    best_model_variant = model_variant
                    if best_score >= 1.0:
                        return round(best_score, 2), best_phonotypes_variant, best_model_variant
        return round(best_score, 2), best_phonotypes_variant, best_model_variant