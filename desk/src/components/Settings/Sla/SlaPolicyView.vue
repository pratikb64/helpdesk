<template>
  <div class="sticky top-0 z-10 bg-white px-10 py-8">
    <div class="flex items-center justify-between w-full">
      <div>
        <div class="flex items-center gap-2">
          <Button
            variant="ghost"
            icon-left="chevron-left"
            :label="slaData.service_level || 'New SLA Policy'"
            size="md"
            @click="goBack()"
            class="cursor-pointer -ml-4 hover:bg-transparent focus:bg-transparent focus:outline-none focus:ring-0 focus:ring-offset-0 focus-visible:none active:bg-transparent active:outline-none active:ring-0 active:ring-offset-0 active:text-ink-gray-5"
          />
          <Badge
            :variant="'subtle'"
            :theme="slaData.enabled ? 'blue' : 'gray'"
            size="sm"
            :label="slaData.enabled ? 'Enabled' : 'Disabled'"
          />
        </div>
      </div>
      <Button label="Save" theme="gray" variant="solid" @click="saveSla()" />
    </div>
    <!-- <div class="text-xs text-red-600 mt-2 flex gap-1 flex-col">
      <span v-for="(error, index) in errors" :key="index">
        {{ index + 1 }}. {{ error }}
      </span>
    </div> -->
  </div>
  <div v-if="!slaData.loading" class="overflow-y-auto px-10 pb-10">
    <div class="flex items-center justify-between gap-2">
      <span class="text-sm"> Enable Policy </span>
      <Switch size="sm" v-model="slaData.enabled" />
    </div>
    <hr class="mb-6 mt-3" />
    <div class="grid grid-cols-2 gap-2">
      <div>
        <FormControl
          :type="'text'"
          size="sm"
          variant="subtle"
          placeholder="Name"
          label="Name"
          v-model="slaData.service_level"
          required
        />
        <span v-if="slaDataErrors.service_level" class="text-red-500 text-xs">
          {{ slaDataErrors.service_level }}
        </span>
      </div>
      <FormControl
        :type="'textarea'"
        size="sm"
        variant="subtle"
        placeholder="Description"
        label="Description"
        v-model="slaData.description"
        :rows="1"
      />
    </div>
    <hr class="my-6" />
    <div>
      <div class="flex flex-col gap-2">
        <span class="text-lg font-medium">Assignment conditions</span>
        <span class="text-sm text-gray-600">
          Choose which tickets are affected by this policy. Learn about
          conditions
        </span>
      </div>
      <div class="mt-4">
        <Checkbox
          label="Apply default SLA conditions"
          v-model="slaData.default_sla"
        />
        <div class="mt-4">
          <SlaAssignmentConditions :conditions="slaData.condition" />
        </div>
      </div>
    </div>
    <hr class="my-6" />
    <div>
      <div class="flex flex-col gap-2">
        <span class="text-lg font-medium">Valid from</span>
        <span class="text-sm text-gray-600">
          Choose how long this SLA policy will be active.
        </span>
      </div>
      <div class="mt-4 flex gap-2">
        <div class="w-full">
          <label for="from_date" class="text-sm text-gray-600">From date</label>
          <DatePicker
            v-model="slaData.start_date"
            variant="subtle"
            placeholder="From date"
            class="w-full"
            id="from_date"
          />
          <span v-if="slaDataErrors.start_date" class="text-red-500 text-xs">
            {{ slaDataErrors.start_date }}
          </span>
        </div>
        <div class="w-full">
          <label for="to_date" class="text-sm text-gray-600">To date</label>
          <DatePicker
            v-model="slaData.end_date"
            variant="subtle"
            placeholder="To date"
            class="w-full"
            id="to_date"
          />
          <span v-if="slaDataErrors.end_date" class="text-red-500 text-xs">
            {{ slaDataErrors.end_date }}
          </span>
        </div>
      </div>
    </div>
    <hr class="my-6" />
    <div>
      <div class="flex flex-col gap-2">
        <span class="text-lg font-medium">Response and resolution</span>
        <span class="text-sm text-gray-600">
          Add time targets around support milestones like first reply and
          resolution times
        </span>
      </div>
      <div class="mt-4">
        <Checkbox
          label="Apply SLA for resolution time"
          v-model="slaData.apply_sla_for_resolution"
        />
        <div class="mt-4">
          <SlaPriorityList
            :priorityList="slaData.priorities"
            :applySlaForResolution="slaData.apply_sla_for_resolution"
          />
        </div>
      </div>
    </div>
    <hr class="my-6" />
    <div>
      <div class="flex flex-col gap-2">
        <span class="text-lg font-medium">Status details</span>
        <span class="text-sm text-gray-600">
          The SLA status updates with ticket progress—fulfilled when conditions
          are met, paused when awaiting external action.
        </span>
      </div>
      <div class="mt-4">
        <div class="mt-4">
          <SlaStatusList :statusList="slaData.statuses" />
        </div>
      </div>
    </div>
    <hr class="my-6" />
    <SlaHolidays
      :workDaysList="slaData.support_and_resolution"
      v-model="slaData.holiday_list"
    />
  </div>
