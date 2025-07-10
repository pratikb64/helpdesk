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
            :label="
              assignmentRuleData.assignment_rule_name || 'New Assignment Rule'
            "
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
      <div class="flex items-center gap-2">
        <Badge
          :variant="'subtle'"
          :theme="'orange'"
          size="sm"
          label="Unsaved changes"
          v-if="isDirty"
        />
        <Button
          :disabled="Boolean(!isDirty && assignmentRulesActiveScreen.data)"
          label="Save"
          theme="gray"
          variant="solid"
          @click="saveAssignmentRule()"
        />
      </div>
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
          v-model="assignmentRuleData.assignment_rule_name"
          required
          @change="debouncedValidateAssignmentRule('assignment_rule_name')"
        />
        <span
          v-if="assignmentRulesErrors.assignment_rule_name"
          class="text-red-500 text-xs"
        >
          {{ assignmentRulesErrors.assignment_rule_name }}
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
        <AssignmentRulesSection
          :conditions="assignmentRuleData.assign_condition"
          name="assign_condition"
          :errors="assignmentRulesErrors.assign_condition_error"
        />
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
          >Unassignment rule</span
        >
        <span class="text-sm text-ink-gray-6">
          Choose which tickets are affected by this un-assignment rule.
          <a
            class="font-medium underline"
            href="https://docs.frappe.io/helpdesk/assignment-rule"
            target="_blank"
            >Learn about conditions</a
          >
        </span>
      </div>
      <div class="mt-4">
        <AssignmentRulesSection
          :conditions="assignmentRuleData.unassign_condition"
          name="unassign_condition"
          :errors="assignmentRulesErrors.unassign_condition_error"
        />
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
  <ConfirmDialog
    v-model="showConfirmDialog"
    title="Unsaved changes"
    message="Are you sure you want to go back? Unsaved changes will be lost."
    :onConfirm="goBack"
    :onCancel="() => (showConfirmDialog = false)"
  />
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from "vue";
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
} from "frappe-ui";
import { useDebounceFn } from "@vueuse/core";
import { assignmentRulesActiveScreen } from "../../../stores/assignmentRules";
import AssignmentRulesSection from "./AssignmentRulesSection.vue";
import AssignmentSchedule from "./AssignmentSchedule.vue";
import AssigneeRules from "./AssigneeRules.vue";
import ConfirmDialog from "@/components/ConfirmDialog.vue";

const isDirty = ref(false);
const initialData = ref(null);

const showConfirmDialog = ref(false);

const debouncedValidateAssignmentRule = useDebounceFn((key?: string) => {
  validateAssignmentRule(key);
}, 300);

const getAssignmentRuleData = createResource({
  url: "helpdesk.api.assignment_rule.get_assignment_rule",
  params: {
    docname: assignmentRulesActiveScreen.value.data?.name,
  },
  onSuccess(data) {
    assignmentRuleData.value = data;
    assignmentRuleData.value.loading = false;
    initialData.value = JSON.parse(JSON.stringify(assignmentRuleData.value));
  },
  transform(data) {
    data.assign_condition = JSON.parse(data.assign_condition || "[]");
    data.unassign_condition = JSON.parse(data.unassign_condition || "[]");
    data.assignment_rule_name = data.name;
    data.users = data.users.map((user) => {
      return {
        ...user,
        ticketCount:
          data.ticket_counts.find(
            (ticketCount) => ticketCount.user == user.user
          )?.count || 0,
      };
    });
    return data;
  },
  auto: false,
});

if (assignmentRulesActiveScreen.value.data) {
  assignmentRuleData.value.loading = true;
  getAssignmentRuleData.submit();
}

const goBack = () => {
  if (isDirty.value && !showConfirmDialog.value) {
    showConfirmDialog.value = true;
    return;
  }
  if (!assignmentRulesActiveScreen.value.data && !showConfirmDialog.value) {
    showConfirmDialog.value = true;
    return;
  }
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
    url: "helpdesk.api.assignment_rule.save_assignment_rule",
    params: {
      doc: {
        doctype: "Assignment Rule",
        name: assignmentRuleData.value.name,
        assignment_rule_name: assignmentRuleData.value.assignment_rule_name,
        description: assignmentRuleData.value.description,
        disabled: assignmentRuleData.value.disabled,
        priority: assignmentRuleData.value.priority,
        assign_condition: assignmentRuleData.value.assign_condition,
        unassign_condition: assignmentRuleData.value.unassign_condition,
        assignment_days: assignmentRuleData.value.assignment_days,
        document_type: "HD Ticket",
        rule: assignmentRuleData.value.rule,
        users: assignmentRuleData.value.users,
      },
      is_new: true,
    },
    auto: true,
    onSuccess(data) {
      getAssignmentRuleData.submit({
        docname: data.name,
      });
      assignmentRulesActiveScreen.value = {
        screen: "view",
        data: data,
      };
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
  createResource({
    url: "helpdesk.api.assignment_rule.save_assignment_rule",
    params: {
      doc: {
        doctype: "Assignment Rule",
        name: assignmentRuleData.value.name,
        assignment_rule_name: assignmentRuleData.value.assignment_rule_name,
        description: assignmentRuleData.value.description,
        disabled: assignmentRuleData.value.disabled,
        priority: assignmentRuleData.value.priority,
        assign_condition: assignmentRuleData.value.assign_condition,
        unassign_condition: assignmentRuleData.value.unassign_condition,
        assignment_days: assignmentRuleData.value.assignment_days,
        document_type: "HD Ticket",
        rule: assignmentRuleData.value.rule,
        users: assignmentRuleData.value.users,
      },
      is_new: false,
    },
    auto: true,
    onSuccess(data) {
      getAssignmentRuleData.submit({
        docname: data.name,
      });
      toast.success("Assignment rule updated");
    },
  });
};

watch(
  assignmentRuleData,
  (newVal) => {
    if (!initialData.value) return;
    isDirty.value =
      JSON.stringify(Object.assign({}, newVal)) !=
      JSON.stringify(Object.assign({}, initialData.value));
  },
  { deep: true }
);

const beforeUnloadHandler = (event) => {
  if (!isDirty.value) return;
  event.preventDefault();
  event.returnValue = true;
};

onMounted(() => {
  addEventListener("beforeunload", beforeUnloadHandler);
});

onUnmounted(() => {
  resetAssignmentRuleErrors();
  resetAssignmentRuleData();
  removeEventListener("beforeunload", beforeUnloadHandler);
});
</script>
