interface MessageTranslator {
  t: (key: string) => string;
  te: (key: string) => boolean;
}

export function translateMessage(message: string, i18n: MessageTranslator) {
  return i18n.te(message) ? i18n.t(message) : message;
}
