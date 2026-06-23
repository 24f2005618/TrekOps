<script setup>
  import {RouterView,RouterLink} from 'vue-router'
</script>

<template>
  <nav class="navbar">
  <RouterLink to="/">Home</RouterLink>
  <RouterLink to="/about">About</RouterLink>
  </nav>
  <RouterView />
</template>