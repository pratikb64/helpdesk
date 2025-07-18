<template>
  <div class="px-10 py-8 overflow-y-auto">
    <div class="flex justify-between">
      <div class="flex flex-col gap-2">
        <h1 class="text-xl text-ink-gray-8 font-semibold">Email Accounts</h1>
        <p class="text-base text-ink-gray-6">
          Choose the email service provider you want to configure.
        </p>
      </div>
      <Button
        label="New"
        variant="solid"
        icon-left="plus"
        v-if="emailAccountList.data?.length > 0"
        @click="
          emailAccountActiveScreen = { screen: 'new', provider: '', data: null }
        "
      />
    </div>
    <div class="mt-6" v-if="emailAccountList.data?.length === 0">
      <EmailProviders />
    </div>
    <div class="mt-6" v-else>
      <EmailAccountsList />
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject } from "vue";
import EmailAccountsList from "./EmailAccountsList.vue";
import EmailProviders from "./EmailProviders.vue";
import { emailAccountActiveScreen } from "@/stores/emailAccount";

const emailAccountList = inject<any>("emailAccountList");
</script>
