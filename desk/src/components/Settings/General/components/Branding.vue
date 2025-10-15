<template>
  <div v-if="settingsData && websiteSettings.data">
    <div class="text-base font-semibold text-gray-900">
      {{ __("Branding") }}
    </div>
    <FormControl
      type="text"
      class="w-1/2 mt-4"
      v-model="settingsData.brand_name"
      :label="__('Brand name')"
      :placeholder="__('Enter brand name')"
      maxlength="30"
    />
    <LogoUpload
      :title="__('Logo')"
      :description="
        __(
          'Appears in the left sidebar. Recommended size is minimum 32x32 px in PNG or SVG'
        )
      "
      :image="settingsData.brand_logo"
      @onUpload="update($event, 'HD Settings', 'brand_logo')"
      @onRemove="onRemove('HD Settings', 'brand_logo')"
      :isLoading="loadingState.logoLoading"
      :isDisabled="loadingState.faviconLoading"
    />
    <LogoUpload
      :title="__('Favicon')"
      :description="
        __(
          'Appears next to the title in your browser tab. Recommended size is minimum 32x32 px in PNG or ICO'
        )
      "
      :image="websiteSettings.data.favicon"
      @onUpload="update($event, 'Website Settings', 'favicon')"
      @onRemove="onRemove('Website Settings', 'favicon')"
      :isLoading="loadingState.faviconLoading"
      :isDisabled="loadingState.logoLoading"
    />
  </div>
  <ConfirmDialog
    v-model="showConfirmDialog.show"
    :title="showConfirmDialog.title"
    :message="showConfirmDialog.message"
    :onConfirm="showConfirmDialog.onConfirm"
    :onCancel="() => (showConfirmDialog.show = false)"
  />
</template>

<script setup lang="ts">
import { inject, reactive, ref } from "vue";
import LogoUpload from "./LogoUpload.vue";
import { createResource, toast } from "frappe-ui";
import { __ } from "@/translation";

const settingsData = inject<any>("settingsData");
const loadingState = reactive({
  logoLoading: false,
  faviconLoading: false,
});

const showConfirmDialog = ref({
  show: false,
  title: "",
  message: "",
  onConfirm: () => {},
});

const websiteSettings = createResource({
  url: "frappe.client.get_value",
  cache: true,
  params: {
    doctype: "Website Settings",
    fieldname: "favicon",
  },
  auto: true,
});

const settingsResource = createResource({
  url: "frappe.client.set_value",
  debounce: 1000,
  onSuccess(data) {
    if (data.doctype === "HD Settings") {
      settingsData.brand_logo = data.brand_logo;
      loadingState.logoLoading = false;
    } else {
      websiteSettings.data.favicon = data.favicon;
      loadingState.faviconLoading = false;
    }
    toast.success(__("Updated successfully"));
  },
  onError() {
    loadingState.logoLoading = false;
    loadingState.faviconLoading = false;
  },
});

function update(file: string, doctype: string, fieldname: string) {
  settingsResource.submit({
    doctype: doctype,
    name: doctype,
    fieldname: fieldname,
    value: file,
  });
  doctype === "HD Settings"
    ? (loadingState.logoLoading = true)
    : (loadingState.faviconLoading = true);
}

const onRemove = (doctype: string, fieldname: string) => {
  showConfirmDialog.value = {
    show: true,
    title: __("Remove Logo"),
    message: __("Are you sure you want to remove the logo?"),
    onConfirm: () => {
      update("", doctype, fieldname);
      showConfirmDialog.value.show = false;
    },
  };
};
</script>
