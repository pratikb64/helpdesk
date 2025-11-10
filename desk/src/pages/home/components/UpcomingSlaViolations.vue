<template>
  <div class="rounded-md p-4 grow">
    <div class="text-lg font-semibold text-ink-gray-8">
      Upcoming SLA Violations
    </div>
    <div class="mt-5 h-full overflow-x-auto hide-scrollbar">
      <div class="min-w-[950px]">
        <div class="grid grid-cols-8 text-sm text-gray-600 py-2 px-3">
          <div class="col-span-1">ID</div>
          <div class="col-span-2">Subject</div>
          <div class="col-span-1">Status</div>
          <div class="col-span-1">Priority</div>
          <div class="col-span-1">Team</div>
          <div class="col-span-1">Response</div>
          <div class="col-span-1">Resolution</div>
        </div>
        <hr />
        <div>
          <div v-for="(ticket, index) in upcomingSlaViolations.data">
            <div class="grid grid-cols-8 text-sm items-center py-3 px-3">
              <div class="col-span-1">{{ ticket.name }}</div>
              <div class="col-span-2">{{ ticket.subject }}</div>
              <div class="col-span-1">{{ ticket.status }}</div>
              <div class="col-span-1">
                <Badge :label="ticket.priority" theme="red" />
              </div>
              <div class="col-span-1">
                {{ ticket.agent_group || __("Not Assigned") }}
              </div>
              <div class="col-span-1 flex gap-1 items-center">
                <TimerIcon class="size-4" />
                <Badge
                  v-if="getStatus(ticket.status)?.category === 'Paused'"
                  label="Paused"
                  theme="blue"
                  variant="outline"
                />
                <Badge
                  v-else-if="
                    ticket.resolution_date &&
                    dayjs(ticket.resolution_date).isBefore(ticket.response_by)
                  "
                  label="Fulfilled"
                  theme="green"
                  variant="outline"
                />
                <Badge
                  v-else-if="
                    dayjs(ticket.resolution_date).isAfter(ticket.response_by)
                  "
                  label="Failed"
                  theme="red"
                  variant="outline"
                />
                <Tooltip v-else :text="dayjs(ticket.response_by).long()">
                  {{ dayjs.tz(ticket.response_by).fromNow() }}
                </Tooltip>
              </div>
              <div class="col-span-1 flex gap-1 items-center">
                <TimerIcon class="size-4" />
                <Badge
                  v-if="getStatus(ticket.status)?.category === 'Paused'"
                  label="Paused"
                  theme="blue"
                  variant="outline"
                />
                <Badge
                  v-else-if="
                    ticket.resolution_date &&
                    dayjs(ticket.resolution_date).isBefore(ticket.resolution_by)
                  "
                  label="Fulfilled"
                  theme="green"
                  variant="outline"
                />
                <Badge
                  v-else-if="
                    dayjs(ticket.resolution_date).isAfter(ticket.resolution_by)
                  "
                  label="Failed"
                  theme="red"
                  variant="outline"
                />
                <Tooltip v-else :text="dayjs(ticket.resolution_by).long()">
                  {{ dayjs.tz(ticket.resolution_by).fromNow() }}
                </Tooltip>
              </div>
            </div>
            <hr v-if="index !== upcomingSlaViolations.data.length - 1" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useTicketStatusStore } from "@/stores/ticketStatus";
import dayjs from "dayjs";
import { Badge, createResource, Tooltip } from "frappe-ui";
import TimerIcon from "~icons/lucide/timer";

const { getStatus } = useTicketStatusStore();

const upcomingSlaViolations = createResource({
  url: "helpdesk.api.agent.get_upcoming_sla_violations",
  cache: "Upcoming SLA Violations",
  initialData: [],
  auto: true,
  transform(upcomingSlaViolations) {
    return upcomingSlaViolations;
  },
});
</script>
