import { ref } from "vue";
import { createResource } from "frappe-ui";

export const slaPolicyListData = createResource({
  url: "frappe.client.get_list",
  params: {
    doctype: "HD Service Level Agreement",
    fields: ["*"],
  },
});

export const slaActiveScreen = ref<{
  screen: "list" | "view";
  data: Record<string, any> | null;
}>({ screen: "list", data: null });

export const slaDataErrors = ref({
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
