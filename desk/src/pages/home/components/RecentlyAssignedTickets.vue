<template>
  <div class="w-full h-full overflow-hidden">
    <div class="rounded-md p-4 grow min-w-[252px] h-full">
      <div class="space-y-2">
        <div class="text-lg font-semibold text-ink-gray-8">
          Recently assigned tickets
        </div>
        <div v-if="data?.count > 0" class="text-base text-ink-gray-6">
          You have
          {{ data?.count }} new tickets this week
        </div>
      </div>
      <div
        v-if="data?.count == 0"
        class="flex flex-col justify-center items-center text-center gap-2 h-full w-full"
      >
        <div class="flex flex-col gap-2 max-w-60">
          <div class="text-base font-medium text-ink-gray-7">
            No tickets assigned this week
          </div>
          <div class="text-base text-ink-gray-6">
            You haven't been assigned any new tickets this week.
          </div>
        </div>
      </div>
      <div class="space-y-5 mt-7">
        <div
          v-for="ticket in data?.tickets"
          class="flex justify-between items-center gap-2 rounded relative group/child my-2 cursor-pointer"
          @click="goToTicket(ticket)"
        >
          <div class="text-base space-y-1 grow truncate">
            <div class="font-medium text-ink-gray-7 truncate">
              {{ ticket.subject }}
            </div>
            <div class="text-ink-gray-5 truncate">
              {{ dateFormat(ticket.creation, "MMM DD, YYYY") }} ·
              {{ ticket.name }}
            </div>
          </div>
          <div>
            <FeatherIcon name="chevron-right" class="size-5" />
          </div>
          <div
            class="absolute -top-2 -left-2 -z-10 rounded group-hover/child:bg-surface-gray-2"
            :style="{
              width: 'calc(100% + 16px)',
              height: 'calc(100% + 16px)',
            }"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { dateFormat } from "@/utils";
import { useRouter } from "vue-router";

const router = useRouter();

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});
console.log("tickets", props);

const goToTicket = (ticket: any) => {
  router.push({
    name: "TicketAgent",
    params: { ticketId: ticket.name },
  });
};
</script>
