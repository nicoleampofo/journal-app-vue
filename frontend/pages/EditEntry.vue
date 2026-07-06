<template>
  <section class="card">
    <h2>Edit Entry</h2>
    <form @submit.prevent="submitEdit">
      <input v-model="title" placeholder="Title" required />
      <textarea v-model="content" placeholder="How do you feel?" required></textarea>
      <input type="date" v-model="date" required />
      <button type="submit">Update Entry</button>
    </form>
    <div v-if="feedback">{{ feedback }}</div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const id = route.params.id

const title = ref('')
const content = ref('')
const date = ref('')
const feedback = ref('')

onMounted(async () => {
  const res = await fetch(`/entries`)
  const entries = await res.json()
  const entry = entries.find(e => e._id === id)
  if (entry) {
    title.value = entry.title
    content.value = entry.content
    date.value = entry.date?.slice(0, 10)
  } else {
    feedback.value = 'Entry not found.'
  }
})

async function submitEdit() {
  const response = await fetch(`/entries/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: title.value,
      content: content.value,
      date: date.value
    })
  })
  if (!response.ok) {
    feedback.value = 'Unable to update your entry.'
    return
  }
  feedback.value = 'Entry updated successfully.'
  setTimeout(() => router.push('/'), 500)
}
</script>

<style scoped>
.card {
  background: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(45, 39, 96, 0.08);
  max-width: 500px;
  margin: 40px auto;
}
form {
  display: grid;
  gap: 12px;
}
input,
textarea,
button {
  border-radius: 10px;
  border: 1px solid #e2deff;
  padding: 10px 12px;
  font: inherit;
}
</style>
