import { createResource } from "frappe-ui";
import { ref } from "vue";

let callMethod = (number?: string) => {};

function setMakeCall(value) {
  callMethod = value;
}

function makeCall(number) {
  callMethod(number);
}

const callEnabled = ref(false);
const twilioEnabled = ref(false);
const exotelEnabled = ref(false);
const defaultCallingMedium = ref("");
createResource({
  url: "telephony.api.is_call_integration_enabled",
  cache: "Is Call Integration Enabled",
  auto: true,
  onSuccess: (data) => {
    twilioEnabled.value = Boolean(data.twilio_enabled);
    exotelEnabled.value = Boolean(data.exotel_enabled);
    defaultCallingMedium.value = data.default_calling_medium;
    callEnabled.value = twilioEnabled.value || exotelEnabled.value;
  },
});

export function telephonyStore() {
  return {
    callEnabled,
    twilioEnabled,
    exotelEnabled,
    defaultCallingMedium,
    callMethod,
    setMakeCall,
    makeCall,
  };
}
