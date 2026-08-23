package dev.guides.java.jobledger;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.Instant;
import org.junit.jupiter.api.Test;

class ConcurrentJobLedgerTest {
  @Test
  void validatesDomainIdentifiersCommandsAndReceipts() {
    JobId creditId = new JobId("credit-1");
    JobId debitId = new JobId("debit-1");
    CreditJob credit = new CreditJob(creditId, 50);
    DebitJob debit = new DebitJob(debitId, 30);
    JobReceipt receipt = new JobReceipt(
        creditId, JobKind.CREDIT, 50, 150, Instant.parse("2026-01-02T03:04:05Z"));

    assertThat(credit.amount()).isEqualTo(50);
    assertThat(debit.amount()).isEqualTo(30);
    assertThat(receipt.balance()).isEqualTo(150);
    assertThatThrownBy(() -> new JobId(" ")).isInstanceOf(IllegalArgumentException.class);
    assertThatThrownBy(() -> new CreditJob(creditId, 0))
        .isInstanceOf(IllegalArgumentException.class);
    assertThatThrownBy(() -> new DebitJob(debitId, -1))
        .isInstanceOf(IllegalArgumentException.class);
  }
}
