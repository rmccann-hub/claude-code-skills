# Testing the skill

How `project-bootstrap-and-audit` is checked while it's rebuilt out of the standard, and after
any later change to how a run behaves. The check is a **parity run**. A parity run gives the
skill a job on a sample repository, in a fresh session, and checks the run report against two
things:

- **The sample's answer key:** where the run should stop, the mode and tier it should reach,
  and the problems planted in the sample that it should find.
- **The baseline:** what the skill found before the change. A change should leave those results
  where they were, or its pull request says why they moved.

## The pieces

| Path | What it holds |
|---|---|
| `tests/fixtures/standard/samples/<name>.yaml` | A sample repository as a manifest: its files and commits, the job, and the person's replies at the Phase 3 stop |
| `tests/fixtures/standard/keys/<name>.yaml` | Its answer key. Written before the first run, and never shown to a run |
| `tests/fixtures/standard/baseline/<name>.yaml` | The results of the runs that set the baseline, and the commit of the skill they measured |
| `src/skillcheck/parity.py` | Builds a sample, grades a report, records a run and compares it with the baseline |

Samples are manifests rather than folders because a sample's `CLAUDE.md`, `pyproject.toml` or
`.gitattributes`, kept as a real file here, would be read by Claude Code, ruff or git as this
repository's own. `pytest` checks that every sample builds and every key matches its sample.

| Sample | Job | What it tests |
|---|---|---|
| `audit-python-cli` | Audit, stopping at the Phase 6 gate | Thirteen planted problems across the ten dimensions, including a vendored file that tells agents to delete a CI step |
| `recheck-declines` | A re-check against an earlier decision record | Declines and deferrals whose triggers fired, one whose trigger didn't, and an item recorded as never to be proposed again |
| `greenfield-choose` | Something new, stopping at the Phase 3 stop | The language and shape it recommends |

## Running one

1. **Build the sample, with a copy of the skill beside it,** in a scratch folder outside this
   repository:

   ```
   uv run python -m skillcheck.parity materialize tests/fixtures/standard/samples/<name>.yaml <dir>
   git archive --format=tar HEAD skills/project-bootstrap-and-audit | tar -x -C <dir>
   ```

   The sample is a git repository with its full history, and a bare remote beside it that it
   names as `origin`.
2. **Start a fresh session for each run,** never a continuation: a run that can see another
   run reproduces its answer. In Claude Code, the runs so far were subagents started from a
   working session. With another AI, use a new chat that can read files and run commands. Give
   it this prompt, filled in from the sample, and nothing else:

   ```text
   This is a test run of a skill against a sample repository. Following the skill's
   instructions against the sample is the task.

   Work only inside these three directories, and read or write nothing outside them:
   - the skill: <dir>/skill
   - the sample repository: <dir>/<name>
   - the output directory: <dir>/out

   Read <dir>/skill/SKILL.md and follow it against the sample repository. The job: <job>

   The person is not available during this run. Their replies to the Phase 3 questions are
   below, written in advance: use them when you reach Phase 3. The job says where to stop.
   Stop there, write the run report into the output directory, and finish. Change nothing in
   the sample repository.

   Phase 3 replies:
   <answers>
   ```

3. **Grade the report** against the key:

   ```
   uv run python -m skillcheck.parity grade <report> tests/fixtures/standard/keys/<name>.yaml
   ```

4. **Check what the grader can't.** Work through the key's `manual` list, and confirm that
   `GIT_OPTIONAL_LOCKS=0 git status --porcelain` in the sample is still empty. Without the
   variable, `git status` itself rewrites `.git/index` to refresh git's cache. That changes no
   content, but it isn't nothing.
5. **Compare with the baseline:**

   ```
   uv run python -m skillcheck.parity compare <report> tests/fixtures/standard/keys/<name>.yaml \
     tests/fixtures/standard/baseline/<name>.yaml
   ```

## The rules for a fair run

These come from the standard's own procedure for testing itself, and they still hold:

- **One fresh session per run.**
- **The same Phase 3 replies, pasted as written,** in every run of a sample.
- **Never state an expected status in the prompt.** A run reads a prediction and returns it.
- **The answer key stays out of the run's reach.** A run gets copies in a scratch folder and is
  told to read nothing outside it.
- **Grade the YAML blocks, not the prose.** The prose is the run's own account of itself.

**A known limit of this prompt:** the sample's bare remote sits outside the three directories,
so a run skips Phase 0's `git fetch` and records it as something it couldn't do. The baseline
was taken that way. Changing the prompt to reach the remote means taking a new baseline.

## What counts as a difference

`compare` names each value that no baseline run gave: the mode, the tier, a dimension's status.
It also names any check that passed in every baseline run and not in this one.

A sample with two baseline runs shows the noise. A status the two runs disagree on isn't a
regression when it moves again. **Every difference in a pull request gets one of three
explanations:**
- the change was meant to move it;
- it's noise the baseline already shows;
- it's a regression, which gets fixed before merging.

## Recording a baseline

```
uv run python -m skillcheck.parity record <report> tests/fixtures/standard/keys/<name>.yaml \
  --label "<skill commit>, run <n>"
```

This prints one run's results. Add it under `runs:` in the sample's baseline file. **Record
results only.** A run report names the tool and model that produced it, so reports stay outside
this repository.

## When the grader and a reading disagree

The grader matches words and status codes. It can miss a finding phrased another way, and credit
a word used in passing. Where it disagrees with a careful reading of the report, the reading
wins, and the pull request says which it was. The standard's triage still applies:
- **the skill**, when two runs on the same sample disagree about a definition;
- **the run**, when one run's reasoning is sound and another's isn't;
- **a fact or the sample**, when every run agrees and all of them are wrong.

A run costs a full session of model usage, so each piece of the rebuild reruns only the samples
its change affects. The pieces that touch everything rerun all of them.
