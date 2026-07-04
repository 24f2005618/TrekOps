

<template>
    <h4 align="center">Trekking Staff List</h4>
<div class="position-relative mx-auto mt-4" style="width:380px;">
    <i class="bi bi-search position-absolute top-50 end-0 translate-middle-y ms-3"></i>
    <input type="search" class="form-control ps-5" placeholder="Search Staffs" style="width: 400px;">
</div>


</template>

<script>
export default{
    data(){
        return{
            staffs: null
        }
    },
    created(){
       fetch(import.meta.env.VITE_SERVER+"getStaffs", {
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "Authentication-Token": this.$store.getters.getToken
        }
       }).then(r=>{
            if(r.status==200){
                r.json().then(x=>{
                    this.staffs=x.staffs;
                })
            }
       })
    }
}
</script>