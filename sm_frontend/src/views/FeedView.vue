<template>
	<div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
		<div class="main-center col-span-3 space-y-4">
			<div class="bg-white border border-gray-200 rounded-lg">
				<FeedForm v-bind:user="null" v-bind:posts="posts" />
			</div>
			<div
				v-if="posts.length"
				class="p-4 bg-white border border-gray-200 rounded-lg"
				v-for="post in posts"
				v-bind:key="post.id">
				<FeedItem v-bind:post="post" v-on:deletePost="deletePost" />
			</div>
			<div v-else class="p-4 bg-yellow border border-gray-200 rounded-lg">
				<h1>
					Theres no posts avaible for you at this moment please touch
					grass and make some friends
				</h1>
			</div>
		</div>

		<div class="main-right col-span-1 space-y-4">
			<div v-if="user.friends_count">
				<PeopleYouMayKnow />
			</div>

			<Trends />
		</div>
	</div>
</template>

<script>
	import axios from "axios";
	import PeopleYouMayKnow from "../components/PeopleYouMayKnow.vue";
	import Trends from "../components/Trends.vue";
	import FeedItem from "../components/FeedItem.vue";
	import FeedForm from "../components/FeedForm.vue";

	export default {
		name: "FeedView",

		components: {
			PeopleYouMayKnow,
			Trends,
			FeedItem,
			FeedForm,
		},

		data() {
			return {
				posts: [],
				body: "",
				user: "",
			};
		},

		mounted() {
			this.getFeed();
		},

		methods: {
			getFeed() {
				axios
					.get("/api/posts/")
					.then((response) => {
						console.error(response.data);

						this.posts = response.data;
					})
					.catch((error) => {
						console.error(error);
					});
			},
			deletePost(id) {
				this.posts = this.posts.filter((post) => post.id !== id);
			},
		},
	};
</script>
