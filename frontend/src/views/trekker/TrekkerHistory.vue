<script setup>
</script>

<template>

<div class="container-fluid">
    <div class="row g-4 align-items-center">
    <h4 class="col-lg-4 mb-0">Booking History</h4>
    <div class="col-lg-8">
        <div class="input-group">
            <span class="input-group-text">
                <i class="bi bi-search"></i>
            </span>
            <input type="search" v-model="search" class="form-control" placeholder="Search History">
        </div>
    </div>
</div>
    <div class="container-fluid mt-4" v-if="searched_history && searched_history.length>0">
    <table class="table  table-striped mt-4">
    <thead>
        <tr>
        <th>#</th>
        <th>Name</th>
        <th>Location</th>
        <th>Assigned Staff</th>
        <th>Start Date</th>
        <th>End Date</th>
        <th>Reporting Time</th>
        <th>Status</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="(booking,index) in searched_history" :key="index">
            <td>{{index+1}}</td>
            <td>{{booking.trek_name}}</td>
            <td>{{booking.location}}</td>
            <td>{{booking.staff}}</td>
            <td>{{booking.start_date}}</td>
            <td>{{booking.end_date}}</td>
            <td>{{booking.reporting_time}}</td>
            <td><span class="badge" :class="booking.status=='C' ? 'bg-danger' : 'bg-success'">{{booking.status=='C' ? 'Cancelled' : 'Completed'}}</span></td>
        </tr>
    </tbody>
</table>
    </div>
    <div class="container-fluid" v-else>
        <div class="alert alert-info mt-4" role="alert">
            No history found.
        </div>
    </div>
</div>
</template>

<script>
export default{
    data(){
        return{
            history: [],
            search: ""
        }
    },
    computed:{
        searched_history(){
            if(this.search.trim()==""){
                return this.history;
            }
            else{
                return this.history.filter(x=>x.trek_name.toLowerCase().includes(this.search.toLowerCase()) || x.location.toLowerCase().includes(this.search.toLowerCase()) || x.staff.toLowerCase().includes(this.search.toLowerCase()));
            }
        }
    },
    created(){
        fetch(import.meta.env.VITE_SERVER + "trekker/getHistory",{
            method: "GET",
            headers: {
                "Authentication-Token": this.$store.getters.getToken
            }
        }).then(r=>{
            if(r.status==200){
                r.json().then(x=>{
                    this.history = x;
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
                    