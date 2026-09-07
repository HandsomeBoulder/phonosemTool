<template>
<q-table
    v-model:pagination="pagination"
    v-model:expanded="expanded"
    v-if="rows.length"
    :columns="columns"
    :rows="rows"
    :row-key="getRowKey"
    :rows-per-page-options="[0]"
    class="table q-ma-xl"
    flat
    hide-pagination
    style="width: 100%;"
    table-style="overflow-y: hidden;"
>

    <template v-slot:header="props">
        <q-tr :props="props">
            <!-- Expand icon column -->
            <q-th auto-width />
            <!-- Other columns -->
            <q-th v-for="col in props.cols" :key="col.name" :props="props">
                {{ col.label }}
            </q-th>
        </q-tr>
    </template>

    <template #body="props">
        <q-tr
            :props="props"
            style="cursor: pointer;"
            :class="rowColor(props.expand)"
            @click="props.expand = !props.expand"
        >
            <!-- Expand icon column -->
            <q-td auto-width>
                <q-icon
                    size="sm"
                    flat
                    dense
                    :name="props.expand ? 'mdi-chevron-down' : 'mdi-chevron-right'"
                />
            </q-td>
            <!-- Spelling -->
            <q-td class="text-left">
                {{ getRowTranslation(props.row) }}
            </q-td>
            <!-- Transcription -->
            <q-td class="text-left">
                {{ getRowTranscription(props.row) }}
            </q-td>
            <!-- Score -->
            <q-td>
                <q-circular-progress
                    :value="getRowScore(props.row)"
                    class="q-my-sm"
                    size="50px"
                    show-value
                    :track-color="props.expand ? 'white' : 'grey-3'"
                    :color="scoreColor(getRowScore(props.row))"
                >
                    {{ getRowScore(props.row) }}%
                </q-circular-progress>
            </q-td>
            <!-- Phonotypes -->
            <q-td>
                <PhonotypeGroup
                    :phonotypes="getRowPhonotypes(props.row) ?? []"
                    :style="{ visibility: props.expand ? 'hidden': 'visible' }"
                />
            </q-td>
        </q-tr>
        <Transition name="slide-fade">
            <q-tr v-show="props.expand" :props="props" no-hover class="bg-grey-3">
                <q-td colspan="100%" class="expand-row">
                    <TranslationCard
                        :examples="props.row.examples"
                        :phonotypes="props.row.phonotypes"
                        :model="props.row.model"
                    />
                </q-td>
            </q-tr>
        </Transition>
        
      </template>
</q-table>

</template>
  
<script setup lang="ts">
import { ref, computed } from 'vue';
import type { QTableColumn } from 'quasar';
import type { TranslationRow, LexicalUnit } from './types';
import PhonotypeGroup from './PhonotypeGroup.vue';
import TranslationCard from './TranslationCard.vue';

interface Props {
  lexicalUnit: LexicalUnit
}
const props = withDefaults(defineProps<Props>(), {});

const expanded = ref<string[]>([]);
const pagination = ref({ rowsPerPage: 0 });

// Make a flat list of translation with their examples
const rows = computed<TranslationRow[]>(
    () => props.lexicalUnit.senses.flatMap(sense => {
        return sense.translations.map(translation => ({
            ...translation,
            examples: sense.examples
        }));
    })
);

