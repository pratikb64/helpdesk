<template>
  <div>
    <div class="flex text-sm text-gray-600">
      <div class="">Schedule name</div>
    </div>
    <hr class="mt-2" />
    <div>
      <div
        v-if="holidayListData.data"
        v-for="holiday in holidayListData.data"
        :key="holiday.name"
      >
        <HolidayListItem :data="holiday" />
        <hr />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import HolidayListItem from "./HolidayListItem.vue";
import { holidayListData } from "./holidayList";
</script>
