<script setup>
</script>

<template>
    <div class="container-fluid">
        <div class="d-flex">
        <div class="col-md-6 me-2">
            <div class="position-relative">
                <i class="bi bi-search position-absolute top-50  translate-middle-y ms-3"></i>
                <input type="search" v-model="search" class="form-control ps-5" placeholder="Search Treks" ">
            </div>
        </div>
        <div class="col-md-3 me-2">
            <select class="form-select" v-model="difficulty">
                <option selected value="">Difficulty</option>
                <option value="Easy">Easy</option>
                <option value="Medium">Medium</option>
                <option value="Hard">Hard</option>
            </select>
        </div>
        <div class="col-md-3">
            <select class="form-select" v-model="location">
                <option selected value="">Location</option>
                <option v-for="location in locations" :key="location.name" :value="location.name">
                    {{ location.name }}
                </option>
            </select>
        </div>
        </div>
    </div>
    <div class="container-fluid mt-4" v-if="searched_treks && searched_treks.length > 0">
        <div class="row g-4">
            <div class="col-lg-3 col-md-4 col-sm-6" v-for="trek in searched_treks" :key="trek.id">
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
    <div class="container-fluid" v-else>
        <div class="alert alert-info mt-4" role="alert">
            No treks found.
        </div>
    </div>
</template>

<script>
export default{
    data(){
        return{
            server: import.meta.env.VITE_SERVER,
            search : '',
            location: '',
            difficulty: '',
            treks: []
        }
    },
    computed:{
        locations(){
            const uniqueLocations = new Set(this.treks.map(trek => trek.location));
            return Array.from(uniqueLocations).map((location, index) => ({ name: location }));
        },
        searched_treks(){
            return this.treks.filter(trek => {
                const matchesSearch = trek.name.toLowerCase().includes(this.search.toLowerCase());
                const matchesLocation = this.location ? trek.location === this.location : true;
                const matchesDifficulty = this.difficulty ? trek.difficulty === this.difficulty : true;
                return matchesSearch && matchesLocation && matchesDifficulty;
            });
        }
    },
    created(){
        this.getTreks();
    },
    methods: {
        getTreks() {
            fetch(import.meta.env.VITE_SERVER + "trekker/getTreks", {
                method:"GET",
                headers:{
                    "Content-Type":"application/json",
                    "Authentication-Token": this.$store.getters.getToken
                }
            })
            .then(r=>{
                if(r.status==200){
                    r.json().then(x=>{
                    this.treks = x;
                    })
                }
                else if(r.status==401){
                    this.$store.commit('logout');
                    this.$router.push({name:'login'});
                }
            })
        }
    }
}
</script>