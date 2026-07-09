<script setup>
</script>

<template>

<div class="d-flex align-items-center position-relative mb-4">
    <i class="bi bi-arrow-left-circle fs-1" style="cursor: pointer;" @click="$router.push({ name: 'manage-treks' })"></i>

    <h4 class="position-absolute start-50 translate-middle-x mb-0">
        Edit Trek
    </h4>
</div>
<div  class="container-fluid  justify-content-center align-items-center mt-4" style="height: 100vh; width:75%">
<form @submit.prevent="editTrek">
<div class="d-flex">
<div class="container">
  <div class="mb-3">
        <label for="route-input" class="form-label">Route</label>
        <select id="route-input" class="form-select" v-model="form.route_id">
                <option disabled value="">-- Select Route --</option>
                <option v-for="route in routes" :key="route.id" :value="route.id">
                        {{ route.name }} - {{ route.location }} ({{ route.difficulty }})
                </option>
        </select>
    </div>
    <div class="mb-3">
    <label for="slots-input" class="form-label">Maximum Slots</label>
    <input v-model="form.slots" type="number" class="form-control" id="slots-input">
  </div>
   <div class="mb-3">
        <label for="staff" class="form-label">Assign Staff</label>

        <select id="staff" class="form-select" v-model="form.staff_id">
            <option disabled value="">-- Select Staff --</option>

            <option v-for="staff in staffs" :key="staff.id" :value="staff.id">
                {{ staff.name }}
            </option>
        </select>
  </div>
  <div class="mb-3">
    <label for="difficulty" class="form-label">Difficulty Level</label>
    <select id="difficulty" class="form-select" v-model="form.difficulty">
        <option disabled value="">-- Select Difficulty --</option>

        <option v-for="difficulty in ['Hard','Medium','Easy']" :key="difficulty" :value="difficulty">
            {{ difficulty }}
        </option>
    </select>
  </div>
</div>
<div class="container">
<div class="mb-3">
  <label for="reporting-time" class="form-label">Reporting Time</label>
  <input type="time" class="form-control" id="reporting-time" v-model="form.reporting_time">
</div>
<div class="mb-3">
  <label for="start-date" class="form-label">Start Date</label>
  <input type="date" class="form-control" id="start-date" v-model="form.start_date">
</div>
<div class="mb-3">
  <label for="end-date" class="form-label">End Date</label>
  <input type="date" class="form-control" id="end-date" v-model="form.end_date">
</div>
</div>
</div>
 <div class="invalid-feedback" style="display: block;" align="center">
                        {{ message }}
</div>
<div class="align-items-center d-flex justify-content-center mt-4">
<button type="submit" class="btn btn-primary" style="width:200px;">Submit</button>
</div>
</form>
</div>
</template>

<script>
export default {
  data(){
        return{
            form:{
                route_id: '',
                slots: '',
                staff_id: '',
                reporting_time: '',
                start_date: '',
                end_date: ''
            },
            routes: [],
            staffs: [],
            message: '',
        }
    },
    created(){
      fetch(import.meta.env.VITE_SERVER+"admin/getRoutes", {
        method:"GET",
        headers:{
            "Content-Type":"application/json",
            "Authentication-Token": this.$store.getters.getToken
        }
       }).then(r=>{
            if(r.status==200){
                r.json().then(x=>{
                    this.routes=x;
                })
            }
       })
      fetch(import.meta.env.VITE_SERVER+"getStaffs", {
                method:"GET",
        headers:{
            "Content-Type":"application/json",
            "Authentication-Token": this.$store.getters.getToken
        }
       }).then(r=>{
            if(r.status==200){
                r.json().then(x=>{
                    this.staffs=x;
                })
            }
       })
       fetch(import.meta.env.VITE_SERVER+"/admin/getTrek", {
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "Authentication-Token": this.$store.getters.getToken
        },
        body: JSON.stringify({id:this.$route.params.id})
       }).then(r=>{
            if(r.status==200){
                r.json().then(x=>{
                    this.form=x;
                })
            }
            else if(r.status==401){
                this.$store.commit("logout");
                this.$router.push({name:"login"});
            }
       })
    },
    methods:{
        validateRoute(value){
            return Number.isInteger(Number(value)) && Number(value) > 0;
        },
        validateSlots(value){
            return Number.isInteger(Number(value)) && Number(value) > 0;
        },
        validateStaff(value){
            return Number.isInteger(Number(value)) && Number(value) > 0;
        },
        validateReportingTime(value){
            return value.trim() !== '';
        },
        validateTrekDate(value){
            const today = new Date();
            today.setHours(0,0,0,0);
            const trekDate = new Date(`${value}T00:00:00`);
            return trekDate >= today;
        },
        validateEndDate(value){
            const trekDate = new Date(`${this.form.start_date}T00:00:00`);
            const endDate = new Date(`${value}T00:00:00`);
            return endDate >= trekDate;
        },
        editTrek(){
            if(!this.validateRoute(this.form.route_id)){
                this.message = "Invalid route.";
            }
            else if(!this.validateStaff(this.form.staff_id)){
                this.message = "Invalid staff member.";
            }
            else if(!this.validateReportingTime(this.form.reporting_time)){
                this.message = "Invalid reporting time.";
            }
            else if(!this.validateSlots(this.form.slots)){
                this.message = "Invalid slots.";
            }
            else if(!this.validateTrekDate(this.form.start_date)){
                this.message = "Invalid start date.";
            }
            else if(!this.validateEndDate(this.form.end_date)){
                this.message = "Invalid end date.";
            }
            else{
                const formData = new FormData();
                formData.append('form', JSON.stringify(this.form));
                fetch(import.meta.env.VITE_SERVER+"/admin/editTrek",{
                        method:"PATCH",
                        headers:{
                                "Authentication-Token":this.$store.state.user.token
                        },
                        body:formData
                }).then(r =>{
                        if(r.status == 409 || r.status == 400){
                            r.json().then(x => this.message = x.message)
                        }
                        if(r.status==401){
                            this.$store.commit('logout')
                            this.$router.push({name:'login'})
                        }
                        if(r.status == 204){
                            this.$router.push({name:'manage-treks'})
                        }
                    })
        }
        }  
    }
}
</script>