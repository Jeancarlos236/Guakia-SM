<template>
	<div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
		<div class="main-left">
			<div class="p-12 bg-white border border-gray-200 rounded-lg">
				<h1 class="mb-6 text-2xl">Edit profile</h1>

				<p class="mb-6 text-gray-500">
					Here you can edit your name and E-mail
				</p>
				<RouterLink to="/profile/edit/password" class="underline"
					>Edit Password</RouterLink
				>
			</div>
		</div>

		<div class="main-right">
			<div class="p-12 bg-white border border-gray-200 rounded-lg">
				<form class="space-y-6" v-on:submit.prevent="submitForm">
					<div>
						<label>Name</label><br />
						<input
							type="text"
							v-model="form.name"
							placeholder="Your full name"
							class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg" />
					</div>

					<div>
						<label
							>E-mail
							<br />
							<input
								type="email"
								v-model="form.email"
								placeholder="Your e-mail address"
								class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg" />
						</label>
					</div>

					<div class="mt-2 py-4">
						<label
							class="py-4 px-6 cursor-pointer bg-purple-600 text-white rounded-lg hover:bg-purple-800">
							<span class="mr-2">Change Avatar</span>
							<input
								type="file"
								ref="file"
								class="hidden"
								@change="onFileChange" />
						</label>
						<div
							class="p-4 flex justify-between items-start border-b border-gray-200">
							<div class="flex items-center space-x-3">
								<div class="w-16 h-16 relative" v-if="url">
									<img
										:src="url"
										class="w-full h-full rounded-full" />
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
												<path
													d="M6 18L18 6M6 6l12 12"></path>
											</svg>
										</button>
									</div>
								</div>
							</div>
						</div>
					</div>

					<template v-if="errors.length > 0">
						<div class="bg-red-500 text-white rounded-lg p-6">
							<p v-for="error in errors" v-bind:key="error">
								{{ error }}
							</p>
						</div>
					</template>

					<div class="flex justify-end">
						<button
							class="py-4 px-6 bg-purple-600 text-white rounded-lg hover:bg-purple-800">
							Save changes
						</button>
					</div>
				</form>
			</div>
		</div>
	</div>
</template>

<script>
	import axios from "axios";

	import { useToastStore } from "@/stores/toast";
	import { useUserStore } from "@/stores/user";

	export default {
		setup() {
			const toastStore = useToastStore();
			const userStore = useUserStore();

			return {
				toastStore,
				userStore,
			};
		},

		data() {
			return {
				form: {
					email: this.userStore.user.email,
					name: this.userStore.user.name,
				},
				errors: [],
				url: null,
			};
		},

		methods: {
			removeImage() {
				this.url = null; // Clear the image URL
				this.$refs.file.value = ""; // Reset the file input
			},
			onFileChange(e) {
				const file = e.target.files[0];
				this.url = URL.createObjectURL(file);
				if (file) {
					this.url = URL.createObjectURL(file);
				} else {
					this.url = this.useUserStore.user.get_avatar;
				}
			},
			submitForm() {
				this.errors = [];

				if (this.form.email === "") {
					this.errors.push("Your e-mail is missing");
				}

				if (this.form.name === "") {
					this.errors.push("Your name is missing");
				}

				if (this.errors.length === 0) {
					let formData = new FormData();
					formData.append("avatar", this.$refs.file.files[0]);
					formData.append("name", this.form.name);
					formData.append("email", this.form.email);

					axios
						.post("/api/editprofile/", formData, {
							headers: {
								"Content-Type": "multipart/form-data",
							},
						})
						.then((response) => {
							if (
								response.data.message === "information updated"
							) {
								this.toastStore.showToast(
									5000,
									"The information was saved",
									"bg-emerald-500",
								);

								this.userStore.setUserInfo({
									id: this.userStore.user.id,
									name: this.form.name,
									email: this.form.email,
									avatar: response.data.user.get_avatar,
								});

								this.$router.back();
							} else {
								this.toastStore.showToast(
									5000,
									`${response.data.message}. Please try again`,
									"bg-red-300",
								);
							}
						})
						.catch((error) => {
							console.log("error", error);
						});
				}
			},
		},
	};
</script>
