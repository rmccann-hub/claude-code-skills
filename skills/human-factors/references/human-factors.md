# Human factors

Read this before a design, an automation or an optimization removes or changes a step people
take: what a habit, workaround, double check or familiar tool is for, purpose versus bias or
drift, the dip after a tool change, taking over from automation, and this reasoning's limits.

People in plans, such as fatigue, shift design and utilization, are the
`optimization-and-scheduling` skill's. Interfaces are the `user-experience` skill's. Checking a
fact or result is the `test-oracles` module of the `testing` skill.

## Rules

1. **Find what a step is for before you remove or automate it.** Watch the work as done, not
   as written (fact `hf-work-as-done`), and ask the people who do it (fact `hf-hse-consult`).
2. **Test each habit: purpose, bias or drift.** Familiarity alone justifies nothing (fact
   `hf-hse-familiar-rules`). Say which it is, on what evidence.
3. **Decide keep, change gradually or override,** and say why.
4. **Budget for a dip of months after a tool change,** and don't promise recovery (facts
   `hf-mcafee-dip`, `hf-ems911`).
5. **Automate so people can still take over,** and trust it as far as it deserves (facts
   `hf-bainbridge`, `hf-misuse-disuse`).
6. **Human factors never alter a fact.** Findings, measurements and quotes stay as found. Mark
   each output **Evidence** or **Recommendation**.
7. **Give each claim's strength and reach:** field study, experiment, case, guidance or
   opinion, and on whom.

### Before removing a step

Ask, and record the answers (our synthesis of HSE's and Hollnagel's guidance):

- What failure or delay did it last catch? Its doers "will have insights", in HSE's words.
- Is it a routine, situational or exceptional departure from the procedure (fact
  `hf-hse-violations`)? The first two usually point at a gap in the design.
- Does it keep alive a skill needed when the automation fails?
- Does it answer an unreliable system, such as false alarms? Fix that first.
- Has the margin it protects been shrinking? Then look for drift.

Observe the step as performed, when it's skipped and what follows, and whether accounts agree.

### Purpose, bias or drift

| Counter-case | How it shows | Test |
|---|---|---|
| Status quo bias (fact `hf-status-quo`) | The current option chosen for being current | Would they choose it fresh? Transition cost is real |
| Familiar-rule mistake (fact `hf-hse-familiar-rules`) | HSE's case: an operator ignored high-level alarms, sure the tank couldn't fill so fast, after its pipe was enlarged | What changed since the rule was learned? |
| Normalization of deviance (fact `hf-vaughan`) | Each anomaly relabeled acceptable | Has the tolerance widened without new evidence? |

### Keep, change gradually or override

- **Keep** a habit that catches failures the new design doesn't, or keeps a take-over skill.
- **Change gradually** a workaround for a real constraint: the constraint first, then the
  workaround, with the dip budgeted.
- **Override** drift, a familiar-rule mistake or a safety violation: HSE holds that departing
  from established health and safety standards is not acceptable.

### Automation

- **Keep the take-over skill.** Physical skills fade unused (fact `hf-bainbridge`): Bainbridge
  suggests hands-on control for a short period each shift, or simulator practice.
- **Calibrate trust.** Misuse is over-reliance, disuse is neglect after false alarms (fact
  `hf-misuse-disuse`), and abuse, in the same paper, automating without regard for the people
  left. Show how reliable the automation is.

### The limit for AI agents

Language models drift toward the user's view (facts `hf-sharma`, `hf-wei`, `hf-gpt4o`), and
reasoning about habits adds a pull. So:

- Facts, measurements, a standard's status and quotes are **Evidence**, with their source. No
  habit or preference changes one.
- Preferences count in **Recommendations**: design choices, trade-offs among valid options,
  taste. Each names the human factors it weighed.
- Load this skill for design, automation and optimization, never for research or retrieval.

### Habits by purpose

Our synthesis; the facts named are the sources.

| Habit | For | Stops serving when | Facts |
|---|---|---|---|
| Keeping a familiar, slower tool | Avoiding a dip of months; keeping skill | The new tool is proven, people trained, the dip budgeted | `hf-mcafee-dip`, `hf-ems911` |
| A second person rechecks | Catching slips the doer can't see | It's a rubber stamp | `hf-hse-checks` |
| A partly done checklist left out | Preventing lapses after interruptions | It's filled in from memory | `hf-hse-checks` |
| Routine or situational rule-bending | Doing the job under real constraints | It becomes normalized deviance | `hf-hse-violations` |
| Adjusting work to conditions | What the procedure didn't foresee | It masks a design flaw | `hf-work-as-done` |
| Manual practice beside automation | Take-over skill | Take-over is never needed | `hf-bainbridge` |
| Ignoring an unreliable alarm | Escaping false alarms | The system is now reliable | `hf-misuse-disuse` |
| Sticking with the default | Saving decision and transition cost | The default no longer fits | `hf-status-quo` |
| Slow change, people consulted | Trust; finding hidden purposes | None found | `hf-hse-consult` |

## Mistakes

