<template>
<div class="q-gutter-lg">
<div
    v-for="(sense, index) in original.senses"
    :key="index"
    class="q-gutter-lg"
>
    <q-separator size="1.5px" color="green" />
    <q-card>
        <q-card-section>
            <div class="text-overline">{{ `Переводы (${sense.translations.length})` }}</div>
            {{ sense.translations }}
        </q-card-section>
        <q-card-section>
            <div class="text-overline">{{ `Примеры (${sense.examples.length})` }}</div>
            {{ sense.examples }}
        </q-card-section>
    </q-card>
</div>
</div>

</template>
  
<script setup lang="ts">
import { ref } from 'vue';


const original = ref({
    "lemma": "бить",
    "pos": "verb",
    "onomatop_type": "I",
    "senses": [
        {
            "translations": [
                {
                    "words": [
                        {
                            "spelling": "beat",
                            "transcription": "/biːt/"
                        }
                    ],
                    "score": 0.67,
                    "phonotypes": [
                        "PLOS▼",
                        "VOC_h_s",
                        "PLOS▲"
                    ],
                    "model": [
                        "PLOS▼",
                        "VOC_h_w",
                        "PLOS▲"
                    ]
                }
            ],
            "examples": [
                {
                    "russian": "В на́ше вре́мя учи́тель никогда́ не бьёт ученика́.",
                    "english": "In our time the teacher never beats the student."
                },
                {
                    "russian": "Ты ду́маешь, меня́ не би́ли? Меня́, Олё́ша, так би́ли, что ты э́того и в стра́шном сне не уви́дишь.",
                    "english": "Do you think I was never thrashed? I got such beatings, the like you’d never see even in a nightmare."
                }
            ]
        },
        {
            "translations": [
                {
                    "words": [
                        {
                            "spelling": "chime",
                            "transcription": "/tʃaɪm/"
                        }
                    ],
                    "score": 0.33,
                    "phonotypes": [
                        "AFFR▲",
                        "VOC_l_s",
                        "SON_lab"
                    ],
                    "model": [
                        "AFFR▲",
                        "VOC_h_w",
                        "PLOS▲"
                    ]
                }
            ],
            "examples": [
                {
                    "russian": "бить в ладо́ши",
                    "english": "to clap (palms), causing applause"
                },
                {
                    "russian": "Режиссёр име́ет привы́чку бить в ладо́ши что́бы привле́чь внима́ние.",
                    "english": "The producer has the habit of clapping to attract attention."
                },
                {
                    "russian": "Часы́ бьют на ба́шне.",
                    "english": "The clock chimes on the top of the tower."
                }
            ]
        },
        {
            "translations": [
                {
                    "words": [
                        {
                            "spelling": "churn",
                            "transcription": "/t͡ʃɝn/"
                        }
                    ],
                    "score": 0.33,
                    "phonotypes": [
                        "AFFR▲",
                        "VOC_l_s",
                        "SON_nas"
                    ],
                    "model": [
                        "AFFR▲",
                        "VOC_h_w",
                        "PLOS▲"
                    ]
                }
            ],
            "examples": []
        }
    ]
})

</script>

<style scoped lang="scss">
.sense {
    display: flex;
    flex-direction: column;
    gap: 20px;
}
</style>
