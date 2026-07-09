<script setup>
</script>

<template>
    <div class="container-fluid d-flex justify-content-center align-items-center" style="height: 100vh;">
        <div class="card col-6">
            <div class="card-body">
                <h4 class="card-title" align="center">Register</h4>
                <form v-on:submit.prevent="register">
                    <div class="mb-3">
                        <label for="name-input" class="form-label">Name</label>
                        <input v-model="form.name" type="text" class="form-control" id="name-input" placeholder="John Doe">
                        <div class="invalid-feedback" style="display: block;" align="center">
                        {{error['name']}}
                      </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="email-input" class="form-label">Email</label>
                        <input v-model="form.email" type="email" class="form-control" id="email-input" placeholder="johndoe@example.com">
                        <div class="invalid-feedback" style="display: block;" align="center">
                        {{error['email']}}
                      </div>
                    </div>

                    <div class="mb-3">
                        <label for="email-input" class="form-label">Phone</label>
                        <input v-model="form.phone" type="text" class="form-control" id="phone-input" placeholder="1234567890">
                        <div class="invalid-feedback" style="display: block;" align="center">
                        {{error['phone']}}
                      </div>
                    </div>
                     
                    <div class="mb-3">
                        <label for="password-input" class="form-label">Password</label>
                        <input v-model="form.password" type="password" class="form-control" id="password-input" placeholder="********">
                        <div class="invalid-feedback" style="display: block;" align="center">
                        {{error['password']}}
                      </div>
                    </div>
                    <div class="mb-3 justify-content-center d-flex">
                        <input type="submit" class="btn btn-primary" value="Register" :disabled="!validatePassword(form.password)">
                    </div>
                </form>
                <div class="text-center mt-3">
                    Already have an account? <RouterLink to="/signin">Login</RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default{
    data(){
        return{
            form:{
                name: '',
                email: '',
                password: '',
                phone: ''
            },
            error: {
                name:'',
                email: '',
                password: '',
                phone: ''
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
        register(){
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
                this.error.email = "Invalid email.";
            }
            else if(!this.validatePassword(this.form.password)){
                this.error.password = "Password must be at least 6 characters long.";
            }
            else{
                fetch(import.meta.env.VITE_SERVER+"trekker/register", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify(this.form)
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
                                else if(code=="ERROR0006"){
                                    this.error.phone=x.message;
                                }
                            })
                        }
                        if(r.status == 201){
                            this.$router.push({name:'login'})
                        }
                    })
            }
        }
    }
}

</script>