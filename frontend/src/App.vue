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
      let item = localStorage.getItem("user");
      item = (item) ? item : JSON.stringify(empty);
      this.$store.commit('setUser', JSON.parse(item));
    }
  }
</script>