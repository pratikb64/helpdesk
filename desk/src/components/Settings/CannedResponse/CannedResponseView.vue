<template>
  <SettingsLayoutBase>
    <template #title>
      <div class="flex items-center gap-2">
        <Button
          variant="ghost"
          icon-left="chevron-left"
          :label="cannedResponseData.title || 'New Canned Response'"
          size="md"
          @click="goBack()"
          class="cursor-pointer -ml-4 hover:bg-transparent focus:bg-transparent focus:outline-none focus:ring-0 focus:ring-offset-0 focus-visible:none active:bg-transparent active:outline-none active:ring-0 active:ring-offset-0 active:text-ink-gray-5 font-semibold text-ink-gray-7 text-xl hover:opacity-70 !pr-0"
        />
        <Badge
          :variant="'subtle'"
          :theme="'orange'"
          size="sm"
          label="Unsaved changes"
          v-if="isDirty"
        />
      </div>
    </template>
    <template #actions>
      <div class="flex items-center gap-4">
        <div
          class="flex items-center justify-between gap-2 cursor-pointer"
          @click="toggleEnabled"
        >
          <Switch size="sm" :model-value="cannedResponseData.enabled" />
          <span class="text-sm text-ink-gray-7 font-medium">Enabled</span>
        </div>
        <Button
          label="Save"
          variant="solid"
          theme="gray"
          @click="onSave"
          :loading="isLoading"
          :disabled="Boolean(!isDirty)"
        />
      </div>
    </template>
    <template #content>
      <div class="flex flex-col gap-5">
        <div class="grid grid-cols-2 gap-5">
          <FormControl
            label="Name"
            type="text"
            v-model="cannedResponseData.title"
            required
          />
          <FormControl
            label="Subject"
            type="text"
            v-model="cannedResponseData.subject"
            required
          />
        </div>
        <div class="flex flex-col gap-1.5">
          <Autocomplete
            label="Teams"
            :multiple="true"
            :options="getTeamsList.data"
            v-model="cannedResponseData.teams"
          />
          <div class="text-xs text-ink-gray-5 cursor-default">
            Restrict visibility to these teams
          </div>
        </div>
        <div class="flex flex-col gap-1.5">
          <FormLabel label="Response" required />
          <TextEditor
            editor-class="!prose-sm max-w-full overflow-auto min-h-[180px] max-h-80 py-1.5 px-2 rounded border border-[--surface-gray-2] bg-surface-gray-2 placeholder-ink-gray-4 hover:border-outline-gray-modals hover:bg-surface-gray-3 hover:shadow-sm focus:bg-surface-white focus:border-outline-gray-4 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-outline-gray-3 text-ink-gray-8 transition-colors"
            ref="content"
            :bubbleMenu="true"
            :content="cannedResponseData.response"
            @change="(val) => (cannedResponseData.response = val)"
            :placeholder="
              __(
                'Hello {{ customer }}, \n\nWe are sorry for the inconvenience, we will get back to you soon. \n\nRegards, \n{{ company }}'
              )
            "
          />
        </div>
      </div>
    </template>
  </SettingsLayoutBase>
</template>

<script setup lang="ts">
import {
  Autocomplete,
  Badge,
  Button,
  call,
  createDocumentResource,
  createListResource,
  createResource,
  FormControl,
  FormLabel,
  Switch,
  TextEditor,
  toast,
} from "frappe-ui";
import SettingsLayoutBase from "../SettingsLayoutBase.vue";
import { inject, onUnmounted, ref, watch } from "vue";
import { __ } from "@/translation";
import { disableSettingModalOutsideClick } from "../settingsModal";

const cannedResponseActiveScreen = inject<any>("cannedResponseActiveScreen");
const cannedResponseListData = inject<any>("cannedResponseListData");

const cannedResponseData = ref({
  name: "",
  enabled: false,
  title: "",
  subject: "",
  response: "",
  teams: [],
});
const isLoading = ref(false);
const initialData = ref("");

