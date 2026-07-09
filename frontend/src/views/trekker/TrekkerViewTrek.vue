<script setup>
import { useRoute } from "vue-router";
const route = useRoute();
</script>

<template>
<div v-if="showAlert" class="alert alert-dismissible fade show" :class="'alert-' + alertType" role="alert">
  {{ alertMessage }}
  <button type="button" class="btn-close" @click="showAlert = false"></button>
</div>
 <div class="container-fluid">
    <div class="row">
    <div class="col-lg-4 col-md-6 col-sm-12 mb-3">
        <img :src="server + 'uploads/' + image_url" :alt="name" class="img-fluid rounded" style="width:100%;height:400px;object-fit: cover;">
    </div>
    <div class="col-lg-8 col-md-6 col-sm-12 text-center">
        <div class="row g-2">
          <h3>{{ name }}</h3>
          <p><i class="fas fa-align-left"></i>{{ description }}</p>
          <p>Start Date: {{ start_date }}</p> 
          <p>End Date: {{ end_date }}</p>
          <p>Reporting Time: {{ reporting_time }}</p>
          <p>Location: {{ location }}</p> 
          <p>Difficulty: {{ difficulty }}</p>
          <p>Slots: {{ slots }}</p>
          <p>Status: <span class="badge" :class="{ 'bg-success': status === 'O', 'bg-danger': status !== 'O' }">{{ status=='O' ? 'Open' : 'Closed' }}</span></p>
        </div>
    </div>
    </div>
    <div class="row">
      <div class="d-flex justify-content-center mt-3">
      <button class="btn btn-success me-5" data-bs-toggle="modal" data-bs-target="#bookModal">Book Trek</button>
      <button class="btn btn-primary" @click="$router.push({name:'trekker-browse-treks'})">Go Back</button>
      </div>
    </div>
  </div>
  <div class="modal fade" id="bookModal" tabindex="-1" aria-labelledby="bookModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="bookModalLabel">Book Trek</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            Are you sure you want to book this trek?
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-success" data-bs-dismiss="modal" @click="bookTrek(trekId)">Book</button>
                        </div>
                        </div>
                    </div>
  </div>
</template>

<script>
export default{
  data(){
    return{
      server: import.meta.env.VITE_SERVER,
      name: "",
      description: "",
      start_date: "",
      end_date: "",
      reporting_time: "",
      image_url: "",
      slots: 0,
      location: "",
      difficulty: "",
      status: "",
      trekId: this.$route.params.id,
      alertMessage: "",
      alertType: "danger",
      showAlert: false
    }
  },
  created(){
    fetch(import.meta.env.VITE_SERVER + "trekker/getTrek", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": this.$store.getters.getToken
      },
      body: JSON.stringify({
        id: this.$route.params.id
      })
    }).then(r=>{
      if(r.status==200){
        r.json().then(x=>{
          this.name = x.name
          this.description = x.description
          this.start_date = x.start_date
          this.end_date = x.end_date
          this.reporting_time = x.reporting_time
          this.image_url = x.image_url
          this.slots = x.slots
          this.location = x.location
          this.difficulty = x.difficulty
          this.status = x.status
        })
      }
      else{
        this.$store.commit("logout");
        this.$router.push({name: "login"});
      }
    })
  },
  methods:{
    displayAlert(message, type = "danger"){
      this.alertMessage = message;
      this.alertType = type;
      this.showAlert = true;

      setTimeout(() => {
        this.showAlert = false;
      }, 3000);
    },
    bookTrek(trekId){
      fetch(import.meta.env.VITE_SERVER + "trekker/bookTrek", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": this.$store.getters.getToken
        },
        body: JSON.stringify({
          id: trekId
        })
      }).then(async r=>{
        if(r.status==201){
          this.$router.push({name: "trekker-browse-treks"});
        }
        else if(r.status==401){
          this.$store.commit("logout");
          this.$router.push({name: "login"});
        }
        else {
        const x = await r.json();
        this.displayAlert(x.message, "danger");
      }
      })
    }
  }

}
</script>