import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/components/AppLayout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/Home.vue')
      },
      {
        path: 'markdown',
        name: 'MarkdownViewer',
        component: () => import('@/views/MarkdownViewer.vue'),
      },
      {
        path: 'markdown/viewer',
        name: 'Viewer',
        component: () => import('@/views/Viewer.vue')
      },
      {
        path: 'html-to-pdf',
        name: 'HtmlToPdf',
        component: () => import('@/views/HtmlToPdf.vue')
      },
    ]
  },
]

const router = createRouter({
  // history: createWebHistory(),
  history: createWebHashHistory(),
  routes
})

export default router 