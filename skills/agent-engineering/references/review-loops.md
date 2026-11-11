# Review loops

Read this for running agent sessions that review each other's work in rounds: two sessions in two
repositories that depend on each other, one agent reviewing another's work in one repository, or
an agent acting on an AI code reviewer's findings. It covers closing a round, whose turn it is,
what counts as evidence, and where the agents stop for a person.

Reviewing code for bugs is the `coding` skill's work. Review comments and steward files are
`commits-and-pull-requests` and `pr-stewardship`. A session's context file is
`agent-context-files`, and a peer's message read as instructions is `ai-agent-security`.

## Rules

1. **Close a round on evidence, never on agreement.** A verdict cites a run, a checker's output
   or a line at a commit. An answer changed with no new evidence counts for nothing. A cause
   read from a small sample is a correlation, withdrawn once the side with the data disagrees.
2. **Fix the close condition, and what proves it, in the round's first message,** with the
   message format settled before it. Only the person's recorded word changes it.
3. **Each message says what is established, what it waits on, how the next verdict will be
   decided, and what it doesn't ask:** "our next message says GO unless the run shows X". Name a
   wait by its condition, not a version.
4. **Stop when a round adds no evidence.** Close if the condition is met; otherwise take both
   positions and their evidence to the person.
5. **Hold the turn in one record that refuses a stale writer,** as *The turn* says. Naming the
   next writer isn't enough.
6. **A request the person gives both sides names one builder.** The other side reviews.
7. **Read the other side's committed state, every branch,** at session start and before ending
   a turn, and every released message before summing up. Check what the code already does
   before recommending it.
8. **Cite claims as `owner/repo@commit:path:line`, and paste every hash from a command's
   output.** A file both sides hold identically is copied byte for byte, checked by SHA-256.
9. **Put what both codebases must agree on in a contract both CIs check.** A change is agreed
   word for word, and checked against the other's tree from a fresh clone.
10. **Stop for the person where agents can't supply the answer:** hardware time, a design both
    accept, merging, releasing, approving, syncing a fork. Ask once, in writing, saying what
    waits. A session that stops says what it waits on, and from whom.
11. **Record the person's ruling once, word for word, where future readers look,** with who and
    when. An answer from one side isn't a settlement.
12. **An AI reviewer's output is findings to check, not a verdict.** No findings isn't a pass;
    an AI approval counts only where a person turned approvals on, in writing.
13. **Keep the rules that end rounds or check evidence, and cut any that never fired.**

### The turn

- **One record holds the turn,** its number and holder, on a branch both sessions can push to.
  Take it by committing on top of the commit you read, then pushing. Git refuses a push that isn't
  a fast-forward (fact `rl-git-push`), so it lands only if the branch hasn't moved: a
  compare-and-set. `--force-with-lease=<ref>:<commit>` names the expected commit outright.
- **A refused push means the other side moved.** Fetch, read, decide again. Pulling, rebasing
  and pushing the same message turns the check off.
- **The turn number is a fencing token** (fact `rl-fencing`). Each message carries it and the
  commit it answers. One with an older number, or answering a superseded commit, is renumbered
  and answered as a reply, without asking the person.
- **With no shared branch,** a message written out of turn is held, not sent. If two cross
  anyway, the earlier committer date counts and the other becomes a reply. Both sides read the
  same dates, so they agree, but this orders crossings and prevents none.
- **A message is sent when its push lands** on the branch the other side reads.

## Mistakes

- **Two sessions writing one message,** both reading "yours, or ours first" as theirs. Name one.
- **Messages crossing three times in two rounds** under a one-writer rule: each side wrote while
  waiting. Take the turn by a push that fails if the branch moved.
- **Closing because both sides agree.** Debate produces agreement, right or wrong; close on the
  run.
- **A green run read as a correct one.** The graders asked whether each check ran, not what it
  found, so two wrong outputs passed. Grade what each check found.
- **Reading one fetched branch.** A side looked idle for an hour while it had pushed twice.
  Fetch every branch.
- **Retyping a hash.** One had its first 16 characters right and the rest invented. Paste it.
- **Taking a person's question as a question.** `I thought we just needed X?` is the instruction.
- **Re-arguing a comment an AI reviewer repeats** after it was resolved (fact
  `rl-copilot-repeats`). Point to the resolution.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Close condition | A first message that doesn't name what closes the round, and what proves it | `GAP` | Add it first |
