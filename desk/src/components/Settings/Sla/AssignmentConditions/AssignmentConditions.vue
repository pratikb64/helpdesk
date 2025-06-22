<template>
  <div class="rounded-lg border border-gray-300 p-3 flex flex-col gap-4 w-full">
    <div v-for="(condition, i) in props.conditions" :key="condition.field">
      <AssignmentCondition
        :condition="condition"
        :doctype="'HD Ticket'"
        :isChild="props.isChild"
        :itemIndex="i"
        @remove="removeCondition(condition)"
        @unGroupConditions="unGroupConditions(condition)"
        :level="props.level + 1"
        @updateConjunction="updateConjunction(props.level)"
      />
    </div>
    <div v-if="props.isChild" class="flex">
      <Dropdown v-slot="{ open }" :options="dropdownOptions">
        <Button :disabled="!areConditionsValid">
          Add condition
          <template #prefix>
            <FeatherIcon :name="'plus'" class="h-4" />
          </template>
          <template #suffix>
            <FeatherIcon
              :name="open ? 'chevron-up' : 'chevron-down'"
              class="h-4"
            />
          </template>
        </Button>
      </Dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { Button, FeatherIcon, Dropdown } from "frappe-ui";
import AssignmentCondition from "./AssignmentCondition.vue";

const areConditionsValid = ref(false);

const props = defineProps({
  conditions: {
    type: Array<any>,
    required: true,
  },
  isChild: {
    type: Boolean,
    default: false,
  },
  level: {
    type: Number,
    default: 0,
  },
});

const dropdownOptions = computed(() => {
  const options = [
    {
      label: "Add condition",
      onClick: () => {
        props.conditions.push({
          field: null,
          operator: "equals",
          value: "",
          conjunction: "and",
        });
      },
    },
  ];
  if (props.level < 3) {
    options.push({
      label: "Add condition group",
      onClick: () => {
        props.conditions.push({
          field: "group",
          operator: "equals",
          value: [
            {
              field: null,
              operator: "equals",
              value: "",
              conjunction: "and",
            },
          ],
          conjunction: "and",
        });
      },
    });
  }
  return options;
});

function removeCondition(condition) {
  props.conditions.splice(props.conditions.indexOf(condition), 1);
}

function unGroupConditions(condition) {
  const index = props.conditions.indexOf(condition);
  if (index !== -1 && Array.isArray(condition.value)) {
    props.conditions.splice(index, 1, ...condition.value);
  } else {
    props.conditions.splice(index, 1);
  }
}

const validateConditions = (conditions) => {
  return conditions.every((condition) => {
    if (condition.field === "group" && Array.isArray(condition.value)) {
      return validateConditions(condition.value);
    }
    return (
      condition.field !== null &&
      condition.field !== "" &&
      condition.operator !== "" &&
      condition.value !== ""
    );
  });
};

function updateConjunction(level) {
  const updateConjunctions = (conditions, targetLevel, currentLevel = 0) => {
    if (!conditions || !Array.isArray(conditions)) return;
    const newConjunction = conditions[1]?.conjunction === "and" ? "or" : "and";
    if (currentLevel === targetLevel) {
      conditions.forEach((condition) => {
        if (condition.conjunction) {
          condition.conjunction = newConjunction;
        }
      });
    } else if (currentLevel < targetLevel) {
      updateConjunctions(props.conditions, level, currentLevel + 1);
    }
  };

  updateConjunctions(props.conditions, level);
}

watch(props.conditions, () => {
  areConditionsValid.value = validateConditions(props.conditions);
});

onMounted(() => {
  areConditionsValid.value = validateConditions(props.conditions);
});
</script>
