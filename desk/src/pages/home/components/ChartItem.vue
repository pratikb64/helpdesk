<template>
  <div class="h-full w-full rounded border border-outline-gray-1">
    <div v-if="item.type == 'card'" class="w-full h-full overflow-hidden">
      <AgentTicketsCard
        v-if="item.chart == 'agent_tickets'"
        :data="item.data.data"
        :percentage_change="item.data.percentage_change"
        :total="item.data.total"
      />
      <AgentAvgFirstResponseCard
        v-if="item.chart == 'avg_first_response_time'"
        :data="item.data.data"
        :percentage_change="item.data.percentage_change"
        :average="item.data.average"
      />
      <AgentAvgResolution
        v-if="item.chart == 'avg_resolution_time'"
        :data="item.data.data"
        :percentage_change="item.data.percentage_change"
        :average="item.data.average"
      />
      <UnresolvedTickets
        v-if="item.chart == 'unresolved_tickets'"
        :tickets="item.data.total"
      />
      <Card
        class="!items-start"
        v-if="item.data"
        :key="index"
        :config="item.data"
      />
    </div>
    <template v-else>
      <div
        class="w-full h-full overflow-hidden"
        v-if="item.chart == 'upcoming_sla_violations'"
      >
        <UpcomingSlaViolations />
      </div>
      <div
        v-else-if="item.chart == 'recently_assigned_tickets'"
        class="overflow-hidden"
      >
        <RecentlyAssignedTickets :tickets="item.data" />
      </div>
      <div
        v-else-if="item.chart == 'rating_card'"
        class="w-full h-full overflow-hidden"
      >
        <RatingChart :config="item.data" />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import AgentAvgFirstResponseCard from "./AgentAvgFirstResponseCard.vue";
import AgentAvgResolution from "./AgentAvgResolution.vue";
import AgentTicketsCard from "./AgentTicketsCard.vue";
import Card from "./Card.vue";
import RatingChart from "./RatingChart.vue";
import RecentlyAssignedTickets from "./RecentlyAssignedTickets/RecentlyAssignedTickets.vue";
import UnresolvedTickets from "./UnresolvedTickets.vue";
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
