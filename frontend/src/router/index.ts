import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/users/LoginView.vue'
import RegisterView from '@/views/users/RegisterView.vue'
import ProfileView from '@/views/users/ProfileView.vue'
import ListDocumentsForAproved from '@/views/documents/ListDocumentsForAproved.vue'

const routes: Array<RouteRecordRaw> = [
  { path: '/', component: HomeView },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/profile', component: ProfileView },
  { path: '/assigned-to-me', component: ListDocumentsForAproved }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
