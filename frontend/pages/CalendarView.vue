<template>
  <section class="card">
    <div class="card-header">
      <div>
        <p class="eyebrow">Timeline</p>
        <h2>{{ monthLabel }}</h2>
      </div>
      <div class="month-actions">
        <button @click="previousMonth">←</button>
        <button @click="today">Today</button>
        <button @click="nextMonth">→</button>
      </div>
    </div>

    <div class="calendar-grid">
      <div v-for="day in weekdayLabels" :key="day" class="weekday">{{ day }}</div>
      <div
        v-for="day in daysInMonth"
        :key="day.fullDate"
        class="day-cell"
        :class="{ muted: !day.isCurrentMonth, today: day.isToday }"
      >
        <div style="position: relative;">
          <strong>{{ day.day }}</strong>
          <span
            v-if="day.entries.length"
            style="display: block; width: 8px; height: 8px; background: #6c63ff; border-radius: 50%; position: absolute; left: 50%; transform: translateX(-50%); bottom: 4px;"
          ></span>
        </div>
        <ul v-if="day.entries.length">
          <li v-for="entry in day.entries" :key="entry._id || entry.title + day.fullDate">
            {{ entry.title }}
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

const entries = ref([])
const currentMonth = ref(new Date())
const weekdayLabels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

const monthLabel = computed(() => currentMonth.value.toLocaleDateString(undefined, { month: 'long', year: 'numeric' }))

const daysInMonth = computed(() => {
  const year = currentMonth.value.getFullYear()
  const month = currentMonth.value.getMonth()
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const days = []

  for (let i = 0; i < firstDay.getDay(); i += 1) {
    days.push({ day: '', fullDate: '', isCurrentMonth: false, entries: [] })
  }

  for (let day = 1; day <= lastDay.getDate(); day += 1) {
    const fullDate = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
    days.push({
      day,
      fullDate,
      isCurrentMonth: true,
      isToday: fullDate === new Date().toISOString().slice(0, 10),
      entries: entriesByDate.value[fullDate] || []
    })
  }

  return days
})

const entriesByDate = computed(() => {
  const map = {}
  for (const entry of entries.value) {
    const key = entry.date?.slice(0, 10)
    if (!key) continue
    if (!map[key]) map[key] = []
    map[key].push(entry)
  }
  return map
})

function previousMonth() {
  currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() - 1, 1)
}

function nextMonth() {
  currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() + 1, 1)
}

function today() {
  currentMonth.value = new Date()
}

onMounted(async () => {
  const response = await fetch('/entries')
  entries.value = await response.json()
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

.month-actions {
  display: flex;
  gap: 8px;
}

button {
  border: none;
  background: #f3f1ff;
  color: #4d3f9a;
  border-radius: 8px;
  padding: 8px 10px;
  cursor: pointer;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 8px;
}

.weekday {
  font-weight: 700;
  color: #6b62a8;
  text-align: center;
}

.day-cell {
  min-height: 90px;
  padding: 8px;
  border-radius: 10px;
  background: #faf8ff;
  border: 1px solid #ece9ff;
}

.day-cell.muted {
  opacity: 0.45;
}

.day-cell.today {
  border-color: #6c63ff;
  box-shadow: inset 0 0 0 1px #6c63ff;
}

ul {
  padding-left: 14px;
  margin: 6px 0 0;
  font-size: 0.8rem;
}
</style>