</template>

<script setup lang="ts">
import { slaActiveScreen, slaDataErrors } from "./sla";
import { createResource, Switch, Checkbox, DatePicker } from "frappe-ui";
import { onUnmounted, ref } from "vue";
import SlaPriorityList from "./SlaPriorityList.vue";
import SlaStatusList from "./SlaStatusList.vue";
import SlaHolidays from "./SlaHolidays.vue";
import SlaAssignmentConditions from "./SlaAssignmentConditions.vue";

const slaData = ref({
  service_level: "",
  description: "",
  enabled: false,
  default_sla: false,
  apply_sla_for_resolution: false,
  priorities: [],
  statuses: [],
  holiday_list: "Default",
  default_priority: "",
  start_date: "",
  end_date: "",
  loading: false,
  support_and_resolution: [],
  condition: [],
});

const getSlaData = createResource({
  url: "helpdesk.api.sla.get_sla",
  params: {
    docname: slaActiveScreen.value.data?.name,
  },
  onSuccess(data) {
    const fulfilledOn =
      data.sla_fulfilled_on?.map((item) => {
        return {
          ...item,
          sla_behavior: "Fulfilled",
        };
      }) || [];
    const pauseOn =
      data.pause_sla_on?.map((item) => {
        return {
          ...item,
          sla_behavior: "Paused",
        };
      }) || [];

    const conditions = JSON.parse(data.condition || "[]");

    slaData.value = {
      ...data,
      statuses: [...pauseOn, ...fulfilledOn],
      loading: false,
      condition: data.condition?.length > 0 ? conditions : [],
    };
  },
});

if (slaActiveScreen.value.data) {
  slaData.value.loading = true;
  getSlaData.submit();
}

const goBack = () => {
  slaActiveScreen.value = {
    screen: "list",
    data: null,
  };
};

const errors = ref([]);
const saveSla = () => {
  errors.value = [];
  slaDataErrors.value = {
    service_level: "",
    description: "",
    enabled: "",
    default_sla: "",
    apply_sla_for_resolution: "",
    priorities: "",
    statuses: "",
    holiday_list: "",
    default_priority: "",
    start_date: "",
    end_date: "",
    support_and_resolution: "",
    condition: "",
  };
  if (!slaData.value.service_level?.trim()) {
    slaDataErrors.value.service_level = "SLA policy name is required";
    errors.value.push("SLA policy name is required");
  }

  if (
    !Array.isArray(slaData.value.priorities) ||
    slaData.value.priorities.length === 0
  ) {
    slaDataErrors.value.priorities = "At least one priority is required";
    errors.value.push("At least one priority is required");
  } else {
    slaData.value.priorities.forEach((priority, index) => {
      const priorityNum = index + 1;
      if (!priority.priority?.trim()) {
        errors.value.push(`Priority ${priorityNum}: Priority name is required`);
      }
      if (!priority.response_time) {
        errors.value.push(`Priority ${priorityNum}: Response time is required`);
      }
      if (
        Boolean(slaData.value.apply_sla_for_resolution) &&
        !priority.resolution_time
      ) {
        errors.value.push(
          `Priority ${priorityNum}: Resolution time is required`
        );
      }
    });

    const hasDefaultPriority = slaData.value.priorities.some(
      (p) => p.default_priority == true
    );
    if (!hasDefaultPriority) {
      slaDataErrors.value.default_priority = "Default priority is required";
      errors.value.push("Default priority is required");
    }
  }

  if (slaData.value.start_date && slaData.value.end_date) {
    const startDate = new Date(slaData.value.start_date);
    const endDate = new Date(slaData.value.end_date);

    if (startDate > endDate) {
      slaDataErrors.value.end_date = "To date must be after from date";
      errors.value.push("To date must be after from date");
    }
  }

  // Validate statuses
  if (
    !Array.isArray(slaData.value.statuses) ||
    slaData.value.statuses.length === 0
  ) {
    slaDataErrors.value.statuses =
      "At least one status for 'Fulfilled on' and 'Paused on' is required";
    errors.value.push(
      "At least one status for 'Fulfilled on' and 'Paused on' is required"
    );
  } else {
    const hasFulfilled = slaData.value.statuses.some(
      (s) => s.sla_behavior === "Fulfilled"
    );
    const hasPaused = slaData.value.statuses.some(
      (s) => s.sla_behavior === "Paused"
    );

    if (!hasFulfilled) {
      slaDataErrors.value.statuses =
        "At least one 'Fulfilled on' status is required";
      errors.value.push("At least one 'Fulfilled on' status is required");
    }
    if (!hasPaused) {
      slaDataErrors.value.statuses =
        "At least one 'Paused on' status is required";
      errors.value.push("At least one 'Paused on' status is required");
    }
  }

  // Validate at least one workday with start and end time exists
  const validWorkdays = slaData.value.support_and_resolution?.filter(
    (day) =>
      !day.is_holiday &&
      day.start_time &&
      day.end_time &&
      day.start_time.trim() !== "" &&
      day.end_time.trim() !== ""
  );

  if (!validWorkdays?.length) {
    slaDataErrors.value.support_and_resolution =
      "At least one valid workday with start and end time is required";
    errors.value.push(
      "At least one valid workday with start and end time is required"
    );
  } else {
    // Validate start time is before end time for each workday
    validWorkdays.forEach((day, index) => {
      const startTime = day.start_time.trim();
      const endTime = day.end_time.trim();

      if (startTime >= endTime) {
        slaDataErrors.value.support_and_resolution = `Workday ${
          day.workday || index + 1
        }: Start time must be before end time`;
        errors.value.push(
          `Workday ${
            day.workday || index + 1
          }: Start time must be before end time`
        );
      }
    });
  }

  // Validate conditions if any exist
  if (slaData.value.condition && slaData.value.condition.length > 0) {
    let conditionError = false;
    slaData.value.condition.forEach((condition, index) => {
      const conditionNum = index + 1;
      if (
        !condition.field ||
        condition.value === undefined ||
        condition.value === null ||
        condition.value === ""
      ) {
        errors.value.push(
          `Condition ${conditionNum}: Field and value are required`
        );
        conditionError = true;
      }
    });
    if (conditionError) {
      slaDataErrors.value.condition = `Field and value are required for all conditions`;
    }
  }

  if (errors.value.length > 0) {
    return;
  }

  if (slaActiveScreen.value.data) {
    updateSla();
  } else {
    createSla();
  }
};

