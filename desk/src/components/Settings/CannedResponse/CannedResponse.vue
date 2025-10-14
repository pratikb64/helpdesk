<template>
  <CannedResponseList v-if="cannedResponseActiveScreen.screen == 'list'" />
  <CannedResponseView v-else-if="cannedResponseActiveScreen.screen == 'view'" />
</template>

<script setup lang="ts">
import { createListResource, createResource } from "frappe-ui";
import CannedResponseList from "./CannedResponseList.vue";
import CannedResponseView from "./CannedResponseView.vue";
import { provide, ref } from "vue";

const cannedResponseActiveScreen = ref({
  screen: "list",
  data: null,
});
const cannedResponseSearchQuery = ref("");

const cannedResponseListData = createListResource({
  doctype: "Email Template",
  fields: ["name", "subject", "enabled", "response", "teams"],
  filters: {
    reference_doctype: "HD Ticket",
  },
  orderBy: "creation desc",
  start: 0,
  pageLength: 999,
  auto: true,
});

const teamBasedList = createResource({
  url: "helpdesk.api.canned_response.get_canned_responses",
  onSuccess: (data) => {
    console.log("teamBasedList", data);
  },
  auto: true,
});

provide("cannedResponseActiveScreen", cannedResponseActiveScreen);
provide("cannedResponseSearchQuery", cannedResponseSearchQuery);
provide("cannedResponseListData", cannedResponseListData);
</script>
