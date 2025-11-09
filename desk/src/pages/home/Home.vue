<template>
  <LayoutHeader>
    <template #left-header>
      <div class="text-lg font-medium text-gray-900">Home</div>
    </template>
    <template #right-header>
      <div class="flex items-center gap-2">
        <Button
          :label="editing ? 'Save' : 'Edit'"
          variant="subtle"
          :icon-left="editing ? '' : 'edit'"
          @click="editing = !editing"
        />
        <Button label="New" variant="solid" icon-left="plus" />
      </div>
    </template>
  </LayoutHeader>
  <div class="p-5 mx-auto max-w-6xl w-full">
    <div>
      <div class="text-xl font-semibold text-ink-gray-8">
        Hey, {{ userName }}
      </div>
      <div class="text-sm text-ink-gray-5 mt-1">
        You have
        <span class="font-semibold text-ink-gray-7">3 overdue responses</span>
        and
        <span class="font-semibold text-ink-gray-7">
          2 tickets about to breach SLA
        </span>
      </div>
      <div class="mt-5">
        <GridLayout
          v-if="items.length > 0"
          class="h-fit w-full"
          :class="[editing ? 'mb-[20rem] !select-none' : '']"
          :cols="50"
          :rowHeight="42"
          :disabled="!editing"
          :modelValue="items.map((item) => item.layout)"
          @update:modelValue="
            (newLayout) => {
              items.forEach((item, idx) => {
                item.layout = newLayout[idx];
              });
            }
          "
        >
          <template #item="{ index }">
            <div class="group relative flex h-full w-full p-2 text-ink-gray-8">
              <div
                class="flex h-full w-full items-center justify-center"
                :class="
                  editing
                    ? 'pointer-events-none  [&>div:first-child]:rounded [&>div:first-child]:group-hover:ring-2 [&>div:first-child]:group-hover:ring-outline-gray-2'
                    : ''
                "
              >
                <DashboardItem
                  :index="index"
                  :item="items[index]"
                  :editing="editing"
                />
              </div>
              <div
                v-if="editing"
                class="flex absolute right-0 top-0 bg-surface-gray-6 rounded cursor-pointer opacity-0 group-hover:opacity-100"
              >
                <div
                  class="rounded p-1 hover:bg-surface-gray-5"
                  @click="items.splice(index, 1)"
                >
                  <FeatherIcon name="trash-2" class="size-3 text-ink-white" />
                </div>
              </div>
            </div>
          </template>
        </GridLayout>
        <!-- <UpcomingSlaViolations />
        <Card :config="{}" /> -->
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { LayoutHeader } from "@/components";
import { Button, GridLayout } from "frappe-ui";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import UpcomingSlaViolations from "./components/UpcomingSlaViolations.vue";
import Card from "./components/Card.vue";
import { ref, watch } from "vue";
import DashboardItem from "./components/DashboardItem.vue";

const { userName } = storeToRefs(useAuthStore());
const editing = ref(false);
const items = ref([
  {
    type: "card",
    data: {
      xAxis: {
        type: "category",
        show: false,
      },
      yAxis: {
        type: "value",
        show: false,
      },
      series: [
        {
          data: [
            210, 42, 470, 360, 35, 170, 16, 380, 242, 31, 390, 30, 170, 12, 280,
            38, 25, 300, 37, 140, 140, 360, 39, 692, 143, 174, 163, 176, 125,
            162, 131,
          ],
          type: "line",
          symbol: "none",
        },
      ],
      color: "green",
      grid: {
        left: 0,
        right: 0,
        top: 0,
        bottom: 0,
      },
    },
    layout: {
      x: 0,
      y: 0,
      w: 17,
      h: 3,
      i: 0,
      moved: false,
    },
  },
  {
    type: "card",
    data: {
      xAxis: {
        type: "category",
        show: false,
      },
      yAxis: {
        type: "value",
        show: false,
      },
      series: [
        {
          data: [
            210, 42, 470, 360, 35, 170, 16, 380, 242, 31, 390, 30, 170, 12, 280,
            38, 25, 300, 37, 140, 140, 360, 39, 692, 143, 174, 163, 176, 125,
            162, 131,
          ],
          type: "line",
          symbol: "none",
        },
      ],
      color: "red",
      grid: {
        left: 0,
        right: 0,
        top: 0,
        bottom: 0,
      },
    },
    layout: {
      x: 17,
      y: 0,
      w: 16,
      h: 3,
      i: 1,
      moved: false,
    },
  },
  {
    type: "card",
    data: {
      xAxis: {
        type: "category",
        show: false,
      },
      yAxis: {
        type: "value",
        show: false,
      },
      series: [
        {
          data: [
            210, 42, 470, 360, 35, 170, 16, 380, 242, 31, 390, 30, 170, 12, 280,
            38, 25, 300, 37, 140, 140, 360, 39, 692, 143, 174, 163, 176, 125,
            162, 131,
          ],
          type: "line",
          symbol: "none",
        },
      ],
      color: "green",
      grid: {
        left: 0,
        right: 0,
        top: 0,
        bottom: 0,
      },
    },
    layout: {
      x: 33,
      y: 0,
      w: 17,
      h: 3,
      i: 2,
      moved: false,
    },
  },
  {
    type: "upcoming_sla_violations",
    data: {},
    layout: {
      x: 0,
      y: 3,
      w: 50,
      h: 8,
      i: 3,
      moved: false,
    },
  },
]);

watch(
  items,
  (newItems) => {
    console.log("items", newItems);
  },
  { deep: true }
);
</script>
