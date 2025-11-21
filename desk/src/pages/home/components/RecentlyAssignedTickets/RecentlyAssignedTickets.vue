<template>
  <div class="rounded-md p-4 grow min-w-[252px]">
    <div class="space-y-2">
      <div class="text-lg font-semibold text-ink-gray-8">
        Recently assigned tickets
      </div>
      <div class="text-base text-ink-gray-6">
        You have
        {{ data?.count }} new tickets this week
      </div>
    </div>
    <div class="space-y-5 mt-7">
      <RecentlyAssignedTicketsItem
        v-for="item in data?.tickets"
        :ticket="item"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject } from "vue";
import RecentlyAssignedTicketsItem from "./RecentlyAssignedTicketsItem.vue";

const dashboardData = inject("dashboardData");

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});
console.log("tickets", props);
</script>
