<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
	<main>
		<!-- Hero Section -->
		<section class="bg-primary text-white py-5">
			<div class="container">
				<p class="text-uppercase small mb-2">TrekOps Platform</p>
				<h1 class="display-4 fw-bold mb-3">Plan. Track. Move every trek with confidence.</h1>
				<p class="lead mb-4">
					A focused control center for trekkers, field staff, and administrators.
					Start by signing in or create a new trekker account.
				</p>

				<div class="d-flex gap-3">
					<RouterLink to="/signin" class="btn btn-light btn-lg">Sign In</RouterLink>
					<RouterLink to="/trekker/register" class="btn btn-outline-light btn-lg">Register as Trekker</RouterLink>
				</div>
			</div>
		</section>

		<!-- Features Section -->
		<section class="py-5" aria-label="Platform highlights">
			<div class="container">
				<div class="row g-4">
					<div class="col-md-4">
						<div class="card h-100 shadow-sm">
							<div class="card-body">
								<h2 class="card-title">Unified Role Access</h2>
								<p class="card-text">One secure login flow routes users to trekker, staff, or admin dashboards.</p>
							</div>
						</div>
					</div>
					<div class="col-md-4">
						<div class="card h-100 shadow-sm">
							<div class="card-body">
								<h2 class="card-title">Fast Onboarding</h2>
								<p class="card-text">New trekkers can register in minutes and immediately access their workspace.</p>
							</div>
						</div>
					</div>
					<div class="col-md-4">
						<div class="card h-100 shadow-sm">
							<div class="card-body">
								<h2 class="card-title">Operational Clarity</h2>
								<p class="card-text">Keep trips, participants, and support teams aligned from a single interface.</p>
							</div>
						</div>
					</div>
				</div>
			</div>
		</section>
	</main>
</template>