<template>
  <div class="px-10 py-8">
    <div class="flex items-center justify-between w-full">
      <div>
        <div class="flex items-center gap-2">
          <Button
            variant="ghost"
            icon-left="chevron-left"
            :label="'Add account'"
            size="md"
            class="cursor-pointer -ml-4 hover:bg-transparent focus:bg-transparent focus:outline-none focus:ring-0 focus:ring-offset-0 focus-visible:none active:bg-transparent active:outline-none active:ring-0 active:ring-offset-0 active:text-ink-gray-5 font-semibold text-ink-gray-7 text-xl hover:opacity-70"
            @click="goBack"
          />
        </div>
      </div>
    </div>
    <div class="mt-6">
      <EmailProviders />
    </div>
  </div>
</template>

<script setup lang="ts">
import { emailAccountActiveScreen } from "@/stores/emailAccount";
import EmailProviders from "./EmailProviders.vue";

const goBack = () => {
  emailAccountActiveScreen.value = {
    screen: "list",
    provider: "",
    data: null,
  };
};
</script>
