<template>
  <div class="rounded-md p-4 grow w-full h-full overflow-hidden">
    <div class="text-lg font-semibold text-ink-gray-8">Pending Tickets</div>
    <div class="mt-5 h-full overflow-auto hide-scrollbar -mx-2">
      <div class="min-w-[950px]">
        <div class="grid grid-cols-8 gap-2 text-sm text-gray-600 py-2 px-3">
          <div class="col-span-1">ID</div>
          <div class="col-span-2">Subject</div>
          <div class="col-span-1">Status</div>
          <div class="col-span-1">Priority</div>
          <div class="col-span-1">Team</div>
          <div class="col-span-1">First Response</div>
          <div class="col-span-1">Resolution</div>
        </div>
        <hr class="mx-2" />
        <div v-if="pendingTickets.data?.length > 0">
          <div
            v-for="(ticket, index) in pendingTickets.data"
            @click="goToTicket(ticket)"
          >
            <div
              class="grid grid-cols-8 gap-2 text-sm items-center py-3 px-3 cursor-pointer hover:bg-gray-50 rounded"
            >
              <div class="col-span-1 truncate">{{ ticket.name }}</div>
              <div class="col-span-2 truncate">{{ ticket.subject }}</div>
              <div class="col-span-1 truncate">{{ ticket.status }}</div>
              <div class="col-span-1">
                <Badge :label="ticket.priority" />
              </div>
              <div class="col-span-1">
                {{ ticket.agent_group || __("Not Assigned") }}
              </div>
              <div class="col-span-1 flex gap-1 items-center">
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
                  <TimerIcon class="size-4" />
                  {{ dayjs.tz(ticket.response_by).fromNow() }}
                </Tooltip>
              </div>
              <div class="col-span-1 flex gap-1 items-center">
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
                  <TimerIcon class="size-4" />
                  {{ dayjs.tz(ticket.resolution_by).fromNow() }}
                </Tooltip>
              </div>
            </div>
            <hr class="mx-2" v-if="index !== pendingTickets.data.length - 1" />
          </div>
        </div>
        <div v-else class="relative">
          <div v-for="i in 5" :key="i">
            <div class="grid grid-cols-8 gap-2 py-3 px-3">
              <div class="col-span-1 h-4 bg-surface-gray-1" />
              <div class="col-span-2 h-4 bg-surface-gray-1" />
              <div class="col-span-1 h-4 bg-surface-gray-1" />
              <div class="col-span-1 h-4 bg-surface-gray-1" />
              <div class="col-span-1 h-4 bg-surface-gray-1" />
              <div class="col-span-1 h-4 bg-surface-gray-1" />
              <div class="col-span-1 h-4 bg-surface-gray-1" />
            </div>
            <hr class="mx-2" v-if="i < 5" />
          </div>
          <div
            class="absolute inset-0 flex flex-col items-center justify-center"
          >
            <div class="bg-surface-white space-y-1 w-64 p-3 rounded">
              <div class="text-ink-gray-7 font-medium text-center text-base">
                No pending tickets
              </div>
              <div class="text-ink-gray-6 text-center text-base">
                All tickets are resolved or in progress.
              </div>
            </div>
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
import { useRouter } from "vue-router";
import TimerIcon from "~icons/lucide/timer";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const { getStatus } = useTicketStatusStore();
const router = useRouter();

const pendingTickets = createResource({
  url: "helpdesk.api.agent_dashboard.get_pending_tickets",
  auto: true,
});

const goToTicket = (ticket: any) => {
  router.push({
    name: "TicketAgent",
    params: { ticketId: ticket.name },
  });
};
</script>
