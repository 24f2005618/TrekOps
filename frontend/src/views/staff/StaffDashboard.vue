<script>
</script>

<template>
    <div class="row g-4">
            <div class="col-12 col-sm-6 col-lg-3">
                <div class="card h-100">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <div class="flex-grow-1">
                            <h5 class="card-title mb-1">Current Trek</h5>
                            <p class="card-text  mt-4 p-2">
                                {{ current_trek ? current_trek.trek_name : 'No Current Trek' }}
                            </p>
                        </div>

                        <i class="bi bi-person-walking fs-1 ms-3 flex-shrink-0"></i>
                    </div>
                </div>
            </div>
            <div class="col-12 col-sm-6 col-lg-3">
                <div class="card h-100">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <div class="flex-grow-1">
                            <h5 class="card-title mb-1">Next Trek</h5>
                            <p class="card-text mt-4 p-2">
                                {{ upcoming_treks && upcoming_treks.length > 0 ? upcoming_treks[0].trek_name : 'No Next Trek' }}
                            </p>
                        </div>

                        <i class="bi bi-skip-forward-fill fs-1 ms-3 flex-shrink-0"></i>
                    </div>
                </div>
            </div>
            <div class="col-12 col-sm-6 col-lg-3">
                <div class="card h-100">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <div class="flex-grow-1">
                            <h5 class="card-title mb-1">Upcoming Treks</h5>
                            <p class="card-text display-6 mb-0 p-2">
                                {{count.upcoming_treks}}
                            </p>
                        </div>

                        <i class="bi bi-calendar-event fs-1 ms-3 flex-shrink-0"></i>
                    </div>
                </div>
            </div>

            <div class="col-12 col-sm-6 col-lg-3">
                <div class="card h-100">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <div class="flex-grow-1">
                            <h5 class="card-title mb-1">Completed Treks</h5>
                            <p class="card-text display-6 mb-0 p-2">
                                {{ count.completed_treks }}
                            </p>
                        </div>

                        <i class="bi bi-check-circle-fill fs-1 ms-3 flex-shrink-0"></i>
                    </div>
                </div>
            </div>
    </div>
    
    <div class="card  mt-3" v-if="current_trek">
        <div class="row g-0">
            <div class="col-md-4">
    <img  :src="server+'/uploads/'+current_trek.image_url" class="img-fluid rounded-start" :alt="current_trek.image_url" style="height:100%; object-fit:cover;">
            </div>
        <div class="col-md-8">
        <div class="card-body">
            <h5>Today's Trek</h5>
            <h3 class="card-title">{{ current_trek.trek_name }}</h3>
            <p class="card-text">{{ current_trek.location }}</p>
            <p class="card-text">{{ current_trek.participants }} participants</p>
            <button class="btn btn-primary" @click="this.$router.push({ name: 'staff-view-trek', params: { id: current_trek.id } })">View Details</button>
        </div>
        </div>
        </div>
    </div>
    <div class="container-fluid mt-4" v-if="upcoming_treks && upcoming_treks.length > 0">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h4 class="mb-0">Upcoming Treks</h4>

                <RouterLink :to="{ name: 'staff-treks' }" class="text-decoration-none">
                    View All Treks
                    <i class="bi bi-arrow-right"></i>
                </RouterLink>
            </div>
            <div class="row g-4">
            <div class="col-lg-3 col-md-4 col-sm-6" v-for="trek in upcoming_treks" :key="trek.id">
                <div class="card h-100">
                    <img :src="server + '/uploads/' + trek.image_url" class="card-img-top" :alt="trek.image_url" style="height:250px; object-fit:cover;">

                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">
                            {{ trek.trek_name }}
                        </h5>

                        <p class="card-text mb-1">
                            <strong>Location:</strong> {{ trek.location }}
                        </p>

                        <p class="card-text mb-1">
                            <strong>Difficulty:</strong> {{ trek.difficulty=='H'? 'Hard': trek.difficulty=='M'?'Medium':'Easy' }}
                        </p>

                        <p class="card-text mb-1">
                            <strong>Duration:</strong> {{ trek.duration }} days
                        </p>

                        <p class="card-text">
                            <strong>Participants:</strong> {{ trek.participants }}
                        </p>

                        <a :href="`/staff/view/trek/${trek.id}`" class="btn btn-primary mt-auto">
                            View Details
                        </a>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
export default{
    data(){
        return {
            count: {
                upcoming_treks: 0,
                completed_treks: 0
            },
            current_trek: {
                "trek_name": "",
                "location": "",
                "participants": 0,
                "image_url": ""
            },
            upcoming_treks: [],
            server: import.meta.env.VITE_SERVER
        }
    },
    created(){
        fetch(import.meta.env.VITE_SERVER+"/staff/getStats",{
            method:"GET",
            headers:{
                "Authentication-Token": this.$store.getters.getToken
            }
        }).then(r=>{
            if(r.status==200){
                r.json().then(x=>{
                    this.count = x.count;
                    this.current_trek = x.current_trek;
                    this.upcoming_treks = x.upcoming_treks;
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