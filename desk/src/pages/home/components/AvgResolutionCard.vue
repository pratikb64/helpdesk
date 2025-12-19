<template>
  <div class="w-full h-full overflow-hidden">
    <CardBase
      :title="__('Avg. Resolution')"
      :text="average"
      :currentDuration="currentDuration"
      :percentageChange="percentageChange"
      :chartData="chartConfig.data"
      :chartDates="chartConfig.dates"
      @changeDuration="changeDuration"
      :chartColor="chartColor"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
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

const chartColor = {
  lineColor: "#7263E8",
  gradientColor: { start: "#a093ee", end: "rgba(239, 237, 252,0)" },
};

const average = computed(() => {
  const _average = getAvgResolutionTimeResource.fetched
    ? getAvgResolutionTimeResource.data?.average
    : props.data?.average;
  return formatTime(_average, { day: true, hour: true, minute: true }) || "0m";
});

const percentageChange = computed(() => {
  const _percentageChange = getAvgResolutionTimeResource.fetched
    ? getAvgResolutionTimeResource.data?.percentage_change
    : props.data?.percentage_change;
  return {
    icon: _percentageChange > 0 ? "arrow-up-right" : "arrow-down-left",
    value: _percentageChange > 0 ? `+${_percentageChange}` : _percentageChange,
    color: _percentageChange > 0 ? "text-red-600" : "text-green-600",
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
});

const changeDuration = (period: string) => {
  currentDuration.value = period;
  getAvgResolutionTimeResource.submit();
};

const chartConfig = computed(() => {
  const isDataFetched = getAvgResolutionTimeResource.fetched;
  const _data = isDataFetched
    ? getAvgResolutionTimeResource.data?.data
    : props.data?.data;
  if (!_data) return {};

  const dates = _data.map((item: any) => item.date);
  const avg_time = _data.map((item: any) => item.avg_time);
  return {
    data: avg_time,
    dates,
  };
});

onMounted(() => {
  if (!props.data?.data) {
    getAvgResolutionTimeResource.submit();
  }
});
</script>
