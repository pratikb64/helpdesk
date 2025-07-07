<template>
  <div
    v-if="assignmentRuleData.loading"
    class="flex items-center h-full justify-center"
  >
    <LoadingIndicator class="w-4" />
  </div>
  <div
    v-if="!assignmentRuleData.loading"
    class="sticky top-0 z-10 bg-white pb-6 px-10 py-8"
  >
    <div class="flex items-center justify-between w-full">
      <div>
        <div class="flex items-center gap-2">
          <Button
            variant="ghost"
            icon-left="chevron-left"
            :label="assignmentRuleData.name || 'New Assignment Rule'"
            size="md"
            @click="goBack()"
            class="cursor-pointer -ml-4 hover:bg-transparent focus:bg-transparent focus:outline-none focus:ring-0 focus:ring-offset-0 focus-visible:none active:bg-transparent active:outline-none active:ring-0 active:ring-offset-0 active:text-ink-gray-5"
          />
          <Badge
            :variant="'subtle'"
            :theme="assignmentRuleData.enabled ? 'blue' : 'gray'"
            size="sm"
            :label="assignmentRuleData.enabled ? 'Enabled' : 'Disabled'"
          />
        </div>
      </div>
      <Button
        label="Save"
        theme="gray"
        variant="solid"
        @click="saveAssignmentRule()"
      />
    </div>
  </div>
  <div v-if="!assignmentRuleData.loading" class="overflow-y-auto px-10 pb-8">
    <div
      class="flex items-center justify-between gap-2"
      @click="assignmentRuleData.enabled = !assignmentRuleData.enabled"
    >
      <span class="text-sm"> Enable Assignment Rule </span>
      <Switch size="sm" :model-value="assignmentRuleData.enabled" />
    </div>
    <hr class="mb-6 mt-3" />
    <div class="grid grid-cols-2 gap-5">
      <div>
        <FormControl
          :type="'text'"
          size="sm"
          variant="subtle"
          placeholder="Name"
          label="Name"
          v-model="assignmentRuleData.name"
          required
          @change="debouncedValidateAssignmentRule()"
        />
        <span v-if="assignmentRulesErrors.name" class="text-red-500 text-xs">
          {{ assignmentRulesErrors.name }}
        </span>
      </div>
      <div class="flex flex-col gap-1.5">
        <FormLabel label="Default priority" required />
        <Popover>
          <template #target="{ togglePopover }">
            <div
              class="flex items-center justify-between text-base rounded h-7 py-1.5 pl-2 pr-2 border border-[--surface-gray-2] bg-surface-gray-2 placeholder-ink-gray-4 hover:border-outline-gray-modals hover:bg-surface-gray-3 focus:bg-surface-white focus:border-outline-gray-4 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-outline-gray-3 text-ink-gray-8 transition-colors w-full dark:[color-scheme:dark] cursor-default"
              @click="togglePopover()"
            >
              <div>
                {{
                  priorityOptions.find(
                    (option) => option.value == assignmentRuleData.priority
                  )?.label
                }}
              </div>
              <FeatherIcon name="chevron-down" class="size-4" />
            </div>
          </template>
          <template #body="{ togglePopover }">
            <div
              class="p-1 text-ink-gray-6 top-1 absolute w-full bg-white shadow-2xl rounded"
            >
              <div
                v-for="option in priorityOptions"
                :key="option.value"
                class="p-2 cursor-pointer hover:bg-gray-50 text-base flex items-center justify-between rounded"
                @click="
                  assignmentRuleData.priority = option.value;
                  togglePopover();
                "
              >
                {{ option.label }}
                <FeatherIcon
                  v-if="assignmentRuleData.priority == option.value"
                  name="check"
                  class="size-4"
                />
              </div>
            </div>
          </template>
        </Popover>
      </div>
      <FormControl
        :type="'textarea'"
        size="sm"
        variant="subtle"
        placeholder="Description"
        label="Description"
        v-model="assignmentRuleData.description"
      />
    </div>
    <hr class="my-6" />
    <div>
      <div class="flex flex-col gap-2">
        <span class="text-lg font-semibold text-ink-gray-7"
          >Assignment rule</span
        >
        <span class="text-sm text-ink-gray-6">
          Choose which tickets are affected by this assignment rule.
          <a
            class="font-medium underline"
            href="https://docs.frappe.io/helpdesk/assignment-rule"
            target="_blank"
            >Learn about conditions</a
          >
        </span>
      </div>
      <div class="mt-4">
        <AssignmentRulesSection />
      </div>
    </div>
    <hr class="my-6" />
    <div>
      <div class="flex flex-col gap-2">
        <span class="text-lg font-semibold text-ink-gray-7"
          >Assignment Schedule</span
        >
        <span class="text-sm text-ink-gray-6">
          Choose the days of the week when this rule should be active.
        </span>
      </div>
      <div class="mt-4">
        <AssignmentSchedule />
      </div>
    </div>
    <hr class="my-6" />
    <AssigneeRules />
  </div>
