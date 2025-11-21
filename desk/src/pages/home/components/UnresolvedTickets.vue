<template>
  <CardBase title="Unresolved Tickets" :hideCardBottom="true">
    <template #body>
      <div class="text-2xl font-medium text-ink-gray-8 mt-3">
        {{ data?.tickets || 0 }}
      </div>
    </template>
  </CardBase>
</template>

<script setup lang="ts">
import CardBase from "./CardBase.vue";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});
</script>
