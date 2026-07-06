import { createRouter, createWebHistory } from 'vue-router'
import CreateEntry from '../pages/CreateEntry.vue'
import EntriesList from '../pages/EntriesList.vue'
import CalendarView from '../pages/CalendarView.vue'

const EditEntry = () => import('../pages/EditEntry.vue')

const routes = [
  { path: '/', name: 'entries', component: EntriesList },
  { path: '/new', name: 'new-entry', component: CreateEntry },
  { path: '/calendar', name: 'calendar', component: CalendarView },
  { path: '/edit/:id', name: 'edit-entry', component: EditEntry, props: true }
]

export default createRouter({
  history: createWebHistory(),
  routes
})