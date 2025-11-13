<template>
  <div class="rounded-md p-4 grow min-w-[252px]">
    <div class="space-y-2">
      <div class="text-lg font-semibold text-ink-gray-8">
        Recently assigned tickets
      </div>
      <div class="text-base text-ink-gray-6">
        You have 4 new tickets this week
      </div>
    </div>
    <div class="space-y-5 mt-7">
      <RecentlyAssignedTicketsItem v-for="item in 4" :key="item" />
    </div>
  </div>
</template>

<script setup lang="ts">
import RecentlyAssignedTicketsItem from "./RecentlyAssignedTicketsItem.vue";
</script>
