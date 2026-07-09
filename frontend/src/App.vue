<script setup>
  import {RouterView,RouterLink} from 'vue-router'
  import L from "leaflet";
  import "leaflet/dist/leaflet.css";
</script>

<template>
  <RouterView />
</template>

<script>
  export default {
    async created(){
      const empty = this.$store.state.user;
      let item = localStorage.getItem("user");
      item = (item) ? item : JSON.stringify(empty);
      this.$store.commit('setUser', JSON.parse(item));
    }
  }
</script>