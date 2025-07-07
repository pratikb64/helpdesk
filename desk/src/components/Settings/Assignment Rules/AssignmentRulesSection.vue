<template>
  <AssignmentConditions
    v-if="assignmentRuleData.condition.length > 0"
    :conditions="assignmentRuleData.condition"
    :level="0"
  />
  <div
    v-if="assignmentRuleData.condition.length == 0"
    class="flex p-4 items-center cursor-pointer justify-center gap-2 text-sm border border-gray-300 text-gray-600 rounded-md"
    @click="
      assignmentRuleData.condition.push({
        field: null,
        operator: 'equals',
        value: '',
        conjunction: 'and',
      })
    "
  >
    <FeatherIcon name="plus" class="h-4" />
    Add a condition
  </div>
  <div class="flex items-center justify-between">
    <Dropdown
      v-if="assignmentRuleData.condition.length > 0"
      class="mt-2"
      v-slot="{ open }"
      :options="[
        {
          label: 'Add condition',
          onClick: () => {
            addCondition();
          },
        },
        {
          label: 'Add condition group',
          onClick: () => {
            const conjunction =
              assignmentRuleData.condition.length > 1
                ? assignmentRuleData.condition[1]?.conjunction
                : 'and';
            assignmentRuleData.condition.push({
              field: 'group',
              operator: 'equals',
              value: [
                {
                  field: null,
                  operator: 'equals',
                  value: '',
                  conjunction: 'and',
                },
              ],
              conjunction: conjunction,
            });
          },
        },
      ]"
    >
      <!-- :disabled="slaDataErrors.condition !== ''" -->
      <Button
        :icon-right="open ? 'chevron-up' : 'chevron-down'"
        label="Add condition"
      />
    </Dropdown>
    <!-- <div v-if="slaDataErrors.condition" class="text-red-500 text-xs mt-2">
        {{ slaDataErrors.condition }}
      </div> -->
  </div>
</template>

<script setup lang="ts">
import { Button, Dropdown, FeatherIcon } from "frappe-ui";
//   import {
//     slaDataErrors,
//     validateConditions,
//     validateSlaData,
//   } from "@/stores/sla";
import { watchDebounced } from "@vueuse/core";
import { assignmentRuleData } from "../../../stores/assignmentRules";

type Conditions = {
  field: string | object | null;
  operator: string;
  value: string | number | boolean | Array<any>;
  conjunction?: string;
};

const addCondition = () => {
  // const isValid = validateConditions(assignmentRuleData.value.condition);
  const isValid = true;

  if (!isValid) {
    return;
  }
  const conjunction =
    assignmentRuleData.value.condition.length > 1
      ? assignmentRuleData.value.condition[1]?.conjunction
      : "and";

  assignmentRuleData.value.condition.push({
    field: null,
    operator: "equals",
    value: "",
    conjunction: conjunction,
  });
};

watchDebounced(
  () => [...assignmentRuleData.value.condition],
  () => {
    // validateSlaData("condition");
  },
  { deep: true, debounce: 300 }
);
</script>
