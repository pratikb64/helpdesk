<template>
  <div class="h-full w-full rounded shadow">
    <div v-if="item.type == 'card'" class="w-full h-full overflow-hidden">
      <Card
        class="!items-start"
        v-if="item.data"
        :key="index"
        :config="item.data"
      />
    </div>
    <div
      class="w-full h-full overflow-hidden"
      v-else-if="item.type == 'upcoming_sla_violations'"
    >
      <UpcomingSlaViolations />
    </div>
  </div>
</template>

<script setup lang="ts">
import Card from "./Card.vue";
import UpcomingSlaViolations from "./UpcomingSlaViolations.vue";

const props = defineProps({
  index: {
    type: Number,
    required: true,
  },
  item: {
    type: Object,
    required: true,
  },
  editing: {
    type: Boolean,
    default: false,
  },
});

console.log("DashboardItem.vue props.item", props.item);
</script>
