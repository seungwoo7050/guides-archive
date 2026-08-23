package dev.guides.java.counterrace;

import java.util.List;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

public final class DeterministicRaceDemo {
  private static final long INITIAL_VALUE = 100;
  private static final long DELTA = 80;
  private DeterministicRaceDemo() {}

  // [Implementation 2] lost update 재현 결과와 실행기 종료를 함께 관리합니다.
  public static void main(String[] arguments) throws Exception {
    RacyCounter counter = new RacyCounter(INITIAL_VALUE);
    CyclicBarrier barrier = new CyclicBarrier(2);
    ExecutorService executor = Executors.newFixedThreadPool(2);
    try {
      List<Future<Boolean>> results = List.of(
          executor.submit(() -> counter.trySubtract(DELTA, barrier)),
          executor.submit(() -> counter.trySubtract(DELTA, barrier)));
      long accepted = 0;
      for (Future<Boolean> result : results) if (result.get(2, TimeUnit.SECONDS)) accepted += DELTA;
      System.out.printf("racy accepted=%d value=%d invariant=%s%n",
          accepted, counter.value(), accepted + counter.value() == INITIAL_VALUE);
    } finally {
      executor.shutdownNow();
      if (!executor.awaitTermination(2, TimeUnit.SECONDS)) {
        throw new IllegalStateException("executor did not terminate before the deadline");
      }
    }
  }
}
