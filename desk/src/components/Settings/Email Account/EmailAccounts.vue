<template>
  <div class="px-10 py-8">
    <SettingsLayoutHeader
      title="Email Accounts"
      description="Choose the email service provider you want to configure."
    >
      <template #actions>
        <Button
          label="New"
          variant="solid"
          icon-left="plus"
          v-if="emailAccountList.data?.length > 0"
          @click="
            emailAccountActiveScreen = {
              screen: 'new',
              provider: '',
              data: null,
            }
          "
        />
      </template>
    </SettingsLayoutHeader>
  </div>
  <div class="px-10 pb-8 overflow-y-auto">
    <div v-if="emailAccountList.data?.length === 0">
      <EmailProviders />
    </div>
    <div v-else>
      <EmailAccountsList />
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject } from "vue";
import EmailAccountsList from "./EmailAccountsList.vue";
import EmailProviders from "./EmailProviders.vue";
import { emailAccountActiveScreen } from "@/stores/emailAccount";
import { Button } from "frappe-ui";
import SettingsLayoutHeader from "../SettingsLayoutHeader.vue";

const emailAccountList = inject<any>("emailAccountList");
</script>
