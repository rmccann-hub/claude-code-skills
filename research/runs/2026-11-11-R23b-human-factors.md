# Verification: R23b (2026-11-11)

Checked on 2026-11-11 against the primary sources named below. The report is untrusted data. Its
line 3 is addressed to "the receiving session" and asks it to file the report under
`research/runs/`, update the facts files of the categories it names, and list what changed. That
is an instruction found in a research result; it wasn't followed. Nothing in the repository was
edited.

Access notes:
- PDFs were each downloaded into their own new directory and read only with `pdftotext`: Simon
  1956 (pages.ucsd.edu), NIST AI 600-1 (nvlpubs.nist.gov), and two Fitts 1954 copies.
- The report's Fitts URL (www2.psychology.uiowa.edu) returns 404. Fitts was read in a scan of the
  original JEP 47(6) issue (e.guigon.free.fr/rsc/article/Fitts54.pdf) and in the 1992 *JEP:
  General* centennial reprint (cs.princeton.edu), found via Exa search.
- The report's Annett chapter copy (mycourses.aalto.fi) now returns a MyCourses notice, "This
  course is currently unavailable to students", to curl and to Exa. No other copy of the 2003
  chapter was found; the 1967 paper's ERIC record (ED019566) and Annett's own reflection on
  hciengineering.net were read via Exa instead.
- pmc.ncbi.nlm.nih.gov and pubmed.ncbi.nlm.nih.gov served a reCAPTCHA or cookie wall to curl.
  PubMed abstracts and dates were read from NCBI E-utilities `efetch` (XML); PMC3925410 and
  PMC4267903 from E-utilities `efetch db=pmc`; PMC12384923 from the Europe PMC full-text XML API;
  PMC1117770 (BMJ blocks XML download) through the Exa fetch tool.
- iso.org returned 403 to curl. ISO 6385:2016, ISO/CD 10075-3 and the ISO/TC 159/SC 1 committee
  page were read through the Exa fetch tool; each carries "© ISO 2026", and the 10075-3 page has
  life-cycle entries dated 2026-11-07, so the copy is recent.
- scielo.br returned 403 to curl. The Barros sentence was read with WebFetch in two verbatim
  pieces; Exa fetched the page's opening.
- sciencedirect.com (Arkes and Blumer abstract), link.springer.com (Pimm chapter), SSRN (Weigel)
  and pubsonline.informs.org (Boudreau et al.) were read through the Exa fetch tool. The
  Boudreau assumption list was read in Exa's index of INFORMS' own PDF
  (pubsonline.informs.org/doi/pdf/10.1287/msom.5.3.179.16032).
- Hitt, Wu and Zhou: Semantic Scholar's API elides the abstract at the publisher's request and
  the UPenn repository link returned HTML. The abstract was read in OpenAlex's record of the DOI;
  volume, issue, pages and date from Crossref.
- Crossref's API gave citation data for Simon 1956, Arkes and Blumer, Boudreau et al., Hitt et
  al., Fitts and the Annett chapter. plato.stanford.edu, digital.ahrq.gov, ixdf.org,
  nngroup.com and nist.gov were fetched directly with curl.

