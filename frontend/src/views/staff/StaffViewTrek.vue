<script setup>
</script>

<template>
    <div class="container py-4" v-if="trek">
            <div class="card border-0 shadow mb-4">
                <img :src="server+'/uploads/'+trek.image_url" class="card-img-top" style="height:350px;object-fit:cover">
                <div class="card-body">
                  <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h2 class="fw-bold mb-1">{{ trek.trek_name }}</h2>

                        <div class="text-secondary">
                            <i class="bi bi-geo-alt-fill text-danger"></i>
                            {{ trek.location }}
                        </div>
                    </div>

                <div class="d-flex flex-column align-items-center gap-2" v-if="trek.status!='D'">
                    <span class="badge fs-6"
                        :class="trek.status=='O' ? 'bg-success' : 'bg-danger'">
                        {{ trek.status=='O' ? 'Open' : 'Closed' }}
                    </span>
                    <button class="btn" :class="trek.status=='O'?'btn-outline-danger':'btn-outline-success'" @click="toggleTrekStatus"> 
                        <span v-if="trek.status=='O'">
                        <i class="bi bi-lock-fill"></i>
                        Close Trek
                        </span>
                        <span v-else>
                        <i class="bi bi-unlock-fill"></i>
                        Open Trek
                        </span>
                    </button>
                </div>
                <div v-else>
                    <h4 class="text-success mt-2 me-2" style="font-weight: bold;">
                        Completed <i class="bi bi-check2-circle" style="font-size: 1.7rem;"></i>
                    </h4>
                </div>
            </div>
            <div v-if="trek.status=='O'" class="mt-4 mb-2">
                <button class="btn btn-success" @click="completeTrek">
                    Mark as Completed <i class="bi bi-check2-all"></i>
                </button>
            </div>
            </div>
    </div>
    <div class="row g-3 justify-content-center">
        <div class="col-lg-3">
            <div class="card shadow-sm">
                <div class="card-body text-center">
                    <i class="bi bi-calendar-event fs-2 text-primary"></i>

                        <h6 class="mt-3 text-muted">Start Date</h6>

                        <h5>{{ trek.start_date }}</h5>
                </div>
            </div>
        </div>
        <div class="col-lg-3">
            <div class="card shadow-sm">
                <div class="card-body text-center">
                     <i class="bi bi-calendar-check fs-2 text-success"></i>

                        <h6 class="mt-3 text-muted">End Date</h6>

                        <h5>{{ trek.end_date }}</h5>
                </div>
            </div>
        </div>
        <div class="col-lg-3">
            <div class="card shadow-sm">
                <div class="card-body text-center">
                     <i class="bi bi-people-fill fs-2 text-warning"></i>

                        <h6 class="mt-3 text-muted">Total Slots</h6>

                        <h5>{{ trek.total_slots }}</h5>
                </div>
            </div>
        </div>
                   <div class="col-lg-3">
                <div class="card shadow-sm h-100">
                    <div class="card-body text-center">
                        <i class="bi bi-person-check-fill fs-2 text-info"></i>

                        <h6 class="mt-3 text-muted">Available Slots</h6>

                        <h5>{{ trek.available_slots }}</h5>
                    </div>
                </div>
            </div>
    </div>

    <div class="card shadow-sm mt-4" v-if="trek.participants && trek.participants.length>0">

            <div class="card-header bg-white">
                <h4 class="mb-0">
                    <i class="bi bi-people-fill me-2"></i>
                 Participants
                </h4>
            </div>

            <div class="table-responsive">

                <table class="table table-hover align-middle mb-0">

                    <thead class="table-light">
                        <tr>
                            <th>#</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Booking Date</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr v-for="(participant,index) in trek.participants" :key="index">
                            <td>{{ index+1 }}</td>

                            <td>
                                <i class="bi bi-person-circle me-2"></i>
                                {{ participant.name }}
                            </td>

                            <td>{{ participant.email }}</td>

                            <td>{{ participant.phone }}</td>

                            <td>{{ participant.booking_date }}</td>
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
            trek:null,
            server:import.meta.env.VITE_SERVER
        }
    },
    created(){
        fetch(import.meta.env.VITE_SERVER+'staff/getTrek',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authentication-Token': this.$store.getters.getToken
            },
            body: JSON.stringify({id:this.$route.params.id})
        }).then(r=>{
            if(r.status==200){
                r.json().then(x=>{
                    this.trek = x;
                })
            }
            else if(r.status==401){
                this.$store.commit("logout");
                this.$router.push({name:"login"});
            }
        })
    },
    methods:{
        toggleTrekStatus(){
            fetch(import.meta.env.VITE_SERVER+'staff/toggleTrekStatus',{
                method:'PATCH',
                headers:{
                    'Content-Type':'application/json',
                    'Authentication-Token': this.$store.getters.getToken
                },
                body: JSON.stringify({id:this.$route.params.id})
            }).then(r=>{
                if(r.status==204){
                        if(this.trek.status=='O'){
                            this.trek.status = 'C';
                        }
                        else{
                            this.trek.status = 'O';
                        } 
                }
                else if(r.status==401){
                    this.$store.commit("logout");
                    this.$router.push({name:"login"});
                }
            })
        },
        completeTrek(){
            fetch(import.meta.env.VITE_SERVER+'staff/completeTrek',{
                method:'PATCH',
                headers:{
                    'Content-Type':'application/json',
                    'Authentication-Token': this.$store.getters.getToken
                },
                body: JSON.stringify({id:this.$route.params.id})
            }).then(r=>{
                if(r.status==204){
                    this.trek.status = 'D';
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