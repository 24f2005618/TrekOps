<script setup>
</script>
<template>
    <div class="container-fluid" style="height: 100vh; width:75%">
        <h4 align="center">Change Password</h4>
        <form @submit.prevent="changePassword">
            <div class="mb-3">
                <label for="current-password-input" class="form-label">Current Password</label>
                <input v-model="form.current_password" type="password" class="form-control" id="current-password-input">
            </div>
            <div class="mb-3">
                <label for="new-password-input" class="form-label">New Password</label>
                <input v-model="form.new_password" type="password" class="form-control" id="new-password-input">
            </div>
            <div class="mb-3">
                <label for="confirm-password-input" class="form-label">Confirm New Password</label>
                <input v-model="form.confirm_password" type="password" class="form-control" id="confirm-password-input">
            </div>
            <div class="invalid-feedback" style="display: block;" align="center">
                {{message}}
            </div>
            <div align="center">
                <button type="submit" class="btn btn-primary">Change Password</button>
                <button type="button" class="btn btn-secondary m-4" @click="$router.back()">Back</button>
            </div>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            form: {
                current_password: '',
                new_password: '',
                confirm_password: ''
            },
            message: ''
        }
    },
    methods: {
        changePassword(){
            fetch(import.meta.env.VITE_SERVER+'/editPassword', {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.$store.getters.getToken
                },
                body: JSON.stringify(this.form)
            }).then(r=>{
                if(r.status==204){
                    this.$router.push({name:'staff-profile'})
                }
                else if(r.status==401){
                    this.$store.commit('logout');
                    this.$router.push({name:'login'})
                }
                else{
                    r.json().then(data=>{
                        this.message = data.message;
                    })
                }
            })
        }
    }
}
</script>