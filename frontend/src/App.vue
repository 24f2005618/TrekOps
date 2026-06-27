<script setup>
  import {RouterView,RouterLink} from 'vue-router'
</script>

<template>
  <RouterView />
</template>

<script>
  export default {
    created(){
      const empty = this.$store.state.user;
      item = localStorage.getItem("user");
      item = (item) ? item : JSON.stringify(empty);
      this.$store.setUser(JSON.parse(item));
    }
  }
</script>