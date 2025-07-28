<template>
  <div class="rounded-lg border border-gray-300 p-3 flex flex-col gap-4 w-full">
    <template v-for="(condition, i) in props.conditions" :key="condition.field">
      <AssignmentCondition
        v-if="Array.isArray(condition)"
        :condition="condition"
        :doctype="'HD Ticket'"
        :isChild="props.isChild"
        :itemIndex="i"
        @remove="removeCondition(condition)"
        @unGroupConditions="unGroupConditions(condition)"
        :level="props.level + 1"
        @updateConjunction="updateConjunction(props.level)"
        :isGroup="isGroupCondition(condition[0])"
      />
    </template>
    <div v-if="props.isChild" class="flex">
      <Dropdown v-slot="{ open }" :options="dropdownOptions">
        <Button
          :disabled="slaDataErrors.condition !== ''"
          label="Add condition"
          icon-left="plus"
          :icon-right="open ? 'chevron-up' : 'chevron-down'"
        />
      </Dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { slaDataErrors } from "@/stores/sla";
import { Button, Dropdown } from "frappe-ui";
import { computed, onMounted } from "vue";
import { filterableFields } from "../utils";
import AssignmentCondition from "./AssignmentCondition.vue";

const props = defineProps({
  conditions: {
    type: Array<any>,
    required: true,
  },
  isChild: {
    type: Boolean,
    default: false,
  },
  level: {
    type: Number,
    default: 0,
  },
});

const isGroupCondition = (condition) => {
  console.log("condition", condition);
  return Array.isArray(condition);
};

const dropdownOptions = computed(() => {
  const options = [
    {
      label: "Add condition",
      onClick: () => {
        // const conjunction = props.conditions[0]?.conjunction;
        console.log("props.conditions dd", props.conditions);
        props.conditions.push("and", ["", "", ""]);
      },
    },
  ];
  if (props.level < 3) {
    options.push({
      label: "Add condition group",
      onClick: () => {
        // const conjunction = props.conditions[0]?.conjunction;
        console.log("props.conditions dd group", props.conditions);

        props.conditions.push("and", [[]]);
      },
    });
  }
  return options;
});

function removeCondition(condition) {
  props.conditions.splice(props.conditions.indexOf(condition) - 1, 2);
}

function unGroupConditions(condition) {
  const index = props.conditions.indexOf(condition);
  if (index !== -1 && Array.isArray(condition.value)) {
    props.conditions.splice(index, 1, ...condition.value);
  } else {
    props.conditions.splice(index, 1);
  }
}

function updateConjunction(level) {
  const updateConjunctions = (conditions, targetLevel, currentLevel = 0) => {
    if (!conditions || !Array.isArray(conditions)) return;
    const newConjunction = conditions[1]?.conjunction === "and" ? "or" : "and";
    if (currentLevel === targetLevel) {
      conditions.forEach((condition) => {
        if (condition.conjunction) {
          condition.conjunction = newConjunction;
        }
      });
    } else if (currentLevel < targetLevel) {
      updateConjunctions(props.conditions, level, currentLevel + 1);
    }
  };

  updateConjunctions(props.conditions, level);
}
onMounted(() => {
  if (!filterableFields.fetched) {
    filterableFields.submit();
  }
});
</script>
