<template>
  <section class="card">
    <h2>Create an entry</h2>
    <form @submit.prevent="submitEntry">
      <label>
        Title
        <input v-model="title" placeholder="Title" required />
      </label>
      <label>
        Date
        <input type="date" v-model="date" required />
      </label>
      <label>
        Entry
        <textarea v-model="content" placeholder="Today was..." required></textarea>
      </label>
      <label>
        Tags
        <select v-model="selectedTag" @change="addSelectedTag">
          <option value="">Choose a tag</option>
          <option v-for="tag in suggestedTags" :key="tag" :value="tag">{{ tag }}</option>
        </select>
      </label>
      <div v-if="tags.length" class="tag-list">
        <span v-for="tag in tags" :key="tag" class="tag-pill">
          {{ tag }}
          <button type="button" class="tag-remove" @click="removeTag(tag)">×</button>
        </span>
      </div>
      <button type="submit">Save entry</button>
    </form>
    <p v-if="feedback" class="feedback">{{ feedback }}</p>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const title = ref('')
const content = ref('')
const date = ref('')
const feedback = ref('')
const tags = ref([])
const selectedTag = ref('')
const suggestedTags = ['work', 'mood', 'family', 'travel', 'health', 'gratitude']

function addSelectedTag() {
  if (!selectedTag.value) return
  addTags([selectedTag.value])
  selectedTag.value = ''
}

function addTags(values) {
  const normalized = values
    .flatMap((value) => value.split(/[\s,;]+/))
    .map((value) => value.trim().toLowerCase())
    .filter(Boolean)

  const unique = normalized.filter((value) => !tags.value.includes(value))
  const merged = [...tags.value, ...unique].slice(0, 5)
  tags.value = merged
}

function removeTag(tag) {
  tags.value = tags.value.filter((item) => item !== tag)
}

async function submitEntry() {
  const response = await fetch('/entries', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: title.value, content: content.value, date: date.value, tags: tags.value })
  })

  feedback.value = 'Entry saved successfully.'
  title.value = ''
  content.value = ''
  date.value = ''
  selectedTag.value = ''
  tags.value = []

  setTimeout(() => router.push('/'), 500)
}
</script>

<style scoped>
.card {
  background: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(45, 39, 96, 0.08);
}

h2 {
  margin: 0 0 16px;
}

form {
  display: grid;
  gap: 12px;
}

label {
  display: grid;
  gap: 6px;
  font-weight: 600;
}

input,
textarea,
button {
  border-radius: 10px;
  border: 1px solid #e2deff;
  padding: 10px 12px;
  font: inherit;
}

textarea {
  min-height: 110px;
  resize: vertical;
}

button {
  cursor: pointer;
  background: #6c63ff;
  color: white;
  border: none;
  font-weight: 700;
}

.feedback {
  margin-top: 12px;
  color: #4e3fa8;
}
</style>