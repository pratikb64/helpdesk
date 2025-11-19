<template>
  <div
    class="flex flex-col w-full h-full rounded-md p-4 min-h-24 max-h-[110px]"
  >
    <div class="text-ink-gray-8 text-lg font-semibold">Recent Feedback</div>
    <div class="flex flex-col gap-2 h-full w-full mt-4">
      <div class="flex items-end w-full h-full gap-2">
        <div class="flex flex-col gap-1">
          <div class="flex items-center gap-2">
            <div class="text-2xl font-medium text-ink-gray-8">4.5</div>
            <FeatherIcon name="info" class="size-4" />
          </div>
          <div class="text-base text-ink-gray-5">Avg rating</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FeatherIcon } from "frappe-ui";

const props = defineProps({
  config: {
    type: Object,
    required: true,
  },
});

console.log("RatingCard.vue props.config", props.config);
</script>
