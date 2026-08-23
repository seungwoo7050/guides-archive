import assert from "node:assert/strict";
import test from "node:test";
import { parseNotificationEnvelope } from "../src/index.ts";

test("parses a bounded record notification envelope", () => {
  assert.equal(parseNotificationEnvelope({
    schemaVersion: 1,
    messageId: "message-1",
    accountId: "account-1",
    intent: { kind: "record-updated", recordId: "record-1" },
  }).kind, "valid");
});

test("rejects business snapshots and unknown fields", () => {
  assert.equal(parseNotificationEnvelope({
    schemaVersion: 1,
    messageId: "message-1",
    accountId: "account-1",
    intent: { kind: "sync-blocked" },
    record: { title: "must-not-cross-boundary" },
  }).kind, "invalid");
});