- **Removing a step the written procedure lacks,** unwatched. Watch the work first.
- **Quoting "don't take a fence down until you know why it was put up" as Chesterton's.** It's
  a short form Kennedy recorded (fact `hf-fence`).
- **Booking a new tool's benefits from go-live day.** Budget months; plan for no recovery.
- **Citing a vendor's weeks-to-proficiency claim as research,** or the productivity J-curve for
  a team's dip: it models mismeasured investment across an economy.
- **"A habit takes 66 days."** That's a median; individuals ranged widely (fact `hf-lally`).
- **Presenting Safety-II as measured.** It's a position (fact `hf-safety-ii-critique`).
- **An agent taking the person's framing while gathering facts,** or softening a finding because
  a habit is at stake. Report it as found; the human factors go in a Recommendation.
- **Calling Western-sample results universal** (fact `hf-weird`).

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Step removed unexplained | A step dropped with no record of its purpose | `GAP` | Observe, ask, record |
| People not consulted | A change to what people do, without them | `GAP` | Consult before the design is fixed |
| No dip budgeted | Full benefit from go-live | `GAP` | Budget months, with a fallback |
| No take-over path | Automation with no practice or fallback | `GAP`; `BLOCKER` where failure is unsafe | Practice time or a simulator |
| Drift kept as habit | A tolerance widened over time, defended as "how we work" | `BLOCKER` where safety is at stake; else `GAP` | Override; restore the margin |
| A fact bent by preference | A finding, measurement or quote changed to suit a view | `BLOCKER` | Restore it; the view goes in a Recommendation |
| Unlabeled output | Evidence and recommendations mixed | `DRIFT` | Label each |
| Evidence overstated | Safety-II, 66 days, vendor figures or Western samples as settled | `DRIFT` | Give strength and reach |
| Loaded for fact-finding | This skill read for research or retrieval | `OVER` | Leave it out |

## Why

### Finding the purpose first

- **The reason:** HSE finds most rule-breaking is to get the job done (fact
  `hf-hse-violations`), and consulted change is accepted more readily (fact `hf-hse-consult`).
  A design built on work as imagined removes what work as done relies on (fact
  `hf-work-as-done`).
- **What it costs:** days of watching and asking. **Choose differently** for a safety
  violation: override it, and fix what drove it.

### Purpose, bias or drift

- **The reason:** the HSE guidance that defends workers' views also documents familiar rules
  causing errors (fact `hf-hse-familiar-rules`). Status quo bias is measured, with economic
  explanations (fact `hf-status-quo`). A habit can be risk accepted a step at a time (fact
  `hf-vaughan`).
- **What it costs:** time per habit; keeping all keeps errors, removing all loses safeguards.

### The dip

- **The reason:** in one firm, lead time and on-time delivery fell at go-live and beat the old
  levels after several months (fact `hf-mcafee-dip`). Another case never got back (fact
  `hf-ems911`), though its authors judged the benefits worth the long decrease.
- **Choose differently** for a small change with little to learn, or a failing old tool.

### Automation and facts

- **Automation:** the skills it lets fade are the ones a take-over needs (fact
  `hf-bainbridge`), and trust follows reliability badly both ways (fact `hf-misuse-disuse`).
  **Cost:** practice time, or a simulator.
- **Facts:** five assistants were consistently sycophantic (fact `hf-sharma`), models agreed
  with statements they knew were wrong when the user did (fact `hf-wei`), and a production
  update was rolled back for it (fact `hf-gpt4o`). **Cost:** labeling every output, and
  findings a person may dislike.
- **Reach:** most psychology samples come from a small share of the world (fact `hf-weird`),
  so universality is unproven; Safety-II is contested (fact `hf-safety-ii-critique`).

## Facts

