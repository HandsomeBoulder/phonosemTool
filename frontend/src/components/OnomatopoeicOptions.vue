<template>
<q-form
  @submit="$emit('submit', { text: text, pos: posModel, type: typeModel })"
  class="column q-gutter-md"
>
  <div class="input-fields">
    <!-- Text input -->
    <q-input
      v-model="text"
      color="primary"
      label="Слово на русском"
      filled
      clearable
      :rules="[
        val => !!val || 'Поле не может быть пустым',
        val => /^[а-яА-ЯёЁ]+$/.test(val) || 'Только кириллица'
      ]"
      autofocus
      hide-bottom-space
    />
    <!-- POS selector -->
    <q-select
      label="Часть речи"
      v-model="posModel"
      :options="posOptions"
      map-options
      emit-value
      filled
      color="primary"
    />
    <!-- Phonosem type selector -->
    <q-select
      label="ЗП класс"
      v-model="typeModel"
      map-options
      emit-value
      :options="typeOptions"
      filled
      color="primary"
    />
  </div>
  <!-- Submit button -->
  <div class="row justify-end">
    <q-btn
      label="Найти переводы"
      type="submit"
      color="primary"
      :loading="loading"
    >
      <template #loading>
        <q-spinner-hourglass class="on-left"/>
        <span class="loading">Поиск</span>
      </template>
    </q-btn>
  </div>
</q-form>
</template>
  
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type { OnomatopoeicTranslatePayload } from './types';

defineEmits<{
  (e: 'submit', payload: OnomatopoeicTranslatePayload): void
}>();

interface Props {
  loading: boolean
}
withDefaults(defineProps<Props>(), {});

const text = ref('');
const posModel = ref('');
const typeModel = ref('');
const posOptions = ref([
  {
    label: 'Глагол',
    value: 'verb',
  },
  {
    label: 'Существительное',
    value: 'noun',
  },
  {
    label: 'Прилагательное',
    value: 'adjective',
  },
]);
const typeOptions = ref([
  {
    label: 'Инстант',
    value: 'I',
  },
  {
    label: 'Тоновый континуант',
    value: 'TC',
  },
  {
    label: 'Шумовой континуант',
    value: 'NC',
  },
  {
    label: 'Тоно-шумовой континуант',
    value: 'TNC',
  },
  {
    label: 'Фреквентатив',
    value: 'F',
  },
]);

/**
 * Return first option value.
 * @param options 
 */
function firstOption(options: {label: string, value: string}[]) {
  return options[0]?.value;
};

// Set first option as a default for q-selections
onMounted(() => {
  const firstPosOption = firstOption(posOptions.value);
  posModel.value = firstPosOption ?? '';

  const firstClassOption = firstOption(typeOptions.value);
  typeModel.value = firstClassOption ?? '';
});

</script>

<style style scoped lang="scss">
.input-fields {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 30px;
}

/* loading dots */
.loading:after {
  content: ' .';
  animation: dots 1.5s steps(5, end) infinite;}

@keyframes dots {
  0%, 20% {
  color: rgba(0,0,0,0);
  text-shadow:
    .25em 0 0 rgba(0,0,0,0),
    .5em 0 0 rgba(0,0,0,0);}
  40% {
  color: white;
  text-shadow:
    .25em 0 0 rgba(0,0,0,0),
    .5em 0 0 rgba(0,0,0,0);}
  60% {
  text-shadow:
    .25em 0 0 white,
    .5em 0 0 rgba(0,0,0,0);}
  80%, 100% {
  text-shadow:
    .25em 0 0 white,
    .5em 0 0 white;}}
</style>