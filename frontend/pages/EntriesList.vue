<template>
  <section class="card">
    <div class="card-header">
      <div>
        <p class="eyebrow">Your story</p>
        <h2>All entries</h2>
      </div>
      <router-link to="/new" class="ghost-link">New entry</router-link>
    </div>

    <div v-if="loading">Loading your journal...</div>
    <div v-else-if="entries.length === 0">No journal entries yet. Start by writing your first!</div>
    <div v-else class="entry-list">
      <article v-for="entry in entries" :key="entry._id || (entry.title + entry.date)" class="entry-card">
        <div class="entry-top">
          <h3>{{ entry.title }}</h3>
          <span>{{ formatDate(entry.date) }}</span>
        </div>
        <p>{{ entry.content }}</p>
        <div v-if="entry.tags?.length" class="tag-list">
          <span v-for="tag in entry.tags" :key="tag" class="tag-pill">{{ tag }}</span>
        </div>
        <div class="entry-actions" style="margin-top: 10px; display: flex; gap: 8px;">
          <button @click="$router.push(`/edit/${entry._id}`)">Edit</button>
          <button @click="deleteEntry(entry._id)">Delete</button>
        </div>
      </article>

      <div v-if="editingEntry" class="edit-modal" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.2); display: flex; align-items: center; justify-content: center;">
        <div style="background: white; padding: 24px; border-radius: 12px; min-width: 300px;">
          <h3>Edit Entry</h3>
          <input v-model="editTitle" placeholder="Title" style="width: 100%; margin-bottom: 8px;" />
          <textarea v-model="editContent" placeholder="Content" style="width: 100%; margin-bottom: 8px;"></textarea>
          <input type="date" v-model="editDate" style="width: 100%; margin-bottom: 8px;" />
          <div style="display: flex; gap: 8px;">
            <button @click="saveEdit">Save</button>
            <button @click="cancelEdit">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const entries = ref([])
const loading = ref(true)
const editingEntry = ref(null)
const editTitle = ref('')
const editContent = ref('')
const editDate = ref('')

function formatDate(date) {
  if (!date) return ''
  if (typeof date === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(date)) {
    const [y, m, d] = date.split('-').map(Number)
    return new Date(y, m - 1, d).toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    })
  }

  return new Date(date).toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

function startEdit(entry) {
  editingEntry.value = entry
  editTitle.value = entry.title
  editContent.value = entry.content
  editDate.value = entry.date?.slice(0, 10)
}

function cancelEdit() {
  editingEntry.value = null
}

async function saveEdit() {
  if (!editingEntry.value || !editingEntry.value._id) return;
  const res = await fetch(`/entries/${editingEntry.value._id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: editTitle.value,
      content: editContent.value,
      date: editDate.value,
      tags: editingEntry.value.tags || []
    })
  })
  if (!res.ok) {
    alert('Failed to update entry.');
    return;
  }
  editingEntry.value = null
  await fetchEntries()
}

async function deleteEntry(id) {
  if (!id) return;
  const res = await fetch(`/entries/${id}`, { method: 'DELETE' })
  if (!res.ok) {
    alert('Failed to delete entry.');
    return;
  }
  await fetchEntries()
}

async function fetchEntries() {
  const response = await fetch('/entries')
  entries.value = await response.json()
}

onMounted(async () => {
  const response = await fetch('/entries')
  entries.value = await response.json()
  loading.value = false
})
</script>

<style scoped>
.card {
  background: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(45, 39, 96, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.eyebrow {
  margin: 0 0 4px;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: #6b62a8;
}

h2 {
  margin: 0;
}

.ghost-link {
  color: #6c63ff;
  font-weight: 700;
  text-decoration: none;
}

.entry-list {
  display: grid;
  gap: 12px;
}

.entry-card {
  border: 1px solid #ece9ff;
  border-radius: 12px;
  padding: 12px 14px;
}

.entry-top {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 8px;
}

h3 {
  margin: 0;
}

span {
  color: #6b62a8;
  font-size: 0.9rem;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.tag-pill, button {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 999px;
  background: #f1efff;
  color: #5b49b6;
  font-size: 0.8rem;
  font-weight: 600;
}

.edit-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.entry-actions {
  margin-top: 10px;
  display: flex;
  gap: 8px;
}
</style>