<template>
  <div class="rounded-md border p-1 border-gray-300 text-sm">
    <div
      class="grid p-2 items-center"
      :style="{
        gridTemplateColumns: '1fr 4fr 22px',
      }"
    >
      <div
        v-for="column in columns"
        :key="column.key"
        class="text-gray-600 overflow-hidden whitespace-nowrap text-ellipsis"
      >
        {{ column.label }}
      </div>
    </div>
    <hr class="my-0.5" />
    <div v-for="(holiday, index) in holidays" :key="holiday.day">
      <div
        class="grid gap-2 px-2 items-center"
        :style="{ gridTemplateColumns: '1fr 4fr 22px' }"
      >
        <div
          v-for="column in columns"
          :key="column.key"
          class="w-full py-2 overflow-hidden whitespace-nowrap text-ellipsis"
        >
          <div v-if="column.key === 'repetition'">
            {{ getRepetitionText(holiday[column.key]) }}
          </div>
          <div v-else>{{ holiday[column.key] }}</div>
        </div>
        <div class="flex justify-end">
          <Dropdown
            :options="[
              {
                label: 'Edit',
                onClick: () => editHoliday(holiday),
                icon: 'edit',
              },
              {
                label: isConfirmingDelete ? 'Confirm Delete' : 'Delete',
                onClick: (event) => deleteHoliday(event, holiday),
                icon: 'trash-2',
              },
            ]"
          >
            <Button icon="more-horizontal" variant="ghost" />
          </Dropdown>
        </div>
      </div>
      <hr class="my-0.5" v-if="index !== holidays.length - 1" />
    </div>
    <div v-if="holidays?.length === 0" class="text-center p-4 text-gray-600">
      No items in the list
    </div>
  </div>
  <Button variant="subtle" @click="addHoliday" class="mt-4">
    Add Recurring Holiday
    <template #prefix>
      <FeatherIcon name="plus" class="size-4" />
    </template>
  </Button>
  <Dialog v-model="dialog" :options="{ size: 'md' }">
    <template #body-title>
      <h3 class="text-2xl font-semibold">
        {{ recurringHolidayData.isEditing ? "Edit" : "Add" }} Recurring Holiday
      </h3>
    </template>
    <template #body-content>
      <div v-if="!props.holidayData.from_date || !props.holidayData.to_date">
        <div class="text-center p-4 text-gray-600">
          Please select start and end date first
        </div>
      </div>
      <div v-else class="flex flex-col gap-4">
        <div class="flex flex-col gap-1.5">
          <FormLabel label="Day" required />
          <Select
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
            v-model="recurringHolidayData.day"
          />
        </div>
        <div class="flex flex-col gap-1.5">
          <FormLabel label="Repetition" required />
          <div class="grid grid-cols-2 gap-2 mt-2">
            <Checkbox
              v-model="recurringHolidayData.repetition.all"
              label="Every week"
              :disabled="
                recurringHolidayData.repetition.first ||
                recurringHolidayData.repetition.second ||
                recurringHolidayData.repetition.third ||
                recurringHolidayData.repetition.fourth
              "
            />
            <Checkbox
              v-model="recurringHolidayData.repetition.first"
              label="Every first week"
              :disabled="recurringHolidayData.repetition.all"
            />
            <Checkbox
              v-model="recurringHolidayData.repetition.second"
              label="Every second week"
              :disabled="recurringHolidayData.repetition.all"
            />
            <Checkbox
              v-model="recurringHolidayData.repetition.third"
              label="Every third week"
              :disabled="recurringHolidayData.repetition.all"
            />
            <Checkbox
              v-model="recurringHolidayData.repetition.fourth"
              label="Every fourth week"
              :disabled="recurringHolidayData.repetition.all"
            />
          </div>
        </div>
      </div>
    </template>
    <template #actions>
      <Button
        variant="solid"
        @click="saveHoliday"
        class="w-full"
        v-if="props.holidayData.from_date && props.holidayData.to_date"
      >
        {{ recurringHolidayData.isEditing ? "Update" : "Add" }} Holiday
        <template #prefix>
          <FeatherIcon
            :name="recurringHolidayData.isEditing ? 'edit-2' : 'plus'"
            class="size-4"
          />
        </template>
      </Button>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { Select, FormLabel, Checkbox, toast } from "frappe-ui";
import dayjs from "dayjs";
import weekday from "dayjs/plugin/weekday";
import isSameOrBefore from "dayjs/plugin/isSameOrBefore";

dayjs.extend(weekday);
dayjs.extend(isSameOrBefore);

const emit = defineEmits(["update:holidays"]);
const dialog = ref(false);
const recurringHolidayData = ref({
  day: null,
  repetition: {
    all: false,
    first: false,
    second: false,
    third: false,
    fourth: false,
  },
  isEditing: false,
});

const props = defineProps({
  holidays: {
    type: Array<any>,
    default: () => [],
    required: true,
  },
  holidayData: {
    type: Object,
    default: () => {},
    required: true,
  },
});

const columns = [
  {
    label: "Day",
    key: "day",
  },
  {
    label: "Repetition",
    key: "repetition",
  },
];

const isConfirmingDelete = ref(false);

