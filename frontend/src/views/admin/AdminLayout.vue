<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

const showSidebar = ref(false)
</script>

<template>
  <div v-if="$store.getters.getRoles.includes('admin')">
    <div class="d-flex min-vh-100" >
      <aside
        class="position-fixed top-0 start-0 h-100 z-3 text-bg-dark border-end flex-column"
        :class="showSidebar ? 'd-flex' : 'd-none'"
        aria-labelledby="adminSidebarLabel"
        style="width: clamp(240px, 28vw, 320px)"
      >
        <div class="d-flex align-items-center justify-content-between px-3 py-3 border-bottom border-secondary">
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
          </nav>
        </div>
      </aside>

      <div class="flex-grow-1">
        <header class="navbar navbar-expand-md navbar-dark bg-dark border-bottom px-3">
          <div class="container-fluid px-0 d-flex align-items-center justify-content-start gap-2">
            <button
              class="btn btn-link p-0 border-0 text-white text-decoration-none"
              type="button"
              @click="showSidebar = !showSidebar"
              :aria-label="showSidebar ? 'Close navigation' : 'Open navigation'"
            >
              <span v-if="showSidebar" aria-hidden="true" style="font-size: 2rem; line-height: 1">&times;</span>
              <span v-else class="navbar-toggler-icon"></span>
            </button>

            <span class="navbar-brand ms-4 mb-0 h1">TrekOps</span>
          </div>
        </header>

        <main class="p-3 p-md-4">
          <RouterView />
        </main>
      </div>
    </div>
  </div>
  <div v-else>
    <h1 align="center" class="p-5">You are Unauthorized!</h1>
  </div>
</template>


