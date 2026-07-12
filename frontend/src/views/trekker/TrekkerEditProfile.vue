<script setup>
</script>
<template>
    <h4 align="center">Edit Profile</h4>
<div  class="container-fluid  justify-content-center align-items-center" style="height: 100vh; width:75%">
<form @submit.prevent="editProfile">
  <div class="mb-3">
    <label for="name-input" class="form-label">Name</label>
    <input v-model="form.name" type="text" class="form-control" id="name-input">
    <div class="invalid-feedback" style="display: block;" align="center">
        {{error['name']}}
    </div>
  </div>
  <div class="mb-3">
    <label for="email-input" class="form-label">Email</label>
    <input v-model="form.email" type="email" class="form-control" id="email-input">
    <div class="invalid-feedback" style="display: block;" align="center">
        {{error['email']}}
    </div>
  </div>
  <div class="mb-3">
        <label for="phone-input" class="form-label">Phone</label>
        <input v-model="form.phone" type="text" class="form-control" id="phone-input">
        <div class="invalid-feedback" style="display: block;" align="center">
            {{error['phone']}}
        </div>
  </div>
  <div class="mb-3">
    <label for="password-input" class="form-label">Enter Your Password</label>
    <input v-model="form.password" type="password" class="form-control" id="password-input">
    <div class="invalid-feedback" style="display: block;" align="center">
        {{error['password']}}
    </div>
  </div>
  <div align="center">
  <button type="submit" class="btn btn-primary" align="center">Save Changes</button>
  <button type="button" class="btn btn-secondary m-4" align="center" @click="this.$router.back()">Back</button>
    </div>
</form>
</div>
</template>

<script>
export default {
  data(){
        return{
            form:{
                name: '',
                email: '',
                phone: '',
                password: ''
            },
            error: {
                name:'',
                email: '',
                phone: '',
                password: ''
            }
        }
    },
    methods:{
        editProfile(){
            if(!this.validateName(this.form.name)){
                this.error.name = "Name cannot be empty.";
            }
            else if(!this.validateEmail(this.form.email)){
                this.error.email = "Invalid email.";
            }
            else if(!this.validatePhone(this.form.phone)){
                this.error.phone = "Invalid phone number.";
            }
            else{
                fetch(import.meta.env.VITE_SERVER+'/updateProfile',{
                    method:'PATCH',
                    headers:{
                        'Content-Type':'application/json',
                        'Authentication-Token': this.$store.getters.getToken
                    },
                    body:JSON.stringify(this.form)
                }).then(r=>{
                    if(r.status==204){
                        this.$router.push({name:'trekker-profile'});
                    }
                    if(r.status == 409){
                            r.json().then(x => this.error.email = x.message)
                        }
                    if(r.status == 403){
                        r.json().then(x=>{
                            let code = x['code']
                            if(code=="ERROR0025"){
                                this.error.password=x.message;
                            }
                        })
                        if(code=="ERROR0025"){
                                this.error.password=x.message;
                            }
                    }
                    if(r.status == 400){
                        r.json().then(x=>{
                            let code = x['code']
                            if(code=="ERROR0002"){
                                this.error.email=x.message;
                            }
                            else if(code=="ERROR0003"){
                                this.error.name=x.message;
                            }
                            else if(code=="ERROR0005"){
                                this.error.email=x.message;
                            }
            
                        })
                    }
                    if(r.status==401){
                        this.$store.commit('logout');
                        this.$router.push({name:'login'});
                    }
                })
            }
        },
        validateEmail(value){
            if(value==""){
                this.error.email="";
                return false;
            }
            else if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)){
                this.error.email = "Invalid email.";
                return false;
            }
            else{
                this.error.email = "";
                return true;
            }
        },
        validatePhone(value){
            if(value==""){
                this.error.phone="";
                return false;
            }
            else if(!/^\d{10}$/.test(value)){
                this.error.phone = "Invalid phone number.";
                return false;
            }
            else{
                this.error.phone = "";
                return true;
            }
        },
        validateName(value){
            if(value==""){
                this.error.name="Name cannot be empty.";
                return false;
            }
            else{
                this.error.name = "";
                return true;
            }
        }
    },
    created(){
        fetch(import.meta.env.VITE_SERVER+'/getProfile',{
            method:'GET',
            headers:{
                'Authentication-Token': this.$store.getters.getToken
            }
        }).then(r=>{
            if(r.status==200){
                r.json().then(x=>{
                    this.form.name=x.name;
                    this.form.email=x.email;
                    this.form.phone=x.phone;
                })
            }
            else if(r.status==401){
                this.$store.commit('logout');
                this.$router.push({name:'login'});
            }
        })
    }
}
</script>