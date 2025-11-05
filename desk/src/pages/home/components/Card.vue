<template>
  <div class="rounded-md border border-outline-gray-1 p-2">
    <div class="text-ink-gray-5 text-base">My Tickets</div>
    <div class="flex flex-col">
      <div class="flex items-end">
        <div>123412</div>
        <div class="h-20 w-56">
          <AxisChart
            :config="{
              data: [
                {
                  date: '2025-10-06',
                  leads: 210,
                },
                {
                  date: '2025-10-07',
                  leads: 42,
                },
                {
                  date: '2025-10-08',
                  leads: 470,
                },
                {
                  date: '2025-10-09',
                  leads: 360,
                },
                {
                  date: '2025-10-10',
                  leads: 35,
                },
                {
                  date: '2025-10-11',
                  leads: 170,
                },
                {
                  date: '2025-10-12',
                  leads: 16,
                },
                {
                  date: '2025-10-13',
                  leads: 380,
                },
                {
                  date: '2025-10-14',
                  leads: 242,
                },
                {
                  date: '2025-10-15',
                  leads: 31,
                },
                {
                  date: '2025-10-16',
                  leads: 390,
                },
                {
                  date: '2025-10-17',
                  leads: 30,
                },
                {
                  date: '2025-10-18',
                  leads: 170,
                },
                {
                  date: '2025-10-19',
                  leads: 12,
                },
                {
                  date: '2025-10-20',
                  leads: 280,
                },
                {
                  date: '2025-10-21',
                  leads: 38,
                },
                {
                  date: '2025-10-22',
                  leads: 25,
                },
                {
                  date: '2025-10-23',
                  leads: 300,
                },
                {
                  date: '2025-10-24',
                  leads: 37,
                },
                {
                  date: '2025-10-25',
                  leads: 140,
                },
                {
                  date: '2025-10-26',
                  leads: 140,
                },
                {
                  date: '2025-10-27',
                  leads: 360,
                },
                {
                  date: '2025-10-28',
                  leads: 39,
                },
                {
                  date: '2025-10-29',
                  leads: 692,
                },
                {
                  date: '2025-10-30',
                  leads: 143,
                },
                {
                  date: '2025-10-31',
                  leads: 174,
                },
                {
                  date: '2025-11-01',
                  leads: 163,
                },
                {
                  date: '2025-11-02',
                  leads: 176,
                },
                {
                  date: '2025-11-03',
                  leads: 125,
                },
                {
                  date: '2025-11-04',
                  leads: 162,
                },
                {
                  date: '2025-11-05',
                  leads: 131,
                },
              ],
              // title: 'Sales trend',
              // subtitle: 'Daily performance of leads, deals, and wins',
              xAxis: {
                title: 'Date',
                key: 'date',
                type: 'time',
                timeGrain: 'day',
                echartOptions: {
                  show: false,
                },
              },
              yAxis: {
                title: 'Count',
                echartOptions: {
                  show: false,
                },
              },
              series: [
                {
                  name: 'leads',
                  type: 'line',
                },
              ],
              echartOptions: {
                tooltip: false,
              },
            }"
          />
        </div>
      </div>
      <div>comparison</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { AxisChart } from "frappe-ui";
</script>
