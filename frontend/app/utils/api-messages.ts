import type { Composer } from "vue-i18n";

export function translateApiMessage(message: string, i18n: Composer) {
  return i18n.te(message) ? i18n.t(message) : message;
}
