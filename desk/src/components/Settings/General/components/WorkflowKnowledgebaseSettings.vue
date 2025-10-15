<template>
  <div>
    <div class="text-base font-semibold text-gray-900">
      {{ __("Workflow & Knowledgebase Settings") }}
    </div>
    <div v-if="settingsData" class="mt-6 flex flex-col gap-6">
      <div class="flex items-center justify-between">
        <div class="flex flex-col gap-1">
          <span class="text-base font-medium text-ink-gray-8">{{
            __("Prefer knowledge base")
          }}</span>
          <span class="text-p-sm text-ink-gray-6">{{
            __("Guide users to articles before tickets.")
          }}</span>
        </div>
        <Switch
          :model-value="settingsData.prefer_knowledge_base"
          @update:model-value="
            (value) => (settingsData.prefer_knowledge_base = value)
          "
        />
      </div>
      <div class="flex items-center justify-between">
        <div class="flex flex-col gap-1">
          <span class="text-base font-medium text-ink-gray-8">{{
            __("Skip Email workflow")
          }}</span>
          <span class="text-p-sm text-ink-gray-6">{{
            __(
              "Skips automated ticket e-mails. No creation, update, or notification e-mails will be sent."
            )
          }}</span>
        </div>
        <Switch
          :model-value="settingsData.skip_email_workflow"
          @update:model-value="
            (value) => (settingsData.skip_email_workflow = value)
          "
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Switch } from "frappe-ui";
import { inject } from "vue";

const settingsData = inject<any>("settingsData");
</script>
