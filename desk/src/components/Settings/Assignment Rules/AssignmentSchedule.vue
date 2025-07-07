<template>
  <div class="rounded-md border p-1 border-gray-300 text-sm">
    <div class="grid p-2 items-center" style="grid-template-columns: 3fr 1fr">
      <div
        v-for="column in columns"
        :key="column.key"
        class="text-gray-600 overflow-hidden whitespace-nowrap text-ellipsis"
      >
        {{ column.label }}
      </div>
    </div>
    <hr class="my-0.5" />
    <AssignmentScheduleItem
      v-for="(day, index) in days"
      :key="day.day"
      :day="day"
      :isLast="index === days.length - 1"
    />
    <!-- <div
      class="grid gap-2 px-2 items-center"
      :style="{
        gridTemplateColumns: 'grid-template-columns: 1fr 1fr 22px;',
      }"
      v-for="day in days"
      :key="day.day"
    >
      <div>{{ day.day }}</div>
      <div class="flex justify-start">
        <Switch v-model="day.active" />
      </div>
    </div> -->
  </div>
</template>

<script setup lang="ts">
import { getGridTemplateColumnsForTable } from "@/utils";
import { Switch } from "frappe-ui";
import { onMounted, ref } from "vue";
import AssignmentScheduleItem from "./AssignmentScheduleItem.vue";
import { assignmentRuleData } from "../../../stores/assignmentRules";

const columns = [
  {
    label: "Days",
    key: "day",
  },
  {
    label: "Active",
    key: "active",
  },
];

const days = ref([
  {
    day: "Monday",
    active: false,
  },
  {
    day: "Tuesday",
    active: false,
  },
  {
    day: "Wednesday",
    active: false,
  },
  {
    day: "Thursday",
    active: false,
  },
  {
    day: "Friday",
    active: false,
  },
  {
    day: "Saturday",
    active: false,
  },
  {
    day: "Sunday",
    active: false,
  },
]);

onMounted(() => {
  assignmentRuleData.value.assignment_days.forEach((day) => {
    const workDay = days.value.find((d) => d.day === day.day);
    if (workDay) {
      workDay.active = true;
    }
  });
});
</script>