const getRepetitionText = (repetition: any) => {
  const parts: string[] = [];

  if (repetition.all) {
    parts.push("week");
  } else {
    if (repetition.first) parts.push("first");
    if (repetition.second) parts.push("second");
    if (repetition.third) parts.push("third");
    if (repetition.fourth) parts.push("fourth");

    if (parts.length === 0) return "";

    if (parts.length > 1) {
      const last = parts.pop();
      parts[parts.length - 1] = `${parts[parts.length - 1]} and ${last}`;
    }

    parts[0] = parts[0].charAt(0) + parts[0].slice(1);
    return `Every ${parts.join(", ")} week`;
  }

  return parts[0] ? `Every ${parts[0]}` : "";
};

const addHoliday = () => {
  recurringHolidayData.value = {
    day: null,
    repetition: {
      all: false,
      first: false,
      second: false,
      third: false,
      fourth: false,
    },
    isEditing: false,
  };
  dialog.value = true;
};

const editHoliday = (holiday: any) => {
  recurringHolidayData.value = holiday;
  recurringHolidayData.value.isEditing = true;
  dialog.value = true;
};
const saveHoliday = () => {
  if (!recurringHolidayData.value.day) {
    return;
  }

  const index = props.holidays.findIndex((h: any) => {
    return h.day === recurringHolidayData.value.day;
  });

  const weeklyOffDates = [];
  for (const day of props.holidays) {
    weeklyOffDates.push(
      ...getWeeklyOffDates(
        props.holidayData.from_date,
        props.holidayData.to_date,
        day.day,
        props.holidays,
        day.repetition
      )
    );
  }
  weeklyOffDates.push(
    ...getWeeklyOffDates(
      props.holidayData.from_date,
      props.holidayData.to_date,
      recurringHolidayData.value.day,
      props.holidays,
      recurringHolidayData.value.repetition
    )
  );

  if (recurringHolidayData.value.isEditing) {
    props.holidays.splice(index, 1, {
      ...recurringHolidayData.value,
    });
    emit("update:holidays", weeklyOffDates);
  } else {
    if (index !== -1) {
      toast.error("Holiday already exists");
      return;
    }
    props.holidays.push({
      ...recurringHolidayData.value,
    });
    emit("update:holidays", weeklyOffDates);
  }
  dialog.value = false;
};

const deleteHoliday = (event, holiday: any) => {
  event.stopPropagation();
  event.preventDefault();
  if (!isConfirmingDelete.value) {
    isConfirmingDelete.value = true;
    return;
  }
  const index = props.holidays.findIndex((h: any) => {
    return h.day === holiday.day;
  });
  props.holidays.splice(index, 1);
  const weeklyOffDates = [];
  for (const day of props.holidays) {
    weeklyOffDates.push(
      ...getWeeklyOffDates(
        props.holidayData.from_date,
        props.holidayData.to_date,
        day.day,
        props.holidays,
        day.repetition
      )
    );
  }
  emit("update:holidays", weeklyOffDates);
  dialog.value = false;
  isConfirmingDelete.value = false;
};

function getWeeklyOffDates(
  startDate,
  endDate,
  weeklyOff,
  holidays,
  repetition
) {
  const dateList = getWeeklyOffDateList(
    startDate,
    endDate,
    weeklyOff,
    holidays,
    repetition
  );
  return dateList.map((date) => ({
    description: weeklyOff,
    holiday_date: date,
    weekly_off: 1,
  }));
}

function getWeeklyOffDateList(
  startDate,
  endDate,
  weeklyOff,
  holidays,
  repetition
) {
  const start = dayjs(startDate);
  const end = dayjs(endDate);

  const dayMap = {
    MONDAY: 1,
    TUESDAY: 2,
    WEDNESDAY: 3,
    THURSDAY: 4,
    FRIDAY: 5,
    SATURDAY: 6,
    SUNDAY: 0,
  };

  const targetDay = dayMap[weeklyOff.toUpperCase()];
  const existingDates = holidays.map((h) =>
    dayjs(h.holiday_date).format("YYYY-MM-DD")
  );
  const result = [];

  let currentDate = start.day(targetDay);
  if (currentDate.isBefore(start, "day")) {
    currentDate = currentDate.add(1, "week");
  }

  if (!repetition || Object.keys(repetition).length === 0) {
    repetition = { all: true };
  }

  if (repetition.all) {
    while (currentDate.isSameOrBefore(end, "day")) {
      const dateStr = currentDate.format("YYYY-MM-DD");
      if (!existingDates.includes(dateStr)) {
        result.push(dateStr);
      }
      currentDate = currentDate.add(1, "week");
    }
    return result;
  }

  const referenceDate = currentDate.clone();
  let weekCount = 0;

  while (currentDate.isSameOrBefore(end, "day")) {
    const weeksSinceStart = Math.floor(
      currentDate.diff(referenceDate, "day") / 7
    );
    const currentWeek = (weeksSinceStart % 4) + 1;

    const isSelectedWeek =
      (repetition.first && currentWeek === 1) ||
      (repetition.second && currentWeek === 2) ||
      (repetition.third && currentWeek === 3) ||
      (repetition.fourth && currentWeek === 4);

    if (isSelectedWeek) {
      const dateStr = currentDate.format("YYYY-MM-DD");
      if (!existingDates.includes(dateStr)) {
        result.push(dateStr);
      }
    }

    currentDate = currentDate.add(1, "week");
  }

  return result;
}
</script>
