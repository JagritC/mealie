import { describe, expect, it } from "vitest";
import { translateMessage } from "./use-translated-message";
import { stubI18n } from "~/tests/utils";

describe("translateMessage", () => {
  it("translates messages that are locale keys", () => {
    const i18n = stubI18n();

    expect(translateMessage("recipe.recipe-created", i18n)).toBe("Recipe created");
  });

  it("leaves ordinary messages unchanged", () => {
    const i18n = stubI18n();

    expect(translateMessage("Recipe created", i18n)).toBe("Recipe created");
  });
});
