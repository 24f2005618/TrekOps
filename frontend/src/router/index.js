import { createRouter, createWebHistory } from 'vue-router'
import store from "../store/index.js"
import Home from '../views/Home.vue'
import Login from '../views/auth/Login.vue'

import TrekkerRegister from '../views/trekker/TrekkerRegister.vue'
import TrekkerDashboard from '../views/trekker/TrekkerDashboard.vue'
import TrekkerLayout from '../views/trekker/TrekkerLayout.vue'
import TrekkerBrowseTreks from '../views/trekker/TrekkerBrowseTreks.vue'
import TrekkerViewTrek from '../views/trekker/TrekkerViewTrek.vue'
import TrekkerMyBookings from '../views/trekker/TrekkerMyBookings.vue'
import TrekkerHistory from '../views/trekker/TrekkerHistory.vue'
import TrekkerProfile from '../views/trekker/TrekkerProfile.vue'
import TrekkerEditPassword from '../views/trekker/TrekkerEditPassword.vue'
import TrekkerEditProfile from '../views/trekker/TrekkerEditProfile.vue'

import AdminLayout from '../views/admin/AdminLayout.vue'
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import AdminAddStaff from '../views/admin/AdminAddStaff.vue'
import AdminAddTrek from '../views/admin/AdminAddTrek.vue'
import AdminAddRoute from '../views/admin/AdminAddRoute.vue'
import AdminEditTrek from '../views/admin/AdminEditTrek.vue'
import AdminManageLayout from '../views/admin/AdminManageLayout.vue'
import AdminManageRoutes from '../views/admin/AdminManageRoutes.vue'
import AdminManageTreks from '../views/admin/AdminManageTreks.vue'
import AdminManageStaffs from '../views/admin/AdminManageStaffs.vue'
import AdminManageTrekkers from '../views/admin/AdminManageTrekkers.vue'
import AdminBookings from '../views/admin/AdminBookings.vue'
import AdminEditRoute from '../views/admin/AdminEditRoute.vue'

import StaffLayout from '../views/staff/StaffLayout.vue'
import StaffDashboard from '../views/staff/StaffDashboard.vue'
import StaffMyTreks from '../views/staff/StaffMyTreks.vue'
import StaffViewTrek from '../views/staff/StaffViewTrek.vue'
import StaffParticipants from '../views/staff/StaffParticipants.vue'
import StaffProfile from '../views/staff/StaffProfile.vue'
import StaffEditProfile from '../views/staff/StaffEditProfile.vue'
import StaffEditPassword from '../views/staff/StaffEditPassword.vue'

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
                            component: AdminManageStaffs
                        },
                        {
                            name: 'manage-trekkers',
                            path: 'trekker',
                            component: AdminManageTrekkers
                        },
                        {
                            name: 'manage-treks',
                            path: 'treks',
                            component: AdminManageTreks
                        },
                        {
                            name: 'manage-routes',
                            path: 'routes',
                            component: AdminManageRoutes
                        }
                    ]
                },
                {
                    name:'add-staff',
                    path:'addStaff',
                    component: AdminAddStaff
                },
                {
                    name:'add-treks',
                    path:'addTreks',
                    component: AdminAddTrek
                },
                {
                    name:'add-route',
                    path:'addRoute',
                    component: AdminAddRoute
                },
                {
                    name:'edit-trek',
                    path:'editTrek/:id',
                    component: AdminEditTrek
                },
                {
                    name:'edit-route',
                    path:'editRoute/:id',
                    component: AdminEditRoute
                },
                {
                    name:'bookings',
                    path:'bookings',
                    component: AdminBookings
                }
            ]
        },
        {
            name: 'trekker-register',
            path: '/trekker/register',
            component: TrekkerRegister
        },
        {
            name:'trekker',
            path: '/trekker',
            beforeEnter: async(to,from) => {
                if( !store.getters.getRoles.includes("trekker")){
                    return {name:"login"}
                }
                await store.dispatch("fetchUser");
            },
            component: TrekkerLayout,
            children: [
                {
                    name:'trekker-dashboard',
                    path:'home',
                    component: TrekkerDashboard
                },
                {
                    name:'trekker-browse-treks',
                    path:'search/treks',
                    component: TrekkerBrowseTreks
                },
                {
                    name:'trekker-view-trek',
                    path:'view/trek/:id',
                    component: TrekkerViewTrek
                },
                {
                    name:'trekker-my-bookings',
                    path:'bookings',
                    component: TrekkerMyBookings
                },
                {
                    name:'trekker-history',
                    path:'history',
                    component: TrekkerHistory
                },
                {
                    name:'trekker-profile',
                    path:'profile',
                    component: TrekkerProfile
                },
                {
                    name:'trekker-edit-profile',
                    path:'edit/profile',
                    component: TrekkerEditProfile
                },
                {
                    name: 'trekker-edit-password',
                    path: 'edit/password',
                    component: TrekkerEditPassword
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
                },
                {
                    name:'staff-treks',
                    path:'treks',
                    component: StaffMyTreks
                },
                {
                    name:'staff-view-trek',
                    path:'view/trek/:id',
                    component: StaffViewTrek
                },
                {
                    name:'staff-participants',
                    path:'participants',
                    component: StaffParticipants
                },
                {
                    name:'staff-profile',
                    path:'profile',
                    component: StaffProfile
                },
                {
                    name:'staff-edit-profile',
                    path:'edit/profile',
                    component: StaffEditProfile
                },
                {
                    name: 'staff-edit-password',
                    path: 'edit/password',
                    component: StaffEditPassword
                }
            ]
        }
    ]
}
)
export default router