<template>
  <q-page class="flex flex-center">
    <div class="column flex-center full-width" style="max-width: 700px">
      <q-list class="full-width">
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
      </q-list>
      <!-- Submit -->
      <div class="full-width">
        <SubmitVerb @responseAPI="updateItems"></SubmitVerb>
      </div>
      <!-- Response -->
      <div class="q-pa-md full-width">
        <!-- оригинал + значение -->
        <q-card class="q-mb-md" v-for="(item, index) in items" :key="index" flat bordered>
          <q-card-section class="bg-green-2">
            <div class="text-h6">
              <q-chip square color="primary" class="text-uppercase" text-color="white">{{ item.verb }}</q-chip>
              <q-chip v-if="item.transcription" dense square outline color="primary" class="transcription" text-color="white">{{ item.transcription }}</q-chip>
              <q-chip v-if="item.category" dense square outline color="primary" class="transitivity" text-color="white">{{ item.category }}</q-chip>
              <q-chip v-if="item.transitivity" dense square outline color="primary" class="transitivity" text-color="white">{{ item.transitivity }}</q-chip>
            </div>
            <div class="text-subtitle2 text-primary">
              {{ item.meaning }}
            </div>
          </q-card-section>
          <!-- переводы -->
          <q-markup-table separator="cell">
            <thead class="bg-grey-2" v-if="item.translations">
              <tr>
                <th class="text-center text-grey-7">
                  <span class="text-body2">Перевод</span>
                </th>
                <th v-if="item.category !== 'нет фоносемантического значения'" class="text-center text-grey-7">
                  <span class="text-body2">Балл</span>
                </th>
                <th v-if="item.transitivity" class="text-center text-grey-7">
                  <span class="text-body2">Переходность</span>
                </th>
              </tr>
            </thead>
            <tbody v-if="item.translations">
              <tr v-for="(translation, idx) in item.translations" :key="idx">
                <td class="text-left">{{ translation }}</td>
                <td v-if="item.category !== 'нет фоносемантического значения'" class="text-left">{{ item.scores[idx] }}</td>
                <td 
                  v-if="item.transitivity" 
                  class="text-left" 
                  :class="item.transitivities[idx] !== item.transitivity ? 'text-negative' : 'text-positive'"
                >
                  <span v-if="item.transitivities[idx]">{{ item.transitivities[idx] }}</span>
                  <span v-else>N/A</span>
                  <q-icon
                    :name="item.transitivities[idx] === item.transitivity ? 'check' : 'close'"
                    :color="item.transitivities[idx] === item.transitivity ? 'positive' : 'negative'"
                  />
                </td>
              </tr>
            </tbody>
          </q-markup-table>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import SubmitVerb from 'src/components/SubmitVerb.vue'

const items = ref([])

const updateItems = (newItems) => {
  items.value = newItems
}
</script>

<style>
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

<!-- дописать отсутсвие переходности и ошибки ввода -->