| Evidence | A verdict resting on agreement, not a run, checker or cited line | `GAP` | Cite, or reopen |
| The turn | No one record holds the turn, or a stale push can move it | `GAP`; `DRIFT` where messages crossed | Move it to one branch |
| One builder | A request to both sides with no builder named | `GAP` | Name one |
| Reading and citing | Relayed copies, one fetched branch, retyped hashes, uncited claims | `DRIFT` | Read every branch; cite and paste |
| Contract | What both sides must agree on lives only in messages | `GAP` | A file both CIs check |
| Rounds | Rounds with no new evidence, neither closed nor taken to the person | `GAP` | Close, or escalate |
| The person | A ruling not recorded verbatim; a stopped side silent on what it waits for | `GAP` | Record it; name the wait |
| AI approvals | AI approvals count toward required reviews, with no written policy | `GAP` | Write the paths and who chose |
| Choreography | Rules that never fired | `DRIFT` | Cut them |

## Why

### Evidence, not agreement

- **The advice:** close on a run, a checker or a cited line, read from the committed source.
- **The reason:** agreement isn't evidence of correctness (fact `rl-agreement`). Voting explains
  most of debate's gains (fact `rl-voting`), peers talk each other out of right answers (fact
  `rl-flips`), and a model doesn't fix its reasoning without outside feedback (fact
  `rl-self-correct`). Over one loop's 31 rounds, the value came from committed files or a run
  on hardware, rarely from argument (L26); a cause read from a few runs fell to the other
  side's data (L45). Copies misled: an operator's message held three stale numbers (L30), and
  four reports in a day each corrected the last, so a coordinator sends one file of record,
  naming what it replaces (L46). An early digest couldn't be reproduced (L35), a reviewer
  reading plans recommended checks the code had (L54), a stale branch gave 13 false refusals
  (L28), and a retyped hash was invented (L38).
- **What others do, and why:** Google puts facts and data over opinions (fact
  `rl-google-disagree`), and contract tools gate a deploy on a recorded check (facts `rl-pact`,
  `rl-oasdiff`).
- **What it costs:** a run or check per verdict, and a fetch of every branch.
- **When to choose differently:** a matter of taste has no test; record it as the person's call.

### Close conditions, and when to stop

- **The advice:** fix the close condition first, commit to the next verdict, and stop when a
  round adds nothing.
- **The reason:** with a verdict committed in advance a round closed in three messages; one
  without took 37 (L26, L36). The format took six changes to settle (L30), and a shorter run
  replaced the agreed one only by the person's word (L37). Gains level off near four rounds
  (fact `rl-plateau`), and a fixed count stops early or runs on (fact `rl-adaptive-stop`).
- **What others do, and why:** Anthropic pauses for a person at blockers and caps iterations
  (fact `rl-agent-stops`); Google escalates rather than let a change sit. No study tests a
  verdict committed in advance: that is this repository's practice.
- **What it costs:** a condition written before the work is understood.
- **When to choose differently:** an exploratory round, named as one, ending in a condition.

### The turn

- **The advice:** one record holds the turn, moved only by a push built on the commit read.
- **The reason:** per-side numbering still let both sides write one message, three times in two
  rounds, and both built one test runner the same evening (L55). MAST counts inter-agent
  misalignment among its failure categories (fact `rl-mast`), 32.3% of failures in its v3
  paper, with step repetition and unawareness of termination conditions, design failures, at
  15.7% and 12.4%. So turn and stop rules stay, while envelopes, digests, a ledger field and
  deadlines that never fired cost more than they caught (L26).
- **What others do, and why:** a lease alone lets a paused holder write on a stale view, so
  distributed systems check a token where the write lands (fact `rl-fencing`).
- **What it costs:** a branch both sessions can push to.
- **When to choose differently:** with no shared branch, the committer-date tiebreak.

### Where the person decides

- **The advice:** ask once for what agents can't supply, and record the ruling.
- **The reason:** no number of messages stood in for hardware time, a design, or the owner's
  acts (L26). Approval given with the request saved a round trip per message (L30).
- **What others do, and why:** Google records a resolution "for future readers" (fact
  `rl-google-disagree`). Claude Code Review never approves or runs code, and reads its rules
  from the base branch (fact `rl-claude-review`). Copilot's approvals count only once an admin
  turns them on (fact `rl-copilot-approvals`).
- **What it costs:** the person's attention.
- **When to choose differently:** a standing word, quoted with its date, covers what it names.

## Facts

