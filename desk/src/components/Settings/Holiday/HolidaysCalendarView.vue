<template>
  <div class="p-3 rounded-md border border-gray-300">
    <div class="mb-4 flex justify-between items-center">
      <div class="*:w-[86px]">
        <Select
          class="bg-white font-semibold text-xl hover:bg-white focus:!ring-0 outline-none border-0"
          :options="yearsOption"
          v-model="currentYear"
        />
      </div>
      <div class="flex gap-2 items-center">
        <Button
          variant="ghost"
          icon="chevron-left"
          class="mt-4"
          :disabled="visibleMonths === 'first-half'"
          @click="visibleMonths = 'first-half'"
        />
        <Button
          variant="ghost"
          label="Today"
          class="mt-4"
          @click="currentYear = new Date().getFullYear()"
        />
        <Button
          variant="ghost"
          icon="chevron-right"
          class="mt-4"
          :disabled="visibleMonths === 'second-half'"
          @click="visibleMonths = 'second-half'"
        />
      </div>
    </div>
    <div class="grid grid-cols-3 gap-5" v-if="visibleMonths === 'first-half'">
      <HLCalender
        v-for="month in months.slice(0, 6)"
        :key="month"
        :year="currentYear"
        :month="month"
        :holidays="props.holidayData.holidays"
      />
    </div>
    <div class="grid grid-cols-3 gap-5" v-else>
      <HLCalender
        v-for="month in months.slice(6, 12)"
        :key="month"
        :year="currentYear"
        :month="month"
        :holidays="props.holidayData.holidays"
      />
    </div>
    <div class="flex gap-2 items-center w-full justify-center mt-8">
      <div
        :class="[
          'size-1.5 rounded-full cursor-pointer',
          {
            'bg-black': visibleMonths === 'first-half',
            'bg-gray-400': visibleMonths === 'second-half',
          },
        ]"
        @click="visibleMonths = 'first-half'"
      />
      <div
        :class="[
          'size-1.5 rounded-full cursor-pointer',
          {
            'bg-black': visibleMonths === 'second-half',
            'bg-gray-400': visibleMonths === 'first-half',
          },
        ]"
        @click="visibleMonths = 'second-half'"
      />
    </div>
  </div>
  <AddHolidayModal v-model="dialog" />
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import HLCalender from "./HLCalender.vue";
import { Select } from "frappe-ui";

const visibleMonths = ref("first-half");
const months = ref([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);
const currentYear = ref(new Date().getFullYear());
const dialog = ref(false);
const yearsOption = ref([]);

const props = defineProps({
  holidayData: {
    type: Object,
    required: true,
  },
});

onMounted(() => {
  const startYear = new Date().getFullYear() - 20;
  const endYear = new Date().getFullYear() + 20;
  const years = [];
  for (let year = startYear; year <= endYear; year++) {
    years.push({
      label: year.toString(),
      value: year,
    });
  }
  yearsOption.value = years;
});
</script>
