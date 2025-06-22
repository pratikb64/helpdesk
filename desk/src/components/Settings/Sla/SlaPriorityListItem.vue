<template>
  <div
    class="grid gap-2 px-2 items-center"
    :style="{ gridTemplateColumns: getGridTemplateColumns(props.columns) }"
  >
    <div
      v-for="column in props.columns"
      :key="column.key"
      class="w-full py-2 overflow-hidden whitespace-nowrap text-ellipsis"
    >
      <div v-if="column.key === 'default_priority'">
        <Checkbox
          v-model="props.row.default_priority"
          @update:modelValue="(e) => onDefaultPriorityChange(e)"
        />
      </div>
      <div v-else-if="column.key === 'response_time'">
        {{ formatTimeHMS(props.row[column.key]) }}
      </div>
      <div v-else-if="column.key === 'resolution_time'">
        {{ formatTimeHMS(props.row[column.key]) }}
      </div>
      <div v-else>
        <Select
          class="w-full bg-transparent !p-0 hover:bg-transparent border-0 focus-visible:!ring-0 bg-none"
          :options="priorityOptions"
          v-model="props.row[column.key]"
        />
      </div>
    </div>
    <div class="flex justify-end">
      <Dropdown
        :options="[
          {
            label: 'Edit',
            onClick: () => editSla(),
            icon: 'edit',
          },
          {
            label: isConfirmingDelete ? 'Confirm Delete' : 'Delete',
            onClick: () => deleteSla(),
            icon: 'trash-2',
          },
        ]"
      >
        <Button icon="more-horizontal" variant="ghost" />
      </Dropdown>
    </div>
  </div>
  <hr class="my-0.5" v-if="!props.isLast" />
  <Dialog v-model="dialog">
    <template #body-title>
      <h3 class="text-2xl font-semibold">Edit Response & Resolution metric</h3>
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
          :options="priorityOptions"
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
          @update:modelValue="onDefaultPriorityChange"
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
import { h, ref } from "vue";
import {
  Button,
  Checkbox,
  Dropdown,
  FeatherIcon,
  Dialog,
  createResource,
  toast,
  Select,
} from "frappe-ui";

const props = defineProps({
  columns: {
    type: Array<any>,
    required: true,
  },
  row: {
    type: Object,
    required: true,
  },
  isLast: {
    type: Boolean,
    default: false,
  },
  priorityList: {
    type: Object,
    required: true,
  },
});

const priorityOptions = [
  {
    label: "Low",
    value: "Low",
  },
  {
    label: "Medium",
    value: "Medium",
  },
  {
    label: "High",
    value: "High",
  },
];

const isConfirmingDelete = ref(false);
const dialog = ref(false);
const priorityData = ref({
  priority: props.row.priority,
  resolution_time: props.row.resolution_time,
  response_time: props.row.response_time,
  default_priority: props.row.default_priority,
});

const deleteSla = () => {
  event.preventDefault();
  if (!isConfirmingDelete.value) {
    isConfirmingDelete.value = true;
    setTimeout(() => {
      isConfirmingDelete.value = false;
    }, 3000);
    return;
  }

  props.priorityList.splice(props.priorityList.indexOf(props.row), 1);
};

const editSla = () => {
  dialog.value = true;
  priorityData.value = {
    priority: props.row.priority,
    resolution_time: props.row.resolution_time,
    response_time: props.row.response_time,
    default_priority: props.row.default_priority,
  };
};

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
  console.log("priorityData.value", priorityData.value);
  props.row.priority = priorityData.value.priority;
  props.row.resolution_time = priorityData.value.resolution_time;
  props.row.response_time = priorityData.value.response_time;
  props.row.default_priority = priorityData.value.default_priority;

  priorityData.value = {
    priority: "",
    resolution_time: "",
    response_time: "",
    default_priority: false,
  };

  dialog.value = false;
};

const onDefaultPriorityChange = (defaultPriority) => {
  props.priorityList.forEach((priority) => {
    priority.default_priority = false;
  });
  props.row.default_priority = defaultPriority;
};

function formatTimeHMS(seconds) {
  const days = Math.floor(seconds / (3600 * 24));
  const hours = Math.floor((seconds % (3600 * 24)) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = Math.floor(seconds % 60);

  let formattedTime = "";

  if (days > 0) {
    formattedTime += `${days}d `;
  }

  if (hours > 0) {
    formattedTime += `${hours}h `;
  }

  if (minutes > 0) {
    formattedTime += `${minutes}m `;
  }

  if (remainingSeconds > 0) {
    formattedTime += `${remainingSeconds}s`;
  }

  return formattedTime.trim();
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
</script>
