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
  <Button variant="subtle" label="Add row" class="mt-4" @click="dialog = true">
    <template #prefix>
      <FeatherIcon name="plus" class="h-4" />
    </template>
  </Button>
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
          placeholder="Select Workday"
          label="Workday"
          v-model="workDayData.workday"
          :options="[
            {
              label: 'Monday',
              value: 'Monday',
            },
            {
              label: 'Tuesday',
              value: 'Tuesday',
            },
            {
              label: 'Wednesday',
              value: 'Wednesday',
            },
            {
              label: 'Thursday',
              value: 'Thursday',
            },
            {
              label: 'Friday',
              value: 'Friday',
            },
            {
              label: 'Saturday',
              value: 'Saturday',
            },
            {
              label: 'Sunday',
              value: 'Sunday',
            },
          ]"
          required
        />
        <FormControl
          :type="'time'"
          size="sm"
          variant="subtle"
          placeholder="Start Time"
          label="Start Time"
          description="Enter time in seconds"
          v-model="workDayData.start_time"
          required
        />
        <FormControl
          :type="'time'"
          size="sm"
          variant="subtle"
          placeholder="End Time"
          label="End Time"
          description="Enter time in seconds"
          v-model="workDayData.end_time"
          required
        />
      </div>
    </template>
    <template #actions>
      <div class="flex gap-2 justify-end">
        <Button variant="subtle" theme="gray" @click="dialog = false">
          Cancel
        </Button>
        <Button variant="solid" @click="onSave"> Save </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { Button, createResource } from "frappe-ui";
import Draggable from "vuedraggable";
import NestedPopover from "@/components/NestedPopover.vue";
import Autocomplete from "@/components/frappe-ui/Autocomplete.vue";
import { computed, ref } from "vue";
import SlaWorkDaysListItem from "./SlaWorkDaysListItem.vue";

const dialog = ref(false);

const props = defineProps({
  workDaysList: {
    type: Array<any>,
    required: true,
  },
});

const workDayData = ref({
  workday: "",
  start_time: "",
  end_time: "",
});

const onSave = () => {
  if (
    workDayData.value.end_time &&
    workDayData.value.start_time &&
    workDayData.value.workday
  ) {
    props.workDaysList.push(workDayData.value);
    dialog.value = false;
    workDayData.value = {
      workday: "",
      start_time: "",
      end_time: "",
    };
  }
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
</script>
