<script setup>
import {RouterLink} from 'vue-router';
</script>

<template>
    <div class="d-flex align-items-center justify-content-end position-relative">
    <h4 class="position-absolute start-50  translate-middle-x m-0">
      Trekking Staffs List
    </h4>

     <RouterLink :to="{name:'add-staff'}" class="btn btn-primary"> Add Staff <i class="bi bi-plus"></i> </RouterLink> 
  </div>
<div class="position-relative mx-auto mt-4" style="width:380px;">
    <i class="bi bi-search position-absolute top-50 end-0 translate-middle-y ms-3"></i>
    <input type="search" v-model="search" class="form-control ps-5" placeholder="Search Staffs" style="width: 400px;">
</div>

<table class="table  table-striped" v-if="searched_staffs && searched_staffs.length>0">
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
        <tr v-for="(staff,index) in searched_staffs" :key="index">
            <td>{{index+1}}</td>
            <td>{{staff.name}}</td>
            <td>{{staff.email}}</td>
            <td>{{staff.phone}}</td>
            <td>{{staff.active ? "Active" : "Disabled"}}</td>
            <td>
                <button @click="toggleStaffStatus(staff.id,index)" class="btn" :class="staff.active ? 'btn-danger' : 'btn-success' ">
                        {{ staff.active ? "Blacklist" : "Whitelist" }}
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
            staffs: null,
            search: ""
        }
    },

    created(){
       fetch(import.meta.env.VITE_SERVER+"getStaffs", {
        method:"GET",
        headers:{
            "Content-Type":"application/json",
            "Authentication-Token": this.$store.getters.getToken
        }
       }).then(r=>{
            if(r.status==200){
                r.json().then(x=>{
                    this.staffs=x;
                })
            }
       })
    },
    computed:{
        searched_staffs(){
            if(this.search.trim()==""){
                return this.staffs;
            }
            else{
                return this.staffs.filter(x=>x.name.toLowerCase().includes(this.search.toLowerCase()) || x.email.toLowerCase().includes(this.search.toLowerCase()) || x.phone.includes(this.search));
            }
        }
    },
    methods:{
        toggleStaffStatus(id,index){
            fetch(import.meta.env.VITE_SERVER+"toggleStaffStatus", {
                method:"PATCH",
                headers:{
                    "Content-Type":"application/json",
                    "Authentication-Token": this.$store.getters.getToken
                },
                body: JSON.stringify({id:id})
            }).then(r=>{
                if(r.status==204){
                    this.staffs[index].active = !this.staffs[index].active;
                }
            })
        }
    }
}

</script>