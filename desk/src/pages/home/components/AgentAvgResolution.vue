<template>
  <CardBase
    title="Avg. Resolution"
    :text="average + ' days'"
    :currentDuration="currentDuration"
    :percentageChange="percentageChange"
    @changeDuration="changeDuration"
  />
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import CardBase from "./CardBase.vue";
import { createResource } from "frappe-ui";

const props = defineProps({
  percentage_change: {
    type: Number,
    required: true,
  },
  average: {
    type: Number,
    required: true,
  },
  data: {
    type: Array<any>,
    required: true,
  },
});

const currentDuration = ref("Last month");

const average = computed(() => {
  const _average = getAvgResolutionTimeResource.fetched
    ? getAvgResolutionTimeResource.data?.average
    : props.average;
  return _average > 0 ? Math.round(_average / 86400) : 0;
});
const percentageChange = computed(() => {
  const _percentageChange = getAvgResolutionTimeResource.fetched
    ? getAvgResolutionTimeResource.data?.percentage_change
    : props.percentage_change;
  return {
    icon: _percentageChange > 0 ? "arrow-up-right" : "arrow-down-left",
    value: _percentageChange > 0 ? `+${_percentageChange}` : _percentageChange,
    color: _percentageChange > 0 ? "text-green-600" : "text-red-600",
  };
});

const getAvgResolutionTimeResource = createResource({
  url: "helpdesk.api.agent_dashboard.get_avg_resolution_time",
  type: "GET",
  makeParams: () => {
    return {
      period: currentDuration.value.toLowerCase(),
    };
  },
  onSuccess: (data) => {
    console.log("@@@ getAvgFirstResponseTimeResource", data);
  },
});

const changeDuration = (period: string) => {
  currentDuration.value = period;
  getAvgResolutionTimeResource.submit();
  console.log("@@@ changeDuration", period);
};
</script>
