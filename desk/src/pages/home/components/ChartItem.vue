<template>
  <div class="h-full w-full rounded border border-outline-gray-1">
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
    <div
      v-else-if="item.type == 'recently_assigned_tickets'"
      class="overflow-hidden"
    >
      <RecentlyAssignedTickets />
    </div>
    <div
      v-else-if="item.type == 'rating_card'"
      class="w-full h-full overflow-hidden"
    >
      <RatingCard :config="item.data" />
    </div>
  </div>
</template>

<script setup lang="ts">
import Card from "./Card.vue";
import RatingCard from "./RatingCard.vue";
import RecentlyAssignedTickets from "./RecentlyAssignedTickets/RecentlyAssignedTickets.vue";
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
