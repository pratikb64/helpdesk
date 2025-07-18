<template>
  <div
    class="grid grid-cols-8 items-center gap-4 cursor-pointer hover:bg-gray-50 rounded p-2.5"
    @click="
      emailAccountActiveScreen = {
        screen: 'edit',
        provider: data.service,
        data: data,
      }
    "
  >
    <div class="col-span-6 flex gap-2 items-center">
      <div class="shadow-sm rounded-md border border-gray-300 p-1">
        <img :src="emailIcons[data.service].icon" class="size-5" />
      </div>
      <div class="flex flex-col gap-1">
        <span class="text-base font-medium text-ink-gray-8">
          {{ data.email_id }}
        </span>
        <span class="text-xs text-ink-gray-5">{{ data.name }}</span>
      </div>
    </div>
    <div class="col-span-2 ml-1 flex justify-between items-center">
      <div class="text-base text-ink-gray-6">
        {{ formatDate(dayjs(data.creation).toISOString()) }}
      </div>
      <Dropdown placement="right" :options="dropdownOptions">
        <Button
          icon="more-horizontal"
          variant="ghost"
          @click="isConfirmingDelete = false"
        />
      </Dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { emailIcons } from "./utils";
import { TemplateOption } from "@/utils";
import { Button, Dropdown } from "frappe-ui";
import dayjs from "dayjs";
import { emailAccountActiveScreen } from "@/stores/emailAccount";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

console.log("props.data", props.data);

const isConfirmingDelete = ref(false);

const dropdownOptions = [
  {
    label: "Duplicate",
    onClick: () => {
      //   duplicateDialog.value = {
      //     show: true,
      //     name: props.data.name + " (Copy)",
      //   };
    },
    icon: "copy",
  },
  {
    label: "Delete",
    component: (props) =>
      TemplateOption({
        option: "Delete",
        icon: "trash-2",
        active: props.active,
        variant: "gray",
        onClick: (event) => {},
      }),
    condition: () => !isConfirmingDelete.value,
  },
  {
    label: "Confirm Delete",
    component: (props) =>
      TemplateOption({
        option: "Confirm Delete",
        icon: "trash-2",
        active: props.active,
        variant: "danger",
        onClick: (event) => {},
      }),
    condition: () => isConfirmingDelete.value,
  },
];

const formatDate = (date: string) => dayjs(date).format("DD MMM YYYY");
</script>
