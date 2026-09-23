# Review QA

**Q: Does your unit test suite run without a database connection?**
A: Yes, using `StubAdapter`.

**Q: Demonstrate a live data break and show your engine catch it.**
A: Run `make demo`. It shows 4 injected bugs being correctly caught.

**Q: How does your engine prevent raw row leakage in log files?**
A: By enforcing count-only aggregation with `sqlglot`, using `SafeQuery`, and having the adapter interface return only scalar integers.
