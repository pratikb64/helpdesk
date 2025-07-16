<template>
  <div>
    <div class="grid grid-cols-8 items-center gap-3 text-sm text-gray-600 ml-2">
      <div class="col-span-6">Name</div>
      <div class="col-span-2">Date created</div>
    </div>
    <hr class="mt-2 mx-2" />
    <div v-for="item in list" :key="item">
      <EmailAccountsListItem />
      <hr class="mx-2" />
    </div>
    <div class="mt-8">
      <h1 class="text-lg text-ink-gray-8 font-semibold">Default settings</h1>
      <div class="mt-6">
        <div class="text-base font-medium text-ink-gray-8">
          Default Incoming
        </div>
        <div class="flex justify-between mt-2 gap-4">
          <div class="text-base text-ink-gray-6 w-4/6 leading-5">
            If enabled, all replies to your company (eg: replies@yourcomany.com)
            will come to this account. Note: Only one account can be default
            incoming.
          </div>
          <div>
            <Autocomplete
              v-model="defaultIncoming"
              class="w-max"
              :options="options"
              placeholder="Select account"
              placement="bottom-end"
            >
              <template #prefix>
                <img
                  v-if="defaultIncoming"
                  :src="defaultIncoming.image"
                  class="mr-2 size-4 rounded-full"
                />
              </template>
              <template #item-prefix="{ option }">
                <img :src="option.image" class="size-4 rounded-full" />
              </template>
            </Autocomplete>
          </div>
        </div>
      </div>
      <hr class="my-4" />
      <div>
        <div class="text-base font-medium text-ink-gray-8">
          Default Outgoing
        </div>
        <div class="flex justify-between mt-2 gap-4">
          <div class="text-base text-ink-gray-6 w-4/6 leading-5">
            If enabled, all outgoing emails will be sent from this account.
            Note: Only one account can be default outgoing.
          </div>
          <div>
            <Autocomplete
              v-model="defaultIncoming"
              class="w-max"
              :options="options"
              placeholder="Select account"
              placement="bottom-end"
            >
              <template #prefix>
                <img
                  v-if="defaultIncoming"
                  :src="defaultIncoming.image"
                  class="mr-2 size-4 rounded-full"
                />
              </template>
              <template #item-prefix="{ option }">
                <img :src="option.image" class="size-4 rounded-full" />
              </template>
            </Autocomplete>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Autocomplete } from "frappe-ui";
import EmailAccountsListItem from "./EmailAccountsListItem.vue";
import { ref } from "vue";

const list = [1, 2, 3, 4, 5];
const options = [
  {
    label: "John Doe",
    value: "john-doe",
    image: "https://randomuser.me/api/portraits/men/59.jpg",
  },
  {
    label: "Jane Doeasdasdasd",
    value: "jane-doe",
    image: "https://randomuser.me/api/portraits/women/58.jpg",
  },
  {
    label: "John Smith",
    value: "john-smith",
    image: "https://randomuser.me/api/portraits/men/59.jpg",
  },
  {
    label: "Jane Smith",
    value: "jane-smith",
    image: "https://randomuser.me/api/portraits/women/59.jpg",
  },
  {
    label: "John Wayne",
    value: "john-wayne",
    image: "https://randomuser.me/api/portraits/men/57.jpg",
  },
  {
    label: "Jane Wayne",
    value: "jane-wayne",
    image: "https://randomuser.me/api/portraits/women/51.jpg",
  },
];
const defaultIncoming = ref(options[0]);
</script>
