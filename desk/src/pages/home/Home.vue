<template>
  <LayoutHeader>
    <template #left-header>
      <div class="text-lg font-medium text-gray-900">Home</div>
    </template>
    <template #right-header>
      <div class="flex gap-2">
        <Button label="New" variant="solid" icon-left="plus" />
      </div>
    </template>
  </LayoutHeader>
  <div class="p-5 mx-auto max-w-7xl w-full">
    <div>
      <div class="text-xl font-semibold text-ink-gray-8">
        Hey, {{ userName }}
      </div>
      <div class="text-sm text-ink-gray-5 mt-1">
        You have
        <span class="font-semibold text-ink-gray-7">3 overdue responses</span>
        and
        <span class="font-semibold text-ink-gray-7">
          2 tickets about to breach SLA
        </span>
      </div>
      <div class="mt-5">
        <UpcomingSlaViolations />
        <Card />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { LayoutHeader } from "@/components";
import { Button } from "frappe-ui";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import UpcomingSlaViolations from "./components/UpcomingSlaViolations.vue";
import Card from "./components/Card.vue";

const { userName } = storeToRefs(useAuthStore());
</script>
