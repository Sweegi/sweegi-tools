import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/viewer',
    name: 'Viewer',
    component: () => import('@/views/Viewer.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 