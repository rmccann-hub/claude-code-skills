# Studying work

Read this for finding out what a step in people's work is for before a change removes it:
watching the work as done, interviewing people at their work, breaking a task into goals and
plans, how deep to go, why asking alone misses purposes, a check that caught nothing while you
watched, and the decision traps that bend what a study finds.

What to do with a purpose once found is the `human-factors` module's: purpose, bias or drift;
keep, change gradually or override; the dip after a tool change; automation. Interfaces are the
`user-experience` skill's. Checking a result against its source is the `testing` skill's.
Cognitive task analysis is left out: the research found no primary source for it.

## Rules

1. **Watch the work and ask about it together, where it's done.** People know more than they
   can tell (fact `sw-polanyi`), and their work practice is tacit (fact `sw-ci-tacit`), so an
   interview in a meeting room or a survey under-reports purposes.
2. **Start from goals, not activities.** Name the goal each step serves (fact `sw-hta-pxc`) and
   what decides when it happens. A step whose goal nobody can name is the one to watch.
3. **Stop breaking a step down when failing at it is unlikely or cheap,** by the p × c rule (fact
   `sw-hta-pxc`).
4. **For a small team: goals at a desk first, then a few visits aimed at what they can't
   explain.** This order is our reasoning, not a sourced finding.
5. **Don't judge a check by the visits where it caught nothing.** Defenses fail when their holes
   line up, and the holes move (fact `sw-reason-holes`). Ask when it last caught something.
6. **Read a step as good enough for something, not as a failure to optimize.** People choose
   what satisfies under their limits (facts `sw-simon-satisfice`, `sw-bounded-rationality`).
   Ask what it's good enough for.
7. **Study before the design is fixed, and write down first what would change it.** Money and
   effort already spent make a team continue (fact `sw-sunk-cost`).
8. **Label each purpose by its evidence:** seen, told or inferred, and by whom.

### Contextual inquiry

Beyer and Holtzblatt's field interview, one step of their Contextual Design process:

- **Where:** one person at a time, at their workplace, while the work happens. Ask about each
  step as it unfolds: what they're doing, and why now.
- **Stance:** the interviewer is the apprentice and the person the master (fact `sw-ci-stance`).
  No list of questions; follow the work.
- **What it gives:** interpretation notes and five work models (fact `sw-ci-models`). The
  sequence model records the intents behind each step, which is this module's question. The
  cultural model shows how people work around constraints.
- **Cost:** each visit, then a team session to interpret it. The research found no measured
  figure in hours.

### Hierarchical task analysis

Annett and Duncan's method, from Hull, built to decide what training a job needs (fact
`sw-hta-training`):

- Start with the task's goal and break it into subgoals: a goal hierarchy (fact `sw-hta-pxc`).
  We also record, for each, a plan: when and in what order its parts happen.
- At each subgoal, weigh p, the chance it's done wrong, against c, the cost to the whole task
  if it is. Stop when the product is low.
- **What it gives:** a goal hierarchy with plans. A step that serves no goal in it is either
  missing a goal you haven't found or a candidate for removal: watch it before deciding.
- **Its limit here:** its stopping rule is about training, so a step can pass p × c and still
  hold a purpose. Use it to aim visits, not to settle a purpose.

### A small team's order of work

Our reasoning from the sources above:

1. Draft the goal hierarchy at a desk from the written procedure, logs and the system.
2. Check it with one or two people who do the work.
3. Make two to four contextual visits aimed at the steps whose goal the hierarchy can't explain
   and the checks that rarely fire.
4. Record each step: its goal, the evidence (seen, told or inferred), what fails without it, and
   who said so. The `human-factors` module takes each step from there.

### A check that caught nothing

A week of visits samples ordinary days. A check that guards against a rare failure looks idle
in it. Ask the people who do it when it last caught something, read incident and defect records,
and ask what changed since. Reason's line applies to what you find: "We cannot change the human
condition, but we can change the conditions under which humans work" (fact
`sw-reason-conditions`). A step that compensates for a condition is a pointer to the condition.

## Mistakes

- **Asking in a meeting room and calling it a study.** People describe the procedure, not the
  work. Go to the work, while it happens.
- **Taking the written procedure as the task.** Build the hierarchy from goals, and check it
  against work as done (fact `hf-work-as-done`).
- **Breaking every step down to the keystroke.** Stop where p × c is low.
- **Dropping a check because it caught nothing while you watched.** Ask when it last fired, and
  read the records.
- **Calling a step irrational because a better option exists.** It may be good enough for a
  goal you haven't found.
- **Studying after the design is built.** The team then discounts what the study finds.
- **Reporting what people said as what you saw.** Label each.
- **Writing Polanyi as "we know more than we can tell".** He wrote "we can know" (fact
  `sw-polanyi`). AI assistants also invent page numbers; give one only with its source.
