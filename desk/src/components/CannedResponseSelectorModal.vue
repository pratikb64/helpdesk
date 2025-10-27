<template>
  <Dialog
    v-model="show"
    :options="{
      title: 'Canned Responses',
      size: '4xl',
    }"
  >
    <template #body-content>
      <div class="flex items-center gap-2">
        <TextInput
          class="w-full"
          ref="searchInput"
          v-model="search"
          type="text"
          :placeholder="'Site Down'"
        >
          <template #prefix>
            <FeatherIcon name="search" class="h-4 w-4 text-gray-500" />
          </template>
        </TextInput>
        <!-- <Popover placement="bottom-end">
          <template #target="{ togglePopover }">
            <Button
              label="Filter"
              icon-left="filter"
              @click="togglePopover()"
            />
          </template>
          <template #body-main>
            <div class="p-2 text-ink-gray-9 w-52 overflow-y-auto max-h-60">
              <div
                v-for="team in filters"
                :key="team.label"
                class="p-2 cursor-pointer hover:bg-gray-50 text-base flex items-center justify-between rounded select-none"
                @click="toggleFilter(team.label)"
              >
                <span class="truncate">
                  {{ team.label }}
                </span>
                <FeatherIcon
                  v-if="isFilterActive(team.label)"
                  name="check"
                  class="size-4"
                />
              </div>
            </div>
          </template>
        </Popover> -->
        <Dropdown :options="filters" placement="right">
          <Button :label="activeFilter" icon-left="filter" />
        </Dropdown>
      </div>
      <div
        v-if="filteredTemplates.length"
        class="mt-2 grid max-h-[560px] grid-cols-1 md:grid-cols-3 gap-2 overflow-y-auto"
      >
        <div
          v-for="template in filteredTemplates"
          :key="template.name"
          class="flex h-56 cursor-pointer flex-col gap-2 rounded-lg border p-3 hover:bg-gray-100 relative"
          @click="onTemplateSelect(template)"
        >
          <div class="text-base font-semibold truncate border-b pb-2">
            {{ template.name }}
          </div>
          <TextEditor
            v-if="template.response"
            :content="template.response"
            :editable="false"
            editor-class="!prose-sm max-w-none !text-sm text-gray-600 focus:outline-none"
            class="flex-1 overflow-hidden"
          />
          <div
            v-if="
              selectedTemplate.name === template.name &&
              selectedTemplate.isLoading
            "
            class="flex items-center justify-center absolute top-0 left-0 w-full h-full bg-black/20 rounded-lg"
          >
            <LoadingIndicator class="size-4" />
          </div>
        </div>
      </div>
      <div v-else class="mt-2">
        <div class="flex h-56 flex-col items-center justify-center">
          <div class="text-p-sm text-gray-500">
            {{ "No Canned Responses found" }}
          </div>
        </div>
      </div>
      <div class="flex justify-end mt-4">
        <Button label="New Canned Response" @click="onNewCannedResponseClick" />
      </div>
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import {
  Button,
  Dropdown,
  FeatherIcon,
  LoadingIndicator,
  Popover,
  TextEditor,
  createListResource,
  createResource,
} from "frappe-ui";
import { ref, computed, nextTick, watch } from "vue";
import {
  setActiveSettingsTab,
  showSettingsModal,
} from "./Settings/settingsModal";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";

const auth = storeToRefs(useAuthStore());

const props = defineProps({
  doctype: {
    type: String,
    default: "",
  },
  ticketId: {
    type: String,
    default: "",
  },
});

const show = defineModel();
const searchInput = ref("");
const activeFilter = ref("My Team");

const filters = [
  {
    label: "My Team",
    onClick: () => (activeFilter.value = "My Team"),
  },
  {
    label: "Global",
    onClick: () => (activeFilter.value = "Global"),
  },
  {
    label: "Personal",
    onClick: () => (activeFilter.value = "Personal"),
  },
];

const isFilterActive = (filter: string) => {
  return activeFilter.value.includes(filter);
};

// const toggleFilter = (filter: string) => {
//   if (activeFilter.value.includes(filter)) {
//     activeFilter.value = activeFilter.value.filter((team) => team !== filter);
//   } else {
//     activeFilter.value = [...activeFilter.value, filter];
//   }
// };

watch(activeFilter, () => {
  cannedResponsesResource.reload({
    teams: activeFilter.value,
  });
});

const emit = defineEmits(["apply"]);

const search = ref("");
const cannedResponsesList = ref([]);
const selectedTemplate = ref({
  name: "",
  isLoading: false,
});

const cannedResponsesResource = createResource({
  url: "helpdesk.api.canned_response.get_canned_responses",
  params: {
    teams: activeFilter.value,
  },
  onSuccess: (data) => {
    cannedResponsesList.value = data;
  },
  auto: true,
});

const filteredTemplates = computed(() => {
  return (
    cannedResponsesList.value?.filter((template) => {
      return (
        template.name.toLowerCase().includes(search.value.toLowerCase()) ||
        template.subject.toLowerCase().includes(search.value.toLowerCase())
      );
    }) ?? []
  );
});

const onTemplateSelect = (template) => {
  if (selectedTemplate.value.isLoading) return;
  selectedTemplate.value = {
    name: template.name,
    isLoading: true,
  };
  const renderResponse = createResource({
    url: "helpdesk.api.canned_response.get_rendered_canned_response",
    params: {
      canned_response_id: template.name,
      ticket_id: props.ticketId,
    },
    onSuccess: (data) => {
      selectedTemplate.value = {
        name: "",
        isLoading: false,
      };
      emit("apply", data);
    },
  });
  renderResponse.submit().catch(() => {
    selectedTemplate.value = {
      name: "",
      isLoading: false,
    };
  });
};

const onNewCannedResponseClick = () => {
  show.value = false;
  showSettingsModal.value = true;
  setActiveSettingsTab("Canned Responses");
};

watch(show, (value) => {
  if (value) {
    // @ts-ignore
    nextTick(() => searchInput.value?.el?.focus());
    cannedResponsesResource.reload();
  }
});
</script>
