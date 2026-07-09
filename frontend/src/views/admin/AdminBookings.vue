<script setup>
</script>

<template>
    <div class="container-fluid">
        <div class="row align-items-center g-3">
    <div class="col-12 col-lg-4 text-center text-lg-start">
        <h4 class="mb-0">Bookings</h4>
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
                placeholder="Search My Bookings"
            >
        </div>
    </div>
</div>
        <div class="table-responsive mt-4" v-if="searched_bookings">
                <table class="table table-striped table-hover align-middle">

                    <thead>
                        <tr>
                            <th>Booking ID</th>
                            <th>Trekker</th>
                            <th>Trek Name</th>
                            <th>Location</th>
                            <th>Booking Date</th>
                            <th>Status</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr v-for="booking in searched_bookings" :key="booking.id">
                            <td>{{ booking.id }}</td>
                            <td>{{ booking.trekker_name }}</td>
                            <td>{{ booking.trek_name }}</td>
                            <td>{{ booking.location }}</td>
                            <td>{{ booking.booking_date }}</td>
                            <td>
                                <span v-if="booking.status == 'B'" class="badge bg-success">
                                    Booked
                                </span>

                                <span v-else-if="booking.status == 'C'" class="badge bg-danger">
                                    Cancelled
                                </span>
                            </td>
                        </tr>
                    </tbody>

                </table>
            </div>
    </div>
</template>

<script>
export default{
    data(){
        return{
            bookings:[],
            search:""
        }
    },
    computed:{
        searched_bookings(){
            if(this.search.length>0){
                return this.bookings.filter(x=>x.trekker_name.toLowerCase().includes(this.search.toLowerCase()) || x.trek_name.toLowerCase().includes(this.search.toLowerCase()) || x.location.toLowerCase().includes(this.search.toLowerCase()) || x.booking_date.toLowerCase().includes(this.search.toLowerCase()) || x.status.toLowerCase().includes(this.search.toLowerCase()))
            }
            else{
                return this.bookings;
            }
        }
    },
    created(){
        fetch(import.meta.env.VITE_SERVER+"admin/getBookings", {
            method:"GET",
            headers:{
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
                this.$router.push("/login");
            }
        })
    }
}
</script>