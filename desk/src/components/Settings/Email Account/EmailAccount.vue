<template>
  <div class="pb-8">
    <EmailAccounts v-if="emailAccountActiveScreen.screen === 'list'" />
    <EditEmailAccount v-if="emailAccountActiveScreen.screen === 'edit'" />
    <NewEmailAccountScreen v-if="emailAccountActiveScreen.screen === 'new'" />
  </div>
</template>

<script setup lang="ts">
import { createListResource } from "frappe-ui";
import EmailAccounts from "./EmailAccounts.vue";
import { provide } from "vue";
import { emailAccountActiveScreen } from "@/stores/emailAccount";
import EditEmailAccount from "./EditEmailAccount.vue";
import NewEmailAccountScreen from "./NewEmailAccountScreen.vue";

const emailAccountList = createListResource({
  doctype: "Email Account",
  cache: ["Email Accounts"],
  fields: ["*"],
  // filters: {
  //   email_id: "abasd",
  // },
  pageLength: 9999,
  auto: true,
});

provide("emailAccountList", emailAccountList);
</script>
