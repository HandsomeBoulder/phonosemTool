<template>
  <q-page class="flex flex-center">
    <div class="column flex-center full-width" style="max-width: 900px">
      <!-- <q-list class="full-width">
          <q-item>
            <q-item-section>
              <q-item-label>1. Введите запрос</q-item-label>
              <q-item-label caption lines="2">Это может быть отдельное слово или целое предложение. Алгоритм сам найдет все глаголы</q-item-label>
            </q-item-section>
          </q-item>
          <q-separator spaced inset />
          <q-item>
            <q-item-section>
              <q-item-label>2. Взгляните на карточки</q-item-label>
              <q-item-label caption lines="2">Приложение создаст отдельную карточку для каждого глагола. Если приложение не распознало ваш глагол, попробуйте поставить перед ним "to"</q-item-label>
            </q-item-section>
          </q-item>
          <q-separator spaced inset />
          <q-item>
            <q-item-section>
              <q-item-label>3. Взгляните на таблицы</q-item-label>
              <q-item-label caption lines="2">Карточки содержат списки переводов, ранжированных по фоносемантическому рейтингу. Чем выше балл, тем лучше перевод выполняет звукоизобразительную функцию оригинала</q-item-label>
            </q-item-section>
          </q-item>
      </q-list> -->
      <!-- Submit -->
      <!-- <div class="full-width"> -->
      <!-- </div> -->

      <!-- Filters -->
      <OnomatopoeicOptions
        @submit="onSubmit"
        class="full-width"
        :loading="loading"
      />
      <!-- Table -->
      <OnomotopoeicTranslations :lexicalUnit="lexicalUnit" />
      
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { apiPost } from '@/api';
import type { OnomatopoeicTranslatePayload, LexicalUnit } from '@/components/types';
import OnomatopoeicOptions from '@/components/OnomatopoeicOptions.vue';
import OnomotopoeicTranslations from '@/components/OnomotopoeicTranslations.vue';

const loading = ref(false);
const lexicalUnit = ref<LexicalUnit>({
  lemma: '',
  pos: '',
  onomatop_type: undefined,
  senses: [],
});

/**
 * Send request to find translations.
 * @param payload 
 */
const onSubmit = async (payload: OnomatopoeicTranslatePayload) => {
  loading.value = true;
  try {
    const response = await apiPost<LexicalUnit>('/onomatopoeic/translate', payload);
    lexicalUnit.value = response;
    console.log(response);
  } catch (error) {
    console.error("Ошибка при запросе:", error);
  } finally {
    loading.value = false;
  }
};
</script>

<style style scoped lang="scss">
.capitalize {
  text-transform: capitalize;
}
.transcription {
  margin-left: 15px;
  /* font-size: 0.9em; */
  text-transform: none;
  font-weight: normal;
  font-style: italic;
}
.transitivity {
  margin-left: 15px;
  text-transform: lowercase;
  /* font-size: 0.9em; */
  text-transform: none;
  font-weight: normal;
  /* font-style: italic; */
}
</style>