- **Dating "bounded rationality" to 1955.** The idea is 1955, the word "satisfice" 1956, the
  term 1957 (facts `sw-simon-dates`, `sw-bounded-rationality`).
- **Citing Weigel 2018 as proof that sunk cost isn't real.** His own experiment finds the effect
  (fact `sw-sunk-cost-economics`).

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Purpose unstudied | A step removed with only the procedure or a meeting as evidence | `GAP` | Visit and watch it |
| Asked, not watched | Only interviews away from the work, or a survey | `GAP` | Add visits to the work |
| No goal named | A step in the design record with no goal | `GAP` | Name the goal, or watch the step |
| Idle check judged by a short visit | "Caught nothing while we watched" as the reason to drop it | `GAP` | Ask when it last fired; read the records |
| Evidence unlabeled | Seen, told and inferred mixed | `DRIFT` | Label each purpose |
| Study after build | Findings due after the design is fixed | `GAP` | Study first; list what would change the plan |
| Over-decomposed | Detailed analysis of steps unlikely or cheap to fail | `OVER` | Stop by p × c |
| Misquoted or misdated source | Polanyi, Simon's dates, Weigel as above | `DRIFT` | Quote and date from the facts |

## Why

### Watching as well as asking

- **The reason:** Polanyi's point (fact `sw-polanyi`), and Contextual Design's: people become
  aware of their practice only in context (fact `sw-ci-tacit`). A step's purpose often lives in
  what they do when something goes wrong, which they don't think to mention.
- **What others do:** surveys and focus groups ask at a distance; they're cheaper and reach more
  people, and miss the tacit part.
- **What it costs:** visits, and the people's time. **Choose differently** when the step's
  purpose is written down with its evidence, such as a regulation or an incident report.

### Goals first, and where to stop

- **The reason:** a list of activities can't say why one is there; a goal hierarchy can.
  Annett's p × c rule keeps the analysis from growing to every movement (fact `sw-hta-pxc`).
- **What others do:** HTA was built for training (fact `sw-hta-training`). Contextual inquiry
  starts from the work, not from goals.
- **What it costs:** a skill: it takes practice to break goals down well. **Choose
  differently** for one step in a short task: watch it, no hierarchy needed.

### The small team's order

- **The reason:** the desk is cheap, and visits are dear. Goals drafted first aim the visits at
  what the desk can't explain, and Polanyi's point is why the visits are still needed.
- **What it costs:** a draft may bias what you look for. Go to each visit ready to be wrong.
- **Choose differently** with a research team and weeks: full Contextual Design.

### A check that caught nothing

- **The reason:** in Reason's model, harm needs the holes in many layers to line up, and they
  open, shut and move (fact `sw-reason-holes`). A layer that stopped nothing this week may stop
  the next line-up.
- **What it costs:** reading records and asking. **Choose differently** when the records show
  the failure it guards against can no longer happen.

### Good enough, and spent effort

- **Satisficing:** in Simon's account, people choose what is good enough, not the best
  (facts `sw-simon-satisfice`, `sw-bounded-rationality`, `sw-simon-dates`). A step that looks
  wasteful may be the cheapest one that works for its doers. So may the study: stopping at the
  first plausible purpose is satisficing too.
- **Sunk cost:** Arkes and Blumer found it in experiments and in a field study, theatre
  subscribers who paid more attending more plays (fact `sw-sunk-cost`). Weigel's incentivized
  experiment finds it too, while noting that economics has doubted it (fact
  `sw-sunk-cost-economics`). Separately, the classic vignettes measure it with low reliability
  (fact `sw-sunk-cost-vignettes`). So treat it as a real risk of unknown size: writing down
  before the build what would change the plan costs little.

## Facts

