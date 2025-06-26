<template>
  <Popover>
    <template #target="{ togglePopover, isOpen }">
      <slot
        name="trigger"
        :toggle="() => handleButtonClick(togglePopover)"
        :isOpen="isOpen"
        :selectedYear="selectedYear"
      >
        <Button
          :variant="buttonVariant"
          :class="buttonClass"
          @click="handleButtonClick(togglePopover)"
          :label="selectedYear + '' || placeholder"
        />
      </slot>
    </template>
    <template #body-main>
      <div class="w-32">
        <div ref="yearsContainer" class="max-h-60 overflow-y-auto py-1">
          <div
            v-for="year in years"
            :key="year"
            ref="yearItems"
            class="cursor-pointer px-3 py-1.5 text-sm hover:bg-gray-100"
            :class="{ 'bg-gray-100 font-medium': year === selectedYear }"
            @click="selectYear(year)"
          >
            {{ year }}
          </div>
        </div>
      </div>
    </template>
  </Popover>
</template>

<script setup lang="ts">
import { Popover, Button } from "frappe-ui";
import { ref, onMounted, nextTick, watch } from "vue";

const props = withDefaults(
  defineProps<{
    modelValue?: string | number;
    startYear?: number;
    endYear?: number;
    buttonVariant?: "solid" | "outline" | "ghost" | "subtle";
    buttonClass?: string | Record<string, boolean> | Array<string>;
    placeholder?: string;
  }>(),
  {
    modelValue: () => new Date().getFullYear(),
    startYear: 2020,
    endYear: () => new Date().getFullYear() + 5,
    buttonVariant: "outline",
    buttonClass: "",
    placeholder: "Select Year",
  }
);

const emit = defineEmits(["update:modelValue"]);

const selectedYear = ref<number | string>(props.modelValue);
const yearsContainer = ref<HTMLElement | null>(null);
const yearItems = ref<HTMLElement[]>([]);
const years = ref<number[]>([]);

const generateYears = () => {
  const yearList = [];
  for (let year = props.startYear; year <= props.endYear; year++) {
    yearList.push(year);
  }
  years.value = yearList;
};

watch(
  [() => props.startYear, () => props.endYear],
  () => {
    generateYears();
  },
  { immediate: true }
);

const scrollToSelectedYear = async () => {
  await nextTick();
  const selectedIndex = years.value.findIndex((y) => y === selectedYear.value);
  if (
    selectedIndex !== -1 &&
    yearItems.value[selectedIndex] &&
    yearsContainer.value
  ) {
    const item = yearItems.value[selectedIndex];
    const container = yearsContainer.value;
    const itemRect = item.getBoundingClientRect();

    const scrollTop =
      item.offsetTop - container.clientHeight / 2 + itemRect.height / 2;

    container.scrollTo({
      top: scrollTop,
    });
  }
};

const handleButtonClick = (togglePopover: () => void) => {
  togglePopover();
  nextTick(() => {
    scrollToSelectedYear();
  });
};

const selectYear = (year: number) => {
  selectedYear.value = year;
  emit("update:modelValue", year);
};

watch(
  () => props.modelValue,
  (newVal) => {
    if (newVal !== selectedYear.value) {
      selectedYear.value = newVal;
      scrollToSelectedYear();
    }
  }
);

onMounted(() => {
  generateYears();
  nextTick(scrollToSelectedYear);
});
</script>
