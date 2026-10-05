> **About this file.** This is the kickstart file from release RELEASE_VERSION of
> REPOSITORY. It holds standard vSTANDARD_VERSION, whose full file has this SHA-256:
> `STANDARD_SHA256`
>
> The two sections no run reads are left out: *Validating a Change to This Standard* and
> *Provenance*. The standard's text is otherwise unchanged. Around it, this file adds its first
> lines, these run instructions, the frontmatter's `extract` and `run_file` lines, and the end
> marker. The routing table and a few sentences still name the two sections; a job that needs
> them needs the full file, from the same release.

**Run instructions.** They say which job to run and what holds throughout. The standard below
governs everything else.

**The job, chosen by what the repository holds.** If the person's message names a job, that job
wins. Otherwise:

- **No repository yet, or one that holds no source:** choose a language and a shape with the
  person, by the routing table's row for that job. Ask what the project is for, who runs it,
  where it runs and what it keeps, then recommend a language and a shape, each with a runner-up
  and what each choice costs. Stop at the Phase 3 wait. Nothing is chosen by default. Once the
  person picks, set the repository up by the row for setting up something new, and stop at the
  Phase 6 gate.
- **A repository with source, whose decision record has no entry from an earlier run of this
  standard:** audit it, through every phase, and stop at the Phase 6 gate.
- **A repository whose decision record has such an entry:** re-check it, as Phase 1 directs.
  Show each recorded answer and ask whether it still holds.

**What holds throughout.**

- Use no other copy of this standard. A copy installed as a plugin or synced from an account may
  be another version. Record this file's SHA-256, as received, in the self-check's
  `standard_sha256`, because an upload may rename it. If the last line isn't the end marker, the
  file arrived cut short: stop and say so.
- Write nothing to the repository and push nothing until the person has answered the Phase 6
  gate: no branch, commit, tag, release or setting.
- Keep the run report outside the repository, in the session's scratch space. At each stop, send
  it as a file and give its path.
- At the Phase 3 wait, draft each answer the repository supports, with its evidence, for the
  person to confirm. Production, dependents and where it runs are never drafted, so ask them
  outright.
- Write for readers other than the person running this. Everything proposed for the repository,
  from documentation and the decision record to commit messages and the pull request, is
  neutral and exact, with no personal or session detail and no shorthand a reader can't look up.
- After the gate, apply only what the person approved, on a branch, and open a pull request for
  it. Don't merge it or cut a release unless the person asks.
