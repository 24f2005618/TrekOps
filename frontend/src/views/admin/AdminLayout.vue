<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>
  <div v-if="$store.getters.getRoles.includes('admin')">
    <div class="d-flex min-vh-100">

      <!-- Sidebar -->
      <aside
        class="position-fixed top-0 start-0 h-100 z-3 text-bg-dark border-end flex-column"
        :class="showSidebar ? 'd-flex' : 'd-none'"
        aria-labelledby="adminSidebarLabel"
        style="width: 280px"
      >
        <div
          class="d-flex align-items-center justify-content-between px-3 py-3 border-bottom border-secondary"
        >
          <button
            type="button"
            class="btn-close btn-close-white"
            @click="showSidebar = false"
            aria-label="Close"
          ></button>
        </div>

        <div class="p-0 d-flex flex-column flex-grow-1">
          <nav class="nav nav-pills flex-column gap-1 p-3">
            <RouterLink to="/admin/home" class="nav-link text-white" active-class="active">
              Dashboard
            </RouterLink>

            <RouterLink to="/admin/manage/treks" class="nav-link text-white" active-class="active">
              Treks
            </RouterLink>

            <RouterLink to="/admin/manage/routes" class="nav-link text-white" active-class="active">
              Routes
            </RouterLink>

            <RouterLink to="/admin/manage/staff" class="nav-link text-white" active-class="active">
              Trekking Staffs
            </RouterLink>

            <RouterLink to="/admin/manage/trekker" class="nav-link text-white" active-class="active">
              Trekkers
            </RouterLink>

            <RouterLink to="/admin/bookings" class="nav-link text-white" active-class="active">
              Bookings
            </RouterLink>

            <RouterLink to="/admin/reports" class="nav-link text-white" active-class="active">
              Reports
            </RouterLink>
            <RouterLink :to="{name:'login'}" class="position-relative top-50 text-white btn btn-danger mx-auto" active-class="active" style="width:40%" v-on:click="logout">
              Logout <i class="bi bi-indent"></i>
            </RouterLink>
          </nav>
        </div>
      </aside>

      <!-- Main Content -->
      <div
        class="flex-grow-1"
        :style="{
          marginLeft: showSidebar ? '280px' : '0',
          transition: 'margin-left 0.3s ease'
        }"
      >
        <header class="navbar navbar-expand-md navbar-dark bg-dark border-bottom px-3">
          <div class="container-fluid px-0 d-flex align-items-center justify-content-start gap-2">
            <button
              class="btn btn-link p-0 border-0 text-white text-decoration-none"
              type="button"
              @click="showSidebar = !showSidebar"
              :aria-label="showSidebar ? 'Close navigation' : 'Open navigation'"
            >
              <span
                v-if="!showSidebar"
                class="navbar-toggler-icon"
              ></span>
            </button>

            <span class="navbar-brand ms-4 mb-0 h1">
              TrekOps
            </span>
       <div class="dropdown ms-auto">
  <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
    <i class="bi bi-person-circle me-2"></i>Admin
  </button>
  <ul class="dropdown-menu dropdown-menu-dark dropdown-menu-end text-center">
    <li><a class="dropdown-item" href="#">Edit</a></li>
    <li><hr class="dropdown-divider"></li>
    <li><button class="dropdown-item text-danger" @click="logout"><b>Logout <i class="bi bi-indent"></i></b></button></li>
  </ul>
</div>
          </div>
        </header>

        <main class="p-3 p-md-4">
          <RouterView />
        </main>
      </div>

    </div>
  </div>

  <div v-else>
    <h1 align="center" class="p-5">
      You are Unauthorized!
    </h1>
  </div>
</template>

<script>
export default{
   data(){
    return{
      showSidebar: false
    }
   },
   methods:{
    logout(){
      fetch(import.meta.env.VITE_SERVER+"logout", {
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "Authentication-Token": this.$store.getters.getToken
        }
       }).then(r=>{
             this.$store.commit("logout");
              this.$router.push({name:"login"});
       })
 
    }
   }
}
</script>


