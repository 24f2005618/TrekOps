import { createRouter, createWebHistory } from 'vue-router'
import store from "../store/index.js"
import Home from '../views/Home.vue'
import Login from '../views/auth/Login.vue'

import TrekkerRegister from '../views/trekker/TrekkerRegister.vue'
import TrekkerDashboard from '../views/trekker/TrekkerDashboard.vue'
import TrekkerLayout from '../views/trekker/TrekkerLayout.vue'

import AdminLayout from '../views/admin/AdminLayout.vue'
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import AdminAddStaff from '../views/admin/AdminAddStaff.vue'
import AdminManageLayout from '../views/admin/AdminManageLayout.vue'
import AdminManageStaff from '../views/admin/AdminManageStaff.vue'

import StaffLayout from '../views/staff/StaffLayout.vue'
import StaffDashboard from '../views/staff/StaffDashboard.vue'


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            name: 'home',
            path: '/',
            component: Home
        },
        {
            name: 'login',
            path: '/signin',
            component: Login
        },
        {
            name: 'admin',
            path: '/admin',
            beforeEnter(to,from){
                if(!store.getters.getRoles.includes("admin")){
                    return {name:"login"}
                }
            },
            component: AdminLayout,
            children: [
                {
                    name: 'admin-dashboard',
                    path: 'home',
                    component: AdminDashboard
                },
                {
                    name : 'manage',
                    path : 'manage',
                    component : AdminManageLayout,
                    children: [
                        {
                            name: 'manage-staff',
                            path: 'staff',
                            component: AdminManageStaff
                        },
                        {
                            name: 'manage-trekkers',
                            path: 'trekker'
                        },
                        {
                            name: 'manage-treks',
                            path: 'treks'
                        }
                    ]
                },
                {
                    name:'add-staff',
                    path:'addStaff',
                    component: AdminAddStaff
                },
                {
                    name:'bookings',
                    path:'bookings'
                },
                {
                    name:'reports',
                    path:'reports'
                }
            ]
        },
        {
            name:'trekker',
            path: '/trekker',
            beforeEnter(to,from){
                if(!store.getters.getRoles.includes("trekker")){
                    return {name:"login"}
                }
            },
            component: TrekkerLayout,
            children: [
                {
                    name:'register',
                    path:'register',
                    component: TrekkerRegister
                },
                {
                    name:'trekker-dashboard',
                    path:'home',
                    component: TrekkerDashboard
                }
            ]
        },
        {
            name: 'staff',
            path: '/staff',
            beforeEnter(to,from){
                if(!store.getters.getRoles.includes("staff")){
                    return {name:"login"}
                }
            },
            component: StaffLayout,
            children: [
                {
                    name: 'staff-dashboard',
                    path: 'home',
                    component: StaffDashboard
                }
            ]
        }
    ]
}
)
export default router