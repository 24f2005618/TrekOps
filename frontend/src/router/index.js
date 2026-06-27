import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AdminLayoutView from '../views/admin/AdminLayoutView.vue'
import AdminLoginView from '../views/admin/AdminLoginView.vue'
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            name: 'home',
            path: '/',
            component: HomeView
        },
        {
            name: 'admin',
            path: '/admin',
            component: AdminLayoutView,
            children: [
                {
                    name:'admin-login',
                    path: '',
                    component: AdminLoginView
                }
            ]
        }
    ]
}
)
export default router