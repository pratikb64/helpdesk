<template>
  <div>
    <div class="text-base font-medium mb-2 text-gray-800 ml-2.5">
      {{ formattedMonth }}
    </div>
    <div class="rounded-md text-sm">
      <div class="flex items-center justify-between text-xs uppercase">
        <div
          class="flex h-6 w-6 items-center justify-center text-center text-gray-600"
          v-for="(d, i) in ['s', 'm', 't', 'w', 't', 'f', 's']"
          :key="i"
        >
          {{ d }}
        </div>
      </div>
      <div class="flex items-center" v-for="(week, i) in datesAsWeeks" :key="i">
        <div v-for="date in week" :key="getDateValue(date)">
          <Popover v-if="isHoliday(date)">
            <template #target="{ open, close }">
              <div
                class="flex size-8 cursor-pointer text-orange-700 bg-yellow-100 items-center justify-center rounded hover:bg-surface-gray-2 select-none"
                :class="{
                  '!text-ink-gray-4 !bg-gray-100': isWeekOff(date),
                }"
                @mouseover="handleMouseEnter(getDateValue(date), open)"
                @mouseleave="handleMouseLeave(getDateValue(date), close)"
              >
                {{ date.getDate() }}
              </div>
            </template>
            <template #body-main="{ close, open }">
              <div
                class="p-3 flex gap-2.5 text-ink-gray-9 w-80 border border-gray-200 rounded-md"
                @mouseover="handleMouseEnter(getDateValue(date), open)"
                @mouseleave="handleMouseLeave(getDateValue(date), close)"
              >
                <div class="w-[5%]">
                  <div class="size-3.5 bg-orange-500 rounded-sm mt-1" />
                </div>
                <div class="grow">
                  <div class="text-sm font-semibold">
                    {{ getHolidayDescription(date) }}
                  </div>
                  <div class="text-xs mt-1">
                    {{ date.toLocaleDateString() }}
                  </div>
                </div>
                <Dropdown
                  :options="[
                    {
                      label: 'Edit',
                      onClick: () => editHoliday(date),
                      icon: 'edit',
                    },
                    {
                      label: isConfirmingDelete ? 'Confirm Delete' : 'Delete',
                      onClick: (event) => deleteHoliday(event, date),
                      icon: 'trash-2',
                    },
                  ]"
                >
                  <Button icon="more-horizontal" variant="ghost" />
                </Dropdown>
              </div>
            </template>
          </Popover>
          <div
            v-else
            class="flex size-8 cursor-pointer items-center justify-center rounded hover:bg-surface-gray-2 select-none"
            :class="{
              'text-ink-gray-3': date.getMonth() !== currentMonth - 1,
              'text-ink-gray-9': getDateValue(date) === getDateValue(today),
              'bg-red-500/90 text-ink-white hover:!bg-red-500':
                getDateValue(date) === dateValue,
              'text-orange-700 bg-yellow-100': isHoliday(date),
            }"
            @dblclick="addHoliday(date)"
          >
            {{ date.getDate() }}
          </div>
        </div>
      </div>
    </div>
  </div>
  <Dialog v-model="dialog" :options="{ size: 'sm' }">
    <template #body-title>
      <h3 class="text-2xl font-semibold">
        {{ editHolidayData.isEditing ? "Edit" : "Add" }} Holiday
      </h3>
    </template>
    <template #body-content>
      <div class="flex flex-col gap-4">
        <div class="flex flex-col gap-1.5">
          <FormLabel label="Date" required />
          <DatePicker
            v-model="editHolidayData.holiday_date"
            variant="subtle"
            placeholder="Date"
            class="w-full"
            id="holiday_date"
            required
          />
        </div>
        <FormControl
          :type="'textarea'"
          size="sm"
          variant="subtle"
          placeholder="Description"
          label="Description"
          v-model="editHolidayData.description"
          required
        />
      </div>
    </template>
    <template #actions>
      <Button variant="solid" @click="saveHoliday" class="w-full">
        {{ editHolidayData.isEditing ? "Update" : "Add" }} Holiday
        <template #prefix>
          <FeatherIcon
            :name="editHolidayData.isEditing ? 'edit-2' : 'plus'"
            class="size-4"
          />
        </template>
      </Button>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { htmlToText } from "@/utils";
import { toast, DatePicker, FormLabel, Popover } from "frappe-ui";
import { useDatePicker } from "frappe-ui/src/components/DatePicker/useDatePicker";
import {
  getDate,
  getDateValue,
} from "frappe-ui/src/components/DatePicker/utils";
import { computed, onMounted, reactive, ref, watch } from "vue";

const dialog = ref(false);
const editHolidayData = ref({
  holiday_date: null,
  description: "",
  isEditing: false,
});
const { currentYear, currentMonth, today, datesAsWeeks, formattedMonth } =
  useDatePicker();
