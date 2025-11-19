<template>
  <LayoutHeader>
    <template #left-header>
      <div class="text-lg font-medium text-gray-900">Home</div>
    </template>
    <template #right-header>
      <div class="flex items-center gap-2">
        <Button
          v-if="!editing"
          :label="'Refresh'"
          variant="subtle"
          :icon-left="'refresh-ccw'"
          @click="agentDashboard.reload()"
          :disabled="agentDashboard.loading"
        />
        <Button
          v-if="editing"
          :label="'Save'"
          variant="subtle"
          :icon-left="'check'"
          @click="onSave"
        />
        <Button
          v-else
          :label="'Edit'"
          variant="subtle"
          :icon-left="'edit'"
          @click="onEdit"
          :disabled="agentDashboard.loading"
        />
        <Button
          v-if="editing"
          :label="'Cancel'"
          variant="subtle"
          @click="onCancel"
        />

        <Dropdown :options="chartsDropdown">
          <Button
            label="New"
            variant="solid"
            icon-left="plus"
            @click="onAdd"
            :disabled="agentDashboard.loading"
          />
        </Dropdown>
      </div>
    </template>
  </LayoutHeader>
  <div class="p-5 mx-auto max-w-6xl w-full">
    <div>
      <div class="text-xl font-semibold text-ink-gray-8">
        Hey, {{ userName }}
      </div>
      <!-- <div class="text-sm text-ink-gray-5 mt-1">
        You have
        <span class="font-semibold text-ink-gray-7">3 overdue responses</span>
        and
        <span class="font-semibold text-ink-gray-7">
          2 tickets about to breach SLA
        </span>
      </div> -->
      <div class="mt-5">
        <GridLayout
          v-if="layout.length > 0"
          class="h-fit w-full"
          :class="[editing ? 'mb-[20rem] !select-none' : '']"
          :cols="50"
          :rowHeight="14"
          :disabled="!editing"
          :modelValue="layout.map((item) => item.layout)"
          @update:modelValue="
            (newLayout) => {
              layout.forEach((item, idx) => {
                item.layout = newLayout[idx];
              });
            }
          "
        >
          <template #item="{ index }">
            <div class="group relative flex h-full w-full p-2 text-ink-gray-8">
              <div
                class="flex h-full w-full items-center justify-center"
                :class="
                  editing
                    ? 'pointer-events-none  [&>div:first-child]:rounded [&>div:first-child]:group-hover:ring-2 [&>div:first-child]:group-hover:ring-outline-gray-2'
                    : ''
                "
              >
                <ChartItem
                  :index="index"
                  :item="layout[index]"
                  :editing="editing"
                />
              </div>
              <div
                v-if="editing"
                class="flex absolute right-0 top-0 bg-surface-gray-6 rounded cursor-pointer opacity-0 group-hover:opacity-100"
              >
                <div
                  class="rounded p-1 hover:bg-surface-gray-5"
                  @click="layout.splice(index, 1)"
                >
                  <FeatherIcon name="trash-2" class="size-3 text-ink-white" />
                </div>
              </div>
            </div>
          </template>
        </GridLayout>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { LayoutHeader } from "@/components";
import { Button, createResource, Dropdown, GridLayout, toast } from "frappe-ui";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { computed, provide, ref, watch } from "vue";
import ChartItem from "./components/ChartItem.vue";

const { userName } = storeToRefs(useAuthStore());
const editing = ref(false);
const layout = ref([]);
const oldLayout = ref([]);
const { userId } = storeToRefs(useAuthStore());

const agentDashboard = createResource({
  url: "helpdesk.api.agent_dashboard.get_dashboard",
  auto: true,
  onSuccess(data) {
    layout.value = data;
  },
});

provide("agentDashboard", agentDashboard);
provide("dashboardData", layout);

const saveDashboard = createResource({
  url: "frappe.client.set_value",
  makeParams() {
    return {
      doctype: "HD Dashboard",
      name: userId.value,
      fieldname: "layout",
      value: JSON.stringify(layout.value),
    };
  },
  onSuccess() {
    toast.success("Dashboard saved");
  },
});

const chartsDropdown = computed(() => {
  return [
    {
      label: "My Tickets",
      onClick: () => addChart("agent_tickets", 15, 9),
    },
    {
      label: "Unresolved Tickets",
      onClick: () => addChart("unresolved_tickets", 11, 9),
    },
    {
      label: "Upcoming SLA Violations",
      onClick: () => addChart("upcoming_sla_violations", 50, 24),
    },
    {
      label: "Average Time Metrics",
      onClick: () => addChart("avg_time_metrics", 50, 24),
    },
    {
      label: "Avg. First Response Time",
      onClick: () => addChart("avg_first_response_time", 17, 9),
    },
    {
      label: "Avg. Resolution Time",
      onClick: () => addChart("avg_resolution_time", 17, 9),
    },
    {
      label: "Rating Card",
      onClick: () => addChart("rating_card", 17, 9),
    },
    {
      label: "Recently Assigned Tickets",
      onClick: () => addChart("recently_assigned_tickets", 20, 23),
    },
  ];
});

const addChart = (chart, width, height) => {
  if (!editing.value) {
    onEdit();
  }
  layout.value.unshift({
    chart: chart,
    data: {},
    layout: {
      x: 0,
      y: 0,
      w: width,
      h: height,
      i: Math.random().toString(),
      moved: false,
    },
  });
};

const onEdit = () => {
  oldLayout.value = JSON.parse(JSON.stringify(layout.value));
  editing.value = true;
};

const onSave = () => {
  saveDashboard.submit();
  editing.value = false;
};

const onCancel = () => {
  layout.value = oldLayout.value;
  editing.value = false;
};

const onAdd = () => {};

watch(
  layout,
  (newLayout) => {
    console.log("layout", newLayout);
  },
  { deep: true }
);
</script>
