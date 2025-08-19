<template>
  <div
    class="flex items-center h-full justify-center"
    v-if="emailAccountData.get.loading && !emailAccountData.doc"
  >
    <LoadingIndicator class="w-4" />
  </div>
  <div class="sticky top-0 z-10 bg-white px-10 pt-8 pb-4">
    <div class="flex items-center justify-between w-full">
      <div>
        <div class="flex items-center gap-2">
          <Button
            variant="ghost"
            icon-left="chevron-left"
            :label="'Account details'"
            size="md"
            class="cursor-pointer -ml-4 hover:bg-transparent focus:bg-transparent focus:outline-none focus:ring-0 focus:ring-offset-0 focus-visible:none active:bg-transparent active:outline-none active:ring-0 active:ring-offset-0 active:text-ink-gray-5 font-semibold text-ink-gray-7 text-xl hover:opacity-70"
            @click="goBack"
          />
        </div>
      </div>
      <div class="flex gap-2 items-center">
        <!-- <Badge
          :variant="'subtle'"
          :theme="'orange'"
          size="sm"
          label="Unsaved changes"
        /> -->
        <Button label="Save" theme="gray" variant="solid" @click="save()" />
        <!-- @click="emailAccountData.save.submit()" -->
      </div>
    </div>
  </div>
  <div
    class="px-10 pb-8 overflow-y-auto"
    v-if="emailAccountData.doc && !emailAccountData.get.loading"
  >
    <div class="flex items-center gap-2">
      <div class="shadow-sm rounded-lg border border-gray-300 p-2 w-max">
        <img
          :src="emailIcons[emailAccountData.doc.service].icon"
          class="size-5.5"
        />
      </div>
      <div>
        <div
          class="text-base font-medium text-ink-gray-8 flex items-center gap-2"
        >
          {{ emailAccountData.doc.email_id }}
          <Badge
            v-if="emailAccountData.doc.default_incoming == 1"
            :theme="'blue'"
            size="sm"
            label="Default"
          />
        </div>
        <div class="text-xs text-ink-gray-5 mt-1">
          {{ emailAccountData.doc.name }}
        </div>
      </div>
    </div>
    <div class="mt-8">
      <div class="text-lg text-ink-gray-8 font-semibold">General settings</div>
      <div class="grid grid-cols-2 gap-4 mt-4">
        <FormControl
          label="Email"
          type="text"
          v-model="emailAccountData.doc.email_id"
          required
        />
        <FormControl
          label="Password"
          type="password"
          v-model="emailAccountData.doc.password"
          required
        />
        <!-- @update:model-value="
            (value) => {
              emailAccountData.doc.password = value;
              console.log('updated emailAccountData', emailAccountData);
            }
          " -->
        <FormControl
          label="Account name"
          type="text"
          :model-value="emailAccountData.doc.name"
          @update:model-value="
            (value) => {
              emailAccountData.doc.name = value;
              console.log('updated emailAccountData', emailAccountData);
            }
          "
          required
        />
      </div>
    </div>
    <div class="mt-8">
      <div class="text-lg text-ink-gray-8 font-semibold">Default settings</div>
      <div class="mt-4">
        <div class="flex items-center justify-between">
          <div class="flex flex-col gap-1">
            <div class="text-base font-medium text-ink-gray-8">
              Enable Incoming
            </div>
            <div class="text-sm text-ink-gray-6">
              Turn this on to automatically turn incoming emails into support
              tickets.
            </div>
          </div>
          <Switch v-model="emailAccountData.doc.enable_incoming" />
        </div>
        <hr class="my-4" />
        <div class="flex items-center justify-between">
          <div class="flex flex-col gap-1">
            <div class="text-base font-medium text-ink-gray-8">
              Enable Outgoing
            </div>
            <div class="text-sm text-ink-gray-6">
              When enabled, this account can be used to send outgoing emails.
            </div>
          </div>
          <Switch v-model="emailAccountData.doc.enable_outgoing" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  Badge,
  createDocumentResource,
  FormControl,
  LoadingIndicator,
  Switch,
} from "frappe-ui";
import { emailIcons, getProviderIcon } from "./utils";
import { emailAccountActiveScreen } from "@/stores/emailAccount";

const emailAccountData = createDocumentResource({
  doctype: "Email Account",
  name: emailAccountActiveScreen.value.data.name,
  auto: true,
  whitelistedMethods: {
    updateDocumentTitle: "frappe.model.rename_doc.update_document_title",
  },
});

console.log("emailAccountData", emailAccountData);

const save = () => {
  emailAccountData.updateDocumentTitle.submit({
    method: "frappe.model.rename_doc.update_document_title",
    doctype: "Email Account",
    docname: emailAccountData.doc.name,
    enqueue: false,
    merge: 0,
    freeze: true,
    name: emailAccountData.doc.name + "new",
    freeze_message: "Updating holiday list name",
  });
};

const goBack = () => {
  emailAccountActiveScreen.value = {
    screen: "list",
    provider: "",
    data: null,
  };
};
</script>
