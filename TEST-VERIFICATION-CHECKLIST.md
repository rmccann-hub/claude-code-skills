# Test Verification Checklist

Run before claiming any task complete. Answer from output, not from memory.

## Did it run at all

- [ ] `uv run pytest` exited zero, and I read the exit code rather than the summary line.
- [ ] The collection count matches or exceeds the baseline in `.test-baseline` (95 at inception).
- [ ] No test was skipped that was not skipped before.
- [ ] `uv run skillcheck .` exited zero, and its summary names the number of skills I expected.
- [ ] After `npm ci`, `npx --no-install claude plugin validate --strict .` exited zero.

## Did it test the change

- [ ] A test exists that fails without this change. **I ran it against the old code and
      watched it fail**, rather than assuming it would.
- [ ] The assertion checks the value, not merely that something was returned.

## Did the gates run

- [ ] Format and lint ran and passed.
- [ ] CI is green **on the remote**, on the pushed commit, including the secret-scan canary.
      Local green is not remote green.

## What I did not check

- <Anything untested, named plainly. An empty section here is almost always false.>
