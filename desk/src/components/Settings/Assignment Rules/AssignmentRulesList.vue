<template>
  <div class="px-10 py-8">
    <div class="flex items-start justify-between">
      <div class="flex flex-col gap-2">
        <h1 class="text-lg font-semibold">Assignment rules</h1>
        <p class="text-sm text-gray-700 max-w-md">
          Assignment Rules automatically route tickets to the right team members
          based on predefined conditions.
        </p>
      </div>
      <Button
        label="Create new"
        theme="gray"
        variant="solid"
        @click="goToNew()"
        icon-left="plus"
      />
    </div>
    <div class="mt-6">
      <AssignmentRulesListView />
    </div>
  </div>
</template>

<script setup lang="ts">
import AssignmentRulesListView from "./AssignmentRulesListView.vue";
import {
  assignmentRulesListData,
  assignmentRulesActiveScreen,
} from "../../../stores/assignmentRules";
import { onMounted } from "vue";
import { Button } from "frappe-ui";

onMounted(() => {
  assignmentRulesListData.fetch();
});

const goToNew = () => {
  assignmentRulesActiveScreen.value = {
    screen: "view",
    data: null,
  };
};
</script>