Each named elsewhere in this module by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `sw-polanyi` | Polanyi, *The Tacit Dimension*, 1966, p. 4 (page per Pimm 2009) | [University of Chicago Press](https://press.uchicago.edu/ucp/books/book/chicago/T/bo6035368.html) | "I shall reconsider human knowledge by starting from the fact that we can know more than we can tell" | 2026-11-11 | 2027-05-11 |
| `sw-ci-tacit` | Work practice is tacit | [Holtzblatt and Beyer, IxDF ch. 8](https://ixdf.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed/contextual-design) | "people are not consciously aware of their own work practice; all of their knowledge is tacit." | 2026-11-11 | 2027-05-11 |
| `sw-ci-stance` | Contextual inquiry's stance | [Holtzblatt and Beyer, IxDF ch. 8](https://ixdf.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed/contextual-design) | "but rather adopts a master-apprentice relationship model" | 2026-11-11 | 2027-05-11 |
| `sw-ci-models` | Five work models; the sequence model shows intents | [Holtzblatt and Beyer, IxDF ch. 8](https://ixdf.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed/contextual-design) | "Five different models provide five perspectives on how work is done" and "the intents or goals that their task steps are trying to accomplish" | 2026-11-11 | 2027-05-11 |
| `sw-hta-training` | Annett and Duncan 1967, Hull: task analysis for training | [ERIC ED019566](https://eric.ed.gov/?id=ED019566) | "TO ESTIMATE THE COST OF INADEQUATE PERFORMANCE TO A SYSTEM AND THE PROBABILITY OF ADEQUATE PERFORMANCE WITHOUT TRAINING" | 2026-11-11 | 2027-05-11 |
| `sw-hta-pxc` | HTA builds a goal hierarchy and stops by p × c, in Annett's words | [Annett, reflection, 2014](https://hciengineering.net/reflections-on-task-analysis-psychological-sciences-and-clinical-psychology-by-john-annett/) | "the process of analysis is to determine a goal hierarchy" and "When this criterion is reached then no further analysis (or decomposition of the goal hierarchy) is worthwhile." | 2026-11-11 | 2027-05-11 |
| `sw-simon-satisfice` | The word "satisfice", Simon 1956 | [Simon, *Psychological Review* 63(2)](https://pages.ucsd.edu/~mckenzie/Simon1956PsychReview.pdf) | "Evidently, organisms adapt well enough to "satisfice"; they do not, in general, "optimize."" | 2026-11-11 | 2027-05-11 |
| `sw-bounded-rationality` | The term, Simon 1957 | [SEP, Bounded Rationality](https://plato.stanford.edu/entries/bounded-rationality/) | "Herbert Simon introduced the term ‘bounded rationality’ (Simon 1957b: 198; see also Klaes & Sent 2005)" | 2026-11-11 | 2027-05-11 |
| `sw-simon-dates` | The idea 1955, the word 1956, the term 1957 | [Barros, 2010](https://www.scielo.br/j/rep/a/CWfwPPVWKvLrndfxR9vYFHL/?format=html&lang=en) | "The idea of choice of satisfactory alternatives emerges in Simon (1955), the term "satisficing" associated with search for alternatives appears fully developed in Simon (1956)" | 2026-11-11 | 2027-05-11 |
| `sw-reason-holes` | Reason's holes move, BMJ 2000 | [Reason, BMJ 2000](https://pmc.ncbi.nlm.nih.gov/articles/PMC1117770/) | "these holes are continually opening, shutting, and shifting their location." and "this can happen only when the holes in many layers momentarily line up to permit a trajectory of accident opportunity" | 2026-11-11 | 2027-05-11 |
| `sw-reason-conditions` | Change the conditions, not the people | [Reason, BMJ 2000](https://pmc.ncbi.nlm.nih.gov/articles/PMC1117770/) | "We cannot change the human condition, but we can change the conditions under which humans work" | 2026-11-11 | 2027-05-11 |
| `sw-sunk-cost` | Sunk cost effect, Arkes and Blumer 1985, with a field study | [OBHDP 35(1)](https://www.sciencedirect.com/science/article/pii/0749597885900494) | "The sunk cost effect is manifested in a greater tendency to continue an endeavor once an investment in money, effort, or time has been made." and "customers who had initially paid more for a season subscription to a theater series attended more plays during the next 6 months" | 2026-11-11 | 2027-05-11 |
| `sw-sunk-cost-economics` | Weigel 2018 finds the effect; economics has doubted it | [Weigel, SSRN 3207806](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3207806) | "Though widely accepted in psychology, the Sunk Cost Effect (SCE) finds little support from recent evidence in economics." and "sunk costs increase one’s willingness to continue along an unprofitable course of action by 21.9%" | 2026-11-11 | 2027-05-11 |
| `sw-sunk-cost-vignettes` | Classic vignettes measure it with low reliability, 2025 | [*Brain Sciences*, PMC12384923](https://pmc.ncbi.nlm.nih.gov/articles/PMC12384923/) | "Across two experiments (N = 395), we examined the reliability and validity of established sunk cost scenarios." | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| Polanyi, *The Tacit Dimension* (University of Chicago Press page) | Tacit knowledge | Copyright: a short quote, our own words |
| Holtzblatt and Beyer, IxDF *Encyclopedia of HCI* ch. 8 | Contextual inquiry | No license seen: short quotes, our own words |
| Annett and Duncan, ERIC record; Annett's reflection on hciengineering.net | HTA | Not stated: short quotes, our own words |
| Simon 1956; SEP; Barros 2010 | Satisficing and its dates | Copyright: short quotes, our own words |
| Reason, BMJ 2000 | Moving holes; conditions | Copyright BMJ: short quotes, our own words |
| Arkes and Blumer 1985; Weigel 2018 | Sunk cost | Copyright: short quotes, our own words |
| *Brain Sciences* 2025 | Vignette reliability | CC BY 4.0: quoted, attributed |
