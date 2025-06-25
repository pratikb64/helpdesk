<template>
  <div
    class="flex items-center justify-between sticky top-0 z-10 bg-white px-10 pt-8 pb-4"
  >
    <div>
      <div class="flex items-center gap-2">
        <Button
          variant="ghost"
          icon-left="chevron-left"
          :label="holidayData?.holiday_list_name || 'New Holiday List'"
          size="md"
          @click="goBack()"
          class="cursor-pointer -ml-4 hover:bg-transparent focus:bg-transparent focus:outline-none focus:ring-0 focus:ring-offset-0 focus-visible:none active:bg-transparent active:outline-none active:ring-0 active:ring-offset-0 active:text-ink-gray-5"
        />
      </div>
    </div>
    <Button label="Save" theme="gray" variant="solid" @click="saveHoliday()" />
  </div>
  <div v-if="!holidayData.loading" class="px-10 pb-8 overflow-y-scroll h-full">
    <div class="flex items-center justify-between gap-2 mt-8">
      <span class="text-sm"> Total holidays (Calculated automatically) </span>
      <div
        class="text-sm font-semibold p-1.5 min-w-10 w-max text-center bg-gray-100 rounded text-gray-800"
      >
        {{ holidayData.holidays.length }}
      </div>
    </div>
    <hr class="mb-6 mt-3" />
    <div class="grid grid-cols-2 gap-2">
      <div>
        <FormControl
          :type="'text'"
          size="sm"
          variant="subtle"
          placeholder="Name"
          label="Name"
          v-model="holidayData.holiday_list_name"
          required
        />
        <div v-if="errors.holiday_list_name" class="text-red-500 text-xs mt-1">
          {{ errors.holiday_list_name }}
        </div>
      </div>
      <FormControl
        :type="'textarea'"
        size="sm"
        variant="subtle"
        placeholder="Description"
        label="Description"
        v-model="holidayData.description"
        required
        rows="1"
      />
    </div>
    <hr class="my-6" />
    <div>
      <div class="flex flex-col gap-2">
        <span class="text-lg font-medium">Valid from</span>
        <span class="text-sm text-gray-600">
          Choose the duration of this holiday list.
        </span>
      </div>
      <div class="mt-4 flex gap-2">
        <div class="w-full">
          <FormLabel label="From date" for="from_date" required />
          <DatePicker
            v-model="holidayData.from_date"
            variant="subtle"
            placeholder="From date"
            class="w-full"
            id="from_date"
          />
          <div v-if="errors.from_date" class="text-red-500 text-xs mt-1">
            {{ errors.from_date }}
          </div>
          <div v-if="errors.dateRange" class="text-red-500 text-xs mt-1">
            {{ errors.dateRange }}
          </div>
        </div>
        <div class="w-full">
          <FormLabel label="To date" for="to_date" required />
          <DatePicker
            v-model="holidayData.to_date"
            variant="subtle"
            placeholder="To date"
            class="w-full"
            id="to_date"
          />
          <div v-if="errors.end_date" class="text-red-500 text-xs mt-1">
            {{ errors.end_date }}
          </div>
        </div>
      </div>
    </div>
    <hr class="my-6" />
    <div>
      <div class="flex flex-col gap-2">
        <div class="text-lg font-medium">Recurring holidays</div>
        <div class="text-sm text-gray-600">
          Add recurring holidays such as weekends.
        </div>
      </div>
      <div class="mt-6">
        <RecurringHolidaysList
          :holidayData="holidayData"
          :holidays="holidayData.recurring_holidays"
          @update:holidays="updateHolidays"
        />
      </div>
    </div>
    <hr class="my-6" />
    <div>
      <div class="flex flex-col gap-1">
        <span class="text-lg font-medium">Holidays</span>
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-600">
            Add holidays here to make sure they’re excluded from SLA
            calculations.
          </div>
          <TabButtons
            :buttons="[
              {
                value: 'list',
                icon: 'list',
              },
              {
                value: 'calendar',
                icon: 'calendar',
              },
            ]"
            v-model="holidayListView"
          />
        </div>
      </div>
      <div class="mt-4">
        <HolidaysListView
          v-if="holidayListView === 'list'"
          :holidayData="holidayData"
        />
        <HolidaysCalendarView :holidayData="holidayData" v-else />
      </div>
      <div class="mt-4">
        <Button variant="subtle" label="Add Holiday" @click="dialog = true">
          <template #prefix>
            <FeatherIcon name="plus" class="size-4" />
          </template>
        </Button>
        <AddHolidayModal v-model="dialog" :holidays="holidayData.holidays" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { holidayListActiveScreen } from "./holidayList";
