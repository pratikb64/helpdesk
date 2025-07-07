<template>
  <div
    class="grid grid-cols-11 items-center gap-4 cursor-pointer hover:bg-gray-50 rounded"
  >
    <div
      @click="assignmentRulesActiveScreen = { screen: 'view', data: data }"
      class="w-full py-3 pl-2 col-span-7"
    >
      <div class="text-base">{{ data.name }}</div>
      <div
        v-if="data.description && data.description.length > 0"
        class="text-sm w-full text-gray-500 mt-1 whitespace-nowrap overflow-ellipsis overflow-hidden"
      >
        {{ data.description }}
      </div>
    </div>
    <div class="col-span-2">
      <Select
        class="w-max bg-transparent -ml-2 border-0 focus-visible:!ring-0 bg-none"
        :options="priorityOptions"
        v-model="data.priority"
        @update:modelValue="onPriorityChange"
      />
    </div>
    <div class="flex justify-between items-center w-full pr-2 col-span-2">
      <div>
        <Switch
          size="sm"
          :modelValue="!data.disabled"
          @update:modelValue="onToggle"
        />
      </div>
      <div>
        <Dropdown
          placement="right"
          :options="[
            {
              label: 'Duplicate',
              onClick: () => {
                duplicateDialog = {
                  show: true,
                  name: props.data.name + ' (Copy)',
                };
              },
              icon: 'copy',
            },
            {
              label: 'Confirm Delete',
              component: (props) =>
                TemplateOption({
                  option: isConfirmingDelete ? 'Confirm Delete' : 'Delete',
                  icon: 'trash-2',
                  active: props.active,
                  variant: isConfirmingDelete ? 'danger' : 'gray',
                  onClick: (event) => deleteAssignmentRule(event),
                }),
            },
          ]"
        >
          <Button
            icon="more-horizontal"
            variant="ghost"
            @click="isConfirmingDelete = false"
          />
        </Dropdown>
      </div>
    </div>
  </div>
  <Dialog
    :options="{ title: `Duplicate Assignment Rule` }"
    v-model="duplicateDialog.show"
  >
    <template #body-content>
      <div class="flex flex-col gap-4">
        <FormControl
          label="New Assignment Rule Name"
          type="text"
          v-model="duplicateDialog.name"
        />
      </div>
    </template>
    <template #actions>
      <div class="flex gap-2 justify-end">
        <Button
          variant="subtle"
          label="Close"
          @click="duplicateDialog.show = false"
        />
        <Button variant="solid" label="Duplicate" @click="duplicate()" />
      </div>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import {
  createResource,
  toast,
  Select,
  Switch,
  Dropdown,
  Button,
  createDocumentResource,
} from "frappe-ui";
import { ref } from "vue";
import {
  assignmentRulesActiveScreen,
  assignmentRulesListData,
} from "../../../stores/assignmentRules";
import { TemplateOption } from "@/utils";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const priorityOptions = [
  { label: "Low", value: "0" },
  { label: "Medium-Low", value: "1" },
  { label: "Medium", value: "2" },
  { label: "Medium-High", value: "3" },
  { label: "High", value: "4" },
];

const duplicateDialog = ref({
  show: false,
  name: "",
});

const isConfirmingDelete = ref(false);

const duplicate = () => {
  createResource({
    url: "helpdesk.api.assignment_rule.duplicate_assignment_rule",
    params: {
      docname: props.data.name,
      new_name: duplicateDialog.value.name,
    },
    onSuccess: () => {
      assignmentRulesListData.reload();
      toast.success("Assignment rule duplicated");
      duplicateDialog.value.show = false;
      duplicateDialog.value.name = "";
    },
    auto: true,
  });
};

const deleteAssignmentRule = (event) => {
  event.preventDefault();
  if (!isConfirmingDelete.value) {
    isConfirmingDelete.value = true;
    return;
  }
  createResource({
    url: "frappe.client.delete",
    params: {
      doctype: "Assignment Rule",
      name: props.data.name,
    },
    onSuccess: () => {
      assignmentRulesListData.reload();
      isConfirmingDelete.value = false;
      toast.success("Assignment rule deleted");
    },
    auto: true,
  });
};

const onPriorityChange = () => {
  createResource({
    url: "frappe.client.set_value",
    params: {
      doctype: "Assignment Rule",
      name: props.data.name,
      fieldname: "priority",
      value: props.data.priority,
    },
    onSuccess: () => {
      assignmentRulesListData.reload();
      toast.success("Assignment rule priority updated");
    },
    auto: true,
  });
};

const onToggle = () => {
  createResource({
    url: "frappe.client.set_value",
    params: {
      doctype: "Assignment Rule",
      name: props.data.name,
      fieldname: "disabled",
      value: !props.data.disabled,
    },
    onSuccess: () => {
      assignmentRulesListData.reload();
      toast.success("Assignment rule status updated");
    },
    auto: true,
  });
};
</script>
