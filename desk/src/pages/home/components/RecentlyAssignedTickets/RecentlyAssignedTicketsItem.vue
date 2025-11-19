<template>
  <div
    class="flex justify-between items-center gap-2 rounded relative group/child my-2 cursor-pointer"
  >
    <div class="text-base space-y-1 grow truncate">
      <div class="font-medium text-ink-gray-7 truncate">
        {{ ticket.subject }}
      </div>
      <div class="text-ink-gray-5 truncate">
        {{ dateFormat(ticket.creation, "MMM DD, YYYY") }} · {{ ticket.name }}
      </div>
    </div>
    <div>
      <FeatherIcon name="chevron-right" class="size-5" />
    </div>
    <div
      class="absolute -top-2 -left-2 -z-10 rounded group-hover/child:bg-surface-gray-2"
      :style="{
        width: 'calc(100% + 16px)',
        height: 'calc(100% + 16px)',
      }"
    />
  </div>
</template>

<script setup lang="ts">
import { dateFormat } from "@/utils";
import { FeatherIcon } from "frappe-ui";

const props = defineProps({
  ticket: {
    type: Object,
    required: true,
  },
});
</script>
