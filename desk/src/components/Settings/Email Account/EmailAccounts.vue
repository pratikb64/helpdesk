<template>
  <div class="flex justify-between">
    <div class="flex flex-col gap-2">
      <h1 class="text-xl text-ink-gray-8 font-semibold">Email Accounts</h1>
      <p class="text-base text-ink-gray-6">
        Choose the email service provider you want to configure.
      </p>
    </div>
    <Button label="New" variant="solid" icon-left="plus" />
  </div>
  <!-- <div class="mt-8">
    <EmailProviders />
  </div> -->
  <div class="mt-8">
    <EmailAccountsList />
  </div>
</template>

<script setup lang="ts">
import EmailAccountsList from "./EmailAccountsList.vue";
import EmailProviders from "./EmailProviders.vue";
</script>
