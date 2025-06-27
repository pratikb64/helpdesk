<template>
  <div>
    <div class="grid grid-cols-6 items-center gap-4 text-sm text-gray-600">
      <div class="col-span-5">Policy Name</div>
      <div class="col-span-1">Enabled</div>
    </div>
    <hr class="mt-2 mx-2" />
    <div>
      <div
        v-if="slaPolicyListData.data"
        v-for="sla in slaPolicyListData.data"
        :key="sla.name"
      >
        <SlaPolicyListItem :data="sla" />
        <hr class="mx-2" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import SlaPolicyListItem from "./SlaPolicyListItem.vue";
import { slaPolicyListData } from "./sla";
</script>
