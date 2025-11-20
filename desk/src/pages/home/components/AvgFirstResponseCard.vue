<template>
  <CardBase
    title="Avg. First Response"
    :text="average + ' hrs'"
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
  const _average = getAvgFirstResponseTimeResource.fetched
    ? getAvgFirstResponseTimeResource.data?.average
    : props.average;
  return _average > 0 ? Math.round(_average / 3600) : 0;
});

const percentageChange = computed(() => {
  const _percentageChange = getAvgFirstResponseTimeResource.fetched
    ? getAvgFirstResponseTimeResource.data?.percentage_change
    : props.percentage_change;
  return {
    icon: _percentageChange > 0 ? "arrow-up-right" : "arrow-down-left",
    value: _percentageChange > 0 ? `+${_percentageChange}` : _percentageChange,
    color: _percentageChange > 0 ? "text-green-600" : "text-red-600",
  };
});

const getAvgFirstResponseTimeResource = createResource({
  url: "helpdesk.api.agent_dashboard.get_avg_first_response_time",
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
  getAvgFirstResponseTimeResource.submit();
  console.log("@@@ changeDuration", period);
};
</script>
