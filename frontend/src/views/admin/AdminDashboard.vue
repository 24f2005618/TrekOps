<script setup>
</script>
<template>
    <div class="container-fluid">
        <h4 class="mb-4">Dashboard</h4>

        <div class="row g-4">

            <div class="col-12 col-sm-6 col-lg-6 col-xl-3">
                <div class="card h-100">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <div class="flex-grow-1">
                            <h5 class="card-title mb-1">Total Treks</h5>
                            <p class="card-text display-6 mb-0">
                                {{ count.treks }}
                            </p>
                        </div>

                        <i class="bi bi-geo-alt fs-1 ms-3 flex-shrink-0"></i>
                    </div>
                </div>
            </div>

            <div class="col-12 col-sm-6 col-lg-6 col-xl-3">
                <div class="card h-100">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <div class="flex-grow-1">
                            <h5 class="card-title mb-1">Total Trekkers</h5>
                            <p class="card-text display-6 mb-0">
                                {{ count.trekkers }}
                            </p>
                        </div>

                        <i class="bi bi-people fs-1 ms-3 flex-shrink-0"></i>
                    </div>
                </div>
            </div>

            <div class="col-12 col-sm-6 col-lg-6 col-xl-3">
                <div class="card h-100">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <div class="flex-grow-1">
                            <h5 class="card-title mb-1">Total Staff</h5>
                            <p class="card-text display-6 mb-0">
                                {{ count.staff }}
                            </p>
                        </div>

                        <i class="bi bi-person-badge fs-1 ms-3 flex-shrink-0"></i>
                    </div>
                </div>
            </div>

            <div class="col-12 col-sm-6 col-lg-6 col-xl-3">
                <div class="card h-100">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <div class="flex-grow-1">
                            <h5 class="card-title mb-1">Total Bookings</h5>
                            <p class="card-text display-6 mb-0">
                                {{ count.bookings }}
                            </p>
                        </div>

                        <i class="bi bi-calendar fs-1 ms-3 flex-shrink-0"></i>
                    </div>
                </div>
            </div>

        </div>

        <div class="mt-5" v-if="recent_bookings.length">

            <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="mb-0">Recent Bookings</h4>

                <RouterLink :to="{ name: 'bookings' }" class="text-decoration-none">
                    View All Bookings
                    <i class="bi bi-arrow-right"></i>
                </RouterLink>
            </div>

            <div class="table-responsive">
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
                        <tr v-for="booking in recent_bookings" :key="booking.id">
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
                                <span v-else class="badge bg-secondary">
                                    Completed
                                </span>
                            </td>
                        </tr>
                    </tbody>

                </table>
            </div>

        </div>

    </div>
</template>
<script>
export default{
    data(){
        return{
            count:{
            treks: 0,
            trekkers: 0,
            staff: 0,
            bookings: 0
            },
            recent_bookings: []
        }
    },
    created(){
        fetch(import.meta.env.VITE_SERVER+"getStats", {
            method:"GET",
            headers:{
                "Authentication-Token": this.$store.getters.getToken
            }
        }).then(r =>{
            if(r.status==200){
                r.json().then(x => {
                this.count.treks = x.treks;
                this.count.trekkers = x.trekkers;
                this.count.staff = x.staff;
                this.count.bookings = x.bookings;
                this.recent_bookings = x.recent_bookings;
            })
            }  
            else{
                this.$store.commit("logout");
                this.$router.push({name:"login"});
            }
        })
    }
} 
</script>