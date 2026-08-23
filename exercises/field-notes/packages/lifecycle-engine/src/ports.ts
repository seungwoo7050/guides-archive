import type {
  AccountReadinessState,
  BoundedWorkerObservation,
  ConflictReadinessState,
  LifecycleSyncTrigger,
  ProcessedIntentClaim,
  ProcessedIntentCompletion,
  RecordReadinessState,
} from "./types.ts";

export interface BoundedWorkerPort {
  run(input: { trigger: LifecycleSyncTrigger; workerId: string; signal?: AbortSignal }): Promise<BoundedWorkerObservation>;
}
export interface LifecycleClock { now(): number; }
export interface DeadlineScheduler { schedule(at: number, callback: () => void): () => void; }
export interface WorkerIdGenerator { next(trigger: LifecycleSyncTrigger): string; }
export interface NotificationStateRepository {
  ready(): Promise<void>;
  currentAccount(): Promise<AccountReadinessState>;
  recordState(recordId: string): Promise<RecordReadinessState>;
  conflictState(recordId: string): Promise<ConflictReadinessState>;
  isSyncBlocked(): Promise<boolean>;
}
export type ProcessedIntentClaimResult =
  | { kind: "claimed"; claim: ProcessedIntentClaim }
  | { kind: "duplicate" }
  | { kind: "busy" };
export interface ProcessedIntentClaimPort {
  claim(input: { messageId: string; ownerId: string; now: number; leaseDurationMs: number }): Promise<ProcessedIntentClaimResult>;
  complete(claim: ProcessedIntentClaim, outcome?: ProcessedIntentCompletion): Promise<void>;
  release(claim: ProcessedIntentClaim): Promise<void>;
}
export interface NotificationOwnerIdGenerator { next(messageId: string): string; }
