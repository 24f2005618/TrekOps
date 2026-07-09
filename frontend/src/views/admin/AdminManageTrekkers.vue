<script setup>
import {RouterLink} from 'vue-router';
</script>

<template>
    <div class="d-flex align-items-center justify-content-end position-relative">
    <h4 class="position-absolute start-50  translate-middle-x m-0">
      Trekkers List
    </h4>

  </div>
<div class="position-relative mx-auto mt-4" style="width:380px;">
    <i class="bi bi-search position-absolute top-50 end-0 translate-middle-y ms-3"></i>
    <input type="search" v-model="search" class="form-control ps-5" placeholder="Search Trekkers" style="width: 400px;">
</div>

<table class="table  table-striped" v-if="searched_trekkers && searched_trekkers.length>0">
    <thead>
        <tr>
        <th>#</th>
        <th>Name</th>
        <th>Email</th>
        <th>Phone</th>
        <th>Status</th>
        <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="(trekker,index) in searched_trekkers" :key="index">
            <td>{{index+1}}</td>
            <td>{{trekker.name}}</td>
            <td>{{trekker.email}}</td>
            <td>{{trekker.phone}}</td>
            <td>{{trekker.active ? "Active" : "Disabled"}}</td>
            <td>
                <button @click="toggleTrekkerStatus(trekker.id,index)" class="btn" :class="trekker.active ? 'btn-danger' : 'btn-success' ">
                        {{ trekker.active ? "Blacklist" : "Whitelist" }}
                </button>
            </td>
        </tr>
    </tbody>
</table>
</template>
<script>
export default{
    data(){
        return{
            trekkers: [],
            search: ""
        }
    },
    created(){
       fetch(import.meta.env.VITE_SERVER+"getTrekkers", {
        method:"GET",
        headers:{
            "Content-Type":"application/json",
            "Authentication-Token": this.$store.getters.getToken
        }
       }).then(r=>{
            if(r.status==200){
                r.json().then(x=>{
                    this.trekkers=x;
                })
            }
       })
    },
    computed:{
    searched_trekkers(){
        if(!this.trekkers){
            return [];
        }

        if(this.search.trim()==""){
            return this.trekkers;
        }

        return this.trekkers.filter(x =>
            x.name.toLowerCase().includes(this.search.toLowerCase()) ||
            x.email.toLowerCase().includes(this.search.toLowerCase()) ||
            x.phone.includes(this.search)
        );
        }
    },
    methods:{
        toggleTrekkerStatus(id,index){
            fetch(import.meta.env.VITE_SERVER+"toggleTrekkerStatus", {
                method:"PATCH",
                headers:{
                    "Content-Type":"application/json",
                    "Authentication-Token": this.$store.getters.getToken
                },
                body: JSON.stringify({id:id})
            }).then(r=>{
                if(r.status==204){
                    this.trekkers[index].active = !this.trekkers[index].active;
                }
            })
        }
    }
}

</script>