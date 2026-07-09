<script setup>
</script>

<template>
<h4 align="center">Add Staff</h4>
<div  class="container-fluid  justify-content-center align-items-center" style="height: 100vh; width:75%">
<form @submit.prevent="addStaff">
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
    <label for="password-input" class="form-label">Password</label>
    <input v-model="form.password" type="password" class="form-control" id="password-input">
    <div class="invalid-feedback" style="display: block;" align="center">
        {{error['password']}}
    </div>
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
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
                password: ''
            },
            error: {
                name:'',
                email: '',
                password: ''
            }
        }
    },
    watch:{
        'form.password'(value){
            this.validatePassword(value);
        }
    },
    methods:{
        validatePassword(value){
            if (value==""){
                this.error.password="";
                return false;
            }
            else if(value.length < 6){
                this.error.password = "Password must be at least 6 characters long.";
                return false;
            }
            else{
                this.error.password = "";
                return true;
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
        },
        addStaff(){
          if(!this.validateName(this.form.name)){
                this.error.name = "Name cannot be empty.";
            }
            else if(!this.validateEmail(this.form.email)){
                this.error.email = "Invalid email.";
            }
            else if(!this.validatePhone(this.form.phone)){
                this.error.phone = "Invalid phone number.";
            }
            else if(!this.validatePassword(this.form.password)){
                this.error.password = "Password must be at least 6 characters long.";
            }
            else{
                fetch(import.meta.env.VITE_SERVER+"staff/register",{
                        method:"POST",
                        headers:{
                                "Content-Type":"application/json",
                                "Authentication-Token":this.$store.state.user.token
                        },
                        body:JSON.stringify(this.form)
                }).then(r =>{
                        if(r.status == 409){
                            r.json().then(x => this.error.email = x.message)
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
                                else if(code=="ERROR0004"){
                                    this.error.password=x.message;
                                }
                                else if(code=="ERROR0005"){
                                    this.error.email=x.message;
                                }
                            })
                        }
                        if(r.status==401){
                            this.$store.commit('logout')
                            this.$router.push({name:'login'})
                        }
                        if(r.status == 201){
                            this.$router.push({name:'manage-staff'})
                        }
                    })
        }
  }
}
}
</script>