import { createRouter, createWebHistory } from 'vue-router'

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
        path: 'markdown-viewer',
        name: 'MarkdownViewer',
        component: () => import('@/views/MarkdownViewer.vue')
      },
      {
        path: 'html-to-pdf',
        name: 'HtmlToPdf',
        component: () => import('@/views/HtmlToPdf.vue')
      }
    ]
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