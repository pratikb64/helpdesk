<template>
  <div class="flex flex-col rounded-md p-4 grow">
    <div class="flex items-center justify-between">
      <div class="text-lg font-semibold text-ink-gray-8">
        Average Time Metrics
      </div>
      <TabButtons
        :buttons="[
          {
            label: '3M',
            value: '3m',
          },
          {
            label: '6M',
            value: '6m',
          },
          {
            label: '1Y',
            value: '1y',
          },
        ]"
        :model-value="currentDuration"
        @update:model-value="onDurationChange"
      />
    </div>
    <div class="flex flex-col mt-5 grow w-full">
      <div class="flex items-center gap-12">
        <div>
          <div class="text-lg font-medium text-ink-gray-8">
            {{ timeAverages.first_response }} min
          </div>
          <div class="text-ink-gray-5 flex items-center gap-2 mt-1">
            <div class="size-2 bg-black rounded-full" />
            Avg. first response
          </div>
        </div>
        <div>
          <div class="text-lg font-medium text-ink-gray-8">
            {{ timeAverages.resolution }} min
          </div>
          <div class="text-ink-gray-5 flex items-center gap-2 mt-1">
            <div class="size-2 bg-gray-400 rounded-full" />
            Avg. resolution time
          </div>
        </div>
      </div>
      <div class="w-full grow">
        <EChart :options="chartConfig" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import EChart from "./EChart.vue";
import { EChartsOption } from "echarts";
import { createResource, TabButtons } from "frappe-ui";

const props = defineProps({
  averages: {
    type: Object,
    required: true,
  },
  data: {
    type: Array<any>,
    required: true,
  },
});

const currentDuration = ref("6m");

const getAvgTimeMetricsResource = createResource({
  url: "helpdesk.api.agent_dashboard.get_avg_time_metrics",
  type: "GET",
  auto: true,
  makeParams: () => {
    return {
      period: currentDuration.value.toLowerCase(),
    };
  },
});

const timeAverages = computed(() => {
  const _averageFirstResponse = getAvgTimeMetricsResource.fetched
    ? getAvgTimeMetricsResource.data?.averages.first_response
    : props.averages.first_response;
  const _averageResolution = getAvgTimeMetricsResource.fetched
    ? getAvgTimeMetricsResource.data?.averages.resolution
    : props.averages.resolution;

  return {
    first_response:
      _averageFirstResponse > 0 ? Math.round(_averageFirstResponse / 3600) : 0,
    resolution:
      _averageResolution > 0 ? Math.round(_averageResolution / 3600) : 0,
  };
});

const chartConfig = computed<EChartsOption>(() => {
  const data = getAvgTimeMetricsResource.fetched
    ? getAvgTimeMetricsResource.data?.data
    : props.data;

  return {
    legend: {},
    tooltip: {},
    dataset: {
      source: data,
    },
    xAxis: {
      type: "category",
      axisLine: { show: false },
      axisTick: { show: false },
    },
    yAxis: {
      axisLabel: {
        formatter: "{value}h",
        margin: 20,
      },
      axisTick: { show: true },
      splitLine: {
        lineStyle: {
          type: "dashed",
          color: "#ddd",
          width: 0.8,
        },
      },
    },
    series: [
      {
        type: "bar",
        color: "black",
        barWidth: 20,
        itemStyle: { borderRadius: [4, 4, 0, 0] },
      },
      {
        type: "bar",
        color: "#E2E2E2",
        barWidth: 20,
        itemStyle: { borderRadius: [4, 4, 0, 0] },
      },
    ],
    grid: {
      left: 50,
      right: 50,
      top: 30,
      bottom: 30,
    },
  };
});

const onDurationChange = (duration: string) => {
  currentDuration.value = duration;
  getAvgTimeMetricsResource.submit();
};
</script>
