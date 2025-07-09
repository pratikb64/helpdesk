<template>
  <div>
    <div class="grid grid-cols-11 items-center gap-4 text-sm text-gray-600">
      <div class="col-span-7 ml-2">Assignment rule</div>
      <div class="col-span-2">Priority</div>
      <div class="col-span-2">Enabled</div>
    </div>
    <hr class="mt-2 mx-2" />
    <div>
      <div
        class="flex items-center justify-center mt-12"
        v-if="assignmentRulesListData.loading && !assignmentRulesListData.data"
      >
        <LoadingIndicator class="w-4" />
      </div>
      <div
        v-else
        v-for="assignmentRule in assignmentRulesListData.data"
        :key="assignmentRule.name"
      >
        <AssignmentRuleListItem :data="assignmentRule" />
        <hr class="mx-2" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { LoadingIndicator } from "frappe-ui";
import { assignmentRulesListData } from "../../../stores/assignmentRules";
import AssignmentRuleListItem from "./AssignmentRuleListItem.vue";
</script>
