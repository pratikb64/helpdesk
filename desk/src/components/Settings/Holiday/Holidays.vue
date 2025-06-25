<template>
  <div class="px-10 py-8">
    <div class="flex items-center justify-between">
      <div class="flex flex-col gap-2">
        <h1 class="text-lg font-semibold">Work schedule and holidays</h1>
        <p class="text-sm text-gray-700 mt-1 max-w-lg">
          Set your team’s working days, hours, and holidays using a template or
          custom schedule.
        </p>
      </div>
      <Button
        label="Create new"
        theme="gray"
        variant="solid"
        @click="goToNew()"
      >
        <template #prefix>
          <LucidePlus class="h-4 w-4" />
        </template>
      </Button>
    </div>
    <div class="mt-6">
      <HolidayList />
    </div>
  </div>
</template>

<script setup lang="ts">
import { holidayListData, holidayListActiveScreen } from "./holidayList";
import HolidayList from "./HolidayList.vue";
import { onMounted } from "vue";

onMounted(() => {
  holidayListData.fetch();
});

const goToNew = () => {
  holidayListActiveScreen.value = {
    screen: "view",
    data: null,
  };
};
</script>
