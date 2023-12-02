<template>
	<form
		v-on:submit.prevent="submitForm"
		method="post"
		class="bg-white shadow-md rounded-lg">
		<div class="p-4 border-b border-gray-200">
			<textarea
				v-model="body"
				class="resize-none w-full bg-gray-100 rounded-lg placeholder-gray-500 text-lg p-4 focus:outline-none"
				placeholder="What's happening?"
				rows="1"
				@input="adjustTextareaHeight"
				ref="textarea"></textarea>
		</div>

		<div
			class="p-4 flex justify-between items-center border-b border-gray-200">
			<label
				class="flex items-center space-x-1 w-25 cursor-pointer bg-purple-600 text-white px-4 py-2 rounded-full hover:bg-purple-700 transition duration-300">
				<input
					type="checkbox"
					v-model="is_private"
					class="form-checkbox appearance-none" />
				<span class="flex items-center space-x-1">
					<svg
						v-if="is_private"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 24 24"
						fill="currentColor"
						class="w-6 h-6">
						<path
							fill-rule="evenodd"
							d="M12 1.5a5.25 5.25 0 00-5.25 5.25v3a3 3 0 00-3 3v6.75a3 3 0 003 3h10.5a3 3 0 003-3v-6.75a3 3 0 00-3-3v-3c0-2.9-2.35-5.25-5.25-5.25zm3.75 8.25v-3a3.75 3.75 0 10-7.5 0v3h7.5z"
							clip-rule="evenodd" />
					</svg>

					<svg
						v-else
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 24 24"
						fill="currentColor"
						class="w-6 h-6">
						<path
							d="M21.721 12.752a9.711 9.711 0 00-.945-5.003 12.754 12.754 0 01-4.339 2.708 18.991 18.991 0 01-.214 4.772 17.165 17.165 0 005.498-2.477zM14.634 15.55a17.324 17.324 0 00.332-4.647c-.952.227-1.945.347-2.966.347-1.021 0-2.014-.12-2.966-.347a17.515 17.515 0 00.332 4.647 17.385 17.385 0 005.268 0zM9.772 17.119a18.963 18.963 0 004.456 0A17.182 17.182 0 0112 21.724a17.18 17.18 0 01-2.228-4.605zM7.777 15.23a18.87 18.87 0 01-.214-4.774 12.753 12.753 0 01-4.34-2.708 9.711 9.711 0 00-.944 5.004 17.165 17.165 0 005.498 2.477zM21.356 14.752a9.765 9.765 0 01-7.478 6.817 18.64 18.64 0 001.988-4.718 18.627 18.627 0 005.49-2.098zM2.644 14.752c1.682.971 3.53 1.688 5.49 2.099a18.64 18.64 0 001.988 4.718 9.765 9.765 0 01-7.478-6.816zM13.878 2.43a9.755 9.755 0 016.116 3.986 11.267 11.267 0 01-3.746 2.504 18.63 18.63 0 00-2.37-6.49zM12 2.276a17.152 17.152 0 012.805 7.121c-.897.23-1.837.353-2.805.353-.968 0-1.908-.122-2.805-.353A17.151 17.151 0 0112 2.276zM10.122 2.43a18.629 18.629 0 00-2.37 6.49 11.266 11.266 0 01-3.746-2.504 9.754 9.754 0 016.116-3.985z" />
					</svg>

					<span>{{ is_private ? "Private" : "Public" }}</span>
				</span>
			</label>

			<label class="relative cursor-pointer">
				<input
					type="file"
					ref="file"
					@change="onFileChange"
					class="hidden" />
				<span class="text-purple-600 hover:text-purple-800">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 24 24"
						fill="currentColor"
						class="w-10 h-10">
						<path
							fill-rule="evenodd"
							d="M1.5 6a2.25 2.25 0 012.25-2.25h16.5A2.25 2.25 0 0122.5 6v12a2.25 2.25 0 01-2.25 2.25H3.75A2.25 2.25 0 011.5 18V6zM3 16.06V18c0 .414.336.75.75.75h16.5A.75.75 0 0021 18v-1.94l-2.69-2.689a1.5 1.5 0 00-2.12 0l-.88.879.97.97a.75.75 0 11-1.06 1.06l-5.16-5.159a1.5 1.5 0 00-2.12 0L3 16.061zm10.125-7.81a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0z"
							clip-rule="evenodd" />
					</svg>
				</span>
			</label>

			<button
				class="bg-purple-600 text-white px-6 py-2 rounded-full hover:bg-purple-700 transition duration-300">
				Post
			</button>
		</div>

		<div
			class="p-4 flex justify-between items-start border-b border-gray-200">
			<div class="flex items-center space-x-3">
				<div class="w-16 h-16 relative" v-if="url">
					<img :src="url" class="w-full h-full rounded-full" />
					<div
						class="absolute top-0 right-0 p-1 bg-white rounded-full">
						<button
							@click="removeImage"
							class="text-red-600 hover:text-red-800">
							<svg
								class="w-4 h-4"
								fill="none"
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								viewBox="0 0 24 24"
								stroke="currentColor">
								<path d="M6 18L18 6M6 6l12 12"></path>
							</svg>
						</button>
					</div>
				</div>
			</div>
		</div>
	</form>
</template>
<script>
	import axios from "axios";

	export default {
		props: {
			user: Object,
			posts: Array,
		},

		data() {
			return {
				body: "",
				is_private: false,
				url: null,
			};
		},

		methods: {
			removeImage() {
				this.url = null; // Clear the image URL
				this.$refs.file.value = ""; // Reset the file input
			},
			adjustTextareaHeight() {
				this.$refs.textarea.style.height = "auto";
				this.$refs.textarea.style.height = `${this.$refs.textarea.scrollHeight}px`;
			},
			onFileChange(e) {
				const file = e.target.files[0];
				this.url = URL.createObjectURL(file);
			},
			submitForm() {
				console.log("submitForm", this.body);

				let formData = new FormData();
				formData.append("image", this.$refs.file.files[0]);
				formData.append("body", this.body);
				formData.append("is_private", this.is_private);

				axios
					.post("/api/posts/create/", formData, {
						headers: {
							"Content-Type": "multipart/form-data",
						},
					})
					.then((response) => {
						console.log("data", response.data);

						this.posts.unshift(response.data);
						this.body = "";
						this.is_private = false;
						this.$refs.file.value = null;
						this.url = null;

						if (this.user) {
							this.user.posts_count += 1;
						}
					})
					.catch((error) => {
						console.log("error", error);
					});
			},
		},
	};
</script>
