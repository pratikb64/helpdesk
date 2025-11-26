<template>
  <div class="rounded-md p-4 grow w-full h-full overflow-hidden">
    <div class="flex items-center justify-between">
      <div class="text-lg font-semibold text-ink-gray-8">
        Upcoming SLA Violations
      </div>
      <div class="flex items-center gap-2">
        <Button
          v-if="priorityFilter !== ''"
          label="Clear"
          variant="subtle"
          @click="priorityFilter = ''"
        />
        <Combobox
          :options="getPriorityListResource?.data || []"
          v-model="priorityFilter"
          placeholder="Ticket priority"
        />
      </div>
    </div>
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
        <div v-if="tickets?.length > 0">
          <div v-for="(ticket, index) in tickets" @click="goToTicket(ticket)">
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
                  v-if="
                    !ticket.first_responded_on &&
                    dayjs(ticket.response_by).isBefore(new Date())
                  "
                  label="Failed"
                  theme="red"
                  variant="outline"
                />
                <Badge
                  v-else-if="
                    ticket.first_responded_on &&
                    dayjs(ticket.first_responded_on).isBefore(
                      ticket.response_by
                    )
                  "
                  label="Fulfilled"
                  theme="green"
                  variant="outline"
                />
                <Badge
                  v-else-if="
                    dayjs(ticket.first_responded_on).isAfter(ticket.response_by)
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
                    dayjs(ticket.resolution_date || dayjs()).isAfter(
                      ticket.resolution_by
                    )
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
            <hr class="mx-2" v-if="index !== tickets.length - 1" />
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
                No upcoming SLA violations
              </div>
              <div class="text-ink-gray-6 text-center text-base">
                You’re well within your response windows.
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
import {
  Badge,
  Combobox,
  createListResource,
  createResource,
  Tooltip,
} from "frappe-ui";
import { computed, h, onMounted, ref, watch } from "vue";
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
const priorityFilter = ref("");

const getPriorityListResource = createListResource({
  doctype: "HD Ticket Priority",
  fields: ["name"],
  auto: true,
  transform(data) {
    return data.map((d) => d.name);
  },
});

const tickets = computed(() => {
  console.log(
    "upcomingSlaViolations",
    upcomingSlaViolations.fetched ? upcomingSlaViolations.data : props.data
  );
  return upcomingSlaViolations.fetched
    ? upcomingSlaViolations.data
    : props.data || [];
});

const upcomingSlaViolations = createResource({
  url: "helpdesk.api.agent_dashboard.get_upcoming_sla_violations",
});

const goToTicket = (ticket: any) => {
  router.push({
    name: "TicketAgent",
    params: { ticketId: ticket.name },
  });
};

function handle_resolution_by_field(row: any, item: string) {
  const status = getStatus(row.status) || {};
  if (status.category === "Paused") {
    return h(Badge, {
      label: "Paused",
      theme: "blue",
      variant: "outline",
    });
  } else if (row.resolution_date && dayjs(row.resolution_date).isBefore(item)) {
    return h(Badge, {
      label: "Fulfilled",
      theme: "green",
      variant: "outline",
    });
  } else if (dayjs(row.resolution_date).isAfter(item)) {
    return h(Badge, {
      label: "Failed",
      theme: "red",
      variant: "outline",
    });
  } else {
    return h(
      Tooltip,
      {
        text: dayjs(item).long(),
      },
      () => dayjs.tz(item).fromNow()
    );
  }
}

onMounted(() => {
  if (!props.data.length) {
    upcomingSlaViolations.submit();
  }
});

watch(priorityFilter, (newPriority) => {
  upcomingSlaViolations.submit({ priority: newPriority });
});
</script>
