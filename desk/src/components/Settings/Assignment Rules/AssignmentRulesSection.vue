<template>
  <AssignmentConditions
    v-if="assignmentRuleData.assign_condition.length > 0"
    :conditions="assignmentRuleData.assign_condition"
    :level="0"
  />
  <div
    v-if="assignmentRuleData.assign_condition.length == 0"
    class="flex p-4 items-center cursor-pointer justify-center gap-2 text-sm border border-gray-300 text-gray-600 rounded-md"
    @click="
      assignmentRuleData.assign_condition.push({
        field: null,
        operator: 'equals',
        value: '',
        conjunction: 'and',
      });
      validateAssignmentRule('assign_condition');
    "
  >
    <FeatherIcon name="plus" class="h-4" />
    Add a condition
  </div>
  <div class="flex items-center justify-between">
    <Dropdown
      v-if="assignmentRuleData.assign_condition.length > 0"
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
              assignmentRuleData.assign_condition.length > 1
                ? assignmentRuleData.assign_condition[1]?.conjunction
                : 'and';
            assignmentRuleData.assign_condition.push({
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
      <Button
        :disabled="assignmentRulesErrors.assign_condition_error !== ''"
        :icon-right="open ? 'chevron-up' : 'chevron-down'"
        label="Add condition"
      />
    </Dropdown>
    <div
      v-if="assignmentRulesErrors.assign_condition_error"
      class="text-red-500 text-xs mt-2"
    >
      {{ assignmentRulesErrors.assign_condition_error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { Button, Dropdown, FeatherIcon } from "frappe-ui";
import { watchDebounced } from "@vueuse/core";
import {
  assignmentRuleData,
  assignmentRulesErrors,
  validateAssignmentRule,
  validateConditions,
} from "../../../stores/assignmentRules";
import AssignmentConditions from "./Assignment Conditions/AssignmentConditions.vue";

const addCondition = () => {
  const isValid = validateConditions(assignmentRuleData.value.assign_condition);

  if (!isValid) {
    return;
  }
  const conjunction =
    assignmentRuleData.value.assign_condition.length > 1
      ? assignmentRuleData.value.assign_condition[1]?.conjunction
      : "and";

  assignmentRuleData.value.assign_condition.push({
    field: null,
    operator: "equals",
    value: "",
    conjunction: conjunction,
  });
};

watchDebounced(
  () => [...assignmentRuleData.value.assign_condition],
  () => {
    validateAssignmentRule("assign_condition");
  },
  { deep: true, debounce: 300 }
);
</script>
