<template>
  <div
    class="grid grid-cols-8 items-center gap-4 cursor-pointer hover:bg-gray-50 rounded p-2.5"
  >
    <div class="col-span-6 flex gap-2 items-center">
      <div class="shadow-sm rounded-md border border-gray-300 p-1">
        <img :src="emailIcons['GMail'].icon" class="size-5" />
      </div>
      <div class="flex flex-col gap-1">
        <span class="text-base font-medium text-ink-gray-8"
          >name@gmail.com</span
        >
        <span class="text-xs text-ink-gray-5">GMail</span>
      </div>
    </div>
    <div class="col-span-2 ml-1 flex justify-between items-center">
      <div class="text-base text-ink-gray-6">
        {{ formatDate(dayjs().toISOString()) }}
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
import { emailIcons } from "./emailConfig";
import { TemplateOption } from "@/utils";
import { Button, Dropdown } from "frappe-ui";
import dayjs from "dayjs";

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