Each named elsewhere in this module by its ID. HSE quotes contain public sector information
published by the Health and Safety Executive and licensed under the Open Government Licence.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `hf-hse-violations` | Most rule-breaking is to do the job; three kinds | [HSG48](https://books.hse.gov.uk/gempdf/hsg48.pdf) | "Most violations are motivated by a desire to carry out the job despite the prevailing constraints, goals and expectations." and "Violations are divided into three categories: routine, situational and exceptional." | 2026-11-11 | 2027-05-11 |
| `hf-hse-familiar-rules` | Familiar rules cause mistakes | [HSG48](https://books.hse.gov.uk/gempdf/hsg48.pdf) | "We have a strong tendency to use familiar rules or solutions even when these are not the most convenient or efficient." | 2026-11-11 | 2027-05-11 |
| `hf-hse-consult` | Consulted change is accepted | [HSG48](https://books.hse.gov.uk/gempdf/hsg48.pdf) | "This will usually lead to any changes being introduced more easily and accepted more readily." | 2026-11-11 | 2027-05-11 |
| `hf-hse-checks` | Independent checks; reminders | [HSG48](https://books.hse.gov.uk/gempdf/hsg48.pdf) | "ensuring proper supervision particularly for inexperienced staff, or for tasks where there is a need for independent checking" and "A useful reminder could be as simple as a partially completed checklist" | 2026-11-11 | 2027-05-11 |
| `hf-work-as-done` | Work as done | [Hollnagel et al., 2015](https://www.england.nhs.uk/signuptosafety/wp-content/uploads/sites/16/2015/10/safety-1-safety-2-whte-papr.pdf) | "Work-As-Done, on the other hand, describes what actually happens, how work unfolds over time in complex contexts." | 2026-11-11 | 2027-05-11 |
| `hf-safety-ii-critique` | Safety-II questioned | [Smith and Valenta, 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6037502/) | "Or, alternatively, is Safety II yet another case of “work as imagined”?" | 2026-11-11 | 2027-05-11 |
| `hf-mcafee-dip` | A dip, then recovery after months, one firm | [McAfee, 2002](https://journals.sagepub.com/doi/10.1111/j.1937-5956.2002.tb00183.x) | "Immediately after adoption, lead time and on‐time delivery performance suffered" and "After several months, performance in these areas improved significantly relative to preadoption levels." | 2026-11-11 | 2027-05-11 |
| `hf-ems911` | A case that never recovered | [McLeod et al., 2008](https://aisel.aisnet.org/cgi/viewcontent.cgi?article=3361&context=cais) | "In the case of EMS911, operational performance in the post-implementation period never approached that observed in the pre-implementation period." | 2026-11-11 | 2027-05-11 |
| `hf-bainbridge` | Unused skills fade | [Bainbridge, 1983](https://ckrybus.com/static/papers/Bainbridge_1983_Automatica.pdf) | "physical skills deteriorate when they are not used" | 2026-11-11 | 2027-05-11 |
| `hf-misuse-disuse` | Misuse and disuse | [Parasuraman and Riley, 1997](https://journals.sagepub.com/doi/10.1518/001872097778543886) | "Misuse refers to over reliance on automation, which can result in failures of monitoring or decision biases." and "Disuse, or the neglect or underutilization of automation, is commonly caused by alarms that activate falsely." | 2026-11-11 | 2027-05-11 |
| `hf-status-quo` | Status quo bias, with explanations | [Samuelson and Zeckhauser, 1988](https://link.springer.com/article/10.1007/BF00055564) | "A series of decision-making experiments shows that individuals disproportionately stick with the status quo." and "Economics, psychology, and decision theory provide possible explanations for this bias." | 2026-11-11 | 2027-05-11 |
| `hf-vaughan` | Risk redefined as acceptable: the book, third-hand | [UChicago Press blog](https://pressblog.uchicago.edu/2016/01/07/the-normalization-of-deviance.html) | "in which the technical deviation of the [O‑rings] from performance predictions was redefined as an acceptable risk." | 2026-11-11 | 2027-05-11 |
| `hf-lally` | 66 days is a median, over a wide range | [Lally et al.](https://repositorio.ispa.pt/server/api/core/bitstreams/370f1dca-cc04-4d3d-a0f0-36d16109ec37/content) | "The median time to reach 95% of asymptote was 66 days, with a range from 18 to 254 days." | 2026-11-11 | 2027-05-11 |
| `hf-weird` | Narrow samples | [Henrich et al.](https://www.konsortswd.de/wp-content/uploads/RatSWD_WP_139.pdf) | "96% of psychological samples come from countries with only 12% of the world’s population." | 2026-11-11 | 2027-05-11 |
| `hf-sharma` | Assistants are sycophantic | [Sharma et al.](https://arxiv.org/abs/2310.13548) | "five state-of-the-art AI assistants consistently exhibit sycophancy across four varied free-form text-generation tasks" | 2026-11-11 | 2027-05-11 |
| `hf-wei` | Models agree with known errors | [Wei et al.](https://arxiv.org/abs/2308.03958) | "despite knowing that these statements are wrong, language models will still agree with them if the user does as well" | 2026-11-11 | 2027-05-11 |
| `hf-gpt4o` | An update rolled back, 2025-04-29 | [OpenAI](https://openai.com/index/sycophancy-in-gpt-4o/) | "As a result, GPT‑4o skewed towards responses that were overly supportive but disingenuous." | 2026-11-11 | 2027-05-11 |
| `hf-fence` | The fence's short form, recorded by Kennedy | [Taking a fence down](https://www.chesterton.org/taking-a-fence-down/) | "was ascribed to Chesterton by John F. Kennedy in a 1945 notebook" | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| HSE, HSG48 | Rule-breaking, familiar rules, consulting, checks | Open Government Licence v3.0: quoted and adapted, attributed above |
| Hollnagel, Wears and Braithwaite | Work as done | No changes allowed: brief quotes, our own words |
| Smith and Valenta; Sharma et al.; Wei et al. | Safety-II critique; sycophancy | CC BY 4.0: quoted, attributed |
| McAfee; McLeod et al.; Bainbridge; Parasuraman and Riley; Samuelson and Zeckhauser; Lally et al.; Henrich et al.; UChicago Press; OpenAI; American Chesterton Society | Their facts | Copyright: brief quotes, our own words |
