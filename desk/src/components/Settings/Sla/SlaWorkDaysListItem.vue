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
      <Dropdown
        :options="[
          {
            label: 'Edit',
            onClick: () => editWorkDay(),
            icon: 'edit',
          },
          {
            label: isConfirmingDelete ? 'Confirm Delete' : 'Delete',
            onClick: (event) => deleteWorkDay(event),
            icon: 'trash-2',
          },
        ]"
      >
        <Button
          icon="more-horizontal"
          variant="ghost"
          @click="isConfirmingDelete = false"
        />
      </Dropdown>
    </div>
  </div>
  <hr class="my-0.5" v-if="!props.isLast" />
  <WorkDayModal v-model="dialog" :workDaysList="props.workDaysList" />
</template>

<script setup lang="ts">
import { ref } from "vue";
import { Button, FeatherIcon, Dialog, Select } from "frappe-ui";
import { EditIcon } from "@/components/icons";
import WorkDayModal from "./WorkDayModal.vue";

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
    type: Array<any>,
    required: true,
  },
});

const dialog = ref({
  show: false,
  isEditing: false,
  data: {},
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

const deleteWorkDay = (event) => {
  event.preventDefault();
  if (!isConfirmingDelete.value) {
    isConfirmingDelete.value = true;
    return;
  }

  const item = props.workDaysList.findIndex(
    (item) => item.workday === props.row.workday
  );
  if (item !== -1) {
    props.workDaysList.splice(item, 1);
  }
};

const editWorkDay = () => {
  dialog.value.show = true;
  dialog.value.isEditing = true;
  dialog.value.data = {
    workday: props.row.workday,
    start_time: props.row.start_time,
    end_time: props.row.end_time,
  };
};

// const onSave = () => {
//   const item = props.workDaysList.findIndex(
//     (item) => item.workday === props.row.workday
//   );
//   if (item !== -1) {
//     props.workDaysList[item].start_time = workDayData.value.start_time;
//     props.workDaysList[item].end_time = workDayData.value.end_time;
//   }
//   workDayData.value = {
//     workday: "",
//     start_time: "",
//     end_time: "",
//   };
//   dialog.value = false;
// };

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
