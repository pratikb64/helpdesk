<template>
  <div class="h-full w-full rounded border border-outline-gray-1">
    <div
      v-if="item.chart == 'agent_tickets'"
      class="w-full h-full overflow-hidden"
    >
      <AgentTicketsCard :data="item.data" />
    </div>
    <div
      v-if="item.chart == 'avg_first_response_time'"
      class="w-full h-full overflow-hidden"
    >
      <AvgFirstResponseCard :data="item.data" />
    </div>
    <div
      v-if="item.chart == 'avg_resolution_time'"
      class="w-full h-full overflow-hidden"
    >
      <AvgResolutionCard :data="item.data" />
    </div>
    <div
      v-if="item.chart == 'unresolved_tickets'"
      class="w-full h-full overflow-hidden"
    >
      <UnresolvedTickets :data="item.data" />
    </div>
    <div
      class="w-full h-full overflow-hidden"
      v-if="item.chart == 'upcoming_sla_violations'"
    >
      <UpcomingSlaViolations :data="item.data" />
    </div>
    <div
      v-else-if="item.chart == 'recently_assigned_tickets'"
      class="overflow-hidden"
    >
      <RecentlyAssignedTickets :data="item.data" />
    </div>
    <div
      v-else-if="item.chart == 'recent_feedback'"
      class="w-full h-full overflow-hidden"
    >
      <RecentFeedback :data="item.data" />
    </div>
    <div
      v-else-if="item.chart == 'avg_time_metrics'"
      class="w-full h-full overflow-hidden flex"
    >
      <AvgTimeMetrics :data="item.data" />
    </div>
    <div
      v-else-if="item.chart == 'pending_tickets'"
      class="w-full h-full overflow-hidden"
    >
      <PendingTickets :data="item.data" />
    </div>
  </div>
</template>

<script setup lang="ts">
import AvgFirstResponseCard from "./AvgFirstResponseCard.vue";
import AvgResolutionCard from "./AvgResolutionCard.vue";
import AgentTicketsCard from "./AgentTicketsCard.vue";
import AvgTimeMetrics from "./AvgTimeMetrics.vue";
import RecentFeedback from "./RecentFeedback.vue";
import RecentlyAssignedTickets from "./RecentlyAssignedTickets.vue";
import UnresolvedTickets from "./UnresolvedTickets.vue";
import UpcomingSlaViolations from "./UpcomingSlaViolations.vue";
import PendingTickets from "./PendingTickets.vue";

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
</script>