Checked 2026-11-10; `rl-git-push` 2026-11-11.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `rl-agreement` | Agents agreeing isn't evidence (Wang et al.) | [arXiv](https://arxiv.org/abs/2604.07667) | "agreement is not evidence of correctness" | 2026-11-10 | 2027-05-10 |
| `rl-voting` | Voting explains most debate gains (Choi et al., NeurIPS 2025) | [arXiv](https://arxiv.org/abs/2508.17536) | "Majority Voting alone accounts for most of the performance gains" | 2026-11-10 | 2027-05-10 |
| `rl-flips` | Debaters switch right answers to wrong (Wynn et al.) | [arXiv](https://arxiv.org/abs/2509.05396) | "models frequently shift from correct to incorrect answers in response to peer reasoning" | 2026-11-10 | 2027-05-10 |
| `rl-self-correct` | No self-correction without outside feedback (Huang et al., ICLR 2024) | [arXiv](https://arxiv.org/abs/2310.01798) | "LLMs struggle to self-correct their responses without external feedback" | 2026-11-10 | 2027-05-10 |
| `rl-mast` | MAST's three failure categories (Cemri et al.) | [arXiv](https://arxiv.org/abs/2503.13657) | "(i) system design issues, (ii) inter-agent misalignment, and (iii) task verification" | 2026-11-10 | 2027-05-10 |
| `rl-plateau` | Gains level off at four rounds (Du et al.) | [arXiv](https://arxiv.org/html/2305.14325v1) | "additional debate rounds above four led to a similar final performance" | 2026-11-10 | 2027-05-10 |
| `rl-adaptive-stop` | Fixed round counts misfire (Hu et al.) | [arXiv](https://arxiv.org/html/2510.12697v1) | "premature stopping before consensus is reached or unnecessary computation after convergence" | 2026-11-10 | 2027-05-10 |
| `rl-agent-stops` | Anthropic: pause at blockers, cap iterations | [Anthropic](https://www.anthropic.com/research/building-effective-agents) | "pause for human feedback at checkpoints or when encountering blockers" and "a maximum number of iterations" | 2026-11-10 | 2027-05-10 |
| `rl-fencing` | A fencing token rises with each grant (Kleppmann) | [Blog](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html) | "a fencing token is simply a number that increases" | 2026-11-10 | 2027-05-10 |
| `rl-git-push` | `git push` refuses a non-fast-forward; a lease fails unless the ref is as expected | [Git](https://git-scm.com/docs/git-push) | "git push refuses to update a remote ref that is not an ancestor of the local ref" and "the current value of the remote ref is the expected value. git push fails otherwise." | 2026-11-11 | 2027-05-11 |
| `rl-claude-review` | Claude Code Review never approves or runs code, reads `REVIEW.md` from the base or default branch, and no findings isn't a pass | [Code Review](https://code.claude.com/docs/en/code-review) | "A review never approves or blocks the pull request" and "without building or running your code" and "never from the pull request's own changes" and "A review with no findings doesn't mean your code is error-free or secure." | 2026-11-10 | 2027-02-10 |
| `rl-copilot-approvals` | Copilot approvals, GA 2026-10-28: off by default; count once on; dismissed by new commits | [GitHub](https://github.blog/changelog/2026-10-28-copilot-code-review-merge-with-confidence-with-max-and-approvals/) | "Approvals are off by default." and "counts toward your repository's required approvals" and "the approval is dismissed" | 2026-11-10 | 2027-02-10 |
| `rl-copilot-repeats` | A Copilot re-review may repeat resolved comments | [GitHub Docs](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/copilot-code-review) | "Copilot may repeat previous comments, even if you resolved or downvoted them" | 2026-11-10 | 2027-02-10 |
| `rl-google-disagree` | Google: facts over opinions; escalate; record the result | [Google](https://google.github.io/eng-practices/review/reviewer/standard.html) | "Technical facts and data overrule opinions" and "the most common way to resolve it would be to escalate" and "for future readers" | 2026-11-10 | 2027-05-10 |
| `rl-pact` | Pact's `can-i-deploy` checks a consumer against its providers | [Pact](https://docs.pact.io/consumer) | "It will give you a definitive answer" | 2026-11-10 | 2027-05-10 |
| `rl-oasdiff` | `oasdiff breaking` exits 1 on a breaking change | [oasdiff](https://oasdiff.com/docs) | "1 when breaking changes are found" | 2026-11-10 | 2027-02-10 |

## Sources

| Source | Used for | License |
|---|---|---|
| This repository's lessons, repositories unnamed | Rules, mistakes | Apache-2.0 |
| arXiv: Wang, Choi, Wynn, Huang, Du | Agreement, rounds | CC BY 4.0: quoted, attributed |
| arXiv: Cemri (MAST), Hu | Failures, stopping | CC BY-NC-ND 4.0: short quotes, no adaptation |
| Anthropic, Claude Code docs | Stopping, Code Review | All rights reserved: short quotes, our own words |
| GitHub Docs and changelog | Copilot | Docs CC BY 4.0; changelog not stated: short quotes |
| Google eng-practices; Kleppmann's blog | Disagreement; fencing | CC BY 3.0: quoted, attributed |
| Git docs | Push | GPL-2.0: short quotes |
| Pact, oasdiff docs | Contracts | Not stated: short quotes, our own words |