const isConfirmingDelete = ref(false);
const popoverTimeouts = ref({});

const props = defineProps({
  year: {
    type: Number,
    required: true,
  },
  month: {
    type: Number,
    required: true,
  },
  holidays: {
    type: Array<any>,
    required: true,
  },
});

const dateValue = reactive(getDateValue(today.value));

const handleMouseEnter = (date, callback) => {
  popoverTimeouts.value[date] = setTimeout(() => {
    callback();
  }, 350);
};

const handleMouseLeave = (date, callback) => {
  clearTimeout(popoverTimeouts.value[date]);
  popoverTimeouts.value[date] = setTimeout(() => {
    callback();
  }, 350);
};

const addHoliday = (date) => {
  editHolidayData.value.holiday_date = date.toLocaleDateString();
  dialog.value = true;
};

const isHoliday = (date: Date): boolean => {
  if (!props.holidays?.length) return false;
  // console.log(isWeekOff(date));
  const inputDate = new Date(date);
  inputDate.setHours(0, 0, 0, 0);

  return props.holidays.some((holiday) => {
    const holidayDate = new Date(holiday.holiday_date);
    holidayDate.setHours(0, 0, 0, 0);

    return holidayDate.getTime() === inputDate.getTime();
  });
};

const isWeekOff = (date: Date): boolean => {
  if (!props.holidays?.length) return false;

  const inputDate = new Date(date);
  inputDate.setHours(0, 0, 0, 0);
  return props.holidays.some((holiday) => {
    const holidayDate = new Date(holiday.holiday_date);
    holidayDate.setHours(0, 0, 0, 0);

    return (
      holidayDate.getTime() === inputDate.getTime() && holiday.weekly_off == 1
    );
  });
};

const dismissPopover = (callback, delay = 600) => {
  setTimeout(() => {
    callback();
  }, delay);
};

const editHoliday = (date) => {
  dialog.value = true;
  const holiday = props.holidays.find((h) => {
    const holidayDate = getDateValue(h.holiday_date);
    const editDate = getDateValue(date);
    return holidayDate === editDate;
  });
  editHolidayData.value = { ...holiday, isEditing: true };
};

const deleteHoliday = (event, date) => {
  event.stopPropagation();
  event.preventDefault();
  if (!isConfirmingDelete.value) {
    isConfirmingDelete.value = true;
    return;
  }
  const holidayToDelete = props.holidays.find((h) => {
    const holidayDate = getDateValue(h.holiday_date);
    const editDate = getDateValue(date);
    return holidayDate === editDate;
  });
  const index = props.holidays.findIndex((h) => {
    const holidayDate = getDateValue(h.holiday_date);
    const editDate = getDateValue(holidayToDelete.holiday_date);
    return holidayDate === editDate;
  });

  props.holidays.splice(index, 1);
  dialog.value = false;
  editHolidayData.value = {
    holiday_date: null,
    description: "",
    isEditing: false,
  };
  isConfirmingDelete.value = false;
};

const saveHoliday = () => {
  if (
    !editHolidayData.value.holiday_date ||
    !editHolidayData.value.description
  ) {
    return;
  }

  const existingHoliday = props.holidays.find(
    (h) =>
      getDateValue(h.holiday_date) ===
      getDateValue(editHolidayData.value.holiday_date)
  );

  if (existingHoliday && !editHolidayData.value.isEditing) {
    toast.error(
      `A holiday already exists for ${new Date(
        editHolidayData.value.holiday_date
      ).toLocaleDateString()}`
    );
    return;
  }

  const index = props.holidays.findIndex(
    (h) =>
      getDateValue(h.holiday_date) ===
      getDateValue(editHolidayData.value.holiday_date)
  );

  if (index === -1 && !editHolidayData.value.isEditing) {
    props.holidays.push({
      ...editHolidayData.value,
      weekly_off: 0,
    });
    dialog.value = false;
    editHolidayData.value = {
      holiday_date: null,
      description: "",
      isEditing: false,
    };
  } else {
    props.holidays.splice(index, 1, {
      ...editHolidayData.value,
      weekly_off: 0,
    });
    dialog.value = false;
    editHolidayData.value = {
      holiday_date: null,
      description: "",
      isEditing: false,
    };
  }
};

const getHolidayDescription = (date: Date): string => {
  const holiday = props.holidays.find((h) => {
    const holidayDate = getDateValue(h.holiday_date);
    const editDate = getDateValue(date);
    return holidayDate === editDate;
  });

  const text = holiday?.weekly_off
    ? `${htmlToText(holiday?.description || "")}: Recurring holiday`
    : htmlToText(holiday?.description || "");

  return text;
};

watch(
  () => [props.year, props.month],
  ([newYear, newMonth]) => {
    currentYear.value = newYear;
    currentMonth.value = newMonth;
  },
  { immediate: true }
);
</script>
