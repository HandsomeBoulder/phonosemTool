export interface LexicalUnit {
    lemma: string
    pos: string
    onomatop_type: string | undefined
    senses: Sense[]
}

export interface Sense {
    translations: Translation[]
    examples: Example[]
}

export interface Example {
    russian: string
    english: string
}

export interface Translation {
    words: Word[]
    score: number | undefined
    phonotypes: string[] | undefined
    model: string [] | undefined
}

export interface TranslationRow extends Translation {
    examples: Example[] | undefined
}

export interface Word {
    spelling: string
    transcription: string
}

export interface OnomatopoeicTranslatePayload {
    text: string
    pos: string
    type: string
}

// Palette used to paint phonotype chips
export const phonotypePalette = {
    'PLOS▼' : 'light-blue',
    'PLOS▲' : 'light-blue',
    'FRIC▼': 'teal',
    'FRIC▲': 'teal',
    'AFFR▼': 'brown',
    'AFFR▲': 'brown',
    'SON_lat': 'purple-5',
    'SON_lab': 'purple-5',
    'SON_nas': 'purple-5',
    'SON_med': 'purple-5',
    'SON_gutt': 'purple-5',
    'R': 'grey-10',
    // Vowels
    'VOC_h_w': 'red',
    'VOC_h_s': 'red',
    'VOC_l_w': 'orange',
    'VOC_l_s': 'orange',
}