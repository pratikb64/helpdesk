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
            :theme="assignmentRuleData.disabled ? 'gray' : 'blue'"
            size="sm"
            :label="assignmentRuleData.disabled ? 'Disabled' : 'Enabled'"
          />
        </div>
      </div>
      <!-- :disabled="getAssignmentRuleData.isDirty" -->
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
      @click="assignmentRuleData.disabled = !assignmentRuleData.disabled"
    >
      <span class="text-sm"> Enable Assignment Rule </span>
      <Switch size="sm" :model-value="!assignmentRuleData.disabled" />
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
          @change="debouncedValidateAssignmentRule('name')"
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
      <div>
        <FormControl
          :type="'textarea'"
          size="sm"
          variant="subtle"
          placeholder="Description"
          label="Description"
          required
          @change="debouncedValidateAssignmentRule('description')"
          v-model="assignmentRuleData.description"
        />
        <span
          v-if="assignmentRulesErrors.description"
          class="text-red-500 text-xs"
        >
          {{ assignmentRulesErrors.description }}
        </span>
      </div>
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
        <div
          v-if="assignmentRulesErrors.assign_condition"
          class="text-red-500 text-xs mt-2"
        >
          {{ assignmentRulesErrors.assign_condition }}
        </div>
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
  resetAssignmentRuleData,
  resetAssignmentRuleErrors,
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
import { convertToConditions, convertToObject } from "@/utils";

const debouncedValidateAssignmentRule = useDebounceFn((key?: string) => {
  validateAssignmentRule(key);
}, 300);

const createAssignmentRuleResource = (name: string) => {
  return createDocumentResource({
    doctype: "Assignment Rule",
    name: name,
    onSuccess() {
      assignmentRuleData.value = getAssignmentRuleData.doc;
      assignmentRuleData.value.loading = false;
    },
    transform(doc) {
      doc.assign_condition = convertToObject(doc.assign_condition);
      return doc;
    },
    auto: false,
  });
};

let getAssignmentRuleData = createAssignmentRuleResource(
  assignmentRulesActiveScreen.value.data?.name
);

if (assignmentRulesActiveScreen.value.data) {
  assignmentRuleData.value.loading = true;
  getAssignmentRuleData.get?.submit();
}

const goBack = () => {
  assignmentRulesActiveScreen.value = {
    screen: "list",
    data: null,
  };
};

const saveAssignmentRule = () => {
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
    url: "frappe.client.insert",
    params: {
      doc: {
        doctype: "Assignment Rule",
        name: assignmentRuleData.value.name,
        description: assignmentRuleData.value.description,
        disabled: assignmentRuleData.value.disabled,
        priority: assignmentRuleData.value.priority,
        assign_condition: convertToConditions(
          assignmentRuleData.value.assign_condition
        ),
        assignment_days: assignmentRuleData.value.assignment_days,
        document_type: "HD Ticket",
        rule: assignmentRuleData.value.rule,
        users: assignmentRuleData.value.users,
      },
    },
    auto: true,
    onSuccess(data) {
      assignmentRulesActiveScreen.value = {
        screen: "view",
        data: data,
      };
      getAssignmentRuleData = createAssignmentRuleResource(data.name);
      getAssignmentRuleData.get?.submit();
      toast.success("Assignment rule created");
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

const updateAssignmentRule = async () => {
  console.log("getAssignmentRuleData", getAssignmentRuleData);
  console.log("getAssignmentRuleData", getAssignmentRuleData.save);
  let convertedCondition = convertToConditions(
    assignmentRuleData.value.assign_condition
  );
  await getAssignmentRuleData.setValue.submit({
    ...assignmentRuleData.value,
    assign_condition: convertedCondition,
  });
};

onUnmounted(() => {
  resetAssignmentRuleErrors();
  resetAssignmentRuleData();
});
</script>
