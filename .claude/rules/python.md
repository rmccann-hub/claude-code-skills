---
paths:
  - "src/**/*.py"
  - "tests/**/*.py"
---

# Python in this repository

- Tests of `skillcheck`'s rules never read real skills. Build a throwaway repository with the
  `repo` fixture in `tests/conftest.py`. Only a skill's own asset tests, such as
  `tests/test_git_workflows_assets.py`, read that skill's bundled examples, to prove they work.
- A new `skillcheck` rule comes with a test that plants the defect and asserts the rule fires
  alone, beside one showing a clean repository still passes.
- The coverage floor is 100% because that was the measured number. Lower it only in its own
  change, with the reason in the commit message.
- Raise `.test-baseline` in the same change that adds tests.
