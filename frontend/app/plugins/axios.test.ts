import { describe, expect, it } from "vitest";
import { stubI18n } from "~/tests/utils";
import { translateApiMessage } from "~/utils/api-messages";

describe("translateApiMessage", () => {
  it("translates API messages that are i18n keys", () => {
    expect(translateApiMessage("recipe.recipe-created", stubI18n())).toBe("Recipe created");
  });

  it("keeps API messages that are already display text", () => {
    expect(translateApiMessage("Recipe imported successfully", stubI18n())).toBe("Recipe imported successfully");
  });
});
