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
      <div v-if="column.key === 'status'">
        <Select
          class="w-max bg-transparent -ml-2 hover:bg-transparent border-0 focus-visible:!ring-0 bg-none"
          :options="statusOptions"
          v-model="props.row['status']"
        />
      </div>
      <div v-else-if="column.key === 'sla_behavior'">
        <Select
          class="w-max bg-transparent -ml-2 hover:bg-transparent border-0 focus-visible:!ring-0 bg-none"
          :options="slaBehaviorOptions"
          v-model="props.row['sla_behavior']"
        />
      </div>
    </div>
    <div class="flex justify-end">
      <Dropdown
        :options="[
          {
            label: 'Edit',
            onClick: () => editItem(),
            icon: 'edit',
          },
          {
            label: isConfirmingDelete ? 'Confirm Delete' : 'Delete',
            onClick: () => deleteItem(),
            icon: 'trash-2',
          },
        ]"
      >
        <Button icon="more-horizontal" variant="ghost" />
      </Dropdown>
    </div>
  </div>
  <hr class="my-0.5" v-if="!props.isLast" />
  <Dialog v-model="dialog" @after-leave="isConfirmingDelete = false">
    <template #body-title>
      <h3 class="text-2xl font-semibold">Edit Status</h3>
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
          :options="statusOptions"
          required
        />
        <FormControl
          :type="'select'"
          size="sm"
          variant="subtle"
          placeholder="Select Status"
          label="SLA behavior"
          v-model="statusData.sla_behavior"
          :options="slaBehaviorOptions"
          required
        />
      </div>
    </template>
    <template #actions>
      <div class="flex justify-between">
        <div>
          <Button
            variant="subtle"
            theme="red"
            :label="isConfirmingDelete ? 'Confirm Delete' : 'Delete'"
            @click="deleteItem"
          >
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
  Select,
  Dropdown,
  FeatherIcon,
  Dialog,
  toast,
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
  statusList: {
    type: Array<any>,
    required: true,
  },
});

const dialog = ref(false);
const isConfirmingDelete = ref(false);
const statusData = ref({
  status: props.row.status,
  sla_behavior: props.row.sla_behavior,
});
const statusOptions = [
  {
    label: "Open",
    value: "Open",
  },
  {
    label: "Replied",
    value: "Replied",
  },
  {
    label: "Resolved",
    value: "Resolved",
  },
  {
    label: "Closed",
    value: "Closed",
  },
];

const slaBehaviorOptions = [
  {
    label: "Fulfilled",
    value: "Fulfilled",
  },
  {
    label: "Paused",
    value: "Paused",
  },
];

const deleteItem = () => {
  event.preventDefault();
  if (!isConfirmingDelete.value) {
    isConfirmingDelete.value = true;
    return;
  }

  props.statusList.splice(props.statusList.indexOf(props.row), 1);
};

const editItem = () => {
  statusData.value = {
    status: props.row.status,
    sla_behavior: props.row.sla_behavior,
  };
  dialog.value = true;
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
    (item) => item.status === statusData.value.status && item !== props.row
  );

  if (isDuplicate) {
    toast.error("A status with this name already exists");
    return;
  }

  props.row.status = statusData.value.status;
  props.row.sla_behavior = statusData.value.sla_behavior;

  statusData.value = {
    status: "",
    sla_behavior: "",
  };

  dialog.value = false;
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
