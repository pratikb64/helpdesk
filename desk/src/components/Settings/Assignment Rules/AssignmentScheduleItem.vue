<template>
  <div
    class="grid p-2 py-3 items-center"
    style="grid-template-columns: 3fr 1fr"
  >
    <div>{{ day.day }}</div>
    <div class="flex justify-start">
      <Switch v-model="day.active" />
    </div>
  </div>
  <hr class="my-0.5" v-if="!props.isLast" />
</template>

<script setup lang="ts">
import { Switch } from "frappe-ui";
import { ref } from "vue";

const props = defineProps({
  day: {
    type: Object,
    required: true,
  },
  isLast: {
    type: Boolean,
    default: false,
  },
});
</script>
