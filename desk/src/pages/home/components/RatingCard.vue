<template>
  <div
    class="flex flex-col w-full h-full rounded-md p-4 min-h-24 max-h-[110px]"
  >
    <div class="text-ink-gray-5 text-base">Rating (Out of 5)</div>
    <div class="flex flex-col gap-2 h-full w-full">
      <div class="flex items-end w-full h-full gap-2 mt-2">
        <div class="text-2xl font-medium text-ink-gray-8">4.5</div>
        <div class="w-full h-full">
          <EChart :options="props.config" />
        </div>
      </div>
      <div class="flex items-center text-sm gap-1">
        <div class="flex items-center gap-1">
          <FeatherIcon name="arrow-up-right" class="size-4" />
          <div class="text-sm text-ink-gray-5">+7%</div>
        </div>
        <div class="text-ink-gray-5">vs last week</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FeatherIcon } from "frappe-ui";
import EChart from "./EChart.vue";

const props = defineProps({
  config: {
    type: Object,
    required: true,
  },
});

console.log("RatingCard.vue props.config", props.config);
</script>
