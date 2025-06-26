<template>
  <div>
    <div class="flex text-sm text-gray-600">
      <div class="w-4/5 ml-2">Policy Name</div>
      <div class="w-1/5">Enabled</div>
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
