<template>
  <CardBase title="Unresolved Tickets" :text="tickets" :hideCardBottom="true" />
</template>

<script setup lang="ts">
import CardBase from "./CardBase.vue";

const props = defineProps({
  tickets: {
    type: Number,
    required: true,
  },
});
</script>
