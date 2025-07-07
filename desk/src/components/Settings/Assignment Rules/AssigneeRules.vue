<template>
  <div>
    <div class="flex flex-col gap-2">
      <span class="text-lg font-semibold text-ink-gray-7">Assignee Rules</span>
      <span class="text-sm text-ink-gray-6">
        Define who receives the tickets and how they’re distributed among
        agents.
      </span>
    </div>
    <div class="mt-10 flex items-center justify-between gap-2">
      <div>
        <div class="text-base font-medium text-ink-gray-7">Ticket Routing</div>
        <div class="text-sm text-ink-gray-6 mt-2">
          Choose how tickets are distributed among selected assignees.
        </div>
      </div>
      <div>
        <Popover placement="bottom-end">
          <template #target="{ togglePopover }">
            <div
              class="flex items-center justify-between text-base rounded h-7 py-1.5 pl-2 pr-2 border border-[--surface-gray-2] bg-surface-gray-2 placeholder-ink-gray-4 hover:border-outline-gray-modals hover:bg-surface-gray-3 focus:bg-surface-white focus:border-outline-gray-4 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-outline-gray-3 text-ink-gray-8 transition-colors w-full dark:[color-scheme:dark] select-none min-w-36"
              @click="togglePopover()"
            >
              <div>
                {{
                  ticketRoutingOptions.find(
                    (option) => option.value == assignmentRuleData.rule
                  )?.label
                }}
              </div>
              <FeatherIcon name="chevron-down" class="size-4" />
            </div>
          </template>
          <template #body="{ togglePopover }">
            <div
              class="p-1 text-ink-gray-6 top-1 absolute w-40 bg-white shadow-xl rounded"
            >
              <div
                v-for="option in ticketRoutingOptions"
                :key="option.value"
                class="p-2 cursor-pointer hover:bg-gray-50 text-base flex items-center justify-between rounded"
                @click="
                  assignmentRuleData.rule = option.value;
                  togglePopover();
                "
              >
                {{ option.label }}
                <FeatherIcon
                  v-if="assignmentRuleData.rule == option.value"
                  name="check"
                  class="size-4"
                />
              </div>
            </div>
          </template>
        </Popover>
      </div>
    </div>
    <div class="mt-10 flex items-center justify-between gap-2">
      <div>
        <div class="text-base font-medium text-ink-gray-7">Assignees</div>
        <div class="text-sm text-ink-gray-6 mt-2">
          Choose who receives the tickets.
        </div>
      </div>
      <!-- <Popover>
        <template #target="{ togglePopover }">
          <Button variant="solid" icon-left="plus" @click="togglePopover()"
            >Add Assignee</Button
          >
        </template>
        <template #body-main>
        </template>
      </Popover> -->
      <Autocomplete :options="usersList.data">
        <!-- <template #target="{ option }">
          <div class="flex gap-2">
            <Avatar
              :image="option.user_image"
              :label="option.full_name"
              size="xl"
            />
            <div class="flex flex-col gap-2">
              <div>{{ option.full_name }}</div>
              <div>{{ option.email }}</div>
            </div>
          </div>
        </template> -->
        <template #target="{ togglePopover }">
          <Button variant="solid" icon-left="plus" @click="togglePopover()"
            >Add Assignee</Button
          >
        </template>
        <template #footer>
          <Button variant="ghost" icon-left="plus" class="w-full"
            >Invite agent</Button
          >
        </template>
      </Autocomplete>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  Popover,
  Button,
  Autocomplete,
  createListResource,
  Avatar,
} from "frappe-ui";
import { assignmentRuleData } from "../../../stores/assignmentRules";
import { ref } from "vue";

const userFilter = ref("");

let usersList = createListResource({
  doctype: "User",
  fields: ["*"],
  start: 0,
  pageLength: 5,
  auto: true,
  onSuccess(data) {
    console.log(data);
  },
  transform(data) {
    return data.map((user) => {
      return {
        label: user.full_name,
        value: user.email,
        description: user.email,
        image: user.user_image,
      };
    });
  },
});
console.log("usersList", usersList);
const ticketRoutingOptions = [
  {
    label: "Round Robin",
    value: "Round Robin",
  },
  {
    label: "Load Balancing",
    value: "Load Balancing",
  },
  {
    label: "Based on Field",
    value: "Based on Field",
  },
];
</script>
