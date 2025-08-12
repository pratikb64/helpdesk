<template>
  <div class="flex flex-col">
    <LayoutHeader>
      <template #left-header>
        <div class="text-lg font-medium text-gray-900">Call Logs</div>
      </template>
      <template #right-header>
        <Button
          label="New Call Log"
          theme="gray"
          variant="solid"
          @click="showCallLogModal = true"
        >
          <template #prefix>
            <LucidePlus class="h-4 w-4" />
          </template>
        </Button>
      </template>
    </LayoutHeader>
    <ListViewBuilder
      ref="listViewRef"
      :options="options"
      @row-click="openCallLog"
      @empty-state-action="showCallLogModal = true"
    />
    <CallLogDetailModal
      v-model="showCallLogDetailModal"
      v-model:callLogModal="showCallLogModal"
      v-model:callLog="callLog"
    />
    <CallLogModal
      v-model="showCallLogModal"
      :data="callLog?.data"
      @after-insert="
        () => {
          listViewRef?.reload();
        }
      "
    />
  </div>
</template>

<script setup lang="ts">
import LayoutHeader from "@/components/LayoutHeader.vue";
import ListViewBuilder from "@/components/ListViewBuilder.vue";
import { createResource, toast, usePageMeta } from "frappe-ui";
import { computed, ref } from "vue";
import CallLogDetailModal from "./CallLogDetailModal.vue";
import CallLogModal from "./CallLogModal.vue";

const showNewCallLogModal = ref(false);
const showCallLogModal = ref(false);
const showCallLogDetailModal = ref(false);
const callLog = ref(null);

const listViewRef = ref(null);

const options = computed(() => {
  return {
    doctype: "TF Call Log",
    selectable: true,
    showSelectBanner: true,
    emptyState: {
      title: "No Call Logs Found",
    },
  };
});

function handleCallLogCreated(): void {
  showNewCallLogModal.value = false;
  listViewRef.value?.reload();
}

function openCallLog(id: string): void {
  showCallLogDetailModal.value = true;
  callLog.value = createResource({
    url: "telephony.api.get_call_log",
    params: { name: id },
    cache: ["call_log", id],
    auto: true,
  });
}

function handleCallLogUpdated(): void {
  toast.success("Call Log updated");
  showCallLogDetailModal.value = !showCallLogDetailModal.value;
  listViewRef.value?.reload();
}

usePageMeta(() => {
  return {
    title: "Call Logs",
  };
});
</script>
