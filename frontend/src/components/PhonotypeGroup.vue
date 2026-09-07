<template>
<div class="group">
    <q-badge
        v-for="(phonotype, index) in phonotypes"
        :key="`${phonotype}-${index}`"
        outline
        :color="phonotypePalette[phonotype as keyof typeof phonotypePalette]"
        class="q-pa-sm text-subtitle3 phonotype"
    > {{ phonotype }} </q-badge>
</div>
</template>
  
<script setup lang="ts">
import { phonotypePalette } from './types';

interface Props {
  phonotypes: string[]
}
withDefaults(defineProps<Props>(), {});

</script>

<style scoped lang="scss">
.group {
    display: flex;
    flex-direction: row;
    gap: 7px;
    .phonotype {
        display: flex;
        justify-content: center;
        width: 70px; text-align: center;
    }
}
</style>