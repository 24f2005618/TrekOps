<script setup>
</script>

<template>

<div class="d-flex align-items-center position-relative mb-4">
	<i class="bi bi-arrow-left-circle fs-1" style="cursor: pointer;" @click="$router.push({ name: 'manage-routes' })"></i>

	<h4 class="position-absolute start-50 translate-middle-x mb-0">
		Add Route
	</h4>
</div>

<div  class="container-fluid  justify-content-center align-items-center mt-4" style="height: 100vh; width:75%">
<form @submit.prevent="addRoute">
<div class="d-flex">
<div class="container">
  <div class="mb-3">
	<label for="name-input" class="form-label">Name</label>
	<input v-model="form.name" type="text" class="form-control" id="name-input">
  </div>
  <div class="mb-3">
	<label for="location-input" class="form-label">Location</label>
	<input v-model="form.location" type="text" class="form-control" id="location-input">
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
	<label for="coordinates" class="form-label">Coordinates (Optional)</label>
	<input type="text" class="form-control" id="coordinates" v-model="form.coordinates">
</div>
<div class="mb-3">
	<label for="description" class="form-label">Description (Optional)</label>
	<textarea class="form-control" id="description" v-model="form.description"></textarea>
</div>
<div class="mb-3">
  <label for="routeImage" class="form-label">Upload Image</label>
  <input class="form-control" type="file" id="routeImage" accept="image/*" @change="handleImageUpload">
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
				name: '',
				location: '',
				difficulty: '',
				coordinates: '',
				description: ''
			},
			message: '',
			image: null
		}
	},
	methods:{
		validateName(value){
			return value.trim() !== '';
		},
		validateLocation(value){
			return value.trim() !== '';
		},
		validateDifficulty(value){
			return value.trim() !== '';
		},
		handleImageUpload(event) {
			this.image = event.target.files[0] || null;
		},
		addRoute(){
			if(!this.validateName(this.form.name)){
				this.message = "Name cannot be empty.";
			}
			else if(!this.validateLocation(this.form.location)){
				this.message = "Invalid location.";
			}
			else if(!this.validateDifficulty(this.form.difficulty)){
				this.message = "Invalid difficulty.";
			}
			else{
				const formData = new FormData();
				formData.append('form', JSON.stringify(this.form));
				if(this.image){
					formData.append('image', this.image);
				}
				fetch(import.meta.env.VITE_SERVER+"/admin/addRoute",{
						method:"POST",
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
						if(r.status == 201){
							this.$router.push({name:'manage-routes'})
						}
					})
		}
		}  
	}
}
</script>
