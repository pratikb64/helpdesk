<template>
  <Dialog v-model="dialog" :options="{ size: 'sm' }">
    <template #body-title>
      <h3 class="text-2xl font-semibold">
        {{ isEditing ? "Edit" : "Add" }} Holiday
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
            :formatter="(date) => getFormat(date)"
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
        {{ isEditing ? "Update" : "Add" }} Holiday
        <template #prefix>
          <FeatherIcon :name="isEditing ? 'edit' : 'plus'" class="size-4" />
        </template>
      </Button>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import {
  Dialog,
  FormControl,
  Button,
  FormLabel,
  DatePicker,
  toast,
} from "frappe-ui";
import { getDateValue } from "frappe-ui/src/components/DatePicker/utils";
import { getFormat } from "@/utils";

const props = defineProps({
  holidays: {
    type: Array<any>,
    required: true,
  },
  isEditing: {
    type: Boolean,
    required: true,
  },
  holiday: {
    type: Object,
  },
});
const dialog = defineModel<boolean>();
const editHolidayData = ref({
  holiday_date: props.holiday?.holiday_date || null,
  description: props.holiday?.description || "",
});
watch(props.holiday, () => {
  editHolidayData.value = {
    holiday_date: props.holiday?.holiday_date || null,
    description: props.holiday?.description || "",
  };
});
onMounted(() => {
  console.log("editHolidayData", editHolidayData.value);
});
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

  if (existingHoliday) {
    console.log("A holiday already exists", existingHoliday);
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

  console.log(
    "editHolidayData.value.holiday_date",
    editHolidayData.value.holiday_date,
    index
  );

  if (index === -1) {
    props.holidays.push({
      ...editHolidayData.value,
      weekly_off: 0,
    });
    dialog.value = false;
    editHolidayData.value = { holiday_date: null, description: "" };
  } else {
    console.log(
      "Cannot add new holidays. Please edit an existing holiday.",
      index
    );
    toast.error("Cannot add new holidays. Please edit an existing holiday.");
  }
};
</script>
