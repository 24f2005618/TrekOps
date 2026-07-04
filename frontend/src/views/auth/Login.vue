<script setup>
import {RouterLink} from 'vue-router';
</script>
<template>
    <div class="container-fluid d-flex justify-content-center align-items-center" style="height: 100vh;">
        <div class="card">
            <div class="card-body">
                <h4 class="card-title" align="center">Login</h4>
                <form v-on:submit.prevent="login">
                    <div class="mb-3">
                        <label for="email-input" class="form-label">Email</label>
                        <input v-model="email" type="email" class="form-control" id="email-input" placeholder="johndoe@example.com">
                    </div>
                    <div class="mb-3">
                        <label for="password-input" class="form-label">Password</label>
                        <input v-model="password" type="password" class="form-control" id="password-input" placeholder="********">
                        <div class="invalid-feedback" style="display: block;" align="center">
                        {{ message }}
                        </div>
                    </div>
                    <div class="mb-3 justify-content-center d-flex">
                        <input type="submit" class="btn btn-primary" value="Login">
                    </div>
                </form>
                Don't have an account? <RouterLink to="/trekker/register">Register as Trekker</RouterLink>
            </div>
        </div>
    </div>
    
</template>
<script>
     export default {
        data(){
            return {
                email: "",
                password: "",
                message: ""
            }
        },
        methods: {
            login(){
                fetch(import.meta.env.VITE_SERVER+"signin", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({email: this.email, password:this.password})
                }).then(r =>{
                    if(r.status == 404){
                        r.json().then(x => this.message = x.message)
                    }
                    if(r.status == 200){
                        r.json().then(x=>{ 
                            this.$store.commit('setUser',x) 
                            if(x.roles.includes("trekker")){
                                this.$router.push({name: 'trekker-dashboard'
})
                            }
                            else if(x.roles.includes("staff")){
                                this.$router.push({name: 'staff-dashboard'})
                            }
                            else if(x.roles.includes("admin")){
                                this.$router.push({name: 'admin-dashboard'})
                            }
                        })
                    }
                })
            }
        }
    }
</script>