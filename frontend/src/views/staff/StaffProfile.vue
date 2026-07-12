<script setup>
</script>

<template>
    <h4 align="center">Profile Details</h4>
    <div class="container mt-4">
    <div class="card p-4 col-lg-6 col-md-8 col-sm-10 mx-auto">
        <div class="row">
            <div class="fs-5  mb-3 text-center">
                <p class="p-3"><strong>Name:</strong> {{ name }}</p>
                <p class="p-3"><strong>Email:</strong> {{ email }}</p>
                <p class="p-3"><strong>Phone:</strong> {{ phone }}</p>
                <div class="d-flex justify-content-center">
                    <RouterLink :to="{name: 'staff-edit-profile'}" class="btn btn-primary">Edit Profile</RouterLink>
                    <RouterLink :to="{name: 'staff-edit-password'}" class="btn btn-secondary ms-2">Change Password</RouterLink>
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
                name: "",
                email: "",
                phone: ""
        }
    },
    created(){
        fetch(import.meta.env.VITE_SERVER + 'getProfile',{
            method:'GET',
            headers:{
                'Authentication-Token': this.$store.getters.getToken
            }}).then(r=>{
                if(r.status==200){
                    r.json().then(x=>{
                        this.name = x.name;
                        this.email = x.email;
                        this.phone = x.phone;
                    })
                }
            })
    }
}
</script>