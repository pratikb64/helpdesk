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
    <SlaWorkDaysListItem
      v-for="(row, index) in workDaysList"
      :key="row.name"
      :row="row"
      :columns="columns"
      :isLast="index === workDaysList.length - 1"
      :workDaysList="workDaysList"
    />
    <div
      v-if="workDaysList?.length === 0"
      class="text-center p-4 text-gray-600"
    >
      No workdays added
    </div>
  </div>
  <div
    v-if="slaDataErrors.support_and_resolution"
    class="text-red-500 text-xs mt-2"
  >
    {{ slaDataErrors.support_and_resolution }}
  </div>
  <Button variant="subtle" label="Add row" class="mt-4" @click="addWorkDay">
    <template #prefix>
      <FeatherIcon name="plus" class="h-4" />
    </template>
  </Button>
  <WorkDayModal v-model="dialog" :workDaysList="workDaysList" />
</template>

<script setup lang="ts">
import { Button } from "frappe-ui";
import { ref, watch } from "vue";
import SlaWorkDaysListItem from "./SlaWorkDaysListItem.vue";
import WorkDayModal from "./WorkDayModal.vue";
import { slaDataErrors } from "./sla";

const dialog = ref({
  show: false,
  isEditing: false,
});

const props = defineProps({
  workDaysList: {
    type: Array<any>,
    required: true,
  },
});

const addWorkDay = () => {
  dialog.value = {
    show: true,
    isEditing: false,
  };
};

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
    label: "Day",
    key: "workday",
    isRequired: true,
  },
  {
    label: "Open time",
    key: "start_time",
    isRequired: true,
  },
  {
    label: "Close time",
    key: "end_time",
    isRequired: true,
  },
];

watch(
  () => props.workDaysList,
  () => {
    dialog.value.show = false;
  }
);
</script>
