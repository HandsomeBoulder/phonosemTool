<template>

<q-card flat class="my-card q-px-md" >
    <q-card-section class="phonotypes">
        <div class="row items-center justify-between">
            <div class="text-overline">Фонотипы переводческого эквивалента:</div>
            <PhonotypeGroup :phonotypes="phonotypes"/>
        </div>
        <div class="row items-center justify-between">
            <div class="text-overline">Наиболее подходящая каноническая модель:</div>
            <PhonotypeGroup :phonotypes="model"/>
        </div>
    </q-card-section>

    <q-separator inset v-if="examples.length"/>

    <q-card-section class="q-gutter-md">
        <div v-for="(example, index) in examples" :key="example.english">
            <div class="text-h7 text-subtitle2 text-bold">{{ `Пример ${index+1}` }}</div>
            <div class="example text-body2">{{ example.english }}</div>
            <div class="example text-body2">{{ example.russian }}</div>
        </div>
    </q-card-section>
</q-card>

</template>
  
<script setup lang="ts">
import PhonotypeGroup from './PhonotypeGroup.vue';
import type { Example } from './types';

interface Props {
  examples: Example[]
  model: string[]
  phonotypes: string[]
}
withDefaults(defineProps<Props>(), {});

</script>


<style scoped lang="scss">
.phonotypes {
    display: flex;
    flex-direction: column;
    gap: 15px;
}
// .my-card {
//     width: 100%;
//     max-width: 900px;
// }
.example {
    white-space: normal;
}
</style>