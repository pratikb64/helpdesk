<template>
  <div>
    <div class="grid grid-cols-8 items-center gap-3 text-sm text-gray-600 ml-2">
      <div class="col-span-6">Name</div>
      <div class="col-span-2">Date created</div>
    </div>
    <hr class="mt-2 mx-2" />
    <div v-for="account in emailAccountList.data" :key="account.name">
      <EmailAccountsListItem :data="account" />
      <hr class="mx-2" />
    </div>
    <div class="mt-8">
      <h1 class="text-lg text-ink-gray-8 font-semibold">Default settings</h1>
      <div class="mt-6">
        <div class="text-base font-medium text-ink-gray-8">
          Default Incoming
        </div>
        <div class="flex justify-between mt-2 gap-4">
          <div class="text-base text-ink-gray-6 w-4/6 leading-5">
            If enabled, all replies to your company (eg: replies@yourcomany.com)
            will come to this account. Note: Only one account can be default
            incoming.
          </div>
          <div>
            <Autocomplete
              :model-value="defaultIncoming"
              @update:model-value="onDefaultIncomingChange"
              class="w-max"
              :options="incomingAccounts"
              placeholder="Select account"
              placement="bottom-end"
            >
              <template #prefix>
                <img
                  v-if="defaultIncoming.icon"
                  :src="defaultIncoming.icon"
                  class="mr-2 size-4"
                />
              </template>
              <template #item-prefix="{ option }">
                <img :src="option?.image" class="size-4" />
              </template>
            </Autocomplete>
          </div>
        </div>
      </div>
      <hr class="my-4" />
      <div>
        <div class="text-base font-medium text-ink-gray-8">
          Default Outgoing
        </div>
        <div class="flex justify-between mt-2 gap-4">
          <div class="text-base text-ink-gray-6 w-4/6 leading-5">
            If enabled, all outgoing emails will be sent from this account.
            Note: Only one account can be default outgoing.
          </div>
          <div>
            <Autocomplete
              :model-value="defaultOutgoing"
              @update:model-value="onDefaultOutgoingChange"
              class="w-max"
              :options="outgoingAccounts"
              placeholder="Select account"
              placement="bottom-end"
            >
              <template #prefix>
                <img
                  v-if="defaultOutgoing.icon"
                  :src="defaultOutgoing.icon"
                  class="mr-2 size-4"
                />
              </template>
              <template #item-prefix="{ option }">
                <img :src="option?.image" class="size-4" />
              </template>
            </Autocomplete>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Autocomplete, toast } from "frappe-ui";
import EmailAccountsListItem from "./EmailAccountsListItem.vue";
import { computed, ref } from "vue";
import { inject } from "vue";
import { emailIcons } from "./utils";

const emailAccountList = inject<any>("emailAccountList");

const defaultIncoming = ref({
  value: "",
  icon: "",
});
const defaultOutgoing = ref({
  value: "",
  icon: "",
});

const incomingAccounts = computed(() => {
  return emailAccountList.data
    ?.filter((account) => account.enable_incoming == 1)
    .map((account) => {
      const providerIcon = emailIcons[account.service];
      if (account.default_incoming == 1) {
        defaultIncoming.value = {
          value: account.name,
          icon: providerIcon?.icon,
        };
      }
      return {
        label: account.name,
        value: account.name,
        image: providerIcon?.icon,
      };
    });
});

const outgoingAccounts = computed(() => {
  return emailAccountList.data
    ?.filter((account) => account.enable_outgoing == 1)
    .map((account) => {
      const providerIcon = emailIcons[account.service];
      if (account.default_outgoing == 1) {
        defaultOutgoing.value = {
          value: account.name,
          icon: providerIcon?.icon,
        };
      }
      return {
        label: account.name,
        value: account.name,
        image: providerIcon?.icon,
      };
    });
});

const onDefaultIncomingChange = (account) => {
  const oldAccount = Object.assign({}, defaultIncoming.value);

  emailAccountList.setValue.submit(
    {
      name: account ? account.value : defaultIncoming.value.value,
      default_incoming: account ? 1 : 0,
    },
    {
      onSuccess: () => {
        toast.success("Default incoming account updated");
        emailAccountList.reload();
        if (!account) {
          defaultIncoming.value = {
            value: "",
            icon: "",
          };
        } else {
          defaultIncoming.value = {
            value: account.value,
            icon: emailIcons[account.service]?.icon,
          };
        }
      },
      onError: () => {
        toast.error("Failed to update default account");
        defaultIncoming.value = {
          value: oldAccount.value,
          icon: oldAccount.icon,
        };
      },
    }
  );
};

const onDefaultOutgoingChange = (account) => {
  const oldAccount = Object.assign({}, defaultOutgoing.value);
  emailAccountList.setValue.submit(
    {
      name: account ? account.value : defaultOutgoing.value.value,
      default_outgoing: account ? 1 : 0,
    },
    {
      onSuccess: () => {
        toast.success("Default outgoing account updated");
        emailAccountList.reload();
        if (!account) {
          defaultOutgoing.value = {
            value: "",
            icon: "",
          };
        } else {
          defaultOutgoing.value = {
            value: account.value,
            icon: emailIcons[account.service]?.icon,
          };
        }
      },
      onError: () => {
        toast.error("Failed to update default account");
        defaultOutgoing.value = {
          value: oldAccount.value,
          icon: oldAccount.icon,
        };
      },
    }
  );
};
</script>
