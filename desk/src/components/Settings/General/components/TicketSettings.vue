<template>
  <div>
    <div class="text-base font-semibold text-gray-900">
      {{ __("Ticket Settings") }}
    </div>
    <div
      v-if="ticketTypeList.data && autoUpdateticketStatusList && settingsData"
      class="mt-6 flex flex-col gap-6"
    >
      <div class="flex items-center justify-between">
        <div class="flex flex-col gap-1">
          <span class="text-base font-medium text-ink-gray-8">{{
            __("Make feedback mandatory")
          }}</span>
          <span class="text-p-sm text-ink-gray-6">{{
            __(
              "The feedback dialog will be shown, when a user tries to close a ticket from the customer portal"
            )
          }}</span>
        </div>
        <Switch v-model="settingsData.is_feedback_mandatory" />
      </div>
      <div>
        <div class="flex items-center justify-between">
          <div class="flex flex-col gap-1">
            <span class="text-base font-medium text-ink-gray-8">{{
              __("Restrict tickets by Team")
            }}</span>
            <span class="text-p-sm text-ink-gray-6">{{
              __("Restrict tickets to be created by team members only.")
            }}</span>
          </div>
          <Switch v-model="settingsData.restrict_tickets_by_agent_group" />
        </div>
        <div
          class="grid grid-cols-2 gap-4 mt-3"
          v-if="settingsData.restrict_tickets_by_agent_group"
        >
          <div
            class="flex items-start sm:items-center gap-2"
            @click="
              () => {
                settingsData.do_not_restrict_tickets_without_an_agent_group =
                  !settingsData.do_not_restrict_tickets_without_an_agent_group;
              }
            "
          >
            <Checkbox
              :model-value="
                settingsData.do_not_restrict_tickets_without_an_agent_group
              "
            />
            <FormLabel :label="__('Do not restrict tickets without a Team')" />
          </div>
          <div
            class="flex items-start sm:items-center gap-2"
            @click="
              () => {
                settingsData.assign_within_team =
                  !settingsData.assign_within_team;
              }
            "
          >
            <Checkbox :model-value="settingsData.assign_within_team" />
            <FormLabel
              :label="__('Restrict agent assignment to selected Team')"
            />
          </div>
        </div>
      </div>
      <div class="flex items-center justify-between">
        <div class="flex flex-col gap-1">
          <span class="text-base font-medium text-ink-gray-8">{{
            __("Auto update status")
          }}</span>
          <span class="text-p-sm text-ink-gray-6">{{
            __(
              "The ticket status will automatically change whenever the agent respond to a ticket."
            )
          }}</span>
        </div>
        <SelectDropdown
          :options="autoUpdateticketStatusList"
          :model-value="settingsData.update_status_to"
          target-class="max-w-40"
          placement="bottom-end"
          @on-reset="
            () => {
              settingsData.update_status_to = null;
              settingsData.auto_update_status = false;
            }
          "
          @on-change="
            (value) => {
              settingsData.update_status_to = value;
              settingsData.auto_update_status = true;
            }
          "
        />
      </div>
      <div class="flex items-center justify-between">
        <div class="flex flex-col gap-1">
          <span class="text-base font-medium text-ink-gray-8">{{
            __("Allow anyone to create tickets")
          }}</span>
          <span class="text-p-sm text-ink-gray-6">{{
            __("Anyone will able to create tickets, e.g. from webform")
          }}</span>
        </div>
        <Switch
          :model-value="settingsData.allow_anyone_to_create_tickets"
          @update:model-value="
            (value) => (settingsData.allow_anyone_to_create_tickets = value)
          "
        />
      </div>
      <div class="flex items-center justify-between">
        <div class="flex flex-col gap-1">
          <span class="text-base font-medium text-ink-gray-8">{{
            __("Default ticket type")
          }}</span>
          <span class="text-p-sm text-ink-gray-6">{{
            __("Select what type all tickets get by default")
          }}</span>
        </div>
        <SelectDropdown
          :options="ticketTypeList.data"
          :model-value="settingsData.default_ticket_type"
          target-class="max-w-40"
          placement="bottom-end"
          @on-reset="() => (settingsData.default_ticket_type = null)"
          @on-change="(value) => (settingsData.default_ticket_type = value)"
        />
      </div>
      <div>
        <div class="flex flex-col gap-1">
          <span class="text-base font-medium text-ink-gray-8">{{
            __("Automatically Close Tickets")
          }}</span>
          <span class="text-p-sm text-ink-gray-6">{{
            __("Automatically close tickets after a certain condition is met.")
          }}</span>
        </div>
        <div class="grid grid-cols-2 gap-4 mt-3">
          <div class="flex flex-col gap-1.5">
            <FormLabel :label="__('Auto-close status')" />
            <SelectDropdown
              :options="autoCloseTicketStatusList"
              :model-value="settingsData.auto_close_status"
              target-class="w-full"
              placement="bottom-end"
              @on-reset="
                () => {
                  settingsData.auto_close_status = null;
                  settingsData.auto_close_tickets = false;
                }
              "
              @on-change="
                (value) => {
                  settingsData.auto_close_status = value;
                  settingsData.auto_close_tickets = true;
                }
              "
            />
          </div>
          <div class="flex flex-col gap-1.5">
            <FormControl
              :label="__('Auto-close after (Days)')"
              placeholder="e.g. 30"
              :model-value="settingsData.auto_close_after_days"
              @update:model-value="
                (value) =>
                  (settingsData.auto_close_after_days = Number(value) || null)
              "
              type="number"
              :debounce="300"
              :disabled="!settingsData.auto_close_status"
            />
            <ErrorMessage
              :message="
                settingsData.auto_close_after_days < 1
                  ? __('The number of days must be 1 or more')
                  : ''
              "
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import SelectDropdown from "@/components/SelectDropdown.vue";
import { useTicketStatusStore } from "@/stores/ticketStatus";
import { HDTicketStatus } from "@/types/doctypes";
import {
  Checkbox,
  createListResource,
  ErrorMessage,
  FormControl,
  FormLabel,
  Switch,
} from "frappe-ui";
import { computed, inject } from "vue";

const { statuses } = useTicketStatusStore();

const ticketTypeList = createListResource({
  doctype: "HD Ticket Type",
  name: "HD Ticket Type",
  auto: true,
  transform: (data) => {
    return data.map((item) => {
      return {
        label: item.name,
        value: item.name,
      };
    });
  },
});

const autoUpdateticketStatusList = computed(() => {
  return (
    statuses.data
      ?.filter(
        (s: HDTicketStatus) => s.category === "Open" || s.category === "Paused"
      )
      .map((s: HDTicketStatus) => {
        return {
          label: s.label_agent,
          value: s.label_agent,
        };
      }) || []
  );
});

const autoCloseTicketStatusList = computed(() => {
  return (
    statuses.data
      ?.filter(
        (s: HDTicketStatus) =>
          s.category === "Resolved" || s.category === "Paused"
      )
      .map((s: HDTicketStatus) => {
        return {
          label: s.label_agent,
          value: s.label_agent,
        };
      }) || []
  );
});

const settingsData = inject<any>("settingsData");
</script>
