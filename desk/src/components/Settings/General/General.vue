<template>
  <div class="pb-8">
    <div class="px-10 py-8">
      <SettingsLayoutHeader
        :description="__('Manage general settings of your app')"
      >
        <template #title>
          <div class="flex items-center gap-2">
            <h1 class="text-lg font-semibold text-ink-gray-8">
              {{ __("General") }}
            </h1>
            <Badge
              :variant="'subtle'"
              :theme="'orange'"
              size="sm"
              :label="__('Unsaved')"
              v-if="isDirty"
            />
          </div>
        </template>
        <template #actions>
          <Button
            :label="__('Save')"
            variant="solid"
            @click="saveSettings.submit()"
            :loading="saveSettings.loading"
            :disabled="!isDirty"
          />
        </template>
      </SettingsLayoutHeader>
    </div>
    <div class="px-10 pb-8 overflow-y-auto hide-scrollbar">
      <div v-if="isWebsiteManager">
        <Branding />
      </div>
      <hr class="my-8" v-if="isWebsiteManager && isAdmin" />
      <div v-if="isAdmin">
        <TicketSettings />
        <hr class="my-8" />
        <WorkflowKnowledgebaseSettings />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Badge, Button, createResource, toast } from "frappe-ui";
import SettingsLayoutHeader from "../SettingsLayoutHeader.vue";
import Branding from "./components/Branding.vue";
import TicketSettings from "./components/TicketSettings.vue";
import WorkflowKnowledgebaseSettings from "./components/WorkflowKnowledgebaseSettings.vue";
import { provide, ref, watch } from "vue";
import { useAuthStore } from "@/stores/auth";
import { __ } from "@/translation";

const { isWebsiteManager, isAdmin } = useAuthStore();
const isDirty = ref(false);
const initialData = ref("");
const settingsData = ref({});
provide("settingsData", settingsData);

const settingsDataResource = createResource({
  url: "frappe.client.get",
  params: {
    doctype: "HD Settings",
    name: "HD Settings",
  },
  fields: [
    "brand_logo",
    "favicon",
    "auto_close_after_days",
    "auto_close_status",
    "auto_close_tickets",
    "assign_within_team",
    "do_not_restrict_tickets_without_an_agent_group",
    "restrict_tickets_by_agent_group",
    "update_status_to",
    "auto_update_status",
    "is_feedback_mandatory",
    "allow_anyone_to_create_tickets",
    "default_ticket_type",
    "prefer_knowledge_base",
    "skip_email_workflow",
  ],
  auto: true,
  onSuccess(data) {
    settingsData.value = {
      ...data,
      is_feedback_mandatory: Boolean(data.is_feedback_mandatory),
      allow_anyone_to_create_tickets: Boolean(
        data.allow_anyone_to_create_tickets
      ),
      assign_within_team: Boolean(data.assign_within_team),
      do_not_restrict_tickets_without_an_agent_group: Boolean(
        data.do_not_restrict_tickets_without_an_agent_group
      ),
      restrict_tickets_by_agent_group: Boolean(
        data.restrict_tickets_by_agent_group
      ),
      prefer_knowledge_base: Boolean(data.prefer_knowledge_base),
      skip_email_workflow: Boolean(data.skip_email_workflow),
    };
    initialData.value = JSON.stringify(settingsData.value);
  },
});

const saveSettings = createResource({
  url: "frappe.client.set_value",
  params: {
    doctype: "HD Settings",
    name: "HD Settings",
    fieldname: settingsData.value,
  },
  onSuccess(data) {
    settingsData.value = {
      ...data,
      is_feedback_mandatory: Boolean(data.is_feedback_mandatory),
      allow_anyone_to_create_tickets: Boolean(
        data.allow_anyone_to_create_tickets
      ),
      assign_within_team: Boolean(data.assign_within_team),
      do_not_restrict_tickets_without_an_agent_group: Boolean(
        data.do_not_restrict_tickets_without_an_agent_group
      ),
      restrict_tickets_by_agent_group: Boolean(
        data.restrict_tickets_by_agent_group
      ),
      prefer_knowledge_base: Boolean(data.prefer_knowledge_base),
      skip_email_workflow: Boolean(data.skip_email_workflow),
    };
    initialData.value = JSON.stringify(settingsData.value);
    toast.success(__("Settings updated"));
  },
});

watch(
  settingsData,
  (data) => {
    if (!initialData.value) return;

    isDirty.value = JSON.stringify(data) !== initialData.value;
  },
  { deep: true }
);
</script>
