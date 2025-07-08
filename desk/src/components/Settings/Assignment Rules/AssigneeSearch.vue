<template>
  <Combobox nullable>
    <Popover>
      <template #target="{ togglePopover }">
        <Button
          variant="solid"
          icon-left="plus"
          @click="togglePopover()"
          label="Add Assignee"
        />
      </template>
      <template #body>
        <div class="mt-1 rounded-lg bg-white py-1 text-base shadow-2xl w-60">
          <div class="relative px-1.5 pt-0.5">
            <ComboboxInput
              ref="search"
              class="form-input w-full"
              type="text"
              @change="
                (e) => {
                  query = e.target.value;
                }
              "
              :value="query"
              autocomplete="off"
              placeholder="Search"
            />
            <button
              class="absolute right-1.5 inline-flex h-7 w-7 items-center justify-center"
              @click="query = ''"
            >
              <FeatherIcon name="x" class="w-4" />
            </button>
          </div>
          <ComboboxOptions
            class="my-2 max-h-[12rem] overflow-y-auto px-1.5"
            static
          >
            <ComboboxOption
              v-show="usersList.data?.length > 0"
              v-for="user in usersList.data"
              :key="user.username"
              :value="user"
              as="template"
              v-slot="{ active, selected }"
            >
              <li
                class="flex items-center rounded p-1.5 w-full text-base"
                :class="{ 'bg-gray-100': active }"
                @click="addAssignee(user)"
              >
                <div class="flex gap-2 items-center w-full select-none">
                  <Avatar
                    v-if="!checkIfUserExists(user)"
                    :shape="'circle'"
                    :image="user.user_image"
                    :label="user.full_name"
                    size="lg"
                  />
                  <div
                    v-else
                    class="size-7 flex items-center justify-center rounded-full bg-gray-200"
                  >
                    <FeatherIcon name="check" class="w-4" />
                  </div>
                  <div class="flex flex-col gap-1">
                    <div class="font-semibold text-ink-gray-7">
                      {{ user.full_name }}
                    </div>
                    <div class="text-ink-gray-6">{{ user.email }}</div>
                  </div>
                </div>
              </li>
            </ComboboxOption>
            <li
              v-if="usersList.data?.length == 0"
              class="mt-1.5 rounded-md p-1.5 text-base text-gray-600"
            >
              No results found
            </li>
          </ComboboxOptions>
          <div class="border-t p-1.5 pb-0.5">
            <Button
              variant="ghost"
              class="w-full"
              icon-left="plus"
              label="Invite agent"
            />
          </div>
        </div>
      </template>
    </Popover>
  </Combobox>
</template>

<script setup lang="ts">
import { assignmentRuleData } from "@/stores/assignmentRules";
import {
  Combobox,
  ComboboxInput,
  ComboboxOption,
  ComboboxOptions,
} from "@headlessui/vue";
import { watchDebounced } from "@vueuse/core";
import { Avatar, createListResource, Popover } from "frappe-ui";
import { ref } from "vue";

const emit = defineEmits(["addAssignee"]);
const query = ref("");

watchDebounced(
  () => query.value,
  (val) => {
    const filters = {
      full_name: undefined,
      email: undefined,
    };
    const isEmail = val.includes("@") || val.includes(".");
    if (isEmail) {
      filters.email = ["like", `%${val}%`];
    } else {
      filters.full_name = ["like", `%${val}%`];
    }
    usersList.update({
      filters,
    });
    usersList.reload();
  },
  { debounce: 500 }
);

const usersList = createListResource({
  doctype: "User",
  fields: ["*"],
  start: 0,
  pageLength: 6,
  auto: true,
  transform: (data) => {
    return data.map((user) => {
      return {
        ...user,
        user: user.email,
      };
    });
  },
});

const addAssignee = (user) => {
  const userExists = assignmentRuleData.value.users.some(
    (u) => u.user === user.user
  );
  if (!userExists) {
    if (user.full_name == "Administrator") {
      user.user = "Administrator";
    }
    if (user.full_name == "Guest") {
      user.user = "Guest";
    }
    assignmentRuleData.value.users.push(user);
    emit("addAssignee", user);
  }
};

const checkIfUserExists = (user) => {
  return assignmentRuleData.value.users.some((u) => u.user === user.email);
};
</script>