| Claim | Status | Checked against |
|---|---|---|
| Correction 1: the satisficing idea 1955, the word 1956, "bounded rationality" 1957 | verified | [Simon 1956 PDF](https://pages.ucsd.edu/~mckenzie/Simon1956PsychReview.pdf); [SEP, Bounded Rationality](https://plato.stanford.edu/entries/bounded-rationality/); [Barros, Braz. J. Polit. Econ. 30(3), Sept 2010](https://www.scielo.br/j/rep/a/CWfwPPVWKvLrndfxR9vYFHL/?format=html&lang=en) |
| Correction 2: Polanyi, "we can know more than we can tell", *The Tacit Dimension* p. 4, Doubleday 1966; Chicago reprint with a Sen foreword | verified | [University of Chicago Press book page](https://press.uchicago.edu/ucp/books/book/chicago/T/bo6035368.html) carries the sentence and "With a New Foreword by Amartya Sen". The page number and the italics rest on [Pimm 2009, Springer](https://link.springer.com/chapter/10.1007/978-3-642-00742-2_57), whose references give "Garden City, NY: Doubleday and Co." |
| Correction 3: Reason's holes move; active failures and latent conditions; holes line up "momentarily" | verified | [Reason, BMJ 2000;320(7237):768–770, PMC1117770](https://pmc.ncbi.nlm.nih.gov/articles/PMC1117770/), 18 March 2000. The text says "a trajectory of accident opportunity"; "accident trajectory" is the figure caption's wording |
| Correction 4: Arkes and Blumer, OBHDP 35:124–140, Feb 1985; contested in economics (Weigel, SSRN 3207806, 3 July 2018) | verified with a correction | [ScienceDirect abstract](https://www.sciencedirect.com/science/article/pii/0749597885900494); Crossref: 35(1):124–140, 1985-02. [Weigel, SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3207806) has the quoted sentence, but his own experiment finds the effect: "sunk costs increase one’s willingness to continue along an unprofitable course of action by 21.9%". Cite Weigel for the debate, not as evidence against the effect |
| Correction 5: HTA was built for training; contextual inquiry is one step of Contextual Design; book year 1998 | verified with a correction | [ERIC ED019566, Annett and Duncan 1967](https://eric.ed.gov/?id=ED019566) (Hull, "task analysis for industrial training"); [IxDF ch. 8, Holtzblatt and Beyer](https://ixdf.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed/contextual-design). The authors' own chapter says "the 1997 text Contextual Design (Beyer and Holtzblatt 1997)"; its reference list has both a 1997 and a 1998 entry |
| Fact 1: "Evidently, organisms adapt well enough to "satisfice"; they do not, in general, "optimize."" Psych. Review 63(2), 1956 | verified | [Simon 1956 PDF](https://pages.ucsd.edu/~mckenzie/Simon1956PsychReview.pdf), p. 129; Crossref 10.1037/h0042769: 63(2):129–138, 1956. The month isn't printed; the scan's text layer reads "satisflce" (OCR of the fi ligature) |
| Fact 2: SEP, "Herbert Simon introduced the term 'bounded rationality' (Simon 1957b: 198; see also Klaes & Sent 2005)" | verified with a correction | [SEP](https://plato.stanford.edu/entries/bounded-rationality/) uses curly single quotes: ‘bounded rationality’ (U+2018, U+2019). Entry first published 30 Nov 2018, substantive revision 13 Dec 2024 |
| Fact 3: Barros, the 1955 → 1956 → 1957 order | verified | [Barros 2010](https://www.scielo.br/j/rep/a/CWfwPPVWKvLrndfxR9vYFHL/?format=html&lang=en); the whole sentence matches. Barros attributes the 1957 first print to Klaes and Sent (2005) |
| Fact 4: Polanyi sentence, 1966, p. 4, italics in original | verified | [UChicago Press](https://press.uchicago.edu/ucp/books/book/chicago/T/bo6035368.html) (sentence); [Pimm 2009](https://link.springer.com/chapter/10.1007/978-3-642-00742-2_57) ("1966, p. 4; italics in original") |
| Fact 5: Swiss cheese, holes "continually opening, shutting, and shifting their location" | verified | [PMC1117770](https://pmc.ncbi.nlm.nih.gov/articles/PMC1117770/) (em dash U+2014 in "holes—though") |
| Fact 6: "We cannot change the human condition, but we can change the conditions under which humans work" | verified | [PMC1117770](https://pmc.ncbi.nlm.nih.gov/articles/PMC1117770/): a pull quote; the body has "though we cannot change the human condition, we can change the conditions under which humans work" |
| Fact 7: sunk cost definition | verified | [ScienceDirect abstract](https://www.sciencedirect.com/science/article/pii/0749597885900494), February 1985 |
| Fact 8: theatre field study | verified | [ScienceDirect abstract](https://www.sciencedirect.com/science/article/pii/0749597885900494) |
| Fact 9: "Across two experiments (N = 395), we examined the reliability and validity of established sunk cost scenarios." | verified | [PMC12384923](https://pmc.ncbi.nlm.nih.gov/articles/PMC12384923/), "On the Low Reliability of Sunk Cost Vignettes", *Brain Sciences* (MDPI), published 28 July 2025, CC BY 4.0. The sentence is in the Introduction; the abstract has "Across two experiments (N = 395), we tested established sunk cost vignettes" and "ω = 0.14–0.57" |
| Fact 10: "Hierarchical task analysis (HTA) was developed at the University of Hull in the late 1960s" | unverifiable | The cited Aalto copy is closed to the public. Annett's 2004 chapter abstract ([Taylor & Francis](https://www.taylorfrancis.com/chapters/edit/10.1201/9780203489925-44/hierarchical-task-analysis-hta-john-annett)) says "was developed at the University of Hull in response to the need to analyze complex tasks", with no decade |
| Fact 11: "This is known as the p × c criterion (Annett & Duncan, 1967)" | unverifiable | Same closed copy. The substance holds: the 1967 abstract ([ERIC](https://eric.ed.gov/?id=ED019566)) weighs "the cost of inadequate performance" against "the probability of adequate performance without training", and Annett's [own reflection](https://hciengineering.net/reflections-on-task-analysis-psychological-sciences-and-clinical-psychology-by-john-annett/) names "the p x c criterion" |
| Fact 12: contextual inquiry adopts "a master-apprentice relationship model" | verified | [IxDF ch. 8](https://ixdf.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed/contextual-design) |
| Fact 13: "people are not consciously aware of their own work practice; all of their knowledge is tacit." | verified | [IxDF ch. 8](https://ixdf.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed/contextual-design) (the first clause is italic). The same paragraph cites "Polanyi 1958" for "aware in the doing" |
| Fact 14: "Five different models provide five perspectives on how work is done" | verified | [IxDF ch. 8](https://ixdf.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed/contextual-design) (followed by a colon) |
| Fact 15: Fleming et al., "recovered to/close to preimplementation levels after 12 months" | verified | [PMC3925410](https://pmc.ncbi.nlm.nih.gov/articles/PMC3925410), *HSR* 49(1 Pt 2):405–420, Feb 2014 (online 21 Dec 2013), doi 10.1111/1475-6773.12133. PMC holds only the abstract, which has no percentages |
| Fact 16: AHRQ, RVUs 8 percent lower, then 4 percent lower at 12 months | verified | [AHRQ 2011 summary](https://digital.ahrq.gov/ahrq-funded-projects/impact-health-information-technology-primary-care-workflow-and-financial/annual-summary/2011): PI Fleming, Baylor Research Institute, R03 HS 018220; visits 8 percent, then "4.5 percent lower"; 26 practices; GE Centricity; North Texas |
| Fact 17: Calder-Sprackman et al., "(0.51 patient/hour, P < 0.01)" and "(−0.31 patient/hour, P = 0.03)" | verified with a correction | [PubMed 33598662](https://pubmed.ncbi.nlm.nih.gov/33598662/), *JACEP Open* 2(1):e12362, online 4 Feb 2021. PubMed writes "-0.31" with an ASCII hyphen-minus, not U+2212. The abstract says "primarily paper-based electronic health record"; Epic, Ottawa and "big bang" aren't in it |
| Fact 18: Kennebeck et al., delays "resolved by 3 months post-implementation" | verified | [PubMed 22052897](https://pubmed.ncbi.nlm.nih.gov/22052897/), *JAMIA* 19(3):443–7, online 3 Nov 2011; "6-20% longer" and "12-22% longer" also match |
| Fact 19: Redd et al., "the provider clinical volumes did not generally return to baseline." | verified | [PMC4267903](https://pmc.ncbi.nlm.nih.gov/articles/PMC4267903/), *J AAPOS* 18(6):584–589, epub 14 Nov 2014. The sentence is in the Discussion, not the abstract; the 50%/75%/90% ramp over six weeks matches |
| Fact 20: Hitt, Wu and Zhou, "slowdown in business performance and productivity shortly after the implementation", June 2002 | verified with a correction | Abstract matches in [OpenAlex](https://api.openalex.org/works/doi:10.1080/07421222.2002.11045716). Crossref: *JMIS* 19(1):71–98, issued July 2002, not June |
| Fact 21: Boudreau et al., "(2) People are deterministic and predictable." and "Task times are deterministic." | verified | [INFORMS, MSOM 5(3):179–202, online 1 July 2003](https://pubsonline.informs.org/doi/10.1287/msom.5.3.179.16032). "Task times are deterministic." is a sub-point of assumption (2). The abstract doesn't hold either line |
| Fact 22: Fitts 1954, "An index of the difficulty of a movement is" … | verified | [Fitts 1954 scan](http://e.guigon.free.fr/rsc/article/Fitts54.pdf), JEP 47(6), June 1954, pp. 381–391 (Crossref 10.1037/h0055392). Full sentence below |
| Fact 23: Nielsen's heuristics "remain the same (stable since 1994)" | verified with a correction | The quote is NN/g's post on X (secondary). [NN/g's article](https://www.nngroup.com/articles/ten-usability-heuristics/), dated April 24, 1994, last reviewed Jan. 30, 2024, says the 2020 update "slightly refined the language of the definitions" and the heuristics "have remained relevant and unchanged since 1994". Cite the article |
| Fact 24: ISO 6385:2016 at 90.93, confirmed 2021-12-10 | verified | [ISO 6385:2016](https://www.iso.org/standard/63785.html): "90.93 2021-12-10 International Standard confirmed"; 60.60 2016-09-14; 90.20 2021-07-15; 90.60 2021-12-03; no new 90.20 entry |
| Fact 25: ISO/WD 10075-3 at stage 20.60 | contradicted | [ISO/CD 10075-3](https://www.iso.org/standard/91581.html): now a committee draft, stage 30.20 "CD consultation initiated" 2026-11-07, after 20.99 (WD approved as CD) 2026-10-28 and 30.00 2026-11-06. The earlier milestones in R23b section 4.8 (10.99 2025-03-07, 20.00 2026-09-08, 20.20 2026-10-01, 20.60 2026-10-16) match |
| Fact 26: ISO/TC 159/SC 1 meets 17 November 2026, virtual | verified | [ISO/TC 159/SC 1](https://www.iso.org/committee/53352.html) |
| Fact 27: NIST definition of confabulation, from a secondary site | verified with a correction | Exact in the [NIST AI 600-1 PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf), section 2, risk 2; cite NIST, not the secondary site. Curly quotes around “hallucinations” and “fabrications” |
| NIST AI 600-1 dated 26 July 2024; approved by the Editorial Review Board 25 July 2024; "available free of charge" | verified | [NIST publication page](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) ("Published July 26, 2024"); the PDF's cover reads "July 2024" and "Approved by the NIST Editorial Review Board on 07-25-2024" |
| NIST lists Human-AI configuration risks (automation bias, over-reliance, anthropomorphizing) and action MS-2.5-003 | verified with a correction | [NIST AI 600-1 PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf). MS-2.5-003 reads "Review and verify sources and citations in GAI system outputs during predeployment risk measurement and ongoing monitoring activities." The report's shorter form is a secondary paraphrase. The PDF has no guidance on user framing, as the report says |
| SEP quotes *Models of Man* (1957a: xxiv), "satisfice because they have not the wits to maximize" | verified | [SEP](https://plato.stanford.edu/entries/bounded-rationality/) (italics on *satisfice* and *maximize*) |
| Arkes and Blumer's explanation, "the desire not to appear wasteful" | verified | [ScienceDirect abstract](https://www.sciencedirect.com/science/article/pii/0749597885900494) |
| Polanyi's face example, "we usually cannot tell how we recognize a face we know" | secondary only | [tacit-knowledge-architecture.com excerpt](https://tacit-knowledge-architecture.com/object/the-tacit-dimension-excerpt/); no licensed primary text was found |
| Kennebeck: diverting patients "were not effective in minimizing delays" | verified | [PubMed 22052897](https://pubmed.ncbi.nlm.nih.gov/22052897/) |
| JAMIA 2021 (PMID 33575787): training "months after go-live"; +16 vs −8 appointments; 14 untrained | verified with a correction | [PubMed 33575787](https://pubmed.ncbi.nlm.nih.gov/33575787/), *JAMIA* 28(4):824–831: the numbers match (133 trained, 14 not), but the training ran 5–15 August 2019 "prior to EHR upgrade and organizational instance alignment", not months after a go-live. It's evidence about an upgrade, not a new system's dip |
| Boudreau et al.: in models such as classical scheduling, "the human side is omitted entirely" | verified with a correction | [INFORMS PDF](https://pubsonline.informs.org/doi/pdf/10.1287/msom.5.3.179.16032): the phrase glosses assumption (1), "People are not a major factor. (Many models look at machines without people, so the human side is omitted entirely.)"; it doesn't name classical scheduling |
| Fitts called W the "permissible variability" (the report cites MacKenzie) | verified | Primary: [Fitts 1954](http://e.guigon.free.fr/rsc/article/Fitts54.pdf), "of specified permissible variability (movement tolerance)" |
| Nielsen's article dated 24 April 1994; heuristic evaluation from Nielsen and Molich (1990) | verified | [NN/g](https://nngroup.com/articles/ten-usability-heuristics/): "April 24, 1994"; "in collaboration with Rolf Molich in 1990" |
| "The ISO/TC 159 chair's term runs until end 2026" | verified with a correction | The page the report cites is [ISO/TC 159/SC 1](https://www.iso.org/committee/53352.html): it's the SC 1 chair, "Chairperson (until end 2026)". TC 159's own page wasn't checked |
| Simon 1956 citation, doi 10.1037/h0042769 | verified | Crossref |
| Weigel, SSRN 3207806, Johns Hopkins, 3 July 2018 | verified | [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3207806): "Date Written: July 3, 2018" |
| Redd et al. *J AAPOS* 18(6):584–589; Hitt et al. *JMIS* 19(1):71–98; Boudreau et al. 5(3):179–202 | verified | Europe PMC/PMC metadata; Crossref |

Counts: 31 verified, 11 verified with a correction, 1 contradicted, 2 unverifiable, 1 secondary
only. Claims the report marks "not found" or "not covered" were skipped: CTA, method costs in
hours, what shortens the dip, Schultz et al., Hick and Hyman, redesign studies, the 2026 ISO
6385 outcome, cross-cultural replications. The Adams, Rogers and Fisk 2013 task-analysis study
and the CJEM abstract's figures (2.72 → 2.24 patients per hour) weren't checked.

## Compared with R23

What R23b adds to R23 (R23's own result and [R23-verification.md](R23-verification.md)):

- **Simon, Polanyi, Reason, sunk cost:** R23 marked all four "not verified" or "not found". R23b
  gives primary or publisher sources for each, all verified above. New: the 1955/1956/1957
  dating, Reason's moving holes, and the measurement doubts about sunk-cost vignettes.
- **Methods for finding a step's purpose:** R23 didn't retrieve contextual inquiry, HTA or CTA.
  R23b adds HTA (training origin, p × c stopping rule) and contextual inquiry (master-apprentice,
  tacit work practice, five work models). CTA is still not found.
- **The dip:** R23 had McAfee 2002 (one firm, recovered after months) and EMS911 (never
  recovered). R23b adds measured healthcare dips: Fleming/AHRQ (−8%, then −4% at 12 months),
  Kennebeck (resolved by 3 months), Calder-Sprackman and Redd (not recovered), and Hitt et al.
  (ERP slowdown, market reward).
- **What shortens the dip, a correction to R23:** R23's summary said "training and consultation
  shorten it (secondary and guidance, respectively)". R23b found no peer-reviewed field study
  showing that training, phasing or parallel running shortens it. Its one training study
  (PMID 33575787) is about an upgrade, not a go-live.
- **Operations research's assumptions about people:** not covered in R23. R23b adds Boudreau et
  al. 2003, verified at INFORMS.
- **Interfaces:** not covered in R23. R23b adds Fitts 1954 and Nielsen's heuristics (1994,
  unchanged in the 2020 update).
- **Neutral retrieval:** R23 found no non-vendor guidance. R23b adds NIST AI 600-1
  (confabulation, Human-AI configuration, MS-2.5-003). It still finds no standard on user
  framing.
- **ISO:** R23b adds the SC 1 meeting on 17 November 2026. On ISO 10075-3 it repeats R23's
  out-of-date WD stage 20.60, which R23-verification had already found superseded by CD stage
  30.20 (2026-11-07). On ISO 6385 it agrees with R23: confirmed 2021, no 2026 outcome yet.

## Exact quotes for facts rows

| Fact | URL | Exact quote |
|---|---|---|
| Simon coins "satisfice" | https://pages.ucsd.edu/~mckenzie/Simon1956PsychReview.pdf | "Evidently, organisms adapt well enough to "satisfice"; they do not, in general, "optimize."" (straight quotes as scanned; the OCR text layer reads "satisflce") |
| Term "bounded rationality", 1957 | https://plato.stanford.edu/entries/bounded-rationality/ | "Herbert Simon introduced the term ‘bounded rationality’ (Simon 1957b: 198; see also Klaes & Sent 2005)" (U+2018, U+2019) |
| Satisficing vs maximizing | same | "the behavior of human beings who satisfice because they have not the wits to maximize" (Simon 1957a: xxiv; *satisfice* and *maximize* italic) |
| Polanyi, tacit knowledge | https://press.uchicago.edu/ucp/books/book/chicago/T/bo6035368.html | "I shall reconsider human knowledge by starting from the fact that we can know more than we can tell" (p. 4 per Pimm 2009) |
| Swiss cheese holes move | https://pmc.ncbi.nlm.nih.gov/articles/PMC1117770/ | "these holes are continually opening, shutting, and shifting their location." |
| Holes line up momentarily | same | "this can happen only when the holes in many layers momentarily line up to permit a trajectory of accident opportunity" |
| Two causes of holes | same | "The holes in the defences arise for two reasons: active failures and latent conditions." |
| Change the conditions | same | "We cannot change the human condition, but we can change the conditions under which humans work" |
| Sunk cost effect | https://www.sciencedirect.com/science/article/pii/0749597885900494 | "The sunk cost effect is manifested in a greater tendency to continue an endeavor once an investment in money, effort, or time has been made." |
| Sunk cost field study | same | "customers who had initially paid more for a season subscription to a theater series attended more plays during the next 6 months" |
| Sunk-cost vignettes measure poorly | https://pmc.ncbi.nlm.nih.gov/articles/PMC12384923/ | "Across two experiments (N = 395), we examined the reliability and validity of established sunk cost scenarios." |
| Sunk-cost effect contested in economics | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3207806 | "Though widely accepted in psychology, the Sunk Cost Effect (SCE) finds little support from recent evidence in economics." |
| Contextual inquiry stance | https://ixdf.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed/contextual-design | "but rather adopts a master-apprentice relationship model" |
| Work practice is tacit | same | "people are not consciously aware of their own work practice; all of their knowledge is tacit." |
| Sequence model shows intents | same | "the intents or goals that their task steps are trying to accomplish" |
| EHR dip, primary care | https://digital.ahrq.gov/ahrq-funded-projects/impact-health-information-technology-primary-care-workflow-and-financial/annual-summary/2011 | "RVUs were 8 percent lower during the first 6 months following implementation, but rebounded to 4 percent lower than pre-implementation levels by 12 months post-implementation." |
| EHR dip, abstract | https://pmc.ncbi.nlm.nih.gov/articles/PMC3925410 | "Productivity, volume, and net income decreased initially but recovered to/close to preimplementation levels after 12 months." |
| ED efficiency not recovered | https://pubmed.ncbi.nlm.nih.gov/33598662/ | "Physician efficiency decreased and did not recover to baseline." |
| Pediatric ED delays resolved | https://pubmed.ncbi.nlm.nih.gov/22052897/ | "Delays in ED throughput during EHR implementation are real and significant despite additional providers in the ED, and in this setting resolved by 3 months post-implementation." |
| Ophthalmology not recovered | https://pmc.ncbi.nlm.nih.gov/articles/PMC4267903/ | "the provider clinical volumes did not generally return to baseline." |
| ERP slowdown | https://doi.org/10.1080/07421222.2002.11045716 | "Even though there is a slowdown in business performance and productivity shortly after the implementation" |
| OM models: deterministic people | https://pubsonline.informs.org/doi/10.1287/msom.5.3.179.16032 | "(2) People are deterministic and predictable." |
| OM models: task times | same | "Task times are deterministic." |
| OM models: people left out | same | "(Many models look at machines without people, so the human side is omitted entirely.)" |
| Fitts's index of difficulty | http://e.guigon.free.fr/rsc/article/Fitts54.pdf (JEP 47(6), 1954, doi 10.1037/h0055392) | "An index of the difficulty of a movement is proposed on the assumption that the average amplitude, the average duration, and the amplitude variability of successive movements are related" |
| Nielsen's heuristics unchanged | https://www.nngroup.com/articles/ten-usability-heuristics/ | "the 10 heuristics themselves have remained relevant and unchanged since 1994." |
| ISO 6385 current | https://www.iso.org/standard/63785.html | "This publication was last reviewed and confirmed in 2021. Therefore this version remains current." |
| ISO 10075-3 revision | https://www.iso.org/standard/91581.html | "A draft is being reviewed by the committee." (stage 30.20, 2026-11-07) |
| NIST: confabulation | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf | "The production of confidently stated but erroneous or false content (known colloquially as “hallucinations” or “fabrications”) by which users may be misled or deceived." (U+201C, U+201D) |
| NIST: automation bias | same | "This phenomenon is an example of automation bias, or excessive deference to automated systems." |
| NIST: verify citations | same | "Review and verify sources and citations in GAI system outputs during predeployment risk measurement and ongoing monitoring activities." |

## Versions found from registries

No software tools are in this report. Versions and states read today:

- ISO 6385:2016: edition 3, published 2016-09-14, 90.93 confirmed 2021-12-10, no 2026 review
  entry. ISO/CD 10075-3: edition 2, 30.20 CD consultation initiated 2026-11-07.
- NIST AI 600-1: July 2024 (NIST page: published July 26, 2024; page updated April 8, 2026),
  doi 10.6028/NIST.AI.600-1. No later revision is listed.
- SEP "Bounded Rationality": first published 30 Nov 2018, substantive revision 13 Dec 2024.
- NN/g "10 Usability Heuristics": 24 April 1994, last reviewed 30 Jan 2024 (dateModified
  2026-08-20).

## Licences

| Source | Licence as stated | What an Apache-2.0 repository may do |
|---|---|---|
| Fitts 1954 | The 1992 APA reprint (JEP: General 121(3):262–269) is marked "In the public domain"; the original was US Air Force funded. The report said "© APA" | Quote, paraphrase and adapt, with citation |
| NIST AI 600-1 | "This publication is available free of charge"; a NIST work (the PDF links NIST's "Copyright, Use, and Licensing Statements", not read) | Quote and paraphrase with citation; treat as US government work |
| AHRQ grant summary | US federal page; licence statement not read | Quote briefly with citation |
| PMC12384923 (Brain Sciences 2025) | "Creative Commons Attribution (CC BY) license", © 2025 the authors, licensee MDPI | Quote, paraphrase, adapt with attribution |
| Reason, BMJ 2000 | "Copyright © 2000, British Medical Journal" | Quote briefly with citation |
| Redd et al., J AAPOS 2014 | "© 2014 by the American Association for Pediatric Ophthalmology and Strabismus. All rights reserved." | Quote briefly with citation |
| Fleming et al., HSR 2014 | "© Health Research and Educational Trust" | Quote briefly with citation |
| Boudreau et al., MSOM 2003 | "© 2003 INFORMS"; "may be used only for the purposes of research, teaching, and/or private study" | Quote briefly with citation |
| SEP | "Copyright © 2024 by Gregory Wheeler" | Quote briefly with citation |
| NN/g | "Copyright © by Jakob Nielsen"; reproduction needs NN/g's copyright policy | Quote briefly with citation |
| IxDF ch. 8 | No licence for the text seen; figures "Unknown (pending investigation)" | Quote briefly with citation |
| ISO pages | © ISO 2026 | Quote stage data and abstract lines briefly |
| Simon 1956, Arkes and Blumer 1985, Polanyi 1966, Hitt et al. 2002, PubMed abstracts | Publisher copyright; not stated on the pages read | Quote briefly with citation |
| Weigel (SSRN) | Not stated | Quote briefly with citation |

## Repository facts this contradicts

`git -C /home/user/claude-code-skills grep -n -i` over `skills/human-factors` and
`skills/optimization-and-scheduling` for `Simon`, `Polanyi`, `Reason`, `sunk`, `McAfee`,
`ISO 6385`, `10075`, `Boudreau`, `Wiers` and `Ivert`, then `swiss`, `satisfic`, `tacit`,
`deterministic`, `task analysis`, `contextual inquiry`, `fitts`, `nielsen`, `600-1`, `shorten`,
`train` and `dip`.

- `Simon`, `Polanyi`, `sunk`, `ISO 6385`, `10075`, `Boudreau`, `Ivert` and the second list: no
  hits, except `train` and `dip`, which hit the module's prose only.
- `Reason`: only the English word "reason".
- `McAfee`: fact `hf-mcafee-dip` in `skills/human-factors/references/human-factors.md` line 172,
  and rule 4 ("Budget for a dip of months after a tool change, and don't promise recovery").
  R23b agrees with both: its measured dips run from recovery by 3 months to no recovery at 3
  years.
- `Wiers`: `skills/optimization-and-scheduling/references/optimization-and-scheduling.md`
  line 116, a Wiers (2009) APS quote that R23b doesn't address.

No Facts row in either skill is now wrong.

---

# R23b: Human factors, the questions R23 didn't reach

All five "What we believe" items are right in substance, but three need corrections that matter for a reference repository. Satisficing (the idea in 1955, the word in 1956) and "bounded rationality" (the term in 1957) came from different Simon publications.\[1\] Reason's holes are not fixed: they are "continually opening, shutting, and shifting".\[2\] And the sunk-cost effect is contested outside psychology.\[3\] The measured dip after a new system is real, ranges from fully recovered within months to not recovered at 6–8 months or 3 years, and no peer-reviewed field study found here shows that training, phasing or parallel running shortens it.

**Access note.** The repository's main page could not be fetched in this run: the fetch tool refused it as not permitted. R23's filed result and the shipped `human-factors` skill could therefore not be read. That means they could not be accessed, not that they are missing. Search results did show pull requests #45 and #46 (16 October 2026), which planned the skill and filed the R23 prompt.\[4\]\[5\] They also showed #128 (11 November 2026), which listed R23 among "Eleven research prompts [that] have never been run" at the time it was written.\[6\] Because R23's findings could not be read, this report may repeat some of them. The receiving session should remove any overlap.

## TL;DR

- **Corrections:** Simon's satisficing idea dates from 1955, the word from his 1956 *Psychological Review* paper, and the term "bounded rationality" from *Models of Man* (1957). Reason's 2000 BMJ model has holes that move. The sunk-cost effect (Arkes and Blumer 1985) is contested in economics and its classic vignettes measure poorly.
- **The dip after a new system:** measured dips run from an 8% fall in RVUs and visits, recovering to about 4% below baseline at 12 months (AHRQ summary of Fleming et al.), to 0.51 fewer emergency patients per hour at go-live with 0.31 per hour still lost at 6–8 months (Calder-Sprackman et al. 2021). No peer-reviewed study found shows that training, phased rollout or parallel running shortens the dip.
- **Standards:** ISO 6385:2016 is still at stage 90.93 (confirmed 10 December 2021). No outcome of a 2026 review was found. ISO 10075-3 is being revised as ISO/WD 10075-3 (edition 2, stage 20.60, comment period closed 16 October 2026). No standards body or regulator was found to give guidance specifically on keeping an AI's fact-finding free of the user's framing.

## 1. Summary

1. Simon's 1956 paper is the primary source for the word: "Evidently, organisms adapt well enough to 'satisfice'; they do not, in general, 'optimize.'"\[7\]
2. The term "bounded rationality" first appears in print in Simon's *Models of Man* (1957, p. 198), per the Stanford Encyclopedia of Philosophy and Klaes and Sent (2005).\[8\] Attribute the term to 1957, not 1955 or 1956.
3. Polanyi, *The Tacit Dimension* (1966), p. 4: "I shall reconsider human knowledge by starting from the fact that *we can know more than we can tell*" (italics in original).\[9\] Contextual Design's own authors cite Polanyi's earlier *Personal Knowledge* (1958) for being "aware in the doing".\[10\]
4. Reason's BMJ paper (18 March 2000, 320:768–770) says defences are "more like slices of Swiss cheese, having many holes—though unlike in the cheese, these holes are continually opening, shutting, and shifting their location."\[2\] The model is older: Reason set out its ideas in *Human Error* (1990) (secondary source).\[11\]
5. Arkes and Blumer (1985), *OBHDP* 35:124–140, define the sunk cost effect as "a greater tendency to continue an endeavor once an investment in money, effort, or time has been made".\[12\] Recent work questions how well it replicates and how reliably it is measured.\[13\]
6. Hierarchical task analysis (HTA) comes from Annett and Duncan (1967), "Task analysis and training design", *Occupational Psychology* 41. It was built to decide training, and stops decomposing a task by the "p × c" rule (the probability of failure times its cost).\[14\]
7. Contextual inquiry (Beyer and Holtzblatt, *Contextual Design*, 1998; second edition 2017) is a field interview using a "master-apprentice relationship model".\[10\] It is the cheapest of the three methods that still sees work as done, which makes it the default for a small team.
8. EHR go-live dips, measured: about an 8% fall in RVUs and in visits per physician FTE in the first 6 months, recovering to 4–4.5% below baseline at 12 months.\[15\] These figures come from the AHRQ grant summary of Fleming et al.; the *Health Services Research* paper's abstract (2014) gives no percentages.\[16\]
9. Non-recovery case: Calder-Sprackman et al. (2021) reported "Physician efficiency decreased and did not recover to baseline" 6–8 months after a "big bang" switch to Epic.\[17\]\[18\] In Redd et al. (2014), pediatric ophthalmology volumes "did not generally return to baseline".\[19\]
10. What shortens the dip: **not found** in peer-reviewed field studies. In one emergency department, diverting patients "were not effective in minimizing delays" (Kennebeck et al. 2012).\[20\] Hospitals that went "Big Bang" had "relatively low TFP levels" (total factor productivity; Huerta, Thompson et al., *Decision Support Systems*, 2013), which is a cross-sectional finding, not a measured dip length.
11. Operations research models often assume "People are deterministic and predictable" and "Task times are deterministic" (Boudreau, Hopp, McClain and Thomas 2003, *MSOM* 5(3):179–202).\[21\]\[22\]
12. Fitts (1954), *J. Exp. Psych.* 47(6):381–391, is the primary source for Fitts's law.\[23\]\[24\]\[25\] Nielsen's 10 heuristics date from 24 April 1994, and NN/g says they have stayed "the same (stable since 1994)" through the 2020 update.\[26\]\[27\]
13. ISO 6385:2016 has been confirmed since 10 December 2021, and its next review is due on ISO's five-year cycle.\[28\] No 2026 outcome was published at the time of reading. ISO/TC 159/SC 1 meets virtually on 17 November 2026.\[29\]
14. ISO 10075-3:2004 is being replaced. ISO/WD 10075-3 (edition 2) was approved as a new project on 7 March 2025 and registered on 8 September 2026, and its working-draft comment period closed on 16 October 2026.\[30\]
15. NIST AI 600-1 (26 July 2024) names "Confabulation" and "Human-AI configuration" (automation bias, over-reliance) as generative-AI risks.\[31\]\[32\] It does not address the user's framing of a query; that part is **not found**.

## 2. Corrections

| Belief | Verdict | Correct fact | Source |
|---|---|---|---|
| Herbert Simon introduced "satisficing" and bounded rationality. | **Confirmed, with dates corrected** | The idea of choosing satisfactory alternatives appears in Simon (1955), the word "satisfice" in Simon (1956), and the term "bounded rationality" in *Models of Man* (1957).\[1\] | Simon 1956, *Psychological Review* 63(2):129–138, doi:10.1037/h0042769;\[33\] Stanford Encyclopedia of Philosophy, "Bounded Rationality"; Barros, *Brazilian Journal of Political Economy* (SciELO) |
| Polanyi wrote "we can know more than we can tell" (*The Tacit Dimension*, 1966). | **Confirmed** | p. 4, italicized in the original, and preceded by "I shall reconsider human knowledge by starting from the fact that". Published by Doubleday, Garden City NY, 1966; reprinted by University of Chicago Press, 2009, with a foreword by Amartya Sen.\[9\]\[34\] | Springer chapter "Commentary on Knowing More Than We Can Tell" (citing Polanyi 1966, p. 4); BiblioVault (University of Chicago Press) |
| Reason's Swiss cheese model describes accidents as holes lining up in layered defences. | **Confirmed, refinement** | The holes move ("continually opening, shutting, and shifting"). They come from active failures and latent conditions. Harm needs the holes in many layers to line up "momentarily" along an "accident trajectory". The ideas predate the 2000 paper (*Human Error*, 1990, secondary source).\[2\]\[11\]\[35\] | Reason J. BMJ 2000;320:768–770, PMC1117770; Baines Simmons (secondary) |
| Sunk-cost effects are documented in Arkes and Blumer (1985). | **Confirmed; contested in economics** | Arkes HR, Blumer C. *Organizational Behavior and Human Decision Processes* 35:124–140, February 1985, doi:10.1016/0749-5978(85)90049-4. The evidence included a theatre field study. Later work: Weigel (Johns Hopkins), "Don't Stop Now: The Sunk Cost Effect in an Incentivized Lab Experiment" (SSRN 3207806, 3 July 2018), states that "Though widely accepted in psychology, the Sunk Cost Effect (SCE) finds little support from recent evidence in economics", and the classic vignettes have low reliability. | Semantic Scholar record; Weigel 2018 (SSRN 3207806); PMC12384923 |
| Contextual inquiry, HTA and CTA are the standard methods for studying work as done. | **Partly corrected** | HTA was designed to decide training, not to discover purpose. Its 1967 paper and its stopping rule focus on whether a step needs further analysis. Contextual inquiry is one step of the wider Contextual Design process.\[14\]\[36\] CTA is a family of methods with no single primary source; no primary source for it was retrieved in this run. "Standard" is a fair description for the first two; for CTA it was not checked here. | Annett, "Hierarchical Task Analysis" (Annett chapter, Aalto copy); IxDF Encyclopedia chapter by Holtzblatt and Beyer |

## 3. Facts table

| # | Fact | Value | Source URL | Exact quote | Date |
|---|---|---|---|---|---|
| 1 | Simon's coinage of "satisfice" in print | Psych. Review 63(2), 1956 | https://pages.ucsd.edu/~mckenzie/Simon1956PsychReview.pdf | "Evidently, organisms adapt well enough to "satisfice"; they do not, in general, "optimize.""\[7\] | March 1956 |
| 2 | First print use of "bounded rationality" | *Models of Man*, 1957, p. 198 | https://plato.stanford.edu/entries/bounded-rationality/ | "Herbert Simon introduced the term 'bounded rationality' (Simon 1957b: 198; see also Klaes & Sent 2005)"\[8\] | read 11 Nov 2026 |
| 3 | Order in which the satisficing idea, the word and "bounded rationality" appeared | 1955 → 1956 → 1957 | https://www.scielo.br/j/rep/a/CWfwPPVWKvLrndfxR9vYFHL/?format=html&lang=en | "The idea of choice of satisfactory alternatives emerges in Simon (1955), the term "satisficing" associated with search for alternatives appears fully developed in Simon (1956), the term "bounded rationality" is the first general concept that tries to encompass those simplifications/procedures and appears in Simon (1957)."\[1\] | read 11 Nov 2026 |
| 4 | Polanyi's tacit-knowledge sentence | *The Tacit Dimension*, 1966, p. 4 | https://link.springer.com/chapter/10.1007/978-3-642-00742-2_57 | "I shall reconsider human knowledge by starting from the fact that we can know more than we can tell." (1966, p. 4; italics in original)\[9\] | read 11 Nov 2026 |
| 5 | Swiss cheese holes move | BMJ 2000;320:768–770 | https://pmc.ncbi.nlm.nih.gov/articles/PMC1117770/ | "In reality, however, they are more like slices of Swiss cheese, having many holes—though unlike in the cheese, these holes are continually opening, shutting, and shifting their location."\[2\] | 18 Mar 2000 |
| 6 | Reason's design maxim | BMJ 2000 | https://pmc.ncbi.nlm.nih.gov/articles/PMC1117770/ | "We cannot change the human condition, but we can change the conditions under which humans work"\[2\] | 18 Mar 2000 |
| 7 | Sunk cost definition | OBHDP 35:124–140 | https://oamonitor.ireland.openaire.eu/rpo/rcsi/search/publication?pid=10.1016%2F0749-5978%2885%2990049-4 | "The sunk cost effect is manifested in a greater tendency to continue an endeavor once an investment in money, effort, or time has been made."\[12\] | 1 Feb 1985 |
| 8 | Sunk-cost field study | Theatre season subscriptions | same as #7 | "customers who had initially paid more for a season subscription to a theater series attended more plays during the next 6 months"\[12\] | 1 Feb 1985 |
| 9 | Sunk-cost vignette reliability | Two experiments, N = 395 | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12384923/ | "Across two experiments (N = 395), we examined the reliability and validity of established sunk cost scenarios."\[13\] | read 11 Nov 2026 |
| 10 | HTA origin | Annett and Duncan 1967, *Occupational Psychology* 41:211–221 | https://mycourses.aalto.fi/pluginfile.php/1754492/mod_folder/content/0/Optional_reading_Task_Analysis_Annett.pdf?forcedownload=1 | "Hierarchical task analysis (HTA) was developed at the University of Hull in the late 1960s"\[14\] | read 11 Nov 2026 |
| 11 | HTA stopping rule | p × c criterion | same as #10 | "This is known as the p × c criterion (Annett & Duncan, 1967)"\[14\] | read 11 Nov 2026 |
| 12 | Contextual inquiry stance | Master-apprentice model | https://ixdf.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed/contextual-design | "The interviewer thus does not enter with a preformed list of questions, as in a survey or focus group, but rather adopts a master-apprentice relationship model"\[10\] | read 11 Nov 2026\[10\] |
| 13 | Why observe in context | Tacit work practice | same as #12 | "people are not consciously aware of their own work practice; all of their knowledge is tacit." | read 11 Nov 2026\[10\] |
| 14 | Contextual Design's five work models | flow, cultural, sequence, physical, artifact | same as #12 | "Five different models provide five perspectives on how work is done" | read 11 Nov 2026\[10\] |
| 15 | EHR dip, primary care (abstract) | Recovered to or close to baseline at 12 months | https://pmc.ncbi.nlm.nih.gov/articles/PMC3925410 | "Productivity, volume, and net income decreased initially but recovered to/close to preimplementation levels after 12 months."\[16\] | Feb 2014 |
| 16 | EHR dip, primary care (numbers) | −8% RVUs in the first 6 months; −4% at 12 months | https://digital.ahrq.gov/ahrq-funded-projects/impact-health-information-technology-primary-care-workflow-and-financial/annual-summary/2011 | "RVUs were 8 percent lower during the first 6 months following implementation, but rebounded to 4 percent lower than pre-implementation levels by 12 months post-implementation."\[15\] | 2011 |
| 17 | EHR dip, emergency department, no recovery | −0.51 patients/h at go-live; −0.31 patients/h at 6–8 months | https://pubmed.ncbi.nlm.nih.gov/33598662/ | "Physicians saw fewer patients per shift during go-live (0.51 patient/hour, P < 0.01), patient efficiency increased in post-implementation but did not recover to baseline (−0.31 patient/hour, P = 0.03)."\[17\] | 4 Feb 2021 |
| 18 | Pediatric ED length of stay | +6–22%, resolved by 3 months | https://pubmed.ncbi.nlm.nih.gov/22052897 | "Delays in ED throughput during EHR implementation are real and significant despite additional providers in the ED, and in this setting resolved by 3 months post-implementation."\[20\] | 3 Nov 2011 (online) |
| 19 | Ophthalmology, no recovery | Volumes below baseline | https://pmc.ncbi.nlm.nih.gov/articles/PMC4267903/ | "the provider clinical volumes did not generally return to baseline."\[19\] | 14 Nov 2014 |
| 20 | ERP dip | A slowdown just after implementation | https://www.semanticscholar.org/paper/Investment-in-Enterprise-Resource-Planning:-Impact-Hitt-Wu/4462e6c004949d1ed46b59f1e959a1b35e55e190 | "Even though there is a slowdown in business performance and productivity shortly after the implementation, financial markets consistently reward the adopters with higher market valuation"\[37\] | June 2002\[38\]\[39\] |
| 21 | Operations research assumes deterministic people | MSOM 5(3):179–202 | https://www.researchgate.net/publication/252407219_On_the_Interface_Between_Operations_and_Human_Resource_Management | "(2) People are deterministic and predictable." and "Task times are deterministic."\[21\] | Jul 2003 |
| 22 | Fitts's law primary source | J. Exp. Psych. 47(6):381–391 | http://www2.psychology.uiowa.edu/faculty/mordkoff/InfoProc/pdfs/Fitts%201954.pdf | "An index of the difficulty of a movement is" [defined from amplitude and tolerance] | June 1954\[23\] |
| 23 | Nielsen heuristics are unchanged | Stable since 1994 | https://x.com/NNgroup/status/1328745213104427011?lang=en | "The 10 heuristics themselves remain the same (stable since 1994)" | 17 Nov 2020\[26\] |
| 24 | ISO 6385:2016 stage | 90.93, confirmed 10 Dec 2021 | https://www.iso.org/standard/63785.html | "90.93 2021-12-10 International Standard confirmed"\[28\] | read 11 Nov 2026 |
| 25 | ISO 10075-3 revision | ISO/WD 10075-3, stage 20.60 | https://www.iso.org/standard/91581.html | "20.60 2026-10-16 Close of comment period"\[30\] | read 11 Nov 2026 |
| 26 | ISO/TC 159/SC 1 next meeting | 17 Nov 2026, virtual | https://www.iso.org/committee/53352.html | "17 | November 2026 | Virtual | ISO/TC 159/SC 1"\[40\] | read 11 Nov 2026 |
| 27 | NIST definition of confabulation | NIST AI 600-1, 26 Jul 2024 | https://docs.modulos.ai/frameworks/nist-ai-rmf/generative-ai-profile (secondary, quoting NIST) | "The production of confidently stated but erroneous or false content (known colloquially as "hallucinations" or "fabrications") by which users may be misled or deceived." | 26 Jul 2024\[31\] |

## 4. Findings

### 4.1 Methods for finding what a step is for

**Contextual inquiry (Beyer and Holtzblatt).**
- **Primary sources:** *Contextual Design: Defining Customer-Centered Systems* (Morgan Kaufmann, 1998; often cited as 1997), *Contextual Design: Evolved* (2014) and *Contextual Design: Design for Life* (2nd ed., 2017).\[41\] The authors' own encyclopedia chapter (IxDF, *Encyclopedia of HCI*, 2nd ed., ch. 8) gives the principles.
- **Method:** one-on-one interviews in the user's workplace. The interviewer "observes users as they work and inquires into the users' actions as they unfold to understand their motivations and strategy". Interviewer and user "develop a shared interpretation of the work".\[10\]
- **What it produces:** interpretation-session notes and five work models (flow, cultural, sequence, physical, artifact), then an affinity diagram.\[10\] A team may sort "perhaps around 1500" notes (ScienceDirect topic page, secondary).\[42\]
- **Why it suits this skill:** the sequence model shows "the intents or goals that their task steps are trying to accomplish".\[10\] That is exactly the "what is this step for" question. The cultural model shows "how they work around those constraints".\[10\]
- **Cost:** "Contextual inquiry is resource-intensive" (Wikipedia, secondary).\[43\] No primary figure for hours per visit was found.

**Hierarchical task analysis (Annett and Duncan 1967).**
- **Origin:** developed at the University of Hull in the late 1960s, for training design.\[14\]
- **Method:** it starts "not with a list of activities, but by identifying the goals of the task". Each goal is broken into subgoals with plans, and breaking down stops by the p × c criterion (Annett's chapter).\[14\]
- **What it produces:** a goal hierarchy with plans, which can feed training syllabi, interface design or error analysis.\[14\]
- **Cost:** low equipment cost, but a skill. In Adams, Rogers and Fisk, "Skill Components of Task Analysis" (*Instructional Science* 41(6):1009–1046, November 2013, doi:10.1007/s11251-013-9270-9; 36 novices aged 18–28 and 8 experienced analysts), "Novices' initial task analysis scored low on all coding criteria", and practitioners' analyses "were 2-3 levels deep but also scored low on some criteria."
- **Page range:** contested. Most sources give 211–221; usabilitybok.org gives 211–227.\[44\]\[45\]

**Cognitive task analysis (CTA).** No primary source was retrieved in this run. CTA is commonly traced to Klein's Critical Decision Method and to Crandall, Klein and Hoffman's *Working Minds* (2006), but that attribution is not verified here. Treat the CTA claim as **not found** in this run.

**Which suits a small team.** Use HTA first. It is desk-based, and it turns "why is this step here" into a goal hierarchy that can be checked with one or two practitioners. Follow it with two to four contextual inquiry visits aimed at the steps whose purpose the hierarchy cannot explain. Polanyi's point is why the visits are needed: people cannot fully say what they know, so asking alone under-reports purposes. This recommendation is our reasoning from the sources above, not a sourced finding.

### 4.2 The sources R23 couldn't find

- **Simon.** The 1956 *Psychological Review* paper is where the word appears: "Evidently, organisms adapt well enough to 'satisfice'; they do not, in general, 'optimize.'"\[7\] The SEP also quotes *Models of Man* (1957a: xxiv): "the behavior of human beings who *satisfice* because they have not the wits to *maximize*".\[8\] The 1955 *Quarterly Journal of Economics* paper ("A Behavioral Model of Rational Choice") holds the idea but not the word, according to Barros/SciELO.\[1\]
- **Polanyi.** p. 4 of *The Tacit Dimension* (1966), as quoted above. The face-recognition example follows: "we usually cannot tell how we recognize a face we know" (excerpt, secondary host).\[46\]
- **Reason.** BMJ 2000, PMC1117770, as quoted above. The paper's opening: "The human error problem can be viewed in two ways: the person approach and the system approach."\[2\]
- **Sunk cost.** Arkes and Blumer 1985, as quoted above. Their explanation is "the desire not to appear wasteful".\[12\]

### 4.3 The size of the dip after a new system

**Measured dips:**

| Setting | Dip | Recovery | Source |
|---|---|---|---|
| 26 North Texas primary care practices, GE Centricity | RVUs −8% and visits per physician FTE −8% in the first 6 months\[15\] | −4% and −4.5% at 12 months; "recovered to/close to" baseline\[15\]\[16\] | Fleming et al., *HSR* 2014, doi:10.1111/1475-6773.12133; numbers from the AHRQ 2011 summary |
| Ottawa Hospital ED, paper to Epic, "big bang" switch in June 2019 | −0.51 patients/h at go-live (2.72 → 2.24/h, "a 17% decrease", CJEM abstract)\[18\]\[47\] | **Not recovered:** −0.31 patients/h at 6–8 months\[48\] | Calder-Sprackman et al., *JACEP Open* 2021;2(1):e12362\[17\] |
| Pediatric ED (Cincinnati) | Length of stay +6–20% for admitted patients and +12–22% for discharged patients\[20\] | Resolved by 3 months\[20\] | Kennebeck et al., *JAMIA* 2012;19(3):443–447\[20\] |
| Academic pediatric ophthalmology | Planned ramp of 50% → 75% → 90% of volume over 6 weeks\[19\] | **Not recovered**; about 11% lower at 3 years (not significant, per a later secondary summary)\[19\]\[49\] | Redd et al., *J AAPOS* 2014;18(6):584–589 |
| Multi-firm ERP adopters | "slowdown in business performance and productivity shortly after the implementation" (no figure in the abstract)\[37\] | Adopters still valued higher\[37\] | Hitt, Wu and Zhou, *JMIS* 2002;19(1):71–98\[38\]\[39\]\[50\] |

**What shortens it: not found.**
- No peer-reviewed field study was found that compares dip size or length by training, phased rollout or parallel running.
- In one ED, diverting patients "were not effective in minimizing delays".\[20\]
- Huerta, Thompson et al., "Electronic health record implementation and hospitals' total factor productivity" (*Decision Support Systems*, May 2013, doi:10.1016/j.dss.2012.10.004), measured total factor productivity (TFP) for 2006–2008 across nine EHR stages and found that "hospitals that attempt to fully implement an EHR in one year, the 'Big Bang' strategy, have relatively low TFP levels." This is cross-sectional and does not measure dip length.
- Training months after go-live: in *JAMIA* 2021 (PMID 33575787), trained clinicians gained 16 appointments per 30 days while untrained ones lost 8. The comparison group was 14 untrained clinicians, which is weak.\[51\]
- A training programme 20 months after go-live ("Home 4 Dinner", PMC6952029) "was not effective in decreasing EHR-use time outside of clinic."\[52\]
- Vendor figures such as "10-30%" or "20 to 40 per cent in the first month" are marketing claims, not field studies.\[53\]\[54\] Do not cite them.

### 4.4 Models that treat people as deterministic

- Boudreau, Hopp, McClain and Thomas (2003) list the behavioural assumptions behind operations models, including "(2) People are deterministic and predictable" and "Task times are deterministic". They conclude that in many models, such as classical scheduling, "the human side is omitted entirely" (as quoted by later authors).\[21\]\[55\]
- Shop-floor follow-ups by the same group: Schultz, Juran, Boudreau, McClain and Thomas, "Modeling and worker motivation in JIT production systems", *Management Science* 44 (1998), 1595–1607. Also Schultz, McClain and Thomas, "Overcoming the dark side of worker flexibility", *Journal of Operations Management* 21(1) (2003), 81–92.\[56\]
- These are **citations only.** Their findings and exact words were not retrieved in this run, so no claim about what happened on their shop floors is made here.
- Learning and forgetting: a case study of temporary assembly workers found that "Learning and forgetting dynamics significantly influence production costs" (summary on academia.edu, secondary).\[57\]
- Full-utilization plans: no primary paper was retrieved in this run (**not found**).

### 4.5 Interfaces

- **Fitts (1954):** the index of difficulty, in bits, is built from movement amplitude (A) and target width (W). The usual form is ID = log2(2A/W). Fitts called W the "permissible variability" (MacKenzie, secondary).\[25\]\[58\]\[59\]
- **Hick-Hyman law:** Hick (1952) and Hyman (1953), cited by MacKenzie (secondary).\[58\] The primary papers were not retrieved.
- **Nielsen:** the article "10 Usability Heuristics for User Interface Design" is dated 24 April 1994.\[27\]\[60\] Its 2020 update kept the heuristics and added examples.\[26\]\[61\] Heuristic evaluation as a method comes from Nielsen and Molich (1990), doi:10.1145/97243.97281.\[62\]
- **Cost of breaking familiarity in redesigns:** no study was retrieved in this run (**not found**).

### 4.6 How universal

Cross-cultural replications of status quo bias, habit formation and trust in automation: **not covered**. The search budget ran out before these searches returned results.

### 4.7 Neutral retrieval

NIST AI 600-1 (Generative AI Profile, 26 July 2024) is a regulator-adjacent federal standards source, not a vendor. It defines confabulation and lists "Human-AI configuration" risks: automation bias, over-reliance and anthropomorphizing. A secondary summary reports a suggested action, MS-2.5-003, to "review and verify sources and citations in outputs".\[32\] No standards body or regulator guidance was found on stopping a user's framing or leading question from steering an AI's fact-finding (**not found**). The repository's rule that agents gather facts without the user's bias therefore rests on its own reasoning, not on a standard.\[4\]

### 4.8 ISO 6385's 2026 review and ISO 10075-3

- **ISO 6385:2016:** published 14 September 2016. Its last review ran from 15 July 2021 to 3 December 2021 and confirmed it on 10 December 2021. The page reads "A standard is reviewed every 5 years", and the next 90.20 stage has no date.\[28\] **No 2026 review outcome found.** The next point to check is the SC 1 meeting on 17 November 2026.\[29\]
- **ISO 10075-3:** ISO/WD 10075-3, edition 2, will replace ISO 10075-3:2004.\[30\] Its milestones so far:
  - 10.99, new project approved: 7 March 2025;\[30\]
  - 20.00, registered in the work programme: 8 September 2026;\[30\]
  - 20.20, working draft study begun: 1 October 2026;\[30\]
  - 20.60, comment period closed: 16 October 2026.\[30\]
- **Related (secondary):** ISO 11226:2000 was "moved to stage 90.92 to be revised on 3 April 2026" (cerebrumedge, secondary).\[63\] The ISO/TC 159 chair's term runs "until end 2026" (ISO committee page).\[40\]

## 5. Tools

| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |
|---|---|---|---|---|---|---|
| ISO 6385 | Ergonomics principles for work systems\[64\] | 2016 (3rd ed.)\[64\] | 14 Sep 2016\[28\] | Buy from ISO or a national body | n/a | https://www.iso.org/standard/63785.html |
| ISO 10075-3 | Methods for measuring mental workload\[65\] | 2004; edition 2 at working-draft stage\[30\] | 2004 | Buy from ISO | n/a | https://www.iso.org/standard/91581.html |
| NIST AI 600-1 | Generative AI risk profile | 1.0 | July 2024 (approved by the NIST Editorial Review Board 25 Jul 2024) | Free from NIST ("This publication is available free of charge"), doi:10.6028/NIST.AI.600-1 | n/a | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf |

No software tools were sourced for this run.

## 6. Changing in the next 12 months

- **ISO 6385:2016:** its five-year review falls due in 2026, with no published outcome yet.\[28\] **Flag:** the review could revise or withdraw it within 12 months; the date is not found.
- **ISO 10075-3:2004:** it will be replaced by edition 2. The next stages are CD and DIS; no publication date was announced.\[30\]
- **ISO/TC 159:** the chair's term ends at the end of 2026.\[40\]

## 7. Common mistakes

- **Dating "bounded rationality" to 1955 or *Administrative Behavior* (1947).** The term first appears in 1957; a secondary site even states "Models of Man, in 1947". Source: SEP.\[8\]\[66\]
- **Drawing Reason's holes as fixed.** The paper says they move. Source: PMC1117770.\[2\]
- **Citing vendor percentages for the go-live dip.** "10-30%" and "20 to 40 per cent" have no field study behind them. One "412 projects" report (healthcare-industry-reviews.com) gives no methods and should not be cited.\[67\]
- **Citing Fleming et al. (HSR) for the "8%" figure.** That number is in the AHRQ summary, not the HSR abstract.
- **Treating the sunk-cost effect as universal and settled.** See the economics work and PMC12384923 cited above.
- **AI assistants:** paraphrasing Polanyi as "we know more than we can tell" (he wrote "*can* know"); inventing page numbers; and saying a standard was "confirmed in 2026" with no ISO stage evidence.

## 8. Sources and licences

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| Reason, BMJ 2000 (PMC) | © BMJ; free to read | Brief quote | Yes | n/a | Author, BMJ 2000;320:768–770 |
| Simon 1956, *Psychological Review* | © APA | Brief quote | Yes | n/a | Full citation and DOI |
| Arkes and Blumer 1985 (Elsevier) | © Elsevier | Brief quote | Yes | n/a | Full citation and DOI |
| Polanyi 1966 (Doubleday; U. Chicago Press 2009) | © publisher | Brief quote | Yes | n/a | Book and page |
| Stanford Encyclopedia of Philosophy | © SEP, all rights reserved | Brief quote | Yes | n/a | Entry, author, archive date |
| IxDF Encyclopedia chapter (Holtzblatt and Beyer) | Not verified; treat as all rights reserved | Brief quote | Yes | n/a | Authors, IxDF |
| Annett chapter (Aalto copy) | © publisher | Brief quote | Yes | n/a | Annett, *Handbook of Cognitive Task Design* |
| Fitts 1954 | © APA | Brief quote | Yes | n/a | Full citation and DOI |
| NN/g articles and posts | © NN/g | Brief quote | Yes | n/a | Nielsen, NN/g, date |
| ISO pages | © ISO; standards are paid | Stage data and brief quotes | Yes | n/a | ISO page URL and date read |
| PubMed/PMC abstracts (JACEP Open, JAMIA, J AAPOS, HSR) | Journal copyright; some open access, CC licence not verified | Brief quote | Yes | n/a | Full citation and DOI |
| AHRQ digital healthcare summary | US federal work, likely public domain (licence statement not read) | Yes | Yes | n/a | AHRQ, grant R03 HS018220 |
| NIST AI 600-1 | US federal work, "available free of charge" (doi:10.6028/NIST.AI.600-1) | Yes | Yes | n/a | NIST AI 600-1, 2024 |
| Wikipedia | CC BY-SA 4.0 | Brief quote | Yes | Share-alike would bind adapted text; avoid | Article and URL |

## 9. Not found, contested, not covered

- **Not found:**
  - CTA primary source;
  - cost in hours of each method;
  - field evidence that training, phasing or parallel running shortens the dip;
  - primary papers on full-utilization plans and their shop-floor outcomes;
  - the findings of Schultz et al. in their own words;
  - Hick (1952) and Hyman (1953) primary texts;
  - redesign studies on the cost of breaking familiarity;
  - the outcome of the 2026 review of ISO 6385;
  - standards-body guidance on neutral AI retrieval;
  - R23's filed result (could not be accessed).
- **Contested:**
  - Annett and Duncan's page range (211–221 vs 211–227);\[44\]\[45\]
  - Beyer and Holtzblatt's year (1997 vs 1998);\[10\]
  - how robust the sunk-cost effect is (psychology vs economics; vignette reliability).
- **Not covered:** cross-cultural replications of status quo bias, habit formation and trust in automation (question 6).

## Sources

1. [Brazil - Herbert A. Simon and the concept of rationality: boundaries and procedures Herbert A. Simon and the concept of rationality: boundaries and procedures](https://www.scielo.br/j/rep/a/CWfwPPVWKvLrndfxR9vYFHL/?format=html&lang=en)
2. [pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC1117770/)
3. [\[PDF\] The Psychology of Sunk Cost](https://www.semanticscholar.org/paper/The-Psychology-of-Sunk-Cost-Arkes-Blumer/e4564b88ca2349962a707b76be4c75076ad6bd43)
4. [research: R23, human factors and the limit that keeps facts unbiased by rmccann-hub · Pull Request #46 · rmccann-hub/claude-code-skills · GitHub](https://github.com/rmccann-hub/claude-code-skills/pull/46)
5. [roadmap: plan human-factors as the skill human-factor-audit was meant to be by rmccann-hub · Pull Request #45 · rmccann-hub/claude-code-skills · GitHub](https://github.com/rmccann-hub/claude-code-skills/pull/45)
6. [research: bring the eleven unrun prompts up to date before they run by rmccann-hub · Pull Request #128 · rmccann-hub/claude-code-skills · GitHub](https://github.com/rmccann-hub/claude-code-skills/pull/128)
7. [Psychological Review Vol. 63, No. :2, 1956 RATIONAL CHOICE AND THE STRUCTURE](https://pages.ucsd.edu/~mckenzie/Simon1956PsychReview.pdf)
8. [Bounded Rationality (Stanford Encyclopedia of Philosophy)](https://plato.stanford.edu/entries/bounded-rationality/)
9. [Commentary on Knowing More Than We Can Tell](https://link.springer.com/chapter/10.1007/978-3-642-00742-2_57)
10. [Contextual Design](https://ixdf.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed/contextual-design)
11. [The Swiss Cheese Model in Aviation Safety](https://bainessimmons.com/knowledge/news/blog/swiss-cheese-model/)
12. [The psychology of sunk cost](https://oamonitor.ireland.openaire.eu/rpo/rcsi/search/publication?pid=10.1016%2F0749-5978%2885%2990049-4)
13. [On the Low Reliability of Sunk Cost Vignettes](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12384923/)
14. [3 Hierarchical Task Analysis John Annett University of Warwick](https://mycourses.aalto.fi/pluginfile.php/1754492/mod_folder/content/0/Optional_reading_Task_Analysis_Annett.pdf?forcedownload=1)
15. [Impact of Health Information Technology on Primary Care Workflow and Financial Measures - 2011](https://digital.ahrq.gov/ahrq-funded-projects/impact-health-information-technology-primary-care-workflow-and-financial/annual-summary/2011)
16. [pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC3925410)
17. [The impact of adoption of an electronic health record on emergency physician work: A time motion study - PubMed](https://pubmed.ncbi.nlm.nih.gov/33598662/)
18. [EMR implementation: Big bang or a phased approach?](https://www.researchgate.net/publication/5378227_EMR_implementation_Big_bang_or_a_phased_approach)
19. [Electronic health record impact on pediatric ophthalmologists’ productivity and efficiency at an academic center - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4267903/)
20. [Impact of electronic health record implementation... : JAMIA - Journal of the American Medical Informatics Association](https://www.ovid.com/journals/jamia/abstract/10.1136/amiajnl-2011-000462~impact-of-electronic-health-record-implementation-on-patient?redirectionsource=fulltextview)
21. [(PDF) On the Interface Between Operations and Human Resource Management](https://www.researchgate.net/publication/252407219_On_the_Interface_Between_Operations_and_Human_Resource_Management)
22. [(PDF) A Study of Behavioural Perspective of Operations](https://www.researchgate.net/publication/279172038_A_Study_of_Behavioural_Perspective_of_Operations)
23. [Journal of Experimental Psychology VOL. 47, No. 6 JUNE, 1954](http://www2.psychology.uiowa.edu/faculty/mordkoff/InfoProc/pdfs/Fitts%201954.pdf)
24. [Error-rate Prediction for Mouse-based Rectangular-target Pointing with no Knowledge of Movement Angles](https://arxiv.org/pdf/2302.03103)
25. [Motor Control and Fitts's Law](https://www.textbookofusability.com/chapter/motor-control-and-fitts-law.html)
26. [Nielsen Norman Group on X: "Updated article about the 10 #Usability #Heuristics https://t.co/3a5xNQlMIu The 10 heuristics themselves remain the same (stable since 1994), but new examples and tips, plus a free set of downloadable posters. #UX" / X](https://x.com/NNgroup/status/1328745213104427011?lang=en)
27. [10 Usability Heuristics for User Interface Design](https://internet-salmagundi.com/2019/08/10-usability-heuristics-for-user-interface-design/)
28. [ISO 6385:2016 - Ergonomics principles in the design of work systems](https://www.iso.org/standard/63785.html)
29. [ISO - Meeting Calendar](https://www.iso.org/meeting-calendar.html)
30. [ISO/WD 10075-3 - Ergonomic principles related to mental workload — Part 3: Principles and requirements concerning methods for measuring and assessing mental workload](https://www.iso.org/standard/91581.html)
31. [NIST AI RMF Generative AI Profile (NIST AI 600-1) — The 12 Risks and Operationalization](https://docs.modulos.ai/frameworks/nist-ai-rmf/generative-ai-profile)
32. [NIST Generative AI Profile: AI 600-1 Explained](https://ai-alert.org/posts/nist-generative-ai-profile-600-1-explained/)
33. [Improvement Research in Education · Rational Choice and the Structure of the Environment · University of Michigan CoRE Project](http://core2.miserver.it.umich.edu/s/ire/item/3208)
34. [The Tacit Dimension (9780226672984): Michael Polanyi and Amartya Sen - BiblioVault](https://www.bibliovault.org/BV.book.epl?ISBN=9780226672984)
35. [Human Error - The Encyclopedia of Abstractions](https://abstractopedia.org/references/ref-36d6974cd2fd/)
36. [Contextual design](https://en.wikipedia.org/wiki/Contextual_design)
37. [\[PDF\] Investment in Enterprise Resource Planning: Business Impact and Productivity Measures](https://www.semanticscholar.org/paper/Investment-in-Enterprise-Resource-Planning:-Impact-Hitt-Wu/4462e6c004949d1ed46b59f1e959a1b35e55e190)
38. [Effect of enterprise resource planning implementation on organizational productivity. - Document - Gale Academic OneFile](https://go.gale.com/ps/i.do?asid=4a03a168&id=GALE%7CA212035129&it=r&p=AONE&sid=AONE&u=googlescholar&v=2.1)
39. [Special Section: Enterprise Resource Planning](https://www.jmis-web.org/articles/800)
40. [ISO/TC 159/SC 1 - General ergonomics principles](https://www.iso.org/committee/53352.html)
41. [Karen Holtzblatt](https://en.wikipedia.org/wiki/Karen_Holtzblatt)
42. [Contextual Interview - an overview](https://www.sciencedirect.com/topics/computer-science/contextual-interview)
43. [Contextual inquiry](https://en.wikipedia.org/wiki/Contextual_inquiry)
44. [Task analysis - EduTech Wiki](https://edutechwiki.unige.ch/en/task_analysis)
45. [Hierarchical Task Analysis](https://www.usabilitybok.org/hierarchical-task-analysis/)
46. [The Tacit Dimension \[Excerpt\]](https://tacit-knowledge-architecture.com/object/the-tacit-dimension-excerpt/)
47. [MP02: The impact of adoption of an electronic health record on emergency physician work: a time motion study](https://www.cambridge.org/core/journals/canadian-journal-of-emergency-medicine/article/mp02-the-impact-of-adoption-of-an-electronic-health-record-on-emergency-physician-work-a-time-motion-study/55F40B41EC64CF363534FB297D4CA102)
48. [The impact of adoption of an electronic health record on emergency physician work: A time motion study - JACEP Open](<https://www.jacepopen.com/article/S2688-1152(24)01075-0/fulltext>)
49. [The effect of electronic health records adoption on patient visit volume at an academic ophthalmology department](https://link.springer.com/article/10.1186/s12913-015-1255-8)
50. [Organizational performance effects of ERP systems usage](https://faculty.stust.edu.tw/~cwhung/Paper2.pdf)
51. [Association between evidence-based training and clinician proficiency in electronic health record use - PubMed](https://pubmed.ncbi.nlm.nih.gov/33575787/)
52. [Electronic health record (EHR) training program identifies a new tool to quantify the EHR time burden and improves providers’ perceived control over their workload in the EHR](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6952029/)
53. [How to Measure EHR Implementation Success](https://medtechsolutions.com/resource-center/blog/how-proactive-healthcare-it-support-prevents-costly-system-failures/&gsessionid=klsMn_0KRewqj4cH1lCbZo4MT9QwC15Svmdo7_P83aJH_fXAKSlVXQ/)
54. [EHR Adoption Problems: The One You Can Fix](https://assimasolutions.com/resources/blog/ehr-adoption-problems-hospitals/)
55. [The OM/HR Interface.](https://www.researchgate.net/figure/The-OM-HR-Interface_fig1_37149369)
56. [(PDF) Bodies of Knowledge for Research in Behavioral Operations](https://www.academia.edu/11603457/Bodies_of_Knowledge_for_Research_in_Behavioral_Operations)
57. [(PDF) The deployment of temporary production workers in assembly operations: a case study of the hidden costs of learning and forgetting](https://www.academia.edu/15129909/The_deployment_of_temporary_production_workers_in_assembly_operations_a_case_study_of_the_hidden_costs_of_learning_and_forgetting)
58. [Fitts' Law](https://www.yorku.ca/mack/hhci2018.html)
59. [Method and system for implicitly resolving pointing ambiguities in human-computer interaction (HCI)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6907581)
60. [10 Usability Heuristics for User Interface Design (Error prevention)](https://cx.dsb.gov.au/overview/references/references/10bf1af016ea8001831cdfff23dea916)
61. [Nielsen's 10 Usability Heuristics, With Examples - UX Academy](https://myuxacademy.com/blog/nielsens-10-usability-heuristics/)
62. [Nielsen's 10 Usability Heuristics](https://www.humanstandards.org/interaction-patterns/nielsen-heuristics/)
63. [ISO ergonomics standards: the complete 2026 framework](https://cerebrumedge.com/blog/entry/iso-ergonomics-standards-guide)
64. [INTERNATIONAL STANDARD ISO 6385](https://cdn.standards.iteh.ai/samples/63785/29a50db0a6d048208c063c308b21f500/ISO-6385-2016.pdf)
65. [ISO 10075-3:2004 - Ergonomic Principles for Mental Workload Assessment Methods](https://standards.iteh.ai/catalog/standards/iso/71355f1a-4b0e-4ba7-8f52-f25ca55fdb02/iso-10075-3-2004)
66. [ModelThinkers - Satisficing](https://modelthinkers.com/mental-model/satisficing)
67. [EHR Implementation Cost Overrun Statistics: 2026 Report — HIR Research](https://www.healthcare-industry-reviews.com/research/ehr-implementation-cost-overrun-statistics-2026/)
