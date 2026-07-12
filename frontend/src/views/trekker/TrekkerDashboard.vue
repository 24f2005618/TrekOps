<script>

</script>

<template>
    <!-- <h3>Welcome </h3> -->
     <div class="row g-4">
            <div class="col-12 col-sm-4">
                <div class="card h-100">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <div class="flex-grow-1">
                            <h5 class="card-title mb-1">Upcoming Treks</h5>
                            <p class="card-text display-6 mb-0 p-2">
                                {{ count.upcoming_treks }}
                            </p>
                        </div>

                        <i class="bi bi-compass fs-1 ms-3 flex-shrink-0"></i>
                    </div>
                </div>
            </div>

            <div class="col-12 col-sm-4">
                <div class="card h-100">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <div class="flex-grow-1">
                            <h5 class="card-title mb-1">Completed Treks</h5>
                            <p class="card-text display-6 mb-0 p-2">
                                {{ count.completed_treks }}
                            </p>
                        </div>

                        <i class="bi bi-check2-circle fs-1 ms-3 flex-shrink-0"></i>
                    </div>
                </div>
            </div>

            <div class="col-12 col-sm-4">
                <div class="card h-100">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <div class="flex-grow-1">
                            <h5 class="card-title mb-1">Available Treks</h5>
                            <p class="card-text display-6 mb-0 p-2">
                                {{ count.available_treks }}
                            </p>
                        </div>

                        <i class="bi bi-calendar fs-1 ms-3 flex-shrink-0"></i>
                    </div>
                </div>
            </div>
        </div>
    <div class="container-fluid mt-4" v-if="available_treks && available_treks.length > 0">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="mb-0">Available Treks</h4>

                <RouterLink :to="{ name: 'trekker-browse-treks' }" class="text-decoration-none">
                    View All Treks
                    <i class="bi bi-arrow-right"></i>
                </RouterLink>
            </div>
            <div class="row g-4">
            <div class="col-lg-3 col-md-4 col-sm-6" v-for="trek in available_treks" :key="trek.id">
                <div class="card h-100">
                    <img :src="server + '/uploads/' + trek.image_url" class="card-img-top" :alt="trek.image_url" style="height:250px; object-fit:cover;">

                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">
                            {{ trek.name }}
                        </h5>

                        <p class="card-text mb-1">
                            <strong>Location:</strong> {{ trek.location }}
                        </p>

                        <p class="card-text mb-1">
                            <strong>Difficulty:</strong> {{ trek.difficulty }}
                        </p>

                        <p class="card-text mb-1">
                            <strong>Duration:</strong> {{ trek.duration }} days
                        </p>

                        <p class="card-text">
                            <strong>Slots left:</strong> {{ trek.slots }}
                        </p>

                        <a :href="`/trekker/view/trek/${trek.id}`" class="btn btn-primary mt-auto">
                            View Details
                        </a>
                    </div>
                </div>
            </div>
        </div>

    </div>
    <div class="container-fluid mt-4" v-if="recent_bookings && recent_bookings.length>0">
        <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="mb-0">Recent Bookings</h4>

                <RouterLink :to="{ name: 'trekker-my-bookings' }" class="text-decoration-none">
                    View All Bookings
                    <i class="bi bi-arrow-right"></i>
                </RouterLink>
            </div>
        <div class="row g-4">
            <div class="col-lg-3 col-md-4 col-sm-6" v-for="booking in recent_bookings">
                <div class="card h-100">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">
                            {{ booking.trek_name }}
                        </h5>
                        <p class="card-text mb-1">
                            <strong>Location:</strong> {{ booking.location }}
                        </p>
                        <p class="card-text mb-1">
                            <strong class="pe-5">Status:</strong> 
                            <span class="badge" :class="{'bg-success': booking.status=='B', 'bg-secondary': booking.status=='D'}">
                                {{ booking.status=='B'?'Booked':'Completed' }}
                            </span>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default{
    data(){
        return{
            count:{
                upcoming_treks: 0,
                completed_treks: 0,
                available_treks: 0
            },
            available_treks: [],
            recent_bookings: [],
            server: import.meta.env.VITE_SERVER
        }
    },
    created(){
        fetch(import.meta.env.VITE_SERVER + '/trekker/getStats', {
            method: 'GET',
            headers: {
                'Authentication-Token': this.$store.getters.getToken
            }
        }).then(r=>{
            if(r.status==200){
                r.json().then(x=>{
                    this.count = x.count
                    this.available_treks = x.available_treks
                    this.recent_bookings = x.recent_bookings
                })
            }
            else{
                this.$store.dispatch('logout')
                this.$router.push({name: 'login'})
            }
        })
    }
}
</script>