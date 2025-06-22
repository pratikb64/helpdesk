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
    <SlaPriorityListItem
      v-for="(row, index) in props.priorityList"
      :key="row.name"
      :row="row"
      :columns="columns"
      :isLast="index === props.priorityList.length - 1"
      :priorityList="props.priorityList"
    />
    <div
      v-if="props.priorityList?.length === 0"
      class="text-center p-4 text-gray-600"
    >
      No items in the list
    </div>
  </div>
  <Button variant="subtle" label="Add row" class="mt-4" @click="dialog = true">
    <template #prefix>
      <FeatherIcon name="plus" class="h-4" />
    </template>
  </Button>
  <div v-if="slaDataErrors.default_priority" class="text-red-500 text-xs">
    {{ slaDataErrors.default_priority }}
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
          placeholder="Select Priority"
          label="Priority"
          v-model="priorityData.priority"
          :options="[
            {
              label: 'Low',
              value: 'Low',
            },
            {
              label: 'Medium',
              value: 'Medium',
            },
            {
              label: 'High',
              value: 'High',
            },
          ]"
          required
        />
        <FormControl
          :type="'number'"
          size="sm"
          variant="subtle"
          placeholder="Response Time"
          label="Response Time"
          description="Enter time in seconds"
          v-model="priorityData.response_time"
          required
        />
        <FormControl
          :type="'number'"
          size="sm"
          variant="subtle"
          placeholder="Resolution Time"
          label="Resolution Time"
          description="Enter time in seconds"
          v-model="priorityData.resolution_time"
          required
        />
        <Checkbox
          v-model="priorityData.default_priority"
          label="Set default priority"
        />
      </div>
    </template>
    <template #actions>
      <div class="flex justify-between">
        <div>
          <Button variant="subtle" theme="red" label="Delete">
            <template #prefix>
              <FeatherIcon name="trash-2" class="size-4" />
            </template>
          </Button>
        </div>
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
import { Button, Checkbox, FormControl, toast } from "frappe-ui";
import SlaPriorityListItem from "./SlaPriorityListItem.vue";
import { ref, computed } from "vue";
import { slaDataErrors } from "./sla";

const dialog = ref(false);

const props = defineProps({
  priorityList: {
    type: Array<any>,
    required: true,
  },
  applySlaForResolution: {
    type: Boolean,
    required: true,
  },
});

const priorityData = ref({
  priority: "",
  resolution_time: "",
  response_time: "",
  default_priority: false,
});

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

const columns = computed(() => [
  {
    label: "Priority",
    key: "priority",
    isRequired: true,
  },
  {
    label: "Default priority",
    key: "default_priority",
    isRequired: true,
  },
  {
    label: "First response time",
    key: "response_time",
    isRequired: true,
  },
  {
    label: "Resolution time",
    key: "resolution_time",
    isRequired: Boolean(props.applySlaForResolution),
  },
]);

const validateForm = () => {
  if (!priorityData.value.priority) {
    toast.error("Please select a priority");
    return false;
  }

  const resolutionTime = parseInt(priorityData.value.resolution_time);
  if (isNaN(resolutionTime) || resolutionTime <= 0) {
    toast.error("Resolution time must be a positive number");
    return false;
  }

  const responseTime = parseInt(priorityData.value.response_time);
  if (isNaN(responseTime) || responseTime <= 0) {
    toast.error("Response time must be a positive number");
    return false;
  }

  if (priorityData.value.default_priority) {
    props.priorityList.forEach((priority) => {
      priority.default_priority = false;
    });
  }

  return true;
};

const onSave = () => {
  if (!validateForm()) return;
  dialog.value = false;
  props.priorityList.push(priorityData.value);
  priorityData.value = {
    priority: "",
    resolution_time: "",
    response_time: "",
    default_priority: false,
  };
};
</script>
