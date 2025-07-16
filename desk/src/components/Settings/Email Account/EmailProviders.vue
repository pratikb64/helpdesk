<template>
  <div>
    <span class="text-lg font-medium text-ink-gray-8"
      >Choose your email provider
    </span>
    <div class="grid grid-cols-3 gap-2 mt-2">
      <div
        v-for="email in Object.values(emailIcons)"
        class="border border-gray-300 rounded p-2 py-3 flex gap-2 items-center text-ink-gray-7 text-base font-medium cursor-pointer hover:bg-gray-50 active:bg-gray-100 hover:border-transparent select-none"
      >
        <img class="size-5" :src="email.icon" />
        {{ email.name }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { emailIcons } from "./emailConfig";
</script>
