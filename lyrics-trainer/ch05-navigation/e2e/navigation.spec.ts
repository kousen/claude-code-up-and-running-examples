import { expect, test } from "@playwright/test";

test("navigation controls and keyboard shortcuts move between lines", async ({ page }) => {
  const consoleErrors: string[] = [];
  page.on("console", (message) => {
    const location = message.location();
    if (message.type() === "error" && !location.url.endsWith("/favicon.ico")) {
      consoleErrors.push(message.text());
    }
  });

  await page.goto("/");

  await expect(page.getByRole("heading", { name: /Sonnet 18.*Line by Line/ })).toBeVisible();
  await expect(page.getByText("Line 1 of 14")).toBeVisible();
  await expect(page.getByText("Shall I compare thee to a summer's day?")).toBeVisible();

  await page.getByRole("button", { name: "Next" }).click();
  await expect(page.getByText("Line 2 of 14")).toBeVisible();
  await expect(page.getByText("Thou art more lovely and more temperate:")).toBeVisible();

  await page.locator("body").click();
  await page.keyboard.press("ArrowRight");
  await expect(page.getByText("Line 3 of 14")).toBeVisible();
  await expect(page.getByText("Rough winds do shake the darling buds of May,")).toBeVisible();

  await page.getByRole("button", { name: "Previous" }).click();
  await expect(page.getByText("Line 2 of 14")).toBeVisible();

  await page.reload();
  await expect(page.getByText("Line 2 of 14")).toBeVisible();
  expect(consoleErrors).toEqual([]);
});
