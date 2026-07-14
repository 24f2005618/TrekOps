<script setup>
</script>

<template>
<div class="container-fluid">
    <div class="row align-items-center g-3">
     <div class="col-lg mb-0 d-flex">
    <h4>My Bookings</h4>
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
                placeholder="Search Bookings"
            >
        </div>
    </div>
</div>

    <div class="container-fluid" v-if="searched_bookings && searched_bookings.length>0">
        <div v-if="message" class="alert alert-danger mt-3" role="alert">
        {{ message }}
        </div>
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
        <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="(booking,index) in searched_bookings" :key="index">
            <td>{{index+1}}</td>
            <td>{{booking.trek_name}}</td>
            <td>{{booking.location}}</td>
            <td>{{booking.staff}}</td>
            <td>{{booking.start_date}}</td>
            <td>{{booking.end_date}}</td>
            <td>{{booking.reporting_time}}</td>
            <td>
                <button  class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#cancelModal">
                        Cancel
                </button>
                <div class="modal fade" id="cancelModal" tabindex="-1" aria-labelledby="cancelModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="cancelModalLabel">Cancel Booking</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            Are you sure you want to cancel this booking?
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-danger" @click="cancelBooking(booking.id)">Cancel</button>
                        </div>
                        </div>
                    </div>
            </div>
            </td>
        </tr>
    </tbody>
</table>
    </div>
    <div class="container-fluid" v-else>
        <div class="alert alert-info mt-4" role="alert">
            No bookings found.
        </div>
</div>
</div>
</template>

<script>
export default{
    data(){
        return{
            bookings: [],
            search: "",
            message: ""
        }
    },
    computed:{
        searched_bookings(){
            if(this.search.trim()==""){
                return this.bookings;
            }
            else{
                return this.bookings.filter(x=>x.trek_name.toLowerCase().includes(this.search.toLowerCase()) || x.location.toLowerCase().includes(this.search.toLowerCase()) || x.staff.toLowerCase().includes(this.search.toLowerCase()));
            }
        }
    },
    created(){
        fetch(import.meta.env.VITE_SERVER + "trekker/getBookings",{
            method: "GET",
            headers: {
                "Authentication-Token": this.$store.getters.getToken
            }
        }).then(r=>{
            if(r.status==200){
                r.json().then(x=>{
                    this.bookings = x;
                })
            }
            else if(r.status==401){
                this.$store.commit("logout");
                this.$router.push({name:"login"});
            }
        })
    },
    methods:{
        cancelBooking(bookingId){
            fetch(import.meta.env.VITE_SERVER + "trekker/cancelBooking",{
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": this.$store.getters.getToken
                },
                body: JSON.stringify({id: bookingId})
            }).then(r=>{
                if(r.status==204){
                    this.bookings = this.bookings.filter(x=>x.id!=bookingId);
                    document.querySelector("#cancelModal .btn-close").click();
                }
                else if(r.status==401){
                    this.$store.commit("logout");
                    this.$router.push({name:"login"});
                }
                else if(r.status==400){
                    r.json().then(x=>{
                        this.message = x.message;
                        document.querySelector("#cancelModal .btn-close").click();
                    })
                }
            })
        }

    }
}
</script>