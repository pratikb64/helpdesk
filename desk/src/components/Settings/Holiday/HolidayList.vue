<template>
  <div>
    <div class="flex text-sm text-gray-600">
      <div class="ml-2">Schedule name</div>
    </div>
    <hr class="mx-2 mt-2" />
    <div>
      <div
        v-if="holidayListData.data"
        v-for="holiday in holidayListData.data"
        :key="holiday.name"
      >
        <HolidayListItem :data="holiday" />
        <hr class="mx-2" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import HolidayListItem from "./HolidayListItem.vue";
import { holidayListData } from "./holidayList";
</script>
