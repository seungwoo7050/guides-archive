import {
  BoundedSyncWorker,
  FixedSyncBudget,
  type SyncRepository,
  type SyncTransport,
} from "@field-notes/sync-engine";

// [Implementation 7]
// SQLite repository와 HTTP transport를 lifecycle package 없이 직접 조합합니다.
export type ProductionSyncRuntime = {
  worker: BoundedSyncWorker;
  run(signal?: AbortSignal): ReturnType<BoundedSyncWorker["run"]>;
};

export function createProductionSyncRuntime(input: {
  repository: SyncRepository;
  transport: SyncTransport;
}): ProductionSyncRuntime {
  const worker = new BoundedSyncWorker({
    repository: input.repository,
    transport: input.transport,
    budget: new FixedSyncBudget({ maxCommands: 16, maxAttemptsPerCommand: 3 }),
  });
  return {
    worker,
    run: (signal) => worker.run({ workerId: "production-sync", signal }),
  };
}