</template>

<script setup lang="ts">
import { onUnmounted } from "vue";
import {
  assignmentRuleData,
  assignmentRulesErrors,
  validateAssignmentRule,
} from "../../../stores/assignmentRules";
import {
  createResource,
  toast,
  LoadingIndicator,
  Switch,
  Button,
  Badge,
  FormControl,
  FormLabel,
  Popover,
  createDocumentResource,
} from "frappe-ui";
import { useDebounceFn } from "@vueuse/core";
import { assignmentRulesActiveScreen } from "../../../stores/assignmentRules";
import AssignmentRulesSection from "./AssignmentRulesSection.vue";
import AssignmentSchedule from "./AssignmentSchedule.vue";
import AssigneeRules from "./AssigneeRules.vue";
import { convertToObject } from "@/utils";

const debouncedValidateAssignmentRule = useDebounceFn(() => {
  validateAssignmentRule();
}, 300);

// const getAssignmentRuleData = createResource({
//   url: "helpdesk.api.assignment_rule.get_assignment_rule",
//   params: {
//     docname: assignmentRulesActiveScreen.value.data?.name,
//   },
//   onSuccess(data) {
//     const conditions = JSON.parse(data.assign_condition || "[]");
//     assignmentRuleData.value = {
//       ...data,
//       loading: false,
//       condition: conditions,
//     };
//   },
// });

const getAssignmentRuleData = createDocumentResource({
  doctype: "Assignment Rule",
  name: assignmentRulesActiveScreen.value.data?.name,
  onSuccess(data) {
    // const conditions = JSON.parse(data.assign_condition || "[]");
    // assignmentRuleData.value.condition = [];
    // assignmentRuleData.value.assign_condition =
    //   data.assign_condition?.length > 0 ? conditions : [];
    // console.log("assignmentRuleData.value", assignmentRuleData.value);
    assignmentRuleData.value = getAssignmentRuleData.doc;
    assignmentRuleData.value.loading = false;
  },
  transform(doc) {
    // const condition = JSON.parse(doc.assign_condition || "[]");
    doc.condition = convertToObject(doc.assign_condition);
    // doc.assign_condition = JSON.parse(doc.assign_condition || "[]");
    return doc;
  },
});

if (assignmentRulesActiveScreen.value.data) {
  assignmentRuleData.value.loading = true;
  getAssignmentRuleData.get.submit();
  console.log("getAssignmentRuleDat", getAssignmentRuleData);
}

const goBack = () => {
  assignmentRulesActiveScreen.value = {
    screen: "list",
    data: null,
  };
};

const saveAssignmentRule = () => {
  // Reset all errors
  assignmentRulesErrors.value = {
    name: "",
  };
  const validationErrors = validateAssignmentRule();
  if (Object.values(validationErrors).some((error) => error)) {
    toast.error("Please provide all required fields");
    return;
  }
  if (assignmentRulesActiveScreen.value.data) {
    updateAssignmentRule();
  } else {
    createAssignmentRule();
  }
};

const createAssignmentRule = () => {
  createResource({
    url: "helpdesk.api.assignment_rule.create_assignment_rule",
    params: {
      doc: {
        doctype: "Assignment Rule",
        enabled: assignmentRuleData.value.enabled,
        description: assignmentRuleData.value.description,
        service_level: assignmentRuleData.value.service_level,
        priorities: assignmentRuleData.value.priorities,
        condition: assignmentRuleData.value.condition,
      },
      is_new: true,
    },
    auto: true,
    onSuccess(data) {
      toast.success("Assignment rule created");
      assignmentRulesActiveScreen.value.data = data;
      assignmentRulesActiveScreen.value.screen = "view";
      getAssignmentRuleData.submit({
        docname: data.name,
      });
    },
  });
};

const priorityOptions = [
  { label: "Low", value: "0" },
  { label: "Medium-Low", value: "1" },
  { label: "Medium", value: "2" },
  { label: "Medium-High", value: "3" },
  { label: "High", value: "4" },
];

const updateAssignmentRule = () => {
  createResource({
    url: "helpdesk.api.assignment_rule.update_assignment_rule",
    params: {
      doc: {
        doctype: "Assignment Rule",
        name: assignmentRulesActiveScreen.value.data.name,
        enabled: assignmentRuleData.value.enabled,
        description: assignmentRuleData.value.description,
        condition: assignmentRuleData.value.condition,
      },
      is_new: false,
    },
    auto: true,
    onSuccess() {
      getAssignmentRuleData.submit();
      toast.success("Assignment rule updated");
    },
  });
};

onUnmounted(() => {
  assignmentRulesErrors.value = {
    name: "",
  };
  assignmentRuleData.value = {
    loading: false,
    name: "",
    enabled: false,
    description: "",
    rule: "Round Robin",
    priority: 1,
    condition: [],
  };
});
</script>
