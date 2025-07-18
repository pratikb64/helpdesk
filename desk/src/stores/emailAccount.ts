import { ref } from "vue";

export const emailAccountActiveScreen = ref<{
  screen: "list" | "edit" | "new";
  provider: string;
  data: Record<string, any> | null;
}>({ screen: "list", provider: "", data: null });
