import { ref } from "vue";
import { createResource } from "frappe-ui";

export const slaPolicyListData = createResource({
  url: "frappe.client.get_list",
  params: {
    doctype: "HD Service Level Agreement",
    fields: ["*"],
  },
});

export const slaData = ref({
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

export const resetSlaData = () => {
  slaData.value = {
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
  };
};

export const slaActiveScreen = ref<{
  screen: "list" | "view";
  data: Record<string, any> | null;
}>({ screen: "list", data: null });

export const slaDataErrors = ref<SlaValidationErrors>({
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
});

export function validateSlaData(): SlaValidationErrors {
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
  // Validate service level name
  if (!slaData.value.service_level?.trim()) {
    slaDataErrors.value.service_level = "SLA policy name is required";
  }

  // Validate priorities
  if (
    !Array.isArray(slaData.value.priorities) ||
    slaData.value.priorities.length === 0
  ) {
    slaDataErrors.value.priorities = "At least one priority is required";
  } else {
    const prioritiesError: string[] = [];
    slaData.value.priorities.forEach((priority, index) => {
      const priorityNum = index + 1;
      if (!priority.priority?.trim()) {
        prioritiesError.push(
          `Priority ${priorityNum}: Priority name is required`
        );
      }
      if (!priority.response_time || priority.response_time == 0) {
        prioritiesError.push(
          `Priority ${priorityNum}: Response time is required`
        );
      }
      if (
        Boolean(slaData.value.apply_sla_for_resolution) &&
        priority.resolution_time == 0
      ) {
        prioritiesError.push(
          `Priority ${priorityNum}: Resolution time is required`
        );
      }
    });

    // Check for duplicate priorities
    const priorityNames = slaData.value.priorities
      .map((p) => p.priority?.trim().toLowerCase())
      .filter(Boolean);
    const uniquePriorities = new Set(priorityNames);

    if (priorityNames.length !== uniquePriorities.size) {
      prioritiesError.push("Priorities must be unique");
    }

    if (prioritiesError.length > 0) {
      slaDataErrors.value.priorities = prioritiesError.join(", ");
    }

    const hasDefaultPriority = slaData.value.priorities.some((p) =>
      Boolean(p.default_priority)
    );
    if (!hasDefaultPriority) {
      slaDataErrors.value.default_priority = "Default priority is required";
    }
  }

  // Validate date range
  if (slaData.value.start_date && slaData.value.end_date) {
    const startDate = new Date(slaData.value.start_date);
    const endDate = new Date(slaData.value.end_date);

    if (startDate > endDate) {
      slaDataErrors.value.end_date = "'To date' must be after 'From date'";
    }
  }

  // Validate statuses
  if (
    !Array.isArray(slaData.value.statuses) ||
    slaData.value.statuses.length === 0
  ) {
    slaDataErrors.value.statuses =
      "At least one status for 'Fulfilled on' and 'Paused on' is required";
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
    }
    if (!hasPaused) {
      slaDataErrors.value.statuses =
        "At least one 'Paused on' status is required";
    }
  }

  // Validate workdays
  const validWorkdays = slaData.value.support_and_resolution?.filter(
    (day) =>
      !day.is_holiday &&
      day.workday &&
      day.workday.trim() !== "" &&
      day.start_time &&
      day.end_time &&
      day.start_time.trim() !== "" &&
      day.end_time.trim() !== ""
  );

  if (!validWorkdays?.length) {
    slaDataErrors.value.support_and_resolution =
      "At least one valid workday with workday, start time, and end time is required";
  } else {
    // Check for duplicate workdays
    const workdayMap = new Map();
    const duplicateWorkdays = [];

    for (const day of validWorkdays) {
      if (workdayMap.has(day.workday)) {
        duplicateWorkdays.push(day.workday);
      } else {
        workdayMap.set(day.workday, true);
      }
    }

    if (duplicateWorkdays.length > 0) {
      slaDataErrors.value.support_and_resolution = `Duplicate workday found: ${duplicateWorkdays.join(
        ", "
      )}. Each workday should be unique.`;
      return slaDataErrors.value;
    }

    // Check for valid time ranges
    const invalidTimeRanges = [];
    for (const [index, day] of validWorkdays.entries()) {
      const startTime = day.start_time.trim();
      const endTime = day.end_time.trim();

      if (startTime >= endTime) {
        invalidTimeRanges.push(`${day.workday} (${startTime} - ${endTime})`);
      }

      // Validate time format (HH:MM or H:MM)
      const timeRegex = /^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/;
      if (!timeRegex.test(startTime) || !timeRegex.test(endTime)) {
        slaDataErrors.value.support_and_resolution = `Invalid time format for ${day.workday}. Please use HH:MM format.`;
        return slaDataErrors.value;
      }
    }

    if (invalidTimeRanges.length > 0) {
      slaDataErrors.value.support_and_resolution = `End time must be after start time for: ${invalidTimeRanges.join(
        ", "
      )}`;
    }
  }

  // Validate conditions
  if (slaData.value.condition && slaData.value.condition.length > 0) {
    const hasInvalidCondition = slaData.value.condition.some(
      (condition) =>
        !condition.field ||
        condition.value === undefined ||
        condition.value === null ||
        condition.value === ""
    );
    if (hasInvalidCondition) {
      slaDataErrors.value.condition = `Field and value are required for all conditions`;
    }
  }

  return slaDataErrors.value;
}

interface SlaData {
  service_level?: string;
  description?: string;
  enabled?: boolean;
  default_sla?: boolean;
  apply_sla_for_resolution?: boolean;
  priorities: Array<{
    priority?: string;
    response_time?: number;
    resolution_time?: number;
    default_priority?: boolean;
    [key: string]: any;
  }>;
  statuses: Array<{
    sla_behavior: string;
    [key: string]: any;
  }>;
  support_and_resolution?: Array<{
    is_holiday: boolean;
    start_time: string;
    end_time: string;
    [key: string]: any;
  }>;
  condition?: any[];
  start_date?: string;
  end_date?: string;
  [key: string]: any;
}

export interface SlaValidationErrors {
  service_level: string;
  description: string;
  enabled: string;
  default_sla: string;
  apply_sla_for_resolution: string;
  priorities: string;
  statuses: string;
  holiday_list: string;
  default_priority: string;
  start_date: string;
  end_date: string;
  support_and_resolution: string;
  condition: string;
  [key: string]: string;
}
