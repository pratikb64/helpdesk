<template>
  <CardBase
    title="Avg. First Response"
    :text="average"
    :currentDuration="currentDuration"
    :percentageChange="percentageChange"
    @changeDuration="changeDuration"
  />
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import CardBase from "./CardBase.vue";
import { createResource } from "frappe-ui";
import { formatTime } from "@/utils";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const currentDuration = ref("Last month");

const average = computed(() => {
  const _average = getAvgFirstResponseTimeResource.fetched
    ? getAvgFirstResponseTimeResource.data?.average
    : props.data?.average;
  return formatTime(_average, { day: true, hour: true, minute: true }) || "0m";
});

const percentageChange = computed(() => {
  const _percentageChange = getAvgFirstResponseTimeResource.fetched
    ? getAvgFirstResponseTimeResource.data?.percentage_change
    : props.data?.percentage_change;
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
  onSuccess: (data) => {},
});

const changeDuration = (period: string) => {
  currentDuration.value = period;
  getAvgFirstResponseTimeResource.submit();
};
</script>
