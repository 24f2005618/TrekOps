<script setup>
</script>

<template>

<div class="container-fluid">
    <div class="row g-4">
        <h4 class="col-lg-4">My Participants</h4>
        <div class=" col-lg-8 d-flex align-items-center justify-content-end">
        <i class="bi bi-search position-relative" style="left:750px"></i>
        <input type="search" v-model="search" class="form-control" placeholder="Search Participants">
        </div>
    </div>
    <div class="container-fluid mt-4" v-if="searched_participants && searched_participants.length>0">
    <table class="table  table-striped mt-4">
    <thead>
        <tr>
        <th>#</th>
        <th>Name</th>
        <th>Email</th>
        <th>Phone</th>
        <th>Booking Date</th>
        <th>Booking Status</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="(participant,index) in searched_participants" :key="index">
            <td>{{index+1}}</td>
            <td>{{participant.name}}</td>
            <td>{{participant.email}}</td>
            <td>{{participant.phone}}</td>
            <td>{{participant.booking_date}}</td>
            <td><span class="badge" :class="participant.booking_status=='C' ? 'bg-danger' : participant.booking_status=='B' ? 'bg-success' : 'bg-secondary'">{{participant.booking_status=='C' ? 'Cancelled' :participant.booking_status=='B'? 'Booked' : 'Completed'}}</span></td>
        </tr>
    </tbody>
</table>
    </div>
    <div class="container-fluid" v-else>
        <div class="alert alert-info mt-4" role="alert">
            No Participants found.
        </div>
    </div>
</div>
</template>

<script>
export default{
    data(){
        return{
            participants: [],
            search: ""
        }
    },
    computed:{
        searched_participants(){
            if(this.search.trim()==""){
                return this.participants;
            }
            else{
                return this.participants.filter(x=>x.name.toLowerCase().includes(this.search.toLowerCase()) || x.email.toLowerCase().includes(this.search.toLowerCase()) || x.phone.toLowerCase().includes(this.search.toLowerCase()));
            }
        }
    },
    created(){
        fetch(import.meta.env.VITE_SERVER + "staff/getParticipants",{
            method: "GET",
            headers: {
                "Authentication-Token": this.$store.getters.getToken
            }
        }).then(r=>{
            if(r.status==200){
                r.json().then(x=>{
                    this.participants = x;
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
                    