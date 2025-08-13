import { defineStore } from "pinia";
import { ref } from "vue";
import { call } from "frappe-ui";

export const useTelephonyStore = defineStore("telephony", () => {
  // State
  const callEnabled = ref(false);
  const twilioEnabled = ref(false);
  const exotelEnabled = ref(false);
  const defaultCallingMedium = ref("");
  let callMethod = (number?: string) => {};

  // Actions
  function setMakeCall(value: (number?: string) => void) {
    callMethod = value;
  }

  function setDefaultCallingMedium(value: string) {
    defaultCallingMedium.value = value;
  }

  function makeCall(number: string) {
    callMethod(number);
  }

  async function fetchCallIntegrationStatus() {
    try {
      const data = await call("telephony.api.is_call_integration_enabled");
      twilioEnabled.value = Boolean(data.twilio_enabled);
      exotelEnabled.value = Boolean(data.exotel_enabled);
      defaultCallingMedium.value = data.default_calling_medium;
      callEnabled.value = twilioEnabled.value || exotelEnabled.value;
    } catch (error) {
      console.error("Failed to fetch call integration status:", error);
    }
  }

  return {
    // State
    callEnabled,
    twilioEnabled,
    exotelEnabled,
    defaultCallingMedium,

    // Actions
    setMakeCall,
    makeCall,
    fetchCallIntegrationStatus,
    setDefaultCallingMedium,
  };
});
