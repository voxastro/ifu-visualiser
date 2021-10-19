import { Store } from '../store'

const routes = [
  {
    name: 'main',
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('src/pages/Landing.vue') }],
  },
  {
    name: 'search',
    path: '/search',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('src/pages/Search.vue') }],
    beforeEnter: (to, from, next) => {
      Store.commit('setQueryString', to.query.q ? to.query.q : '')
      next()
    },
  },
  {
    path: '/visualise',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/Visualise.vue') },
      {
        name: 'cube',
        path: 'cube/:cube_id',
        component: () => import('src/pages/VisualiseCube.vue'),
        props: true,
      },
    ],
  },
  {
    name: 'docs',
    path: '/docs',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('src/pages/Docs.vue') }],
  },
  {
    name: 'about',
    path: '/about',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('src/pages/About.vue') }],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue'),
  },
]

export default routes
