<template>
  <div
    class="flex flex-col w-full h-full rounded-md p-4 min-w-72 min-h-24 max-h-[110px]"
  >
    <div class="text-ink-gray-5 text-base">My Tickets</div>
    <div class="flex flex-col gap-2 h-full w-full">
      <div class="flex items-end w-full h-full gap-2">
        <div class="text-2xl font-medium text-ink-gray-8">
          {{ props.config.total }}
        </div>
        <div class="w-full h-full">
          <EChart :options="chartConfig" />
        </div>
      </div>
      <div class="flex items-center text-sm gap-1">
        <div class="flex items-center gap-1" :class="percentageChange.color">
          <FeatherIcon :name="percentageChange.icon" class="size-4" />
          <div>{{ percentageChange.value }}%</div>
        </div>
        <Dropdown :options="durationOptions">
          <div
            class="flex items-center gap-0.5 text-ink-gray-5 hover:text-ink-gray-6 cursor-pointer"
          >
            vs {{ currentDuration.toLowerCase() }}
            <FeatherIcon name="chevron-down" class="size-4" />
          </div>
        </Dropdown>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Dropdown, FeatherIcon } from "frappe-ui";
import EChart from "./EChart.vue";
import { computed, ref } from "vue";
import { EChartsOption } from "echarts";

const props = defineProps({
  config: {
    type: Object,
    required: true,
  },
});

const currentDuration = ref("Last month");

const percentageChange = computed(() => {
  return {
    icon:
      props.config.percentage_change > 0 ? "arrow-up-right" : "arrow-down-left",
    value:
      props.config.percentage_change > 0
        ? `+${props.config.percentage_change}`
        : props.config.percentage_change,
    color:
      props.config.percentage_change > 0 ? "text-green-600" : "text-red-600",
  };
});

const chartConfig = computed<EChartsOption>(() => {
  if (!props.config.data) return {};

  const dates = props.config.data.map((item) => item.date);
  const counts = props.config.data.map((item) => item.count);

  return {
    xAxis: {
      type: "category",
      data: dates,
      show: false,
    },
    yAxis: {
      type: "value",
      show: false,
    },
    series: [
      {
        data: counts,
        type: "line",
        symbol: "none",
      },
    ],
    color: props.config.percentage_change > 0 ? "green" : "red",
    grid: {
      left: 2,
      right: 2,
      top: 2,
      bottom: 2,
    },
  };
});

const durationOptions = computed(() => {
  const options = [
    {
      label: "Last week",
      onClick: () => changeDuration("Last week"),
    },
    {
      label: "Last month",
      onClick: () => changeDuration("Last month"),
    },
    {
      label: "Last 3 months",
      onClick: () => changeDuration("Last 3 months"),
    },
  ];

  return options.filter((option) => option.label !== currentDuration.value);
});

const changeDuration = (period: string) => {
  currentDuration.value = period;
};

console.log("Card.vue props.config", props.config);
</script>