const getRowTranslation = (row: TranslationRow) => row.words.map(word => word.spelling).join(" ");
const getRowKey = (row: TranslationRow) => row.words.map(word => word.spelling).join(' ');
const getRowTranscription = (row: TranslationRow) => row.words.map(word => word.transcription).join("").replace(/\/\//g, " ");
const getRowScore = (row: TranslationRow) => (row.score ?? 0) * 100;
const getRowPhonotypes = (row: TranslationRow) => row.phonotypes ?? [];

const rowColor = (expanded: boolean) => {
    return expanded ? 'bg-grey-3' : '';
}

const columns: QTableColumn[] = [
    {
        name: 'spelling',
        label: 'Перевод',
        align: 'left',
        field: getRowTranslation,
        sortable: true,
    },
    {
        name: 'transcription',
        label: 'Транскрипция',
        field: getRowTranscription,
        align: 'left',
        sortable: true,
    },
    {
        name: 'score',
        label: 'Балл',
        field: getRowScore,
        align: 'left',
        sortable: true,
    },
    {
        name: 'phonotypes',
        label: 'Фонотипы',
        field: getRowPhonotypes,
        align: 'left',
        sortable: false,
    },
];

/**
 * Get Quasar palette color for score widget.
 * @param score 
 */
function scoreColor(score: number) {
    if (score > 66) return 'green';
    else if (score > 33) return 'yellow-8';
    else return 'red';
}

// const original = ref<LexicalUnit>({
//     "lemma": "бить",
//     "pos": "verb",
//     "onomatop_type": "I",
//     "senses": [
//         {
//             "translations": [
//                 {
//                     "words": [
//                         {
//                             "spelling": "beat",
//                             "transcription": "/biːt/"
//                         },
//                         {
//                             "spelling": "beat",
//                             "transcription": "/biːt/"
//                         }
//                     ],
//                     "score": 0.67,
//                     "phonotypes": [
//                         "PLOS▼",
//                         "VOC_h_s",
//                         "PLOS▲"
//                     ],
//                     "model": [
//                         "PLOS▼",
//                         "VOC_h_w",
//                         "PLOS▲"
//                     ],
//                     // "expand": false,
//                 }
//             ],
//             "examples": [
//                 {
//                     "russian": "В на́ше вре́мя учи́тель никогда́ не бьёт ученика́.",
//                     "english": "In our time the teacher never beats the student."
//                 },
//                 {
//                     "russian": "Ты ду́маешь, меня́ не би́ли? Меня́, Олё́ша, dsffffffffffff fssssss sfffffffff sfddddddd fsdddddтак би́ли, что ты э́того и в стра́шном сне не уви́дишь. Ты ду́маешь, меня́ не би́ли? Меня́, Олё́ша, dsffffffffffff fssssss sfffffffff sfddddddd fsdddddтак би́ли, что ты э́того и в стра́шном сне не уви́дишь.",
//                     "english": "Do you think I was never thrashed? I got such beatings, the like you’d never see even in a nightmare."
//                 }
//             ]
//         },
//         {
//             "translations": [
//                 {
//                     "words": [
//                         {
//                             "spelling": "ahime",
//                             "transcription": "/tʃaɪm/"
//                         }
//                     ],
//                     "score": 0.33,
//                     "phonotypes": [
//                         "AFFR▲",
//                         "VOC_l_s",
//                         "SON_lab"
//                     ],
//                     "model": [
//                         "AFFR▲",
//                         "VOC_h_w",
//                         "PLOS▲"
//                     ],
//                     // "expand": false,
//                 }
//             ],
//             "examples": [
//                 {
//                     "russian": "бить в ладо́ши",
//                     "english": "to clap (palms), causing applause"
//                 },
//                 {
//                     "russian": "Режиссёр име́ет привы́чку бить в ладо́ши что́бы привле́чь внима́ние.",
//                     "english": "The producer has the habit of clapping to attract attention."
//                 },
//                 {
//                     "russian": "Часы́ бьют на ба́шне.",
//                     "english": "The clock chimes on the top of the tower."
//                 }
//             ]
//         },
//         {
//             "translations": [
//                 {
//                     "words": [
//                         {
//                             "spelling": "churn",
//                             "transcription": "/t͡ʃɝn/"
//                         }
//                     ],
//                     "score": 0.33,
//                     "phonotypes": [
//                         "AFFR▲",
//                         "VOC_l_s",
//                         "SON_nas"
//                     ],
//                     "model": [
//                         "AFFR▲",
//                         "VOC_h_w",
//                         "PLOS▲"
//                     ],
//                     // "expand": false,
//                 }
//             ],
//             "examples": []
//         }
//     ]
// })

</script>

<style scoped lang="scss">
.phonotypes {
    display: flex;
    flex-direction: row;
    gap: 5px;
}
:deep(.expand-row) {
  padding: 10px 10px 10px 10px !important;
}
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}
.slide-fade-leave-active {
  transition: all 0.3s ease-out;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(20px);
  opacity: 0;
}
</style>