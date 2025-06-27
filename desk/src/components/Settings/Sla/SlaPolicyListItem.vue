<template>
  <div class="flex items-center gap-2 cursor-pointer hover:bg-gray-50 rounded">
    <div
      @click="slaActiveScreen = { screen: 'view', data: data, fetchData: true }"
      class="w-4/5 py-3 pl-2"
    >
      <div class="text-base">{{ data.name }}</div>
      <div
        v-if="data.description && data.description.length > 0"
        class="text-sm w-11/12 text-gray-500 mt-1 whitespace-nowrap overflow-ellipsis overflow-hidden"
      >
        {{ data.description }}
      </div>
    </div>
    <div class="flex justify-between items-center w-1/5 pr-2">
      <div>
        <Switch
          size="sm"
          :modelValue="data.enabled"
          @update:modelValue="onToggle"
        />
      </div>
      <div>
        <Dropdown
          placement="right"
          :options="[
            {
              label: 'Duplicate',
              onClick: () => duplicate(),
              icon: 'copy',
            },
            {
              label: 'Confirm Delete',
              component: (props) =>
                TemplateOption({
                  option: isConfirmingDelete ? 'Confirm Delete' : 'Delete',
                  icon: 'trash-2',
                  active: props.active,
                  variant: 'danger',
                  onClick: (event) => deleteSla(event),
                }),
            },
          ]"
        >
          <Button
            icon="more-horizontal"
            variant="ghost"
            onclick="(e) => e.stopPropagation()"
          />
        </Dropdown>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { Switch, Button, Dropdown, createResource, toast } from "frappe-ui";
import { ref } from "vue";
import { slaActiveScreen, slaPolicyListData } from "./sla";
import { TemplateOption } from "@/utils";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const isConfirmingDelete = ref(false);

const duplicate = () => {
  createResource({
    url: "helpdesk.api.sla.duplicate_sla",
    params: {
      docname: props.data.name,
    },
    onSuccess: () => {
      slaPolicyListData.reload();
      toast.success("SLA policy duplicated");
    },
    onError: () => {
      toast.error("Failed to duplicate SLA policy");
    },
    auto: true,
  });
};

const deleteSla = (event) => {
  event.preventDefault();
  if (!isConfirmingDelete.value) {
    isConfirmingDelete.value = true;
    return;
  }

  createResource({
    url: "frappe.client.delete",
    params: {
      doctype: "HD Service Level Agreement",
      name: props.data.name,
    },
    onSuccess: () => {
      slaPolicyListData.reload();
      isConfirmingDelete.value = false;
      toast.success("SLA policy deleted");
    },
    onError: () => {
      toast.error("Failed to delete SLA policy");
    },
    auto: true,
  });
};

const onToggle = () => {
  createResource({
    url: "frappe.client.set_value",
    params: {
      doctype: "HD Service Level Agreement",
      name: props.data.name,
      fieldname: "enabled",
      value: !props.data.enabled,
    },
    onSuccess: () => {
      slaPolicyListData.reload();
      toast.success("SLA policy status updated");
    },
    onError: () => {
      toast.error("Failed to update SLA policy status");
    },
    auto: true,
  });
};
</script>
