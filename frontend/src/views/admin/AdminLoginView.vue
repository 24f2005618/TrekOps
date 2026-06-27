<script setup>
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
                fetch(import.meta.env.VITE_SERVER+"/admin", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({email: this.email, password:this.password})
                }).then(r =>{
                    if(r.status == 404){
                        r.json().then(x => this.message = x.message)
                    }
                    if(r.status == 200){
                        r.json().then(x=> this.$store.commit('setUser',x))
                        this.$router.push({name: "home"})
                    }
                })
            }
        }
    }
</script>