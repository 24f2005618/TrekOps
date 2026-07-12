<script setup>
</script>

<template>
<div class="container-fluid">
    <div class="row align-items-center g-3">
    <div class="col-12 col-lg-4">
        <h4 class="mb-0">My Treks</h4>
    </div>

    <div class="col-12 col-lg-8">
        <div class="input-group">
            <span class="input-group-text">
                <i class="bi bi-search"></i>
            </span>
            <input
                type="search"
                v-model="search"
                class="form-control"
                placeholder="Search Treks"
            >
        </div>
    </div>
</div>
</div>
<div class="container-fluid" v-if="searched_treks && searched_treks.length>0">
    <table class="table  table-striped mt-4">
    <thead>
        <tr>
        <th>#</th>
        <th>Name</th>
        <th>Location</th>
        <th>Duration (days)</th>
        <th>Participants</th>
        <th>Status</th>
        <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="(trek,index) in searched_treks" :key="index">
            <td>{{index+1}}</td>
            <td>{{trek.trek_name}}</td>
            <td>{{trek.location}}</td>
            <td>{{trek.duration}}</td>
            <td>{{trek.participants}}</td>
            <td>
                <span class="badge" :class="trek.status=='C' ? 'bg-danger' : trek.status=='O' ? 'bg-success' : 'bg-secondary'">
                    {{ trek.status=='O' ? 'Open' : trek.status=='C' ? 'Closed' : 'Completed' }}
                </span>
            </td>
            <td>
                <button  class="btn btn-primary" @click="this.$router.push({name:'staff-view-trek', params: { id: trek.id }})">
                        View Trek
                </button>
            </td>
        </tr>
    </tbody>
</table>
    </div>
    <div class="container-fluid" v-else>
        <div class="alert alert-info mt-4" role="alert">
            No treks found.
        </div>
</div>
</template>

<script>
export default {
    data(){
        return{
            search : '',
            treks : []
        }
    },
    computed:{
        searched_treks(){
            if(this.search.trim()=="")
                return this.treks;
            else
            return this.treks.filter(x=>x.trek_name.toLowerCase().includes(this.search.toLowerCase()) || x.location.toLowerCase().includes(this.search.toLowerCase()));
        }
    },
    created(){
        fetch(import.meta.env.VITE_SERVER +'staff/getTreks',{
            method:'GET',
            headers:{
                "Content-Type": "application/json",
                "Authentication-Token": this.$store.getters.getToken}
        }).then(r=>{
            if(r.status==200){
                r.json().then(x=>{
                    this.treks = x;
                })
            }
            else if(r.status==401){
                this.$store.commit("logout");
                this.$router.push({name:"login"});
            }
        })
    }
}
</script>