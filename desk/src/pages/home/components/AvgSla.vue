<template>
  <div class="flex flex-col rounded-md p-4 grow w-full h-full overflow-hidden">
    <div class="flex items-center justify-between">
      <div class="text-lg font-semibold text-ink-gray-8">Average SLA</div>
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
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { createResource } from "frappe-ui";

const currentDuration = ref("6m");

const getAvgSlaMetricsResource = createResource({
  url: "helpdesk.api.agent_dashboard.get_avg_sla_metrics",
  type: "GET",
  auto: true,
  makeParams: () => {
    return {
      period: currentDuration.value.toLowerCase(),
    };
  },
});

const onDurationChange = (duration: string) => {
  currentDuration.value = duration;
  getAvgSlaMetricsResource.submit();
};
</script>
