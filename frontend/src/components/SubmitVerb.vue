<template>
    <div class="q-pa-md">
      <q-form @submit="onSubmit" class="q-gutter-md">
        <q-input
          v-model="text"
          color="primary"
          label="Глагол или предложение"
          filled
          clearable
          :rules="[
            val => !!val || 'Поле не может быть пустым',
            val => /^[a-zA-Z ]+$/.test(val) || 'Только латинские буквы'
          ]"
          hide-bottom-space
        />
        <!-- кнопка -->
        <div>
          <q-btn label="подобрать переводы" type="submit" color="primary"/>
        </div>
      </q-form>
    </div>
</template>
  
<script setup>
import { ref, defineEmits } from 'vue'
import axios from 'axios'

const text = ref('')
const emit = defineEmits(["responseAPI"])

const onSubmit = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/api/data', { text: text.value })
    emit('responseAPI', response.data)
  } catch (error) {
    console.error("Ошибка при запросе:", error)
    emit('responseAPI', [])
  }
}
</script>