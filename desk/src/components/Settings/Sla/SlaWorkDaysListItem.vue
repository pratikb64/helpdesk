<template>
  <div
    class="grid gap-2 px-2 py-1 items-center"
    :style="{ gridTemplateColumns: getGridTemplateColumns(props.columns) }"
  >
    <div
      v-for="column in props.columns"
      :key="column.key"
      class="w-full py-2 overflow-hidden whitespace-nowrap text-ellipsis"
    >
      <div v-if="column.key === 'start_time' || column.key === 'end_time'">
        {{ formatTime(props.row[column.key]) }}
      </div>
      <div v-else>
        <Select
          class="bg-transparent w-max -ml-2 hover:bg-transparent border-0 focus-visible:!ring-0 bg-none"
          :options="workDayOptions"
          v-model="props.row[column.key]"
        />
      </div>
    </div>
    <div class="flex justify-end">
      <Button variant="ghost" @click="editWorkDay">
        <template #icon>
          <EditIcon class="size-4" />
        </template>
      </Button>
    </div>
  </div>
  <hr class="my-0.5" v-if="!props.isLast" />
  <Dialog v-model="dialog">
    <template #body-title>
      <h3 class="text-2xl font-semibold">Edit Workday</h3>
    </template>
    <template #body-content>
      <div class="flex flex-col gap-4">
        <FormControl
          :type="'select'"
          size="sm"
          variant="subtle"
          placeholder="Workday"
          label="Workday"
          v-model="workDayData.workday"
          required
          :options="workDayOptions"
        />
        <FormControl
          :type="'time'"
          size="sm"
          variant="subtle"
          placeholder="Start Time"
          label="Start Time"
          v-model="workDayData.start_time"
          required
        />
        <FormControl
          :type="'time'"
          size="sm"
          variant="subtle"
          placeholder="End Time"
          label="End Time"
          v-model="workDayData.end_time"
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
            @click="deleteWorkDay"
          >
            <template #prefix>
              <FeatherIcon name="trash-2" class="size-4" />
            </template>
          </Button>
        </div>
        <div class="flex justify-end">
          <div class="flex gap-2">
            <Button variant="subtle" theme="gray" @click="dialog = false">
              Cancel
            </Button>
            <Button variant="solid" @click="onSave"> Save </Button>
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { Button, FeatherIcon, Dialog, Select } from "frappe-ui";
import { EditIcon } from "@/components/icons";

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
  workDaysList: {
    type: Object,
    required: true,
  },
});
const workDayOptions = [
  {
    label: "Monday",
    value: "Monday",
  },
  {
    label: "Tuesday",
    value: "Tuesday",
  },
  {
    label: "Wednesday",
    value: "Wednesday",
  },
  {
    label: "Thursday",
    value: "Thursday",
  },
  {
    label: "Friday",
    value: "Friday",
  },
  {
    label: "Saturday",
    value: "Saturday",
  },
  {
    label: "Sunday",
    value: "Sunday",
  },
];
const isConfirmingDelete = ref(false);

const deleteWorkDay = () => {
  if (!isConfirmingDelete.value) {
    isConfirmingDelete.value = true;
    setTimeout(() => {
      isConfirmingDelete.value = false;
    }, 3000);
    return;
  }

  const item = props.workDaysList.findIndex(
    (item) => item.workday === props.row.workday
  );
  if (item !== -1) {
    props.workDaysList.splice(item, 1);
  }
};
const dialog = ref(false);
const workDayData = ref({
  workday: props.row.workday,
  start_time: props.row.start_time,
  end_time: props.row.end_time,
});

const editWorkDay = () => {
  dialog.value = true;
  workDayData.value = {
    workday: props.row.workday,
    start_time: props.row.start_time,
    end_time: props.row.end_time,
  };
};

const onSave = () => {
  const item = props.workDaysList.findIndex(
    (item) => item.workday === props.row.workday
  );
  if (item !== -1) {
    props.workDaysList[item].start_time = workDayData.value.start_time;
    props.workDaysList[item].end_time = workDayData.value.end_time;
  }
  workDayData.value = {
    workday: "",
    start_time: "",
    end_time: "",
  };
  dialog.value = false;
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

const formatTime = (time) => {
  if (!time) return "00:00";
  const [hours, minutes] = time.split(":");
  const date = new Date();
  date.setHours(parseInt(hours) || 0, parseInt(minutes) || 0, 0);

  return date.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
};
</script>
