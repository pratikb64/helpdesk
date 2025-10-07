<template>
  <div class="px-10 py-8 sticky top-0">
    <SettingsLayoutHeader>
      <template #title>
        <h1 class="text-lg font-semibold text-ink-gray-8">
          {{ __("Assignment rules") }}
        </h1>
      </template>
      <template #description>
        <p class="text-p-sm max-w-md text-ink-gray-6">
          {{
            __(
              "Assignment Rules automatically route tickets to the right team members based on predefined conditions."
            )
          }}
        </p>
      </template>
      <template #actions>
        <Button
          :label="__('Create new')"
          theme="gray"
          variant="solid"
          @click="goToNew()"
          icon-left="plus"
        />
      </template>
      <template
        v-if="assignmentRulesListData.data?.length > 0 || search.length"
        #bottom-section
      >
        <div class="relative">
          <Input
            v-model="search"
            @input="search = $event"
            placeholder="Search"
            type="text"
            class="bg-white hover:bg-white focus:ring-0 border-outline-gray-2"
            icon-left="search"
            debounce="300"
            inputClass="p-4 pr-12"
          />
          <Button
            v-if="search"
            icon="x"
            variant="ghost"
            @click="search = ''"
            class="absolute right-1 top-1/2 -translate-y-1/2"
          />
        </div>
      </template>
    </SettingsLayoutHeader>
  </div>
  <div class="overflow-y-auto px-10 pb-8">
    <AssignmentRulesListView />
  </div>
</template>

<script setup lang="ts">
import { Button, createResource } from "frappe-ui";
import { provide, ref, watch } from "vue";
import {
  assignmentRulesActiveScreen,
  resetAssignmentRuleData,
} from "../../../stores/assignmentRules";
import AssignmentRulesListView from "./AssignmentRulesListView.vue";
import SettingsLayoutHeader from "../SettingsLayoutHeader.vue";

const search = ref("");

const assignmentRulesListData = createResource({
  url: "helpdesk.api.assignment_rule.get_assignment_rules_list",
  cache: ["assignmentRules", "get_assignment_rules_list"],
  auto: true,
});

provide("assignmentRulesList", assignmentRulesListData);

const goToNew = () => {
  resetAssignmentRuleData();
  assignmentRulesActiveScreen.value = {
    screen: "view",
    data: null,
  };
};
</script>