import {
  createResource,
  Input,
  TabButtons,
  DatePicker,
  Dialog,
  Button,
  Checkbox,
  FormControl,
  toast,
} from "frappe-ui";
import { ref } from "vue";
import HolidaysListView from "./HolidaysListView.vue";
import RecurringHolidaysList from "./RecurringHolidaysList.vue";

interface HolidayErrors {
  holiday_list_name?: string;
  from_date?: string;
  end_date?: string;
  dateRange?: string;
  holidays?: string;
}
import HolidaysCalendarView from "./HolidaysCalendarView.vue";
import AddHolidayModal from "./AddHolidayModal.vue";
import { htmlToText } from "@/utils";
import FormLabel from "frappe-ui/src/components/FormLabel.vue";

const dialog = ref(false);
const errors = ref<HolidayErrors>({});

const holidayListView = ref("list");

const holidayData = ref({
  holiday_list_name: "",
  description: "",
  associate_holiday_list: true,
  loading: false,
  total_holidays: 0,
  holidays: [],
  from_date: null,
  to_date: null,
  recurring_holidays: [],
});

const getHolidayData = createResource({
  url: "helpdesk.api.holiday_list.get_holiday_list",
  params: {
    docname: holidayListActiveScreen.value.data?.name,
  },
  onSuccess(data) {
    holidayData.value = data;
  },
  transform(data) {
    for (let holiday of data.holidays) {
      holiday.description = htmlToText(holiday.description);
    }
    data.recurring_holidays = JSON.parse(data.recurring_holidays || "[]");
    return data;
  },
});

if (holidayListActiveScreen.value.data?.name) {
  holidayData.value.loading = true;
  getHolidayData.fetch();
}

const goBack = () => {
  holidayListActiveScreen.value = {
    screen: "list",
    data: null,
  };
};

const validateHoliday = () => {
  // Reset errors
  errors.value = {};
  let isValid = true;

  // Required field validation
  if (!holidayData.value.holiday_list_name?.trim()) {
    errors.value.holiday_list_name = "Holiday list name is required";
    isValid = false;
  }

  // Date validation
  if (!holidayData.value.from_date) {
    errors.value.from_date = "Start date is required";
    isValid = false;
  }

  if (!holidayData.value.to_date) {
    errors.value.end_date = "End date is required";
    isValid = false;
  }

  // Validate date range
  if (holidayData.value.from_date && holidayData.value.to_date) {
    const startDate = new Date(holidayData.value.from_date);
    const endDate = new Date(holidayData.value.to_date);

    if (startDate > endDate) {
      errors.value.dateRange = "Start date cannot be after end date";
      isValid = false;
    }
  }

  return isValid;
};

const saveHoliday = () => {
  if (!validateHoliday()) {
    return;
  }
  if (holidayListActiveScreen.value.data) {
    updateHoliday();
  } else {
    createHoliday();
  }
};

const createHoliday = () => {
  createResource({
    url: "frappe.client.insert",
    params: {
      doc: {
        doctype: "HD Service Holiday List",
        holiday_list_name: holidayData.value.holiday_list_name,
        description: holidayData.value.description,
        from_date: holidayData.value.from_date,
        to_date: holidayData.value.to_date,
        holidays: holidayData.value.holidays,
      },
    },
    auto: true,
    onSuccess() {
      toast.success("Holiday created successfully");
    },
  });
};

const updateHoliday = () => {
  createResource({
    url: "frappe.client.set_value",
    params: {
      doctype: "HD Service Holiday List",
      name: holidayListActiveScreen.value.data.name,
      fieldname: {
        description: holidayData.value.description,
        from_date: holidayData.value.from_date,
        to_date: holidayData.value.to_date,
        holidays: holidayData.value.holidays,
      },
    },
    auto: true,
    onSuccess() {
      toast.success("Holiday updated successfully");
    },
  });
};

const updateHolidays = (holidays) => {
  const newHolidays = holidayData.value.holidays.filter((h) => {
    return h.weekly_off == 0;
  });
  newHolidays.push(...holidays);
  holidayData.value.holidays = newHolidays;
};
</script>

<style scoped>
input[type="radio"] {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  border: 2px solid #c5c2c2;
  border-radius: 50%;
  outline: none;
  transition: all 0.2s ease;
  background-color: white;
}

input[type="radio"]:checked {
  background-color: black;
  border: 2px solid #000;
}

input[type="radio"]:checked::after {
  content: "";
  background-color: #fff;
}

input[type="radio"]:focus {
  outline: none !important;
  box-shadow: none !important;
}
</style>
