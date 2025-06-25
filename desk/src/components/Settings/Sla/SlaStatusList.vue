<template>
  <div class="rounded-md border p-1 border-gray-300 text-sm">
    <div
      class="grid p-2 items-center"
      :style="{
        gridTemplateColumns: getGridTemplateColumns(columns),
      }"
    >
      <div
        v-for="column in columns"
        :key="column.key"
        class="text-gray-600 overflow-hidden whitespace-nowrap text-ellipsis"
      >
        {{ column.label }}
        <span v-if="column.isRequired" class="text-red-500">*</span>
      </div>
    </div>
    <hr class="my-0.5" />
    <SlaStatusListItem
      v-for="(row, index) in statusList"
      :key="row.name"
      :row="row"
      :columns="columns"
      :isLast="index === statusList.length - 1"
      :statusList="statusList"
    />
    <div v-if="statusList?.length === 0" class="text-center p-4 text-gray-600">
      No items in the list
    </div>
  </div>
  <div class="flex items-center justify-between">
    <Button variant="subtle" label="Add row" class="mt-4" @click="addRow">
      <template #prefix>
        <FeatherIcon name="plus" class="h-4" />
      </template>
    </Button>
    <div v-if="slaDataErrors.statuses" class="text-red-500 text-xs mt-2">
      {{ slaDataErrors.statuses }}
    </div>
  </div>
  <Dialog v-model="dialog">
    <template #body-title>
      <h3 class="text-2xl font-semibold">New row</h3>
    </template>
    <template #body-content>
      <div class="flex flex-col gap-4">
        <FormControl
          :type="'select'"
          size="sm"
          variant="subtle"
          placeholder="Select Status"
          label="Status"
          v-model="statusData.status"
          :options="[
            {
              label: 'Open',
              value: 'Open',
            },
            {
              label: 'Replied',
              value: 'Replied',
            },
            {
              label: 'Resolved',
              value: 'Resolved',
            },
            {
              label: 'Closed',
              value: 'Closed',
            },
          ]"
          required
        />
        <FormControl
          :type="'select'"
          size="sm"
          variant="subtle"
          placeholder="Select Status"
          label="SLA behavior"
          v-model="statusData.sla_behavior"
          :options="[
            {
              label: 'Fulfilled',
              value: 'Fulfilled',
            },
            {
              label: 'Paused',
              value: 'Paused',
            },
          ]"
          required
        />
      </div>
    </template>
    <template #actions>
      <div class="flex justify-end">
        <div class="flex gap-2">
          <Button variant="subtle" theme="gray" @click="dialog = false">
            Cancel
          </Button>
          <Button variant="solid" @click="onSave"> Save </Button>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { Button, toast } from "frappe-ui";
import SlaStatusListItem from "./SlaStatusListItem.vue";
import { ref } from "vue";
import { slaDataErrors, validateSlaData } from "./sla";
import { watchDebounced } from "@vueuse/core";

const props = defineProps({
  statusList: {
    type: Array<any>,
    required: true,
  },
});

watchDebounced(
  () => [...props.statusList],
  () => {
    validateSlaData();
  },
  { deep: true, debounce: 300 }
);
const dialog = ref(false);
const statusData = ref({
  status: "",
  sla_behavior: "",
});

const addRow = () => {
  props.statusList.push({
    status: "Open",
    sla_behavior: "Fulfilled",
  });
};

function onSave() {
  if (!statusData.value.status) {
    toast.error("Please select a status");
    return;
  }

  if (!statusData.value.sla_behavior) {
    toast.error("Please select an SLA behavior");
    return;
  }

  const isDuplicate = props.statusList.some(
    (item) => item.status === statusData.value.status
  );

  if (isDuplicate) {
    toast.error("A status with this name already exists");
    return;
  }
  props.statusList.push(statusData.value);
  dialog.value = false;
  statusData.value = {
    status: "",
    sla_behavior: "",
  };
}

function getGridTemplateColumns(columns) {
  let columnsWidth = columns
    .map((col) => {
      let width = col.width || 1;
      if (typeof width === "number") {
        return width + "fr";
      }
      return width;
    })
    .join(" ");
  return columnsWidth + " 22px";
}
const columns = [
  {
    label: "Status",
    key: "status",
    isRequired: true,
  },
  {
    label: "SLA behavior",
    key: "sla_behavior",
    isRequired: true,
  },
];
</script>
