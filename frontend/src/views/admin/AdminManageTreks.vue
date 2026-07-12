<script setup>
import {RouterLink} from 'vue-router';
</script>

<template>
    <div class="alert alert-info" role="alert" v-if="message">
        {{ message }}
    </div>
    <div class="d-flex align-items-center justify-content-end position-relative">
    <h4 class="position-absolute start-50  translate-middle-x m-0">
      Treks List
    </h4>

     <RouterLink :to="{name:'add-treks'}" class="btn btn-primary"> Add Treks <i class="bi bi-plus"></i> </RouterLink> 
  </div>
<div class="position-relative mx-auto mt-4" style="width:380px;">
    <i class="bi bi-search position-absolute top-50 end-0 translate-middle-y ms-3"></i>
    <input type="search" v-model="search" class="form-control ps-5" placeholder="Search Treks" style="width: 400px;">
</div>

<table class="table  table-striped" v-if="searched_treks && searched_treks.length>0">
    <thead>
        <tr>
        <th>#</th>
        <th>Name</th>
        <th>Location</th>
        <th>Difficulty</th>
        <th>Slots</th>
        <th>Status</th>
        <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="(trek,index) in searched_treks" :key="index">
            <td>{{index+1}}</td>
            <td>{{trek.name}}</td>
            <td>{{trek.location}}</td>
            <td>{{trek.difficulty}}</td>
            <td>{{trek.slots}}</td>
            <td>
                <span v-if="trek.status=='O'" class="badge bg-success">Open</span>
                <span v-else-if="trek.status=='C'" class="badge bg-danger">Closed</span>
                <span v-else class="badge bg-secondary">Completed</span>
            </td>
            <td v-if="trek.status!='D'">
               <button class="btn btn-warning me-2" @click="$router.push({name:'edit-trek', params:{id: trek.id}})"><i class="bi bi-pencil"></i></button>
               <button class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="bi bi-trash"></i></button>
            <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="deleteModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="deleteModalLabel">Delete Trek</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            Are you sure you want to delete this trek?
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-danger" @click="deleteTrek(trek.id)">Delete</button>
                        </div>
                        </div>
                    </div>
            </div>

            </td>
        </tr>
    </tbody>
</table>
</template>
<script>
export default{
    data(){
        return{
            treks: null,
            search: "",
            message: ""
        }
    },

    created(){
       fetch(import.meta.env.VITE_SERVER+"admin/getTreks", {
        method:"GET",
        headers:{
            "Content-Type":"application/json",
            "Authentication-Token": this.$store.getters.getToken
        }
       }).then(r=>{
            if(r.status==200){
                r.json().then(x=>{
                    this.treks=x;
                })
            }
       })
    },
    computed:{
        searched_treks(){
            if(this.search.trim()==""){
                return this.treks;
            }
            else{
                return this.treks.filter(x=>x.name.toLowerCase().includes(this.search.toLowerCase()) || x.location.toLowerCase().includes(this.search.toLowerCase()) || x.difficulty.includes(this.search));
            }
        }
    },
    methods:{
        deleteTrek(trekId){
            fetch(import.meta.env.VITE_SERVER+"admin/deleteTrek", {
                method:"DELETE",
                headers:{
                    "Content-Type":"application/json",
                    "Authentication-Token": this.$store.getters.getToken
                },
                body: JSON.stringify({id: trekId})
            }).then(r=>{
                if(r.status==204){
                    this.treks = this.treks.filter(x=>x.id!=trekId);
                    document.querySelector("#deleteModal .btn-close").click();
                }
                else if(r.status==404){
                    r.json().then(x=>{
                        this.message = x.message;
                    })
                }
                else if(r.status==401){
                    this.$store.commit("logout");
                    this.$router.push({name:"login"});
                }
            })
        }
    }
}

</script>