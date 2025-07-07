import { createListResource } from "frappe-ui";
import { ref } from "vue";

export const assignmentRulesListData = createListResource({
  doctype: "Assignment Rule",
  fields: ["*"],
  orderBy: "modified desc",
});

export const assignmentRuleData = ref<Record<string, any> | null>({
  loading: false,
  condition: [],
});

export const assignmentRulesActiveScreen = ref<{
  screen: "list" | "view";
  data: Record<string, any> | null;
}>({ screen: "list", data: null });

export const validateAssignmentRule = (key?: string) => {
  const validateField = (field: string) => {
    if (key && field !== key) return;

    switch (field) {
      case "name":
        assignmentRulesErrors.value.name =
          assignmentRuleData.value.name?.length > 0 ? "" : "Name is required";
        break;
    }
  };

  if (key) {
    validateField(key);
  } else {
    (Object.keys(assignmentRulesErrors.value) as string[]).forEach(
      validateField
    );
  }

  return assignmentRulesErrors.value;
};

export const assignmentRulesErrors = ref<Record<string, any> | null>({
  name: "",
});
