import { createRouter, createWebHistory} from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/generator'
    },
    {
      path: '/generator',
      name: 'generator',
      component: () => import('../views/GeneratorView.vue')
    },
    {
      path: '/load',
      name: 'load',
      component: () => import('../views/LoadJsonView.vue')
    },
    {
      path: '/barCode',
      name: 'barCode',
      component: () => import('../views/BarcodeView.vue')
    }
  ]
})

export default router
