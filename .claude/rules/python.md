---
paths:
  - "src/**/*.py"
  - "tests/**/*.py"
---

# Python in this repository

- Tests never read real skills. Build a throwaway repository with the `repo` fixture in
  `tests/conftest.py`.
- A new `skillcheck` rule comes with a test that plants the defect and asserts the rule fires
  alone, beside one showing a clean repository still passes.
- The coverage floor is 100% because that was the measured number. Lower it only in its own
  change, with the reason in the commit message.
- Raise `.test-baseline` in the same change that adds tests.