const createSla = () => {
  const fulfilledOn = slaData.value.statuses.filter(
    (status) => status.sla_behavior === "Fulfilled"
  );
  const pauseOn = slaData.value.statuses.filter(
    (status) => status.sla_behavior === "Paused"
  );
  createResource({
    url: "helpdesk.api.sla.save_sla",
    params: {
      doc: {
        doctype: "HD Service Level Agreement",
        enabled: slaData.value.enabled,
        description: slaData.value.description,
        service_level: slaData.value.service_level,
        default_sla: slaData.value.default_sla,
        apply_sla_for_resolution: slaData.value.apply_sla_for_resolution,
        priorities: slaData.value.priorities,
        sla_fulfilled_on: fulfilledOn,
        pause_sla_on: pauseOn,
        holiday_list: slaData.value.holiday_list,
        default_priority: slaData.value.default_priority,
        start_date: slaData.value.start_date,
        end_date: slaData.value.end_date,
        support_and_resolution: slaData.value.support_and_resolution,
        condition: slaData.value.condition,
      },
      is_new: true,
    },
    auto: true,
  });
};

const updateSla = () => {
  const fulfilledOn = slaData.value.statuses.filter(
    (status) => status.sla_behavior === "Fulfilled"
  );
  const pauseOn = slaData.value.statuses.filter(
    (status) => status.sla_behavior === "Paused"
  );
  createResource({
    url: "helpdesk.api.sla.save_sla",
    params: {
      doc: {
        doctype: "HD Service Level Agreement",
        name: slaActiveScreen.value.data.name,
        enabled: slaData.value.enabled,
        description: slaData.value.description,
        service_level: slaData.value.service_level,
        default_sla: slaData.value.default_sla,
        apply_sla_for_resolution: slaData.value.apply_sla_for_resolution,
        priorities: slaData.value.priorities,
        sla_fulfilled_on: fulfilledOn,
        pause_sla_on: pauseOn,
        holiday_list: slaData.value.holiday_list,
        default_priority: slaData.value.default_priority,
        start_date: slaData.value.start_date,
        end_date: slaData.value.end_date,
        support_and_resolution: slaData.value.support_and_resolution,
        condition: slaData.value.condition,
      },
      is_new: false,
    },
    auto: true,
    onSuccess() {
      getSlaData.submit();
    },
  });
};

onUnmounted(() => {
  slaDataErrors.value = {
    service_level: "",
    description: "",
    enabled: "",
    default_sla: "",
    apply_sla_for_resolution: "",
    priorities: "",
    statuses: "",
    holiday_list: "",
    default_priority: "",
    start_date: "",
    end_date: "",
    support_and_resolution: "",
    condition: "",
  };
});
</script>