const getCannedResponseData = createResource({
  url: "frappe.client.get",
  params: {
    doctype: "Email Template",
    name: cannedResponseActiveScreen.value.data?.name,
  },
  auto: false,
  onSuccess: (data) => {
    cannedResponseData.value = {
      name: data.name,
      enabled: data.enabled,
      title: data.name,
      subject: data.subject,
      response: data.response,
      teams: data.teams.map((team) => ({
        label: team.team,
        value: team.team,
      })),
    };
    initialData.value = JSON.stringify(cannedResponseData.value);
  },
});

const getTeamsList = createListResource({
  doctype: "HD Team",
  auto: true,
  fields: ["name"],
  start: 0,
  pageLength: 999,
  transform: (data) => {
    return data.map((item) => ({
      value: item.name,
      label: item.name,
    }));
  },
});

if (cannedResponseActiveScreen.value.data?.name) {
  getCannedResponseData.submit();
} else {
  initialData.value = JSON.stringify(cannedResponseData.value);
}

const isDirty = ref(false);

const goBack = () => {
  cannedResponseActiveScreen.value = {
    screen: "list",
    data: null,
  };
};

const toggleEnabled = () => {
  cannedResponseData.value.enabled = !cannedResponseData.value.enabled;
};

const onSave = () => {
  isLoading.value = true;

  if (cannedResponseActiveScreen.value.data?.name) {
    updateCannedResponse();
  } else {
    cannedResponseListData.insert.submit(
      {
        name: cannedResponseData.value.title,
        enabled: cannedResponseData.value.enabled,
        title: cannedResponseData.value.title,
        subject: cannedResponseData.value.subject,
        response: cannedResponseData.value.response,
        teams: cannedResponseData.value.teams.map((team) => ({
          team: team.value,
        })),
        reference_doctype: "HD Ticket",
      },
      {
        onSuccess: (data) => {
          toast.success(__("Canned response saved"));
          isLoading.value = false;
          cannedResponseData.value = {
            ...cannedResponseData.value,
            name: data.name,
          };
          initialData.value = JSON.stringify(cannedResponseData.value);
          cannedResponseActiveScreen.value = {
            screen: "view",
            data: { name: data.name },
          };
        },
        onError: (er) => {
          toast.error(
            er?.messages?.[0] ||
              "Some error occurred while saving canned response"
          );
          isLoading.value = false;
        },
      }
    );
  }
};

const updateCannedResponse = async () => {
  let renameError = false;

  if (cannedResponseData.value.name !== cannedResponseData.value.title) {
    await call("frappe.client.rename_doc", {
      doctype: "Email Template",
      old_name: cannedResponseData.value.name,
      new_name: cannedResponseData.value.title,
    })
      .then(() => {
        cannedResponseData.value = {
          ...cannedResponseData.value,
          name: cannedResponseData.value.title,
        };
      })
      .catch(async (er) => {
        const error =
          er?.messages?.[0] ||
          "Some error occurred while renaming canned response";
        toast.error(error);
        isLoading.value = false;
        renameError = true;
      });
    await cannedResponseListData.list.reload();
  }
  if (renameError) return;

  cannedResponseListData.setValue.submit(
    {
      name: cannedResponseData.value.title,
      enabled: cannedResponseData.value.enabled,
      title: cannedResponseData.value.title,
      subject: cannedResponseData.value.subject,
      response: cannedResponseData.value.response,
      teams: cannedResponseData.value.teams.map((team) => ({
        team: team.value,
      })),
    },
    {
      onSuccess: () => {
        isDirty.value = false;
        isLoading.value = false;
        toast.success(__("Canned response updated"));
      },
    }
  );
};

watch(
  cannedResponseData,
  (newVal) => {
    if (!initialData.value) return;

    isDirty.value = JSON.stringify(newVal) != initialData.value;
    if (isDirty.value) {
      disableSettingModalOutsideClick.value = true;
    } else {
      disableSettingModalOutsideClick.value = false;
    }
  },
  { deep: true }
);

onUnmounted(() => {
  disableSettingModalOutsideClick.value = false;
});
</script>
