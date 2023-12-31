<template>
	<div
		v-if="conversations.length"
		class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
		<div class="main-left col-span-1">
			<div class="p-4 bg-white border border-gray-200 rounded-lg">
				<div class="space-y-4">
					<div
						class="flex items-center justify-between"
						v-for="conversation in conversations"
						v-bind:key="conversation.id"
						v-on:click="setActiveConversation(conversation.id)">
						<div class="flex items-center space-x-2">
							<template
								v-for="user in conversation.users"
								v-bind:key="user.id">
								<img
									:src="user.get_avatar"
									class="w-[50px] h-[50px] rounded-full object-cover" />
								<p
									class="text-xs font-bold"
									v-if="user.id !== userStore.user.id">
									{{ user.name }}
								</p>
							</template>
						</div>

						<span class="ml-2 text-xs text-gray-500">
							{{ conversation.modified_at_formatted }} ago</span
						>
					</div>
				</div>
			</div>
		</div>

		<div class="main-center col-span-3 space-y-4">
			<div class="bg-white border border-gray-200 rounded-lg">
				<div class="flex flex-col flex-grow p-4">
					<template
						v-for="message in activeConversation.messages"
						v-bind:key="message.id">
						<div
							class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
							v-if="message.created_by.id == userStore.user.id">
							<div>
								<div
									class="bg-purple-600 text-white p-3 rounded-l-lg rounded-br-lg">
									<p class="text-sm">{{ message.body }}</p>
								</div>
								<span class="text-xs text-gray-500 leading-none"
									>{{
										message.created_at_formatted
									}}
									ago</span
								>
							</div>
							<div class="flex-shrink-0 h-10 w-10 rounded-full">
								<img
									:src="message.created_by.get_avatar"
									class="w-[50px] h-[50px] rounded-full object-cover" />
							</div>
						</div>

						<div class="flex w-full mt-2 space-x-3 max-w-md" v-else>
							<div class="flex-shrink-0 h-10 w-10 rounded-full">
								<img
									:src="message.created_by.get_avatar"
									class="w-[50px] h-[50px] rounded-full object-cover" />
							</div>
							<div>
								<div
									class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
									<p class="text-sm">{{ message.body }}</p>
								</div>
								<span class="text-xs text-gray-500 leading-none"
									>{{
										message.created_at_formatted
									}}
									ago</span
								>
							</div>
						</div>
					</template>
				</div>
			</div>

			<div class="bg-white border border-gray-200 rounded-lg">
				<form v-on:submit="submitForm">
					<!-- on prevent? -->
					<div class="p-4">
						<textarea
							v-model="body"
							class="p-4 w-full bg-gray-100 rounded-lg"
							placeholder="What do you want to say?"></textarea>
					</div>

					<div class="p-4 border-t border-gray-100 flex justify-end">
						<button
							class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 24 24"
								fill="currentColor"
								class="w-6 h-6">
								<path
									d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
							</svg>
						</button>
					</div>
				</form>
			</div>
		</div>
	</div>
	<div v-else>
		<h1>
			You do not have any active conversation please start a conversation
			by clicking "open DM" button in the profile of another user
		</h1>
	</div>
</template>

<script>
	import axios from "axios";
	import { useUserStore } from "@/stores/user";
	import VueNativeSock from "vue-native-websocket";
	import { useSocketStoreWithOut } from '../stores/socket';
		// 	 Use the WebSocket plugin
		// app.use(VueNativeSock, webSocketUrl, {
		//   store: useSocketStoreWithOut(), // Install the socket store here
		// });

	export default {
		name: "chat",

	setup() {
    const userStore = useUserStore();

    // Set up the WebSocket connection when the component is created
    const initializeWebSocket = (conversationId) => {
      const webSocketUrl = `ws://127.0.0.1:8000/ws/chat/${conversationId}/`;
      const store = useSocketStoreWithOut();

      VueNativeSock.install(Vue, webSocketUrl, {
        store: store,
        format: "json",
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 3000,
      });

      // Add WebSocket event listeners
      VueNativeSock.addVueNativeSockListener({
        // Handle incoming WebSocket messages
        message: (event) => {
          const message = JSON.parse(event.data);
          // Handle the received message (update UI, etc.)
          console.log("Received message:", message);
        },

        // Handle WebSocket connection opened
        connect: () => {
          console.log("WebSocket connected");
        },

        // Handle WebSocket connection closed
        disconnect: () => {
          console.log("WebSocket disconnected");
        },
      });
    };

    return {
      userStore,
      initializeWebSocket,
      
    };
  },
		data() {
			return {
				conversations: [],
				activeConversation: {},
				body: "",
			};
		},

		mounted() {
			this.getConversations();
			
		},

		methods: {
			setActiveConversation(id) {
				console.log("setActiveConversation", id);

				this.activeConversation = id;
				this.initializeWebSocket(id);

     			this.getMessages();
			},
			getConversations() {
				console.log("getConversations");

				axios
					.get("/api/chat/")
					.then((response) => {
						console.log(response.data);

						this.conversations = response.data;

						if (this.conversations.length) {
							this.activeConversation = this.conversations[0].id;
						}

						this.getMessages();
					})
					.catch((error) => {
						console.log("Error geting conversations: ", error);
					});
			},

			getMessages() {
				console.log("getMessages");

				axios
					.get(`/api/chat/${this.activeConversation}/`)
					.then((response) => {
						console.log(response.data);

						this.activeConversation = response.data;
					})
					.catch((error) => {
						console.log("error getting messages: ", error);
					});
			},

			submitForm() {
				console.log("submitForm", this.body);

				axios
					.post(`/api/chat/${this.activeConversation.id}/send/`, {
						body: this.body,
					})
					.then((response) => {
						console.log(response.data);

						this.activeConversation.messages.push(response.data);
					})
					.catch((error) => {
						console.log("Error sending message: ", error);
					});
			},
		},
	};
</script>
