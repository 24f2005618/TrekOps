<script setup>
import {RouterLink} from 'vue-router';
</script>

<template>
	<div class="d-flex align-items-center justify-content-end position-relative">
	<h4 class="position-absolute start-50  translate-middle-x m-0">
	  Routes List
	</h4>

	 <RouterLink :to="{name:'add-route'}" class="btn btn-primary"> Add Route <i class="bi bi-plus"></i> </RouterLink> 
  </div>
<div class="position-relative mx-auto mt-4" style="width:380px;">
	<i class="bi bi-search position-absolute top-50 end-0 translate-middle-y ms-3"></i>
	<input type="search" v-model="search" class="form-control ps-5" placeholder="Search Routes" style="width: 400px;">
</div>

<div v-if="message" class="alert alert-danger mt-3" role="alert">
	{{ message }}
</div>

<table class="table table-striped" v-if="searched_routes && searched_routes.length>0">
	<thead>
		<tr>
		<th>#</th>
		<th>Name</th>
		<th>Location</th>
		<th>Difficulty</th>
		<th>Coordinates</th>
		<th>Actions</th>
		</tr>
	</thead>
	<tbody>
		<tr v-for="(route,index) in searched_routes" :key="route.id">
			<td>{{index+1}}</td>
			<td>{{route.name}}</td>
			<td>{{route.location}}</td>
			<td>{{route.difficulty}}</td>
			<td>{{route.coordinates || '-'}}</td>
			<td>
				<button class="btn btn-warning me-2" @click="editRoute(route.id)"><i class="bi bi-pencil"></i></button>
			   <button class="btn btn-danger" :data-bs-target="`#deleteRouteModal-${route.id}`" data-bs-toggle="modal"><i class="bi bi-trash"></i></button>
			   <div class="modal fade" :id="`deleteRouteModal-${route.id}`" tabindex="-1" :aria-labelledby="`deleteRouteModalLabel-${route.id}`" aria-hidden="true">
					<div class="modal-dialog">
						<div class="modal-content">
						<div class="modal-header">
							<h1 class="modal-title fs-5" :id="`deleteRouteModalLabel-${route.id}`">Delete Route</h1>
							<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
						</div>
						<div class="modal-body">
							Are you sure you want to delete this route?
						</div>
						<div class="modal-footer">
							<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
							<button type="button" class="btn btn-danger" @click="deleteRoute(route.id)">Delete</button>
						</div>
						</div>
					</div>
			</div>

			</td>
		</tr>
	</tbody>
</table>
</template>
<script>
export default{
	data(){
		return{
			routes: null,
			search: "",
			message: ""
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
	},
	computed:{
		searched_routes(){
			if(!this.routes){
				return this.routes;
			}
			if(this.search.trim()==""){
				return this.routes;
			}
			return this.routes.filter(x=>x.name.toLowerCase().includes(this.search.toLowerCase()) || x.location.toLowerCase().includes(this.search.toLowerCase()) || x.difficulty.toLowerCase().includes(this.search.toLowerCase()) || (x.coordinates || "").toLowerCase().includes(this.search.toLowerCase()));
		}
	},
	methods:{
		deleteRoute(routeId){
			fetch(import.meta.env.VITE_SERVER+"admin/deleteRoute", {
				method:"DELETE",
				headers:{
					"Content-Type":"application/json",
					"Authentication-Token": this.$store.getters.getToken
				},
				body: JSON.stringify({id: routeId})
			}).then(r=>{
				if(r.status==204){
					this.routes = this.routes.filter(x=>x.id!=routeId);
					document.querySelector(`#deleteRouteModal-${routeId} .btn-close`).click();
				}
				else if(r.status==400 || r.status==404){
					r.json().then(x=>{
						this.message = x.message;
					})
				}
				else if(r.status==401){
					this.$store.commit("logout");
					this.$router.push({name:"login"});
				}
			})
		},
		editRoute(routeId){
			this.$router.push({name:"edit-route", params:{id:routeId}});
		}
	}
}

</script>
