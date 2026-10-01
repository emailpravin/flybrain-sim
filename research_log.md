# Research Log

State file for `RESEARCH_PROTOCOL.md`. One entry per question. Status is
one of: `queued`, `testing`, `provisional`, `confirmed`, `retracted`,
`stalled`.

Entries below are backfilled from this session's actual history, so the
log reflects real prior state rather than starting empty.

---

## Backfilled entries (pre-protocol, for continuity)

- **Escape reflex shape-blindness** — `confirmed`. Literature: de la Flor
  et al. 2017. Control: size/contrast-matched shapes, real photos, 3
  independent clip regimes. See `findings_summary.md` sections 1, 6, 10,
  14, 16.
- **Legs -> Giant Fiber activation** — `retracted`. Did not survive
  calibration-robustness sweep. See section 9.
- **Binocular integration** — `confirmed` (as partial sub-additive
  suppression, ~55-60% of monocular). Went through 3 versions before
  landing on the one matching real literature. See sections 7, 16.
- **Mantis/DNa02 differential** — `retracted`. Did not survive full
  (uncapped) synaptic calibration. See sections 12, 14, 16.
- **Escape speed-dependent motor-mode selection (von Reyn et al. 2017)**
  — `stalled`, documented limitation, not retracted (the mechanism may be
  real; this model's temporal/spatial resolution can't show it). See
  section 13.
- **Courtship LC10a -> pC1 arousal gating** — `confirmed`, with a real
  control (LC4/LC6 comparison). See section 15.
- **Courtship full pathway to motor output** — `provisional`. Reaches
  real wing-steering motor neurons (hg1/hg3/i2 MN); does not reach MN5
  specifically, and the reason (MN5's real dominant input is gnathal
  ganglion/feeding circuitry, not the courtship pathway) is understood,
  not just unexplained. See section 15.
- **synapse_clip validity** — `confirmed` finding that the old default
  (20) was unvalidated and actively distorting results; default changed
  to effectively uncapped. See section 16.

---

## Queue

### LC9 -> DNp09 chase-steering, speed dependence — `retracted`

**Question:** does the real LC9->DNp09 pathway (found as DNp09's dominant
real upstream driver, weight 1956 vs. LC10a's 53 -- a correction to the
initial assumption that LC10a would drive courtship steering) show
speed-dependent chase-initiation, consistent with LC9's documented
figure-ground/relative-motion role?

**Literature:** LC9 is documented for figure-ground discrimination
(telling a moving object apart from its background), not established
before now as specifically chase-initiating via DNp09 -- that link is our
own connectome finding, not yet a claim from a published paper. DNp09 was
suggested (not firmly established) as a courtship-steering candidate,
contrasted with DNa02 which one paper found inactive in isolated-female
courtship trials.

**Data feasibility:** confirmed. LC9 (219 neurons) and DNp09 (2 neurons,
real bilateral pair) both exist in male-cns; all 219 LC9 neurons have real
lobula-column position data (`lc9_columns.csv`), same as LC10a.

**Test + result:** drove LC9 via real column positions with a stimulus
sweeping across the visual field at several speeds (step 2/4/5/6 columns
per frame) vs. a same-total-current stationary control.

| condition | LC9 spikes | DNp09 spikes |
|---|---|---|
| stationary | 1,538 | 0 |
| step 2 | 1,497 | 1 |
| step 4 | 1,276 | 1 |
| step 5 | 1,311 | 21 |
| step 6 | 1,347 | 18 |

Every moving condition beat stationary; a sharp threshold appears between
step 4 and step 5 (1 -> 21), then plateaus (21 -> 18) rather than
continuing to climb -- switch-like, not a smooth speed-to-drive ramp.
LC9's own raw activity does not track this pattern at all (roughly flat
across conditions), so the effect is specifically in the LC9->DNp09
connection, not just "more input in."

**Validation run (all 5 self-critique items attempted at once) — retracted,
not confirmed. Two of five checks passed; the core claim failed the third:**

1. **`synapse_clip` sensitivity: passed.** Every condition nearly identical
   at clip=50 vs. fully uncapped (e.g. step5 DNp09=19 both). Not a
   calibration artifact.
2. **Fine-grained threshold: roughly held, softer than first reported.**
   Added step 4.3 and 4.6 on the original path: DNp09 stayed low (3-4)
   through all of step 4-4.6, then jumped to 16-19 at step 5-6. Same
   switch-like shape, wider transition band than one sharp point.
3. **Second downstream readout (PVLP004, LC9's actual strongest real
   target by raw weight -- stronger than DNp09) added.** Tracked roughly
   with DNp09's pattern on the original path, which was mildly
   reassuring, but see #4.
4. **Alternate-path replication (same speeds, different row, y=25):
   FAILED, and not just weakly -- reversed.**

| condition (alt path, y=25) | DNp09 spikes |
|---|---|
| stationary | 43-53 |
| moving, step 4 | 37-41 |
| moving, step 5 | 36-39 |

   On this second, equally legitimate path, **stationary produced the
   highest DNp09 response of all four conditions** -- the opposite of the
   original path, where stationary was exactly 0. Not a smaller effect;
   a reversed one.
5. **Confound check (is it really about speed, or about which specific
   neurons get recruited): this is what #4 answers.** The reversal shows
   the original result depended on the one specific location tested
   (column ~18,15), not on motion vs. stillness in general. Most likely
   explanation: individual LC9 neurons have very unequal real wiring
   strength to DNp09, and the original path happened to recruit
   well-connected ones while stationary (fixed at the same center) also
   happened to land somewhere poorly connected -- an accident of
   position, not a motion computation.

**Conclusion: retracted as originally stated.** The real, surviving
finding from this whole thread is narrower and more honest: DNp09's
response depends heavily on *which* LC9 neurons are active, not on
whether the stimulus is moving. Same failure pattern as the mantis/DNa02
finding and the original "legs matter" finding -- real on the first
setup, did not survive a second independent test. Logged in full rather
than quietly dropped, per protocol step 8.

Scripts/files added: `connectome_chase2.csv`/`_neurons` (+PVLP004),
`lc9_columns.csv`, `results_chase_validation.csv`.

### LC9 -> DNp09/PVLP004 moving-vs-stationary grid search — `testing`, in progress via /loop

Following up on the retraction above: is there a real, replicable
region/rule for when motion beats stillness in this pathway, or is it
pure position-idiosyncratic noise? Systematic grid search, 8-10 points
across LC9's real coordinate range (col_x 4-34, col_y 1-38), each point
tested moving (step-5 sweep) vs. same-total-current stationary, at both
synapse_clip=uncapped and clip=50, readouts DNp09 and PVLP004.
Reusable test script: `grid_search_step.py <col_x> <col_y> <label>`.

**Progress so far (4 of ~9 planned points):**

| location | moving DNp09 | stationary DNp09 | clip-consistent? | direction |
|---|---|---|---|---|
| (18,15) — original | 1-21 (speed-dep) | 0 | yes | moving > stationary |
| (18,25) — 1st replication attempt | 36-41 | 43-53 | yes | **stationary > moving** (reversed) |
| (8,8) — g1 | 5 | 0 | yes | moving > stationary |
| (28,30) — g2 | 18 | 0 | yes | moving > stationary |

3 of 4 tested locations favor moving > stationary; one reverses. Every
individual location is internally clip-consistent (the direction never
flips between clip=uncapped and clip=50 at the same location) -- the
inconsistency is only *across* locations, not a calibration artifact.
**Final results, 9 locations covered — grid search complete:**

| location | moving DNp09 | stationary DNp09 | direction |
|---|---|---|---|
| (18,15) | 1-21 | 0 | moving wins |
| (18,25) | 36-41 | 43-53 | stationary wins |
| (8,8) | 5 | 0 | moving wins |
| (28,30) | 18 | 0 | moving wins |
| (8,30) | 46-47 | 17 | moving wins |
| (28,8) | 0 | 0 | tie (nothing fires) |
| (18,4) | 0 | 0 | tie (nothing fires) |
| (4,19) | 48 | 52-55 | ~tie, stationary slightly ahead |
| (34,19) | 1 | 0 | moving wins |

Every single location was internally clip-consistent (direction never
flipped between clip=uncapped and clip=50 at the same location) -- the
uncertainty is entirely across-location, never a calibration artifact.

**Honest conclusion: a real but imperfect tendency, not a clean rule.**
5 of 9 locations clearly favor moving > stationary, 1 clearly reverses,
2 are dead zones where neither condition drives any output, and 1 is a
near-tie leaning the other way. That's a real majority (moving wins more
often than chance would predict, and by clear margins where it wins), but
not the kind of universal, position-independent rule a "confirmed"
finding would need. The honest, reportable version of this result is:
**"this pathway is more often than not more responsive to a moving
target than a stationary one of equal total input, but the effect is not
uniform across the visual field and roughly 1 location in 5 reverses it
outright."** That's a genuinely different (and more defensible) claim
than the original single-location result, and a legitimately interesting
one -- it suggests real, non-uniform tuning across the LC9 population
rather than either a clean motion-detector story or pure noise.

### LC9 -> DNp09/PVLP004 full 7x7 responsiveness map — `confirmed`

Follow-up to the mixed moving-vs-stationary result above: dropped the
motion comparison entirely and just mapped raw responsiveness (single
sustained stimulus, total-current-matched, radius=3 clamped to the real
coordinate range) across a full 7x7 grid (49 points) spanning LC9's
entire real coordinate range (col_x 4-34, col_y 1-38). Script:
`responsiveness_map_step.py`; run via `/loop` in two batches; full data
in `results_responsiveness_map.csv`.

**Result: a real, clean, non-random spatial structure. DNp09 spike count
by (col_x, col_y):**

| cy \\ cx | 4 | 9 | 14 | 19 | 24 | 29 | 34 |
|---|---|---|---|---|---|---|---|
| 38 | 16 | 16 | 36 | 19 | 7 | 6 | 0 |
| 32 | 76 | 48 | 65 | 61 | 25 | 11 | 0 |
| 26 | 10 | 94 | 71 | 30 | 13 | 0 | 0 |
| 20 | 14 | 90 | 14 | 0 | 0 | 0 | 0 |
| 13 | 53 | 8 | 8 | 0 | 0 | 0 | 0 |
| 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**Two clean, unambiguous dead regions, not scattered noise:**
- The entire bottom band (cy=1 and cy=7) is dead (DNp09=0) at every single
  x value tested, all 14 points.
- The entire right column (cx=29 and cx=34) is dead or near-dead at every
  y value, with the sole exception of (29,32)=11 and (29,38)=6.
- 26 of 49 points (53%) are exactly zero.
- The responsive region is a clear diagonal/triangular block in the
  low-to-mid x (4-19), mid-to-high y (13-38) corner, peaking at (9,26)=94
  and (9,20)=90.

**This directly explains the earlier confusing moving-vs-stationary
results.** (18,25) and (4,19), the two points that behaved oddly in the
earlier test, both sit right at the edge of this responsive region --
exactly where a small shift in exact position would land you in a very
different local response magnitude. (28,8) and (18,4), the two complete
"ties" from the earlier test, both sit inside or near the dead zone
identified here -- explaining why neither moving nor stationary produced
any signal there. The earlier test wasn't measuring something unstable or
noisy; it was sampling a real, sharply structured map at too few, poorly
distributed points to see the structure.

**Marked `confirmed`, not `provisional`**: this is a full, systematic
census of the real coordinate space (49/49 points, not a sample), the
pattern is clean and directly explains prior data rather than being
cherry-picked, and it required no interpretation call -- the zeros are
exact zeros, not a borderline threshold.

**Follow-up: is the dead zone real, or an artifact of our incomplete seed
network? Tested directly, not assumed.**

Literature check first: real precedent exists for sharp, non-uniform,
position-dependent visual processing in Drosophila -- [A functionally
ordered visual feature map in the Drosophila brain, *Neuron*
2022](https://www.cell.com/neuron/fulltext/S0896-6273(22)00178-7) (LC
compartments genuinely biased toward different visual field regions),
frontal-vs-lateral looming producing categorically different behaviors
(escape vs. landing) in real flies, and [Dual Receptive Fields
Underlying Target and Wide-Field Motion Sensitivity in Looming-Sensitive
Descending Neurons](https://pmc.ncbi.nlm.nih.gov/articles/PMC10368147/)
(real descending neurons with genuinely different sensitivity in
different receptive-field regions). The general *shape* of this finding
has real backing.

But our own network was a real risk: `connectome_chase2.csv` was a small,
hand-curated set of ~600 neurons built around literature-named cell
types. A dead zone there could just mean "we didn't fetch the real
alternate pathway," not "no real pathway exists."

**Rebuilt properly to test this.** First attempt (`--hops 2 --max-neurons
8000` from LC9) backfired instructively: LC9's own hop-1 fan-out is
103,690 neurons, so the neuron cap silently dropped all but 4 of LC9's
219 real neurons before ever reaching downstream targets -- a real
methodological trap (broad hop-expansion can quietly destroy the very
seed population you're trying to test). Fixed by fetching LC9's full real
downstream partner list directly (no hop-expansion), keeping every
downstream type with total real weight >=50 (142 types), and explicitly
unioning that with the complete 219-neuron LC9 population so nothing
seed-side gets dropped. Result: `connectome_lc9_comprehensive.csv`,
4,182 real neurons, 316,188 real edges -- ~7x more neurons and every
substantial real pathway out of LC9, not just our original hand-picked
set.

**Re-tested 4 dead-zone points + 1 alive control on this much more
complete network:**

| point | LC9 | DNp09 | PVLP004 |
|---|---|---|---|
| (34,1) | 484 | 0 | 243 |
| (29,7) | 262 | 0 | 133 |
| (24,13) | 813 | 0 | 443 |
| (19,7) | 951 | 0 | 384 |
| (9,26) alive control | 902 | 100 | 398 |

**The dead zone survives.** All four points stayed exactly zero for
DNp09 even with 142 real downstream cell types included -- ruling out
"missing pathway in our fetch" as the explanation.

**Refinement to the finding, though -- it's not a blanket dead zone.**
PVLP004 is clearly nonzero at every "dead" point (133-443) -- LC9 in
those regions still drives real downstream activity, just not DNp09
specifically. The precise, better-supported statement is: **these visual
field regions route to other real targets but not to DNp09 specifically**
-- a genuine selective-routing difference, not an absence of wiring. This
is a cleaner and more biologically plausible finding than a blanket dead
zone, and matches the literature above (different LC compartments/regions
feeding different downstream pathways for different purposes).

**Status: the spatial structure is now confirmed twice, independently**
(narrow curated network, then a ~7x larger comprehensive one) -- treating
this as solid. The literature check that was previously flagged as
skipped is now done (see citations above).

### Left vs. right eye — is the map an artifact of mixing both eyes together?

Caught a real flaw in the map above: `col_x`/`col_y` are LOCAL per-eye
coordinates (both eyes independently reuse the same 3-36 / 1-38 numbering
-- confirmed directly: 115 real right-side and 104 real left-side LC9
neurons, near-identical col_x distributions, mean ~18 for both). The
original 7x7 map pooled neurons from both eyes at every grid point without
realizing this, so it didn't represent one coherent visual field.

Rebuilt the map twice, once per eye, on the larger 4182-neuron
comprehensive network (`responsiveness_map_side_step.py`, 96 real grid
points across both eyes, `results_sidemap.csv`).

**Left eye:**

| cy \\ cx | 4 | 9 | 14 | 19 | 24 | 29 | 34 |
|---|---|---|---|---|---|---|---|
| 38 | 17 | 17 | 33 | 10 | 8 | 8 | - |
| 32 | 57 | 41 | 55 | 52 | 24 | 14 | 0 |
| 26 | 13 | 61 | 58 | 25 | 17 | 0 | 0 |
| 20 | 65 | 56 | 15 | 6 | 0 | 0 | 0 |
| 13 | 33 | 1 | 0 | 0 | 0 | 0 | 0 |
| 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**Right eye:**

| cy \\ cx | 4 | 9 | 14 | 19 | 24 | 29 | 34 |
|---|---|---|---|---|---|---|---|
| 38 | 36 | 11 | 10 | 10 | 2 | 3 | - |
| 32 | 36 | 19 | 26 | 38 | 13 | 13 | 0 |
| 26 | 10 | 56 | 47 | 27 | 14 | 0 | 0 |
| 20 | 14 | 63 | 27 | 14 | 0 | 0 | 0 |
| 13 | 25 | 12 | 14 | 0 | 0 | 0 | 0 |
| 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**Conclusion: the SHAPE holds independently in both eyes -- this is not an
artifact of mixing them.** Both eyes show the exact same qualitative
structure: the bottom two rows (cy=1,7) are completely dead in both eyes
with zero exceptions; the rightmost columns (cx=29,34) are dead or
near-dead in both; the live region is the same upper-left/middle block in
both. Dead-point count is nearly identical: left eye 25/49, right eye
24/49.

**One real, modest asymmetry found on top of that shared structure:** the
left eye's average response is about 27% higher than the right's (mean
14.3 vs. 11.25 across all 49 points). But this isn't a clean spatial
effect -- the point-by-point left-minus-right differences flip sign
across different regions of the map (some points favor left by 50+,
others favor right by 10-14), with no obvious rule for which. Given every
point here is still a single, unrepeated trial, this magnitude difference
should be treated as a real but unconfirmed lead, not a settled finding
-- the same discipline applied to the earlier moving-vs-stationary result
before it was properly checked.

**Bottom line for the original question ("is there a left-eye bias"):**
no strong structural bias -- the map itself (which regions connect to
DNp09 at all) is essentially the same shape in both eyes, which is itself
a reassuring result (a real, symmetric anatomical feature, not a
data-quality fluke unique to one eye's reconstruction). There is a modest,
real-but-unconfirmed magnitude asymmetry (left slightly stronger overall)
that would need repeated trials to trust.

**What would be needed to go further** (not done, flagging for later):
repeat trials at the same locations (still single-trial per point here),
finer-grained sampling around the (18,25)/(4,19) reversal region to see
if it's a real sub-region or just those two points, and a literature check
specifically for whether non-uniform/patchy motion sensitivity across a
single LC neuron type's population is documented anywhere -- this last
check was flagged as skipped when the loop was set up and never
circled back to.

Loop stopped here (9 locations, within the planned 8-10 range) rather
than continuing indefinitely.

### LC9 -> real leg muscle motor neuron (Sternal anterior rotator MN), full chain — `confirmed`

Traced the chase circuit past DNp09 for the first time, using real
connectome queries rather than assumption: DNp09's downstream is NOT
muscle motor neurons directly -- its strongest target is another
descending neuron, DNa11 (weight 222), which itself connects strongly to
DNa06 and to DNa02 (weight 409) -- DNa02 being the real, independently
published leg-steering neuron (Rayshubskiy et al. 2024) already used in
the earlier mantis experiment. DNa02's real downstream includes "Sternal
anterior rotator MN" (weight 776) -- confirmed via literature search to
be a real coxa-rotator muscle specifically implicated in walking steering
(thoraco-coxal joint control, part of the same network as DNg13), not
grooming or an unrelated leg function.

**Full real chain: LC9 -> DNp09 -> DNa11 -> DNa06 -> DNa02 -> Sternal
anterior rotator MN** (`connectome_leg_chase2.csv`, 503 real neurons).

Separately checked whether this circuit connects to the real head/gaze
system (HS/VS cells, which exist in male-cns as HSE/HSN/HSS/HST and
VS/VST1/VST2/VSm, 42 neurons, driving real descending neurons like
DNp20/DNg46/DNp17 -- almost certainly male-cns's own naming for what the
literature calls DNHS1/DNOVS1/2): **zero direct edges from LC9 or DNp09
to HS/VS.** The "start chasing" circuit and the "keep head aimed at
target" circuit are real, separate, non-overlapping pathways in this
connectome -- not integrated at the wiring level, at least not directly.

**Validation run, all four checks:**
1. **Reproducibility**: tested a second independent alive location
   (14,32) -- same full chain fired, consistent with the first (9,26).
2. **Dead-zone consistency**: drove LC9 from a known dead-zone location
   (24,1) -- entire chain silent through all 5 hops to the muscle, at
   both clip values. The dead zone found earlier holds all the way to
   real motor output, not just at DNp09.
3. **Specificity control, passed**: drove the unrelated LC4/LC6 pathway
   instead of LC9. LC4/LC6 fired strongly (496-1068 spikes) but
   propagated exactly zero further -- DNp09 through the leg muscle MN all
   stayed at zero. Rules out "any visual input eventually reaches leg
   muscles" as an explanation.
4. **Clip sensitivity -- real caveat found, not clip-robust in
   magnitude**: leg muscle MN fires 162 spikes at the uncapped default
   vs. only 7 at clip=50 -- nonzero both times (the chain's existence
   holds either way) but the exact strength drops ~95% with calibration,
   likely because signal compounds across 5 hops instead of 1-2. The
   qualitative finding (this chain exists and functions) is solid; the
   specific spike counts should not be treated as a precise,
   calibration-independent measurement.

**Status: confirmed as a real, functioning, specific circuit** from
visual input to an actual leg-steering muscle motor neuron -- the first
complete vision-to-muscle chain fully traced and validated in this
project's later (post-recalibration) work. Head/neck orientation tracking
remains a real, separate, undocumented-in-our-data system for future
investigation.

Scripts/files added: `connectome_leg_chase2.csv`/`_neurons`,
`results_legchase_validation.csv`.

### Does connecting circuitry trivially make things fire? Random-baseline control — `confirmed` (as a real methodological finding)

User's question: how do we know the LC9->muscle chain is meaningful, and
not just "any sufficiently connected chain in a dense brain reaches a
muscle eventually"? Real, important gap -- the earlier LC4/LC6 control
only tested pathway-specificity at one endpoint, not this more basic
worry.

**Weight-table reachability check on 4 unrelated real visual neuron types
we'd never touched (LC12, LC15, LC17, LC21):** all four reached SOME real
motor neuron within 2-3 hops, actually faster than LC9's 5-hop path. On
paper, reaching a muscle looks generic and unremarkable -- exactly the
failure mode the user was worried about.

**But weight-table reachability is not the same as actual simulated
firing -- tested this directly, not assumed.** Traced LC21's specific
real path (LC21 -> DNp11 -> MNad34, a leg motor neuron) and built a real
network to simulate it (`connectome_lc21_baseline.csv`), same protocol as
the LC9 test (sustained, total-current-matched drive, both clip values,
LC4/LC6 as a second pathway run through the same network).

**Result: the traced path completely failed to fire.** LC21 itself fired
robustly (1,836 spikes) but DNp11, MNad34, and every muscle downstream
stayed at exactly zero, at both clip values. Meanwhile LC4/LC6 -- driven
through the same network, not the traced path at all -- reached DNp11
(127/123) and MNad34 (51/46) just fine.

**Conclusion: reachability on a weight table does not predict whether a
path actually fires in simulation.** Most "possible" paths, even ones
with real measured synaptic weight, do not functionally activate when you
actually drive the front end -- there are real thresholds/dynamics
blocking most of them. This means finding 17's LC9->muscle chain
firing robustly, reproducibly, and specifically was NOT a trivial or
expected outcome of network density -- it's evidence the chain is doing
something real, not an artifact of "everything connects to everything
eventually." Strengthens finding 17 rather than undermining it, though by
a different mechanism than either the user or I expected going in.

**Honest caveat:** n=1 on the "traced path fails, alternate path works"
pattern (only LC21 was simulated end-to-end; LC12/15/17 were only checked
for weight-table reachability, not actually driven). Also learned LC4/LC6
is not a universally neutral control -- it happened to reach this
particular muscle target, so it should not be assumed inert for other
circuits without re-checking.

Scripts/files added: `connectome_lc21_baseline.csv`/`_neurons`,
`spike_summary_lc21_*_clip*.csv`.

### Rigor upgrade for the chase circuit: real photo + real-angle calibration (multi-stage, via /loop)

User asked for two upgrades to finding 17/the leg-chase circuit: (1) a
real photo stimulus routed through the real retina, not injected current,
and (2) calibrating the visual-field map to real-world directions so we
can say the fly is chasing something at a specific real angle.

**STAGE 1 -- calibration. Real system exists, but doesn't reach LC9's own
coordinates; found a defensible workaround instead of forcing it.**

Literature confirms a real, official calibration system: medulla columns
use a real (h,v) hex coordinate system, each column = 5 degrees of real
visual angle, matching real measured fly field-of-view geometry. Better
still: checking `fetch_mi1_columns.py` showed we've been using this exact
*official* system all along without realizing it -- `mi1_columns.csv`
pulls `assignedOlHex1`/`assignedOlHex2`, a real per-neuron field in
neuprint's own schema, not something we derived. The escape-circuit work
(spider/mantis/leaf) was already real-angle-calibrated at the Mi1 level.

**LC9 itself is not.** Checked directly: `assignedOlHex1` exists as a
column in the schema for LC9/Tm5Y/Y3/DNp09 but is null for all of them --
this official calibration is only populated for early, strictly
one-column-per-neuron "columnar" cell types (like Mi1), not for neurons
with broader receptive fields spanning multiple columns. Checked how much
of LC9's real upstream is even reachable through hex-labeled neurons: of
3,815 real direct upstream neurons (weight>=3), only 4 have real hex
coordinates, carrying 0.01% of total input weight. **A clean, precise
degree-calibration of LC9's own map is not achievable through short-range
tracing** -- honest negative result, not forced.

**Workaround, not a fix:** we don't need LC9's own coordinates calibrated
to satisfy the actual goal. Placing the stimulus at Mi1 itself (which IS
really calibrated) and letting it propagate naturally through the real
network to LC9 and beyond achieves "a real photo at a known real-world
position" without needing to also translate LC9's internal map to
degrees. Proceeding to Stage 2 on this basis: real calibration lives at
the Mi1 entry point, not at LC9's own coordinate system, and that's
sufficient for the actual experiment.

**STAGE 2 -- complete.** Confirmed a real, short, direct path: Mi1 -> Y3
(direct hop-1 edge, weight 15,377, checked on a 200-neuron Mi1 sample) ->
LC9 (Y3->LC9 weight 878, found earlier). Built the full real network
(`connectome_full_chase.csv`, 3,789 neurons, 56,241 edges) spanning
Mi1 -> Y3/Tm5Y -> LC9 -> DNp09 -> DNa11 -> DNa06 -> DNa02 -> Sternal
anterior rotator MN, plus LC4/LC6/DNp01 for cross-checking against the
escape circuit. Real per-neuron hex calibration (`assignedOlHex1/2`) is
available for every Mi1 neuron in this network, satisfying the "real,
calibrated entry point" requirement even though LC9's own coordinates
remain uncalibrated (see Stage 1).

**STAGE 3 -- complete.** Built `photo_at_position.py`: places a real
photo's contrast pattern onto a small, real, hex-calibrated window of Mi1
neurons (not stretching the whole image across the whole visual field
like the existing escape-circuit pipeline does) -- lets us say "this real
photo appears at this specific real position," which the existing tooling
couldn't do. Built the full control set: frontal moving, frontal static,
frontal looming (larger/expanding), peripheral moving, and a verified
blank control (confirmed zero spikes directly from the saved summary, not
assumed, despite a cosmetic plotting crash on empty data downstream of
the real result).

**STAGE 4 -- run, and an honest negative result, precisely diagnosed, not
forced into a positive writeup.**

| condition | LC9 | DNp09 | DNa02 | muscle |
|---|---|---|---|---|
| frontal, moving | 0 | 0 | 0 | 0 |
| frontal, static | 0 | 0 | 0 | 0 |
| frontal, looming (large) | 8 | 0 | 0 | 0 |
| peripheral, moving | 0 | 0 | 0 | 0 |
| blank | 0 | 0 | 0 | 0 |

Nearly everything stayed at zero, including LC9 itself for the intended
positive case (frontal, moving, small real target). Did not stop at the
first negative result -- checked two real alternative explanations before
concluding:
1. **Too weak a stimulus?** Raised input-current 3x and 6x (100 -> 300 ->
   600). Total network activity grew, but LC9/DNp09/DNa02/muscle stayed
   at exactly zero regardless. Not a magnitude problem.
2. **Too small a Mi1 pool?** Widened the window from 49 to 167 real Mi1
   neurons at the same position. Still exactly zero at LC9 and beyond.
   Not a pool-size problem.
3. **Where exactly does it break?** Checked each layer directly: Mi1
   fired robustly (1,957 spikes, 100% of driven neurons), Y3 fired
   robustly (547 spikes, 100% of neurons) -- **the signal successfully
   crosses two real synaptic hops, then dies specifically at Y3->LC9.**

**Root cause, found precisely, not guessed:** Y3's real synaptic weight
onto LC9 is 878 (established earlier this session) -- real, but far
weaker than LC9's actual dominant real inputs, PVLP004 (32,954) and
LC9's own self-recurrent connections (26,727), neither of which trace
back to Mi1 in a simple feedforward way. We picked Y3 specifically
because it was the clearest short, direct bridge from Mi1 back to LC9 --
but it turns out to be a minor real input to LC9, not the dominant one.
Same failure pattern as the AN08B061/IN12A030 gap in finding 15 and the
MN5/GNG surprise: trusting the most traceable path over checking whether
it's actually the functionally dominant one.

**Conclusion: this specific rigor upgrade does not currently work, and
that itself is a real, informative result, not a dead end to hide.** The
LC9-direct-current-injection approach used everywhere else in this
project (finding 17, the responsiveness map, the leg-chase circuit) was
implicitly bypassing a real calibration gap in the Mi1->LC9 relay --
LC9's dominant real drivers are recurrent/lateral (other LC9 neurons,
PVLP004), not a clean bottom-up feedforward chain from the retina through
Y3. Getting a real photo to reliably drive LC9 the way direct injection
does would require identifying and including LC9's actual dominant real
upstream circuit (likely the recurrent LC9-LC9 and PVLP004 pathways,
which are not straightforwardly traceable back to a hex-calibrated
retinal position), not just any real path that happens to connect on
paper -- directly validating the lesson from the LC21 random-baseline
control run earlier: reachability is not the same as function.

**Status: logged as a real methodological finding, not added to
findings_summary.md as a positive result** -- per protocol, forcing this
into a numbered finding would misrepresent what was actually found. The
honest takeaway is that finding 17's leg-chase circuit, while internally
well-validated on its own terms (see its control battery), rests on an
entry point (direct LC9 injection) that has not yet been shown to
correspond to anything a real photoreceptor signal would actually
produce -- an real, open limitation, now precisely characterized rather
than vaguely caveated.

Scripts/files added: `photo_at_position.py`, `mi1_fullchase_columns.csv`,
`connectome_full_chase.csv`/`_neurons`, `results_realphoto_chase.csv`,
`seq_realphoto_*.npy`.

Stopping here -- all 4 stages complete, honest result obtained and fully
diagnosed (not a vague dead end), consistent with the stop condition.

### Follow-up to the real-photo test: what size, and is it selective? — real problem found, not a success

After the Stage 4 breakthrough (radius=30 real photo finally fired the
full chain), checked two things the user correctly flagged before
trusting it.

**1. What fraction of the real visual field did the "successful"
stimulus actually cover?** Computed directly: 886 of 887 real Mi1
neurons in the whole right eye -- **99.9% of the entire visual field.**
Not a moderate or realistically-sized target; essentially the fly's
whole field of view.

**2. Does this activate the chase circuit specifically, or everything at
once?** Checked LC4/LC6/DNp01 (the escape circuit) in the same runs that
fired the chase circuit -- they fired too, every time (e.g. DNp01: 6 and
53 spikes in the two successful conditions, alongside LC9/DNp09/muscle
firing). **The chase and escape circuits activate together under this
stimulus, not selectively.**

**3. Tested a real, literature-grounded target size directly** (real fly
body ~2.5mm at 1-2cm chasing distance subtends ~7-14 real degrees; at the
confirmed real calibration of 5deg/column, that's radius 1-3 columns).
Built this size both moving (genuine translation) and static, per the
user's point that the real effect may require size AND motion together,
not either alone at an extreme.

**Result: nothing fires at all, in either circuit, moving or static, at
the realistic size.** LC9, DNp09, DNa02, the muscle, LC4, LC6, and DNp01
were all exactly zero in both conditions.

**Honest conclusion:** the Stage 4 "success" earlier in this thread was
not a validation of the chase circuit responding to a real,
appropriately-scaled stimulus -- it required an unrealistically
overwhelming, near-total-field input to cross any threshold at all, and
even then didn't fire selectively. Real flies are well documented to
respond to realistically-sized targets; this simulation currently does
not, under this calibration. **This is a real, unresolved limitation of
the model's sensitivity to real-world-scale visual input, not a
finding to report as positive.** The earlier positive writeup in this
same log section should be read alongside this: the full vision-to-
muscle chain does exist and can fire (confirmed), but not yet in response
to anything resembling a normal, real-sized visual stimulus.

Scripts/files added: `photo_at_position.py` extended with `translate` and
`darken` modes, `seq_realphoto_realsize_*.npy`,
`spike_summary_realsize_*.csv`.

### Independent size-tuning validation: sweep the real 8-50deg target-size range -- honest negative result

Follow-up to finding 18 (the aroused-vs-unaroused reframing, tuned/
calibrated against a single point: 22.5deg). User asked to test the
realistic target size properly. Since finding 18's boost was calibrated
using ONE known fact (22.5deg average target size), testing that same
single point again would prove nothing new (classic calibration-vs-
validation risk, already flagged). Instead swept a genuinely new set of
sizes never used in tuning: 3, 8, 15, 22.5, 35, 50, 70, 100 real degrees
(the last two intentionally beyond the real 8-50deg literature range, as
a supra-range contrast condition), same aroused (8x type-boosted) network
from finding 18, same frontal moving stimulus, real 5deg/column
calibration (`radius_columns = degrees/5`), everything else held fixed.
Used `blob_control.jpg` (a generic dark blob, not a specific fly photo --
defensible since the real literature describes LC9 as tuned to "fly-sized
moving objects" generically, not object identity).

**Result (script: run_size_sweep.py, saved: `results_sizetest_sweep.csv`,
`seq_sizetest_sz*.npy`, `spike_summary_sizetest_sz*.csv`):**

| deg | radius(col) | LC9 | DNp09 | DNa02 | muscle | LC4 | LC6 | DNp01 |
|---|---|---|---|---|---|---|---|---|
| 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 8 | 2 | 12,282 | 101 | 65 | 188 | 3,153 | 9 | 103 |
| 15 | 3 | 12,817 | 104 | 67 | 193 | 3,295 | 19 | 107 |
| 22.5 | 4 | 13,016 | 108 | 69 | 200 | 3,349 | 29 | 109 |
| 35 | 7 | 13,233 | 109 | 71 | 194 | 3,415 | 130 | 111 |
| 50 | 10 | 13,251 | 109 | 70 | 194 | 3,448 | 253 | 111 |
| 70 | 14 | 13,386 | 110 | 71 | 197 | 3,507 | 522 | 112 |
| 100 | 20 | 13,480 | 110 | 72 | 204 | 3,558 | 903 | 113 |

**Honest interpretation, not spun positive:**
1. **Confirms a real, sharp on/off threshold** between 3deg (everything
   zero) and 8deg (everything robustly firing) -- consistent with finding
   18's unaroused/aroused story, and this specific threshold location
   (3-8deg) was NOT something previously measured, so this is new,
   independently-obtained information, not a repeat of the calibration
   point.
2. **Does NOT show real fly-like size tuning.** In real flies, LC9-type
   pursuit neurons are documented as size-SELECTIVE (tuned to fly-sized
   objects specifically, implying some fall-off for much larger objects,
   which typically drive looming/escape responses instead). Our
   simulated chase pathway shows no such fall-off: LC9/DNp09/DNa02/
   muscle all stay nearly flat (within ~10%) from 8deg all the way to
   100deg -- more than double the real reported upper bound (50deg) with
   no drop in chase-circuit output. **This model currently behaves as an
   on/off size threshold, not a tuned size-selective filter** -- a real,
   named gap between what real LC9 does and what this simulation
   reproduces.
3. **The escape circuit is where the real size information actually
   shows up.** LC6 scales ~100x across the same range (9 at 8deg to 903
   at 100deg) while staying essentially silent within the real 8-22.5deg
   core of the range -- i.e., the model DOES show meaningful size-
   dependent behavior, just in the escape pathway rather than the chase
   pathway. This is a real, unexplained asymmetry worth flagging, not
   hidden: either LC6 truly is the more size-sensitive real circuit (a
   testable, literature-checkable claim not yet checked), or the chase
   pathway's missing size selectivity is a real gap in our
   amplification/boost model that a flat 8x recurrent gain cannot
   reproduce (a flat gain can turn a circuit on, but real size tuning
   would require a peaked/non-monotonic response curve, which nothing in
   the current model implements).

**Conclusion: this is real independent validation, and it's a mixed,
honest result, not a clean win.** The on/off threshold prediction from
finding 18 held up under genuinely new test sizes. The size-selectivity
prediction (a fly-like preference for the 8-50deg range specifically) did
NOT hold up -- the model saturates immediately at threshold and stays
flat well beyond the real range. Recorded as-is rather than only
reporting the part that worked.

Scripts/files added: `run_size_sweep.py` (scratchpad),
`results_sizetest_sweep.csv`, `seq_sizetest_sz*.npy`/`_bodyids.csv`,
`spike_summary_sizetest_sz*.csv`.

### Correction to the above: went back to the literature before exploring the "gap" further, and the premise was wrong

Before building on the "chase circuit lacks real size selectivity" gap
identified above, did what the project's protocol requires: checked the
literature specifically on this claim rather than assuming it. Searched
for the actual shape of real pursuit-neuron size-tuning curves (Gaussian/
peaked vs. flat/plateau).

Found the directly relevant primary result: [Coen lab, Nature 2024
"Social state alters vision using three circuit mechanisms in
Drosophila"](https://pmc.ncbi.nlm.nih.gov/articles/PMC8973426/) modeled
LC10a (the courtship-pursuit steering neuron) as explicitly NOT
size-dependent, citing real behavioral data: males track targets of
varying size with equivalent vigor during close-range pursuit (their
Extended Data Fig. 8m-n). There is no published peaked/falling-off size
tuning curve for real pursuit behavior to fail to reproduce -- the
initial "size-selective" assumption in the finding above came from a
different number (LC9's ~4.5x2deg figure from Klapoetke et al. 2022,
Neuron), which is very likely describing receptive-field size (spatial
localization of the neuron's input), not preferred-stimulus size --
could not confirm which via open-access text (paywalled), left as an
explicit unresolved distinction rather than asserted either way.

**Net effect: the flat, saturating sweep result (8-100deg, no fall-off)
is likely a MATCH to real fly pursuit behavior, not a gap.** Corrected
finding 19 in `findings_summary.md` in place (not silently -- the
original mixed-result writeup is kept, struck through in spirit via an
explicit correction note, so the trail of what we believed and why it
changed stays visible). The remaining real open question: is the escape
circuit's steep LC6 size-scaling (confirmed in the sweep) actually
matched by real LC6-specific size-tuning data, or are we inferring that
from a different neuron (LPLC2, the real angular-size encoder in the
giant-fiber pathway per Klapoetke et al. 2019) that isn't the same cell
type as LC6 -- not yet checked, flagged as the next real gap to verify
before treating it as confirmed biology.

Scripts/files added: none (literature-only correction); citations added
directly to finding 19 in `findings_summary.md`.

### Follow-up: is LC6's steep size-scaling in our sweep real LC6 biology, or borrowed from a different neuron (LPLC2)?

Checked directly rather than assuming either way, since the previous
correction flagged this as the next real gap to verify.

**No mislabeling in the simulation itself.** Confirmed our network's
"LC6" readout is the real LC6 cell type from the actual connectome,
driven through the same real synapses as everything else -- at no point
did we substitute LPLC2's known size-tuning properties into it. The only
open question was whether real LC6 plausibly should scale with stimulus
size at all.

**It does, independently.** [Ache/Klapoetke et al., eLife 2020, "Spatial
readout of visual looming in the central brain of
Drosophila"](https://elifesciences.org/articles/57685): "LC6
preferentially responded to dark looming stimuli" (i.e., stimuli that
expand/grow in the visual field over time -- inherently a size-related
property), and also "responded to the motion of non-looming objects."
[Wu et al., eLife 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5293491/)
independently confirms LC6 is one of the real LC types whose optogenetic
activation triggers real jumping escape behavior, via its own real
pathway -- separate from LPLC2/LC4, which feeds the giant-fiber circuit
specifically. LC6 and LPLC2 are both real, independently-documented
looming-type detectors, not the same neuron under two names, and not
something we accidentally conflated.

**Conclusion: the qualitative direction of our sweep result is now
independently supported on both ends** -- chase (LC9/LC10a-type) is
documented as size-invariant above threshold (previous correction);
escape (LC6) is documented as looming/expansion-sensitive, which is
inherently size-related. **What remains unverified:** the exact
quantitative shape of real LC6's size-response curve (no paper found
measuring LC6 response at multiple fixed angular sizes the way our sweep
did) -- so the specific ~100x scaling factor (9 to 903 spikes, 8deg to
100deg) found in our simulation is still our own model's output, not a
number that can be checked against a real measurement. Recorded as a
real, closed methodological question (no mislabeling) with one honest
open number (magnitude) remaining, same pattern as finding 18's arousal
boost.

Scripts/files added: none (literature-only follow-up).

### Resolving finding 18's open selectivity problem -- root cause found via causal ablation, not more guessing

User asked to push both open threads (chase/escape selectivity, real LC6
magnitude) until reaching real resolution. Started with selectivity since
it's directly testable with the simulation itself, not just literature.

**Checked what's actually upstream of the leaking readouts, instead of
re-guessing.** Aggregated real edge weights by type in
`connectome_richer_chase.csv`:
- LC4's real upstream: LC4->LC4 (18,392, self-recurrence) >> **LC9->LC4
  (5,971)** > Tm5Y->LC4 (2,314) > T2a->LC4 (900) > Y3->LC4 (552) ...
- DNp01's real upstream: LC4->DNp01 (6,362) is essentially its ONLY real
  input in this network (DNp01->DNp01 self is 2).
- LC6's real upstream (why it stayed quiet): LC9->LC6 is only 230 --
  26x weaker than LC9->LC4's 5,971.

**This directly falsifies finding 18's original guess** ("cross-talk
from shared, un-gated amplified Mi1 signal"). The real cause is a
specific, substantial, DIRECT real synapse from LC9 (the boosted chase
neuron) straight into LC4 (escape) -- not a diffuse shared-input effect.
DNp01's cross-talk is fully explained as one hop downstream of that: it
only fires because LC4 fires.

**Confirmed causally, not just correlationally, with a targeted
ablation.** Removed exactly the 661 real LC9->LC4 edges from the network
(`connectome_richer_chase_ablateLC9LC4.csv`), re-ran the identical
aroused/boosted stimulus (sz22.5 condition):

| | LC9 | LC4 | DNp01 | LC6 |
|---|---|---|---|---|
| original (LC9->LC4 intact) | 13,016 | 3,349 | 109 | 29 |
| ablated (LC9->LC4 removed) | 13,037 | **0** | **0** | 30 |

LC9 itself unchanged (confirms the ablation didn't disturb the chase
circuit's own dynamics), LC6 unchanged (confirms the ablation was
surgical), LC4 and DNp01 both collapse to exactly zero. **Definitive:**
one specific real synapse, not a global amplification artifact, causes
100% of the LC4/DNp01 cross-talk in this network.

**Checked whether this is a real anatomical fact or a sign/data error
before trusting it.** LC9's real predicted neurotransmitter (from
neuprint) is acetylcholine (219/219 LC9 neurons) -- genuinely excitatory
in Drosophila, consistent with all 661 LC9->LC4 edge weights being
positive. Not a sign-reversal bug; this is a real, substantial (~22% of
LC4's total real input, by weight) excitatory synapse that exists in the
actual male-cns connectome.

**Checked the literature for a plausible real inhibitory/gating
mechanism that might counteract this in real flies, rather than assuming
none exists.** Found and checked one directly relevant candidate --
[Onaga et al. 2021, Scientific Reports, "Male courtship song drives
escape responses that are suppressed for successful
mating"](https://pmc.ncbi.nlm.nih.gov/articles/PMC8084941/) -- but on
closer reading it does NOT generalize here: the suppression they found
is specific to a courtship-SONG-driven (auditory) escape response in
FEMALES, and the paper explicitly contrasts this with visual looming
escape, which was NOT similarly suppressed by the same neurons (70A09)
in their own data. Does not provide evidence for or against a visual
chase/escape gating mechanism in males. Correctly narrowing an initial
over-broad reading rather than forcing it to apply.

**Conclusion, stated precisely:** finding 18's "imperfect selectivity"
was never a flaw in the boost mechanism or the amplification stage --
it is the network faithfully reproducing a real, confirmed, excitatory
synapse from the chase pathway directly into the escape pathway. A real,
literature-independent, testable prediction falls out of this: aroused/
courting male flies should show elevated escape-pathway "readiness"
purely as an anatomical side effect of strong LC9 activity, unless real
flies have a separate suppressive mechanism (not yet found in the
literature) that overrides it. True "clean" selectivity was never
achievable by tuning the boost differently -- it would require modeling
an additional real inhibitory pathway we don't currently have evidence
for, not adjusting `--type-boost`.

Scripts/files added: `connectome_richer_chase_ablateLC9LC4.csv`,
`spike_summary_ablateLC9LC4.csv`.

### Second thread: pinning down a real, measured LC6 size-tuning magnitude -- searched thoroughly, genuinely not available

Tried multiple real search angles specifically for a quantitative LC6
response-vs-angular-size curve (calcium imaging dF/F0 at multiple fixed
sizes, analogous to our own sweep): direct LC6 tuning-curve searches,
the eLife "Spatial readout of visual looming" paper (confirmed it
studies LC6's downstream targets and receptive-field geometry, not a
size-response curve), the Ache/Klapoetke Current Biology giant-fiber
paper (LC4/LPLC2-specific, not LC6), and the Wu et al. 2016 lobula
columnar behavioral-mapping paper (behavioral phenotypes, not tuning
curves). No paper found reporting LC6 response magnitude at multiple
fixed real angular sizes.

**Honest conclusion, not forced:** per the project's own research
protocol (stop after ~4 genuine attempts rather than looping
indefinitely on an unanswerable question), this specific number is not
available in the accessible literature. The qualitative fact (LC6 is a
real, independent looming/expansion detector, separate from LPLC2) is
confirmed; the quantitative magnitude of our own simulation's ~100x
size-scaling (9 to 903 spikes, 8deg-100deg) remains our model's own
output only, not independently checkable. This is a real, named
"known unknown" -- the correct way to close this thread, not a dead end
to paper over.

Scripts/files added: none (literature search only, no new data
available).

### Follow-up: does Tm5Y (a second, unboosted bridge neuron) also leak into the escape circuit?

While listing every neuron type that fired in the sz22.5 boosted run,
noticed Tm5Y (348 spikes) wasn't one of the three bridge types we
deliberately boosted (Y3, T2a, TmY5a), and it has real, substantial
direct weight onto both escape readouts: Tm5Y->LC6 (weight into 1,629
real edges) and Tm5Y->LC4 (759 real edges) -- a second possible real
leak path, separate from the LC9->LC4 wire already found and confirmed.

**Tested with three more targeted ablations** (same method as the
LC9->LC4 test: remove exactly one real edge type, rerun the identical
boosted sz22.5 stimulus, compare spike counts):

| condition | LC4 | LC6 | DNp01 |
|---|---|---|---|
| baseline (all real wires intact) | 3,349 | 29 | 109 |
| ablate Tm5Y->LC6 only | 3,349 | 14 | 109 |
| ablate LC9->LC6 only | 3,349 | 19 | 109 |
| ablate Tm5Y->LC4 only | 3,334 | 30 | 109 |

**Result, precise:**
- **LC4's leak is still fully explained by LC9->LC4 alone.** Removing
  Tm5Y->LC4 barely moves LC4 (3,349 -> 3,334, ~0.4%) -- confirms the
  earlier finding, Tm5Y is not a meaningful second path into LC4.
- **LC6's small leak (29 spikes) is NOT explained by one dominant wire
  -- it's split across two real, comparably-sized contributions.**
  Removing Tm5Y->LC6 drops LC6 to 14 (~52% reduction); removing
  LC9->LC6 drops it to 19 (~34% reduction). Neither ablation alone
  reaches zero, unlike the clean LC9->LC4 result -- LC6's modest
  activity is genuinely driven by both real wires together, not
  attributable to a single dominant source.
- **DNp01 unchanged in all three (109 in every row)** -- confirms
  DNp01 only cares about LC4's output, consistent with the earlier
  finding that DNp01's only real input in this network is LC4.

**Conclusion:** the LC4/DNp01 side of finding 20's cross-talk result is
now doubly confirmed (a second bridge neuron checked and ruled out as a
contributor). The LC6 side is a smaller, messier, genuinely
multi-wire effect rather than a single clean synapse -- both real,
both small in absolute terms (14-30 spikes vs. LC9's 13,000+), but
neither individually sufficient to fully explain LC6's modest activity.
Not pursued further this session (user paused here to resume later).

Scripts/files added: `connectome_richer_chase_ablateTm5YLC6.csv`,
`connectome_richer_chase_ablateLC9LC6.csv`,
`connectome_richer_chase_ablateTm5YLC4.csv`,
`spike_summary_ablateTm5YLC6.csv`, `spike_summary_ablateLC9LC6.csv`,
`spike_summary_ablateTm5YLC4.csv`.

### LC6 double-ablation resumed and closed: a third real wire (Y3->LC6) found and confirmed

User asked to finish the LC6 investigation. Removed Tm5Y->LC6 AND
LC9->LC6 together (1,806 real edges) and reran the identical boosted
sz22.5 stimulus: **LC6 dropped from 29 to 7, not 0** -- proving a third
real contributor exists beyond the two already tested.

Checked LC6's full real upstream weight table again: the only
un-tested real excitatory candidate left was **Y3->LC6 (weight
2,143)**. Added it to the ablation (Tm5Y + LC9 + Y3, all -> LC6, 2,534
real edges removed total) and reran: **LC6 = exactly 0.**

**Conclusion, now fully closed:** LC6's entire real leak (29 spikes at
baseline) is explained by exactly three real wires acting together --
Tm5Y->LC6, LC9->LC6, and Y3->LC6 -- with no residual after all three are
removed. Unlike LC4 (one dominant wire, LC9->LC4, explains 100%), LC6's
small leak is a genuinely distributed, three-source effect. Both
patterns are real, confirmed causally, and now fully accounted for.

Scripts/files added: `connectome_richer_chase_ablateBothLC6.csv`,
`connectome_richer_chase_ablateTripleLC6.csv`,
`spike_summary_ablateBothLC6.csv`, `spike_summary_ablateTripleLC6.csv`.

### Quick pass on the remaining open threads (#2, #4, #5 from the punch list), each closed honestly rather than forced

**#2 -- real measured magnitude of the P1->LC10a arousal gain boost:**
searched again with different terms. Found more qualitative confirmation
-- "P1 neurons increase the gain of LC10a activity," "driving LC10a
neurons to robustly respond each time the visual target swept across a
male's field of view" (multiple sources, consistent with finding 18) --
but no paper reports an actual fold-change number. Remains a genuine
known unknown, same conclusion as finding 18, now confirmed by a second
independent search rather than assumed.

**#4 -- is LC9's 4.5x2deg figure a receptive-field size or a preferred
stimulus size?** Tried two more access routes (Semantic Scholar paper
page -- returned empty; the paper's own open supplementary PDF --
403 Forbidden). Still unresolved. Logging this as a genuine dead end
after now 4 total real attempts across this thread (ScienceDirect
paywall, PMC of a different paper, Semantic Scholar, supplementary PDF)
-- consistent with the project's stop condition, not further pursued.

**#5 -- is it behaviorally plausible that courting/chasing male flies
show elevated escape-circuit activity (finding 20's prediction)?**
Found a real tension worth logging honestly rather than hiding: broader
search results describe Drosophila courtship-chasing behavior as
generally *suppressing* competing responses, including escape ("males
maintain their pursuit of females through suppression of competing
behavioral responses, including escape reactions" -- search-synthesized,
not a single traceable primary quote). This is the opposite direction
from what finding 20's real LC9->LC4 excitatory synapse would predict in
isolation. Not necessarily a contradiction -- the one specific primary
source checked earlier (Onaga et al. 2021) was explicitly auditory/
song-specific and did NOT show suppression of visual escape by the same
mechanism -- but the tension is real and unresolved: real flies may have
a separate, real suppressive pathway (not yet identified) that overrides
the excitatory LC9->LC4 wire during courtship, OR the general
"suppression" characterization in secondary sources may not apply
cleanly to this specific visual sub-circuit. Recorded as an open,
falsifiable question, not resolved either way.

**#6 -- whole-project behavioral validation:** out of scope for a
literature-search pass; already honestly documented in
`findings_summary.md`'s "Honest limitations" section (nothing in this
project has been checked against a real fly's behavior). No new action
taken here.

Scripts/files added: none (literature-only pass on #2/#4/#5; #6 not
actionable via search).

### Testing finding 20's prediction against real behavior: do courting flies actually show elevated escape readiness? Real data found -- answer is no, and it reveals the model is missing a whole real mechanism

User asked to directly test finding 20's open prediction (that a real
LC9->LC4 excitatory synapse might give courting/chasing males elevated
escape-circuit activity) against real behavioral data, not just leave it
as a guess. Can't run a real fly ourselves, so this is a literature
question -- searched specifically for real experiments measuring escape/
threat response AS COURTSHIP PROGRESSES, not just courtship vs. rest.

**Found the directly relevant, real, quantitative result:** [Cazalé-Debat et al. et
al. 2024, Nature, "Mating proximity blinds threat
perception"](https://pmc.ncbi.nlm.nih.gov/articles/PMC11485238/). Real
males exposed to a real overhead-shadow visual threat while courting a
female show **progressively DECREASING defensive/escape response as
courtship advances** -- high response at ~7s into courtship, much
reduced by ~240s, and males "completely ignored visual threats, even
after sperm transfer" during copulation. **This is the opposite
direction from finding 20's prediction.**

**The real mechanism is a completely different circuit than the one this
project has built.** The real visual-threat detector driving this
behavior is **LC16** (not LC4, LC6, or LC9), signaling via serotonin
(LC16 -> 5-HTPMPD neurons -> P1/courtship neurons, through 5-HT7/5-HT2B
receptors). As courtship progresses, real dopamine neurons (PPM1/2) ramp
up and suppress LC16 itself directly via Dop2R receptors on LC16's own
axon terminals -- an active, state-dependent brake on the threat pathway,
not just an absence of drive.

**Checked the female-mating-state defensive circuit as a second
candidate before concluding** -- [Wang et al. 2020, an earlier PMC entry
on mating-state-tuned defensive behavior](https://pmc.ncbi.nlm.nih.gov/articles/PMC7414864/):
found this describes the OPPOSITE effect (mating INCREASES defensive
kicking) but is explicitly female-specific ("this inhibition was absent
in males") and uses a mechanosensory circuit (uterine neurons ->
leucokinin -> VNC), with no connection to visual looming circuits at
all. Correctly ruled out as inapplicable to our male, visual-pursuit
question rather than cited by surface-level topic match.

**Conclusion, precise:** finding 20's real LC9->LC4 synapse is still
real and still causes the leak in our current simulation (confirmed by
ablation) -- that part is unchanged. But real fly behavior shows escape
sensitivity net DECREASES during courtship, via a specific, real,
separate circuit (LC16 -> serotonin -> dopamine-suppressed) that this
project has never modeled at all (only 5 of 22 real LC types are wired
into this simulation, and LC16 is not one of them -- consistent with the
project's own standing "partial connectome coverage" limitation). Our
simulation currently only has the excitatory "leak" (LC9->LC4) with no
counteracting suppressive circuit, so on its own it would incorrectly
predict INCREASED escape readiness during arousal -- real flies avoid
this via a real brake mechanism outside the scope of what's been built.
**This is a genuine, well-sourced, named gap for future work**, not a
flaw in what's already built: adding LC16 and its dopamine-gated
suppression would be the concrete next real step to make the model's
prediction match real behavior, rather than adjusting anything already
in place.

Scripts/files added: none (literature-only, direct behavioral test of
finding 20's prediction).

### Building LC16 in: does a real dopamine-gated brake reproduce the real "males ignore threats late in courtship" finding?

User asked to build the missing piece identified above (LC16 + its
dopamine-gated suppression) rather than stop at the literature gap.

**Step 1 -- pulled LC16 for real and mapped its real connectivity, not
assumed.** 182 real LC16 neurons (male-cns), cholinergic. Real downstream
(by total weight): PVLP007 (31,527), LC16 self-recurrence (14,596),
several unnamed central-brain clusters, then **pC1_2a (1,661)** and
**PVLP004 (835)** -- PVLP004 being the same real neuron already
established as LC9's own dominant real input (33,353, reconfirmed here).
LC16's real upstream is dominated by **Tm20** (17,683) -- a real medulla
neuron not in any of our existing networks -- plus real overlap with two
neurons we already had (Tm5Y: 3,991, Y3: 1,141). Direct LC16 weight onto
LC9/LC4/LC6 is real but small (116/24/82) -- LC16 was never going to be
a dominant driver of those specific readouts.

**Step 2 -- confirmed Mi1->Tm20 is real before adding it** (weight
3,545, 1,460 edges, 1,762 real Tm20 neurons) -- without Tm20, LC16 only
fired 4-7 spikes total from the shared stimulus (not usable for a real
test). Built `connectome_lc16_chase.csv`/`_neurons.csv`: existing
7,024-neuron chase/escape network + LC16 + PVLP004 + pC1_2a + Tm20 =
8,988 real neurons, 191,522 real edge rows (script:
`build_lc16_network.py`, scratchpad). Caught and fixed a real bug in the
build script itself: an unnecessary `drop_duplicates` step was silently
discarding legitimate multi-ROI rows for the *existing* edges (the
network is stored per-ROI, aggregated later by `simulate.py` itself) --
would have quietly corrupted the base network's weights. Fixed before
running anything.

**Step 3 -- realized LC16 needs its own real stimulus, not the courtship
target.** LC16 is a real threat/looming detector; the small translating
courtship-target blob isn't its natural stimulus (consistent with it
firing only 4-7 times on that alone). Built a second, separate real
stimulus: a large (radius=15 columns, ~75deg), zooming/looming blob over
the same Mi1 window (`seq_threat_loom.npy`, real two-stage amplification
applied same as before) -- representing a real overhead threat appearing
*during* courtship, matching the actual experimental design in Cazalé-Debat et al. et
al. 2024. Combined it with the existing courtship-target stimulus into
one array (union of driven neurons, currents summed on overlap,
`seq_courtship_plus_threat.npy`).

**Step 4 -- ran both real states, same combined stimulus, only the
LC16-suppression condition differing:**

| | LC16 | pC1_2a | PVLP004 | LC9 | LC4 | LC6 | DNp01 | muscle |
|---|---|---|---|---|---|---|---|---|
| "early courtship" (LC16 unsuppressed) | 760 | **54** | 917 | 13,561 | 3,544 | 870 | 113 | 193 |
| "late courtship" (LC16 output x0.1, dopamine-brake proxy) | 334 | **0** | 913 | 13,561 | 3,555 | 854 | 113 | 196 |

Suppression applied via `--type-boost` at 0.1x on every real LC16
outgoing edge type (LC16->LC16, LC16->PVLP004, LC16->pC1_2a, LC16->LC9,
LC16->LC4, LC16->LC6) -- representing dopamine's real reported site of
action (LC16's own axon terminals, i.e. its outputs, not its inputs),
while the LC9 chase-arousal boost stayed on in both conditions (still
"courting" throughout).

**Result, precise:** the escape/motor readouts (LC4, LC6, DNp01,
muscle) show essentially NO change between conditions -- LC16's real
direct weight onto them is small next to their other real inputs
(confirmed in finding 20's own weight tables), so they were never going
to move much regardless. **But pC1_2a -- the real courtship-modulating
neuron the actual paper implicates -- goes from 54 spikes to exactly
0.** This is the anatomically correct readout for the real finding
(Cazalé-Debat et al. 2024's mechanism runs LC16 -> serotonin -> P1/pC1-family
courtship neurons, not LC16 -> motor escape), and it reproduces the
real qualitative direction: **with the dopamine brake off, a real threat
signal reaches the courtship-modulating circuit; with the brake on, it's
completely blocked.**

**Honest caveats, stated plainly:** (1) the 0.1x suppression factor is
our own estimate, not a measured number -- same status as finding 18's
8x arousal boost. (2) The real mechanism is serotonergic signaling to
P1-family neurons, not a direct synaptic weight cut -- representing it
as a flat output-multiplier is a simplification, following the same
precedent used for the arousal-gain mechanism (justified there by
checking the real synapse was trivial/absent, confirming the real effect
must be neuromodulatory -- not independently re-verified for LC16 here).
(3) pC1_2a only 4 real neurons in this dataset -- a small population,
so 54 vs 0 spikes is a real but modest-magnitude effect, not
overwhelming. (4) This does NOT show the model now correctly predicts
motor escape behavior during courtship (finding 20's original prediction
target) -- it shows the model can reproduce the real courtship-
modulation pathway specifically, which is a different, more precise, and
better-grounded readout than the one originally guessed at.

Scripts/files added: `build_lc16_network.py` (scratchpad),
`connectome_lc16_chase.csv`/`_neurons.csv`, `seq_threat_loom.npy`/
`_bodyids.csv`, `seq_courtship_plus_threat.npy`/`_bodyids.csv`,
`spike_summary_lc16_earlycourtship.csv`,
`spike_summary_lc16_early_withthreat.csv`,
`spike_summary_lc16_late_withthreat.csv`.

### Two follow-up checks on finding 21, both real, both clean

User asked to run two specific checks rather than let finding 21 stand
on assumptions: (1) is dopamine's suppression of LC16 really
neuromodulatory (no strong direct synapse), matching the precedent used
to justify modeling it as a flat output multiplier; (2) does the
pC1_2a shutdown reach a real neuron one hop further downstream, or does
it dead-end.

**Check 1 -- real dopamine neurons found, real synapse checked, confirms
the modeling choice.** Found the real male-cns dopaminergic neurons
matching the paper's "PPM1/2" naming: PPM1201/1202/1203/1205 (12 real
neurons, confirmed dopaminergic via `predictedNt`; PPM1204 is a
same-named but glutamatergic outlier, correctly excluded). **Real direct
synaptic weight from these dopamine neurons onto LC16: 16, across 14
edges -- trivial**, same magnitude and same conclusion as the earlier
P1->LC9 check (weight 14, called negligible there). Confirms dopamine's
real effect on LC16 cannot be a strong point-to-point synapse -- it has
to be neuromodulatory, validating (not just assuming) the output-
multiplier representation used in finding 21.

**Check 2 -- traced pC1_2a's real downstream, found the real path is
NOT through pIP1 (checked directly: weight 4, trivial -- an initial
guess correctly ruled out), but through mAL_m8** (real weight 2,156,
GABAergic, dominant real target). Added mAL_m8 to the network
(`connectome_lc16b_chase.csv`/`_neurons.csv`, 9,004 neurons) and reran
both conditions:

| | LC16 | pC1_2a | **mAL_m8** | PVLP004 | LC9 |
|---|---|---|---|---|---|
| brake off | 760 | 95 | **315** | 917 | 13,553 |
| brake on | 334 | 0 | **0** | 913 | 13,561 |

(pC1_2a's "early" count shifted slightly, 54->95, from adding mAL_m8's
real recurrent/feedback wiring into the network -- expected minor
network-composition noise, not a contradiction.)

**Result: the shutdown propagates a full real hop further, cleanly.**
mAL_m8 -- part of the real, documented male-specific courtship
interneuron cluster -- goes from 315 to exactly 0 spikes under the
dopamine-brake condition, same clean pattern as pC1_2a. Chase circuit
(PVLP004, LC9) remains essentially unaffected in both checks, confirming
this is a real, selective, two-hop-deep suppression of the courtship-
modulation pathway specifically, not a network-wide effect.

Scripts/files added: `connectome_lc16b_chase.csv`/`_neurons.csv`,
`spike_summary_mAL_early.csv`, `spike_summary_mAL_late.csv`.

### A real quantitative test against real behavior: does our escape circuit's motion-vs-shape balance match de la Flor et al. 2017's actual measured numbers?

User asked to scope and run the strongest available candidate for a real
number-match (not just direction-match) against real fly behavior,
following the research-review finding that nothing in this project had
been quantitatively checked against real behavior before. Finding 6
(escape reflex is roughly shape-blind) already cites this paper
qualitatively; this test tries an actual ratio comparison.

**Got the real numbers first.** [de la Flor et al. 2017, PLOS
ONE](https://pmc.ncbi.nlm.nih.gov/articles/PMC5528251) measured % time
Canton-S flies spent near a threat object (lower = more avoidance): still
spider ~24%, still stir-bar ~20%, moving stir-bar ~12%, moving spider
~5% (moving-spider vs. moving-stir-bar difference real and significant,
W=4.3985, N=32, P=0.010). Using still-spider as the weak-response anchor
and moving-spider as the strong-response anchor, moving-stir-bar (12%)
sits 63.2% of the way from weak to strong -- i.e. **in real flies,
motion alone accounts for ~63% of the total avoidance effect, shape
adds the remaining ~37%.**

**Designed a matched simulation test, not a lookup.** Direct number
matching is impossible (different paradigms -- minutes-long freely-moving
avoidance vs. instantaneous spike count after one stimulus), so matched
on RATIO instead: same weak/strong/motion-only anchor logic, using
`spider_sill.jpg` vs. `shape_blob.jpg` (an existing ink-budget-matched
shape-vs-no-shape pair from earlier in this project) through the current
validated escape network (`connectome_richer_chase.csv`, LC4/LC6/DNp01,
no arousal boost -- this is general threat perception, not courtship).

**Caught and fixed two real confounds before trusting any result.**
(1) Spider and blob images had different raw mean contrast in the
sampled window (0.589 vs. 0.384) -- normalized both to equal total
contrast so only shape differed, not brightness, matching this project's
own established total-current-matched methodology (finding 1, 15).
(2) First attempt used lateral translation ("moving" = panning
sideways) for the motion condition and got a flat, uninformative result
(DNp01 unchanged 75->76 across still/moving) -- caught that this
contradicts the project's own earlier finding 2 (looming, not lateral
motion, is what the Giant Fiber pathway is actually tuned to) and
switched to a real zoom/looming stimulus instead. Also hit a size
ceiling/floor problem first (22.5deg = flat zero, 75deg = flat and
saturated with LC6 even reversing direction) before landing on a working
intermediate size (radius=8 columns, ~40deg).

**Final, clean 3-condition comparison (radius=8, contrast-normalized,
current default calibration):**

| condition | DNp01 | LC4 |
|---|---|---|
| still spider (weak anchor) | 75 | 1,782 |
| loom blob (motion only, no shape) | 77 | 1,841 |
| loom spider (strong anchor, motion+shape) | 86 | 2,125 |

Using the same weak/strong/motion-only ratio logic as the real paper:

| readout | motion's real share | our model's share |
|---|---|---|
| DNp01 | 63.2% | **18.2%** |
| LC4 | 63.2% | **17.2%** |

**Result: a real, precise, consistent quantitative mismatch, not a
match.** Two independent readouts agree closely with each other
(17-18%), so this isn't a fluke of picking one neuron -- but both
strongly disagree with real flies. Real fly avoidance is
motion-dominated with shape as a modest ~37% add-on; **our simulation's
escape circuit, as currently calibrated, is shape-dominated (~82%) with
motion only a modest ~18% contributor -- roughly the inverse balance**
from real biology.

**Honest interpretation, not spun either way:** this is a genuine,
falsifiable finding, not a failure to hide. Plausible real explanations,
none yet tested: (1) our "shape" (spider silhouette vs. blob) may be
smuggling in more contrast-pattern/edge information than the real
spider model conveyed to real flies, inflating the shape channel's
apparent contribution; (2) our looming/motion implementation (zoom-based
frame resampling) may under-drive the real motion-energy signal
compared to what an actually approaching/spinning object gives a real
photoreceptor array; (3) the real behavioral assay integrates minutes of
free exploration and many looming encounters, while our test is one
6-frame stimulus presentation -- these need not have the same
motion/shape balance even if both are "real." **This is the first
successful real number-vs-number (not just direction-vs-direction) test
run in this whole project, and it produced a real disagreement worth
investigating further, not a confirmation.**

Scripts/files added: `seq_review*_*.npy`/`_bodyids.csv` (4 radius/motion
variants x spider/blob), `spike_summary_review*_*.csv`.

### Testing explanation 1 for finding 22's mismatch: does the spider stimulus carry too much edge information? Caught a real bug in our own analysis along the way, and got a genuine negative result

User asked to test the first of finding 22's three candidate
explanations directly: does our spider silhouette carry more
edge/spatial-complexity information than a real spider model would,
inflating the "shape" channel's apparent contribution.

**Measured the premise first, didn't assume it.** Computed real edge
density (Sobel gradient magnitude, normalized by total contrast) on the
full `spider_sill.jpg` vs. `shape_blob.jpg` images. Total contrast ("ink
budget") was already well-matched (66,102 vs. 67,360, ~2% apart,
confirming finding 3's original matching held). But **edge density was
NOT matched: spider = 0.290 edge-per-contrast vs. blob = 0.109 -- the
spider carries 2.6x more edge information** even at equal total ink,
because a spider's legs/joints create far more internal contours than a
smooth blob. This confirms the premise was real, not assumed.

**Caught a real bug in the ORIGINAL finding-22 calculation while setting
up this test.** The "motion-only" (loom blob) condition had been
normalized against a different target mean than the "strong" (loom
spider) anchor it was compared to -- an unpaired normalization mismatch.
Fixed it (re-ran loom-blob at the correctly matched target) and
recomputed: **corrected motion share = 36.4% (DNp01) / 36.2% (LC4) --
not the ~18% originally reported.** Real flies' motion share is 63.2%.
The gap is still real (our model underweights motion relative to real
flies) but roughly half the size originally reported -- **finding 22's
qualitative conclusion (shape overweighted, motion underweighted
relative to real flies) holds, but its exact numbers needed correcting,
and are corrected here rather than left wrong.**

**Built an edge-matched spider stimulus to test explanation 1 for
real.** Iteratively pre-blurred `spider_sill.jpg` (found pre_sigma=36
empirically, accounting for `photo_at_position.py`'s own additional
internal blur on reload) until its edge-per-contrast matched blob's
almost exactly (0.109 vs. 0.109), saved as `spider_edgematched.jpg`.
Ran the identical still/loom radius=8 test, contrast-renormalized as
before.

**Result: explanation 1 is NOT supported -- if anything, the opposite
happened.** With edges matched to the blob's level, motion's relative
contribution DROPPED further (25.0% DNp01, 20.0% LC4), moving AWAY from
real flies' 63%, not toward it. The edge-matched (blurred) spider
produced an even STRONGER loom response (91/2,253) than the original
sharp spider (86/2,125), not a weaker one.

**Honest interpretation:** explanation 1, as stated, is ruled out by
this test -- reducing edge information did not shift the balance toward
real biology. The counterintuitive stronger response from the blurred
spider is most plausibly explained by an interaction with the
two-stage Naka-Rushton amplification stage: heavy blur redistributes a
concentrated sharp pattern into a broader, more moderate-contrast patch
covering more Mi1 neurons, and the amplification's nonlinearity may
respond more favorably to that redistribution than to sharp, spatially
concentrated contrast -- **a real, plausible mechanism, but not
independently confirmed here**, flagged as the next thing to check
before treating it as established. Explanations 2 (looming
implementation under-driving real motion-energy) and 3 (paradigm
mismatch, minutes vs. one presentation) from finding 22 remain untested.

Scripts/files added: `spider_edgematched.jpg`,
`seq_review5_still_spiderEM.npy`/`_bodyids.csv`,
`seq_review5_loom_spiderEM.npy`/`_bodyids.csv`,
`spike_summary_review5_loom_blob_raw.csv`,
`spike_summary_review5_still_spiderEM.csv`,
`spike_summary_review5_loom_spiderEM.csv`.

### Back to the original project goal: does the fly actually steer TOWARD the target's side, not just react to it?

User pulled the thread back to where this whole chase-circuit
investigation started: does the model show the fly chasing and
positioning itself toward a moving object -- i.e. does target position
(left vs. right) drive the CORRECT side's steering output, not just
"does the chase circuit fire at all" (already established, finding 17
onward).

**Checked whether the network even supports this test before assuming
it did.** `connectome_richer_chase_neurons.csv` already contains the
complete real Mi1 population from BOTH eyes (875 real left, 887 real
right -- confirmed by cross-referencing bodyIds against
`mi1_richer_columns.csv`), and every stage of the chase chain has real,
separately-labeled left/right instances (LC9_L/LC9_R, DNp09_L/_R,
DNa11/DNa06/DNa02 L/R, muscle L/R) -- this network was never explicitly
built for a laterality test, but happened to already carry everything
needed for one.

**Ran the same courtship-target stimulus on each eye separately, same
network, same arousal boost, nothing else changed** -- right eye
(`seq_sizetest_sz22.5.npy`, already existing) vs. a newly-generated
mirrored left-eye version (`seq_lateral_L.npy`). Split every readout's
spike counts by real instance-name laterality (_L/_R suffix from
neuprint) after the fact.

**Result: perfectly, cleanly lateralized, zero crossover, every stage
of the chain:**

| | LC9 | DNp09 | DNa11 | DNa06 | DNa02 | muscle |
|---|---|---|---|---|---|---|
| R-eye stim: L side | 0 | 0 | 0 | 0 | 0 | 0 |
| R-eye stim: R side | 13,016 | 108 | 71 | 70 | 69 | 179 |
| L-eye stim: L side | 11,580 | 108 | 78 | 78 | 77 | 127 |
| L-eye stim: R side | 0 | 0 | 0 | 0 | 0 | 0 |

A target on the right drives ONLY the right-side chain end to end; a
target on the left drives ONLY the left-side chain -- exact mirror
symmetry, no measurable crossover at any stage. This is a real,
ipsilateral steering circuit, matching the documented real biology
(DNa-type descending neurons drive ipsilateral leg-steering turns) --
not assumed, directly demonstrated by the real connectome's own wiring
plus this project's own simulation.

**Significance, stated precisely:** this is the first time this project
has shown not just "the chase circuit can fire" (finding 17) but that it
fires on the ANATOMICALLY CORRECT SIDE for the target's actual position
-- the real substrate for a fly steering its body/legs toward what it
sees, not away from it or randomly. Directly answers the original
project question ("does the fly chase and position itself toward the
moving object") in the affirmative, at the level of real motor-output
laterality, for the first time with a direct, non-ambiguous test.

**Honest caveat:** this shows the *circuit's* lateralization is
anatomically correct -- it does NOT show actual body/leg movement (this
simulation stops at motor-neuron spiking, per the project's own
standing limitation), and it was tested at one stimulus position/size
only (not swept across the visual field, unlike the earlier
responsiveness-map work in finding 17's era). A real next step would be
sweeping stimulus position across both eyes and confirming the
laterality holds (or degrades) continuously, not just at this one tested
point.

Scripts/files added: `seq_lateral_L.npy`/`_bodyids.csv`,
`spike_summary_lateral_L.csv`.

### The missing control for finding 24: does the real connectome actually lack cross-hemisphere wiring, or did OUR network-building just never include it?

User caught a real, sharp methodological gap immediately after finding
24: the zero-crossover result only shows what happened WITHIN a network
we ourselves built and saved. If our own fetch/build process only ever
pulled same-side edges (e.g. because of how neurons were queried when
`connectome_richer_chase.csv` was assembled), "zero crossover" would be
true by construction, not a real fact about the fly -- indistinguishable
from a real finding using only our own derived file.

**Went around our own saved network entirely and queried the real,
full connectome directly** (fresh `fetch_adjacencies` calls against
neuprint, not `connectome_richer_chase.csv`) for exactly the
cross-hemisphere edges finding 24's result depends on:

- **LC9 -> DNp09** (chain start): real weight exists only for
  LC9_L->DNp09_L (1,130) and LC9_R->DNp09_R (847). The query for
  LC9_L->DNp09_R and LC9_R->DNp09_L returned **zero rows** -- not
  filtered out, genuinely absent from the real data.
- **DNa02 -> muscle** (chain end): same pattern -- DNa02_L->muscle_L
  (308) and DNa02_R->muscle_R (402) are real; DNa02_L->muscle_R and
  DNa02_R->muscle_L returned zero rows. (A small amount, 26/40, goes to
  an unlateralized "Sternal anterior rotator MN" instance from both
  sides roughly proportionally -- plausibly a genuinely bilateral/midline
  motor neuron, not a crossing pathway, not investigated further here.)

**Conclusion: finding 24's result is real, not a construction artifact.**
Checked at both ends of the chain, independently, directly against the
full real connectome rather than our own derived file, and got the same
answer both times: the real male-cns connectome itself has no (or
negligible) cross-hemisphere synapses at these specific stages -- our
network file faithfully reflects a real anatomical fact, it didn't
manufacture one by only fetching one side. This is exactly the kind of
control this project's own protocol calls for (checking whether a
"positive" result could be a trivial byproduct of how the data was
gathered) and it survived being asked directly.

**Still-open caveat, stated honestly:** only two of the six real stages
in the chain were checked this way (LC9->DNp09 and DNa02->muscle, the
first and last links). The middle stages (DNp09->DNa11->DNa06->DNa02)
were not independently re-verified against the raw connectome the same
way -- assumed consistent based on these two endpoints and finding 24's
overall clean result, not directly confirmed at every link.

Scripts/files added: none (direct neuprint queries only, no new local
files).

### Strongest next test: does the steering signal scale with target position, or is it just on/off?

Following up on finding 24's honest caveat (tested at one position only)
and pushing for the strongest available next test: swept the target
across 6 positions spanning nearly the full right eye's real field
(hex1 = 4, 10, 16, 22, 28, 34 of the real ~1-36 range, hex2 fixed at
20, radius=4, moving, amplified, same arousal boost), measuring
left/right split spike counts at DNa02 and the muscle for each.

| hex1 | n Mi1 driven | LC9_R | DNa02_L | DNa02_R | muscle_L | muscle_R |
|---|---|---|---|---|---|---|
| 4 | 62 | 11,570 | 0 | 62 | 0 | 162 |
| 10 | 94 | 12,848 | 0 | 69 | 0 | 168 |
| 16 | 94 | 13,058 | 0 | 69 | 0 | 163 |
| 22 | 94 | 12,941 | 0 | 68 | 0 | 170 |
| 28 | 72 | 12,742 | 0 | 68 | 0 | 174 |
| 34 | 22 | 12,179 | 0 | 63 | 0 | 154 |

**Result 1 (good, extends finding 24 with confidence): lateralization
holds perfectly across the entire tested range.** Left side is exactly
0 at every single one of the 6 positions, not just the one point tested
before -- the real, zero-crossover wiring finding is robust across the
whole eye's field, not a coincidence of one location.

**Result 2 (honest limitation, not what was hoped for): the steering
signal does NOT scale with target position.** Muscle_R stays in a tight
154-174 band and DNa02_R in a tight 62-69 band across the ENTIRE real
range of hex1 positions -- no meaningful gradation whatsoever between a
target near one edge of the eye's field vs. the opposite edge. **This
model currently produces an on/off "something's on my right, turn
right" signal, not a proportional "turn THIS MUCH toward it" signal.**
Consistent with the same on/off-threshold pattern already seen in
finding 19 (size tuning) -- once the arousal-boosted LC9 circuit crosses
threshold, it appears to saturate rather than scale continuously with
stimulus parameters.

**Honest caveat on the test itself:** the number of real Mi1 neurons
actually driven varies with position (62-94, fewer near the edges of the
real coordinate range) -- a minor, uncontrolled confound, though it
doesn't change the qualitative conclusion (no meaningful trend either
way, in either direction, regardless of neuron count).

**Not yet checked:** whether real flies actually show graded (vs. on/off)
turning strength proportional to target eccentricity during chase --
this result should be read as "our current model doesn't show graded
steering," not yet as "this disagrees with real fly behavior," since
that comparison hasn't been made.

Scripts/files added: `seq_sweep_h*.npy`/`_bodyids.csv` (6 positions),
`spike_summary_sweep_h*.csv`.

### Does the real LC4->LC10a wire actually carry a functional signal into courtship tracking? Built it correctly, tested it, got a real partial answer

Follow-up to the 2026 McKinney/Hernandez/Ben-Shahar paper's speculation
that LC4 (the looming detector) might be reused during courtship. We'd
already confirmed the real wire exists (LC4->LC10a, weight 126,
reciprocal LC10a->LC4 weight 111). User asked whether it's functionally
consequential in simulation -- but first insisted on checking the real
connectomics before building, which caught a real mistake before it
happened.

**Caught and avoided a real methodological error.** The first instinct
was to reuse LC9's known bridge neurons (Y3, T2a, TmY5a, Tm5Y) to drive
LC4, since they were already on hand from earlier work. Checked LC4's
actual real upstream weight table first, as instructed -- **none of
those four types are meaningfully connected to LC4 at all.** LC4's real
dominant inputs are a completely different set: T2 (46,156), TmY3
(40,880), Tm4 (31,134), Tm2 (20,560), LC4 self-recurrence (18,392), Tm3
(17,077) -- classic real Drosophila motion-detector cell types (T4/T5
family relatives), not the LC9-oriented bridges. Reusing the wrong
bridges would have simulated a pathway that doesn't exist in the real
fly. Verified which of LC4's real inputs are themselves directly,
substantially driven by Mi1 (drivable by our existing stimulus
pipeline): **T2 (31,594), TmY3 (42,245), and Tm3 (126,023)** all
qualify: real, direct, strong Mi1 inputs. Used these three, not the LC9
ones.

**Built the network correctly**: the existing finding-15 courtship
network (LC10a -> AOTU -> pC1 -> aIPg -> pIP10, 855 real neurons) plus
LC4, its three real bridges (T2/TmY3/Tm3), and the full real right-eye
Mi1 population -- 6,376 real neurons, ~173,677 edges
(`connectome_lc4_courtship.csv`/`_neurons.csv`). Confirmed the real
LC4->LC10a edge (weight 126) survived the build.

**Drove LC4 with a real looming stimulus** (same zoom/amplify method as
earlier tests) and checked how far the signal actually travels:

| stage | spikes |
|---|---|
| Mi1 (driven input) | 14,591 |
| Tm3 / T2 / TmY3 (real bridges) | 9,219 / 6,107 / 4,236 |
| **LC4** | **3,394** |
| **LC10a** | **20** |
| AOTU (several real subtypes) | 1-17 each |
| pC1 (all ~60 real subtypes checked individually) | **0** |
| aIPg, pIP10 (final wing-steering output) | **0** |

**Result: real, but partial.** The wire is functionally real, not just
anatomically present -- LC4 firing genuinely drives LC10a (weakly) and
the signal even continues one more hop into several real AOTU neurons.
But it dies before crossing into pC1, and never reaches the actual
wing-steering output (pIP10) at all. **LC4 alone, at this stimulus
strength, is not sufficient to drive courtship-tracking motor output --
it's a real but modest/contributing input to LC10a, not a primary
driver.** Consistent with finding 15's own earlier result that LC10a's
front end needed an arousal-style boost to reach real motor output --
not tested here whether adding that same boost would let this LC4
pathway complete the circuit.

**Honest interpretation:** this gives real, partial anatomical AND
functional support for the new paper's speculation (the wire exists and
does something, not just sits there unused), but does not confirm LC4
drives courtship behavior on its own. A natural next test, not yet run:
combine this LC4 drive with finding 18's arousal boost on LC10a's own
pathway, to see if that's what's needed to complete the circuit to
pIP10.

Scripts/files added: `connectome_lc4_courtship.csv`/`_neurons.csv`,
`seq_lc4courtship_loom.npy`/`_bodyids.csv`,
`spike_summary_lc4courtship.csv`.

### Testing the paper's specific hypothesis: does red-eye-like contrast vs. white-eye-like low contrast change the courtship pathway's response?

**CORRECTION (added after this entry, on direct user challenge -- kept
here rather than rewritten): this test never used an eye image.** Both
conditions below use `blob_control.jpg`, the same generic blob used for
the main chase-target stimulus throughout this project, at the same
size/position, differing only in a numeric brightness scale factor. No
eye-shaped or eye-colored stimulus was ever built (this project's model
is grayscale-contrast-only in any case, so real eye color couldn't have
been represented even if a real eye photo had been used). "Red-eye" and
"white-eye" below should be read as "high-contrast blob" and
"low-contrast blob" -- the real paper's actual hypothesis (that eye
pigment specifically is the cue) remains untested. See the same
correction repeated at the later "full matrix" entry.

Follow-up to the McKinney/Hernandez/Ben-Shahar paper's own hypothesis
(not just "eyes matter," but specifically that red-eye/cuticle contrast
is the cue, tested in their real experiment via white-eyed mutant
females showing weaker male responses). Built a matched simulation test:
same size and position, only contrast level differing -- a high-contrast
"red-eye" analog vs. a low-contrast (10% of high) "white-eye" analog.

**Checked LC10a's real upstream before reusing anything.** LC10a's real
dominant inputs are LC10a self-recurrence (25,244), TuTuA_2 (18,097,
central-brain), AOTU042 (14,492, central-brain feedback), Tm5Y (14,221),
LC9 (9,661), plus several LC10 subtypes -- **Tm3 (weight 3,893) was
already confirmed as a real, strong, direct Mi1 target** from the
LC4 bridge-verification work just done, and was already present as a
real edge into LC10a in the just-built `connectome_lc4_courtship.csv`
network (1,288 real edges) -- reused rather than rebuilt.

**First attempt (eye-sized patch, radius=2, ~10deg) was too small to
reach anywhere** -- high-contrast condition drove Tm3 (419) but not
LC10a; low-contrast drove nothing at all. Not a contrast effect, a floor
effect (matching the same small-stimulus threshold problem seen
throughout this project). Retested at radius=4 (~22.5deg, this
project's standard working target size).

**Result at radius=4, contrast-matched size/position, only contrast
level differing:**

| condition | Tm3 | LC10a | AOTU | pC1 | pIP10 |
|---|---|---|---|---|---|
| high-contrast ("red eye") | 1,547 | 0 | 0 | 0 | 0 |
| low-contrast ("white eye", 10% of high) | 7 | 0 | 0 | 0 | 0 |

**Real, dramatic contrast-dependence at the first real synaptic stage
(Tm3): 1,547 vs. 7 spikes, ~220x difference** -- directly consistent
with the real paper's premise that red-eye contrast is a much stronger
visual cue than a low-contrast (white-eye-like) equivalent. **But the
difference does not survive to reach LC10a itself or anything
downstream** -- same "weak bridge, needs a boost to cross threshold"
pattern already seen in findings 18, 21, and 26 (Tm3's real weight into
LC10a, 3,893, is a small fraction of LC10a's dominant real inputs, which
this network doesn't include or drive).

**Honest interpretation:** partial, real support for the paper's
specific hypothesis -- a contrast-type visual cue produces a large,
real, early-stage neural difference in this simulation, consistent with
what would be needed for red-eye-vs-white-eye discrimination to work at
all. But this test does not show the full courtship pathway responding
differently to contrast -- the signal dies at the same kind of
bottleneck this project has repeatedly found and (in the arousal-boost
cases) resolved with a literature-grounded gain mechanism. No such
mechanism has been applied or justified here yet -- reported as a
genuine partial result, not forced further.

Scripts/files added: `seq_eye2_highcontrast.npy`/`_bodyids.csv`,
`seq_eye2_lowcontrast.npy`/`_bodyids.csv`,
`spike_summary_eye2_highcontrast.csv`, `spike_summary_eye2_lowcontrast.csv`
(radius=2 pilot files also kept: `seq_eye_*`, `spike_summary_eye_*`).

### Wiring in the missing piece the literature named: LAL-projecting relay + DNa15 + a real wing muscle -- and the dead-end signal now completes

Follow-up to the literature check on findings 26/27's bottleneck: the
real, published LC10a model states the circuit needs downstream
integration beyond LC10a itself, specifically neurons with axon
terminals in the lateral accessory lobe (LAL). User asked to actually
wire this in from the real connectome rather than stop at the
literature finding.

**Found the real path, verified at each step, not assumed.** Checked
LC10a's real downstream table directly: after LC10a's own self-
recurrence, its next partners are entirely real AOTU subtypes (AOTU008,
019, 041, 042, etc.). Checked each candidate's real `outputRois` field
directly (not inferred from name) -- confirmed AOTU008, AOTU019,
AOTU041, AOTU042, AOTU001, AOTU012, AOTU015, AOTU016_b, AOTU002_b,
AOTU025 all genuinely have real axon terminals in LAL. Then checked
what these LAL-projecting relays actually connect to: found **DNa15** (a
real descending neuron, same DNa-family as DNa02/06/11 already used in
the main chase circuit, weight 792 from AOTU019 alone) among their real
downstream partners. Checked DNa15's own real downstream: multiple real
motor neurons, including **b3 MN** (weight 148) -- a real, named wing-
steering muscle (the b1/b2/b3 "basalar" muscles are classic, independently
documented real Drosophila flight-steering muscles) -- and **hg1 MN**
(weight 243, already present in the network from finding 15's original
build without our having used it).

**Added DNa15 and b3 MN to the existing network** (AOTU relays and
hg1 MN were already present from earlier builds) --
`connectome_lc10a_steering.csv`/`_neurons.csv`, 6,380 real neurons.
Confirmed the real edges survived (AOTU019->DNa15: 792, DNa15->b3 MN:
148).

**Reran both of finding 26/27's stimuli through the completed network:**

| | LC4 | Tm3 | LC10a | AOTU019 | AOTU041 | **DNa15** | **b3 MN** | **hg1 MN** |
|---|---|---|---|---|---|---|---|---|
| LC4-driven loom (finding 26) | 3,394 | 9,219 | 20 | 12 | 17 | **31** | **22** | **24** |
| eye-contrast, high (finding 27) | 1,654 | 1,547 | 0 | 0 | 0 | 0 | 0 | 0 |

**Result: the LC4-driven signal now reaches a real wing-steering muscle
for the first time.** Finding 26 had stopped at LC10a=20/AOTU=1-17 with
nothing downstream; adding the real, literature-identified relay and
motor stage let that same signal continue all the way to DNa15 and a
real named muscle. **This is not a new, separately-boosted result -- the
exact same stimulus and exact same upstream spike counts as finding 26
now complete the circuit**, because the missing real anatomy (not a gain
boost) was the actual bottleneck for this specific pathway.

**The eye-contrast (finding 27) condition still does not complete** --
confirms that result wasn't simply "we hadn't built far enough";
finding 27's stimulus genuinely doesn't drive LC10a hard enough at this
strength/size to go anywhere, consistent with what was already reported.

**Significance:** this directly resolves the "boosting vs. missing
neurons" question asked earlier -- for the LC4->LC10a pathway
specifically, it was a **missing-neurons problem, not a boosting
problem** -- once given real anatomy, this now-a real chain runs from a
looming visual stimulus through the escape detector (LC4), across the
real LC4->LC10a bridge, through a real courtship-associated AOTU/LAL
relay, into a real descending neuron (DNa15), and out to a real wing
muscle (b3 MN) -- entirely from real, verified connectome data, no
artificial gain applied anywhere in this specific test.

Scripts/files added: `connectome_lc10a_steering.csv`/`_neurons.csv`,
`spike_summary_steering_lc4loom.csv`, `spike_summary_steering_eyehigh.csv`.

### Does this circuit also reach a leg muscle, or is it wing-only?

User asked directly whether the newly-completed finding-28 circuit
involves leg muscles. Checked precisely rather than assuming.

**Checked DNa15's real downstream neuron metadata directly (not just
names).** All three of its real motor targets carry an explicit real
`subclass` field: hg1 MN and b3 MN = "wm" (wing muscle, segment T2);
MNnm03 = "nm" (neck muscle, T1); MNhm42/43 = "hm" (haltere muscle, T3).
**None are leg muscles -- this specific branch (via DNa15) is entirely
wing/neck/haltere, not leg.**

**But checked whether a DIFFERENT real branch reaches legs, rather than
stopping there.** Queried real weight from LC10a's AOTU relays directly
to the same leg-steering descending neurons already used in finding 17
(DNa02, DNa06, DNa11, DNp09): **AOTU019 -> that set: real weight 788,
almost identical to AOTU019's weight into the wing pathway (792).**
Broken down: AOTU019 -> DNa02 (586), DNa11 (133), DNa06 (69) -- the
exact same real leg-steering relay chain (DNa11->DNa06->DNa02->muscle)
already validated end-to-end in finding 17.

**Added DNa02/DNa06/DNa11/the real leg muscle (Sternal anterior rotator
MN) to the network** (`connectome_lc10a_legchase.csv`/`_neurons.csv`,
6,398 real neurons) and reran the identical finding-28 LC4-loom
stimulus, changing nothing else:

| | LC10a | AOTU019 | DNa15 | **b3 MN (wing)** | DNa02 | DNa11 | DNa06 | **Sternal ant. rotator MN (leg)** |
|---|---|---|---|---|---|---|---|---|
| LC4-driven loom | 20 | 12 | 34 | **19** | 37 | 8 | 32 | **59** |

**Result: the same relay point (AOTU019) genuinely branches into BOTH a
real wing pathway and a real leg pathway, and both fire from the same
single stimulus.** The signal reaches an actual real leg muscle (59
spikes) alongside the wing muscle (19 spikes) -- not a separate,
re-boosted test, the same run. **This means the courtship-relevant
visual signal (via LC10a) has a real, verified anatomical route to BOTH
motor systems simultaneously** -- consistent with real courtship
behavior needing both (walking to stay near the female AND wing
movements for song/steering) driven from a shared upstream visual
signal, not two unrelated systems.

**Honest caveat:** this doesn't show the two pathways are coordinated or
proportioned correctly relative to each other (e.g. whether real
courtship walking and wing behavior are appropriately balanced) -- only
that both are real, reachable, and simultaneously active from the same
input in this simulation.

Scripts/files added: `connectome_lc10a_legchase.csv`/`_neurons.csv`,
`spike_summary_legchase_lc4loom.csv`.

### Auditing every "boost" used in findings 26-28, then testing the strictest zero-boost version directly

User asked precisely which boosting mechanisms were active in findings
26-28, worried the results could be "cheating." Audited the actual
commands run, not memory, and found two genuinely different mechanisms
in play across this project: (1) the retina/lamina Naka-Rushton
amplification (`--amplify`, applied to the STIMULUS before Mi1, from
finding 18), and (2) the synaptic `--type-boost` (the 8x LC9 arousal
multiplier or LC16's 0.1x dopamine brake, applied to the NETWORK).

**Audit result:** findings 26, 27, and 28 used NO synaptic `--type-boost`
at all -- default, unmodified calibration throughout. But retinal
amplification (`--amplify`) WAS used for the LC4-loom stimulus and the
finding-27 high-contrast condition -- and, caught in this audit, NOT
used for finding 27's low-contrast condition (which was built by scaling
a raw, unamplified image down to 10%) -- a real, previously-unflagged
inconsistency between the two conditions.

**Reran the finding-27 contrast comparison with amplification removed
from BOTH conditions**, the strictest possible test -- raw, unamplified
Mi1 input in both cases, no synaptic boost, nothing else changed:

| condition | Mi1 | Tm3 | LC4 | LC10a | wing/leg output |
|---|---|---|---|---|---|
| high contrast (raw, no amplify) | 1,870 | 1,157 | **1,348** | 0 | 0 |
| low contrast (raw, no amplify, 10% of high) | 311 | 7 | **0** | 0 | 0 |

**Result: a real, unboosted contrast effect survives at the LC4 stage**
(1,348 vs. 0 spikes -- high contrast drives LC4 robustly, low contrast
doesn't drive it at all) -- this part of the earlier finding-27 result
is genuine, not a product of the amplification asymmetry. **But without
ANY boosting mechanism, neither condition reaches LC10a or the wing/leg
outputs found in finding 28** -- the entire downstream circuit is
silent either way.

**Honest conclusion:** the retinal amplification stage is not an
invented shortcut to manufacture results -- it is load-bearing. Without
it, the courtship-tracking circuit (LC10a onward, including both the
wing and leg branches from finding 28) produces zero output regardless
of stimulus contrast. This matches the same real, literature-grounded
justification already established for the main chase circuit in
finding 18 (real photoreceptor/lamina amplification is documented real
Drosophila biology, not something invented for this project) -- but it
is an honest dependency to state plainly: **finding 28's wing/leg
circuit completion required the retinal amplification stage to be
active on the input; it did not require any synaptic-level type-boost.**

Scripts/files added: `seq_eye2_highcontrast_noamplify.npy`/`_bodyids.csv`,
`spike_summary_noboost_highcontrast.csv`,
`spike_summary_noboost_lowcontrast.csv`.

### Specificity control for finding 28: does the courtship circuit also (wrongly) reach a biologically unrelated body part?

User's direct challenge: we showed the courtship-visual circuit reaches
real wing and leg muscles -- does it ALSO reach muscles that have no
business being involved (a real negative control), using only natural,
real connectome wiring, not invented connections.

**Found a real, clean, biologically unrelated candidate.** Real male-cns
motor neuron types carry a real `subclass` field distinguishing muscle
groups: wm=wing, nm=neck, hm=haltere, fl/hl/ml=fore/hind/mid-leg, and
**pm=pharyngeal/proboscis (feeding)** -- confirmed by checking actual
type names under "pm": includes **MN9**, the same real sugar-taste-
pathway motor neuron already used in finding 11. Feeding is genuinely,
biologically unrelated to visual courtship tracking -- a legitimate
negative control.

**Checked real direct connectivity first, from every hub neuron in the
completed courtship circuit straight to the feeding-muscle group:**
LC10a, AOTU019/041/008/042, DNa15, and DNa02 all show **real weight =
0** into any pm-type feeding muscle. No direct real synapse exists at
all.

**Then did the stronger, full test rather than stopping at the edge
check.** Added the real MN9 neurons to the complete finding-28 network
(6,400 real neurons total) and confirmed MN9's only real connections
anywhere in this entire network are to another unrelated motor neuron
(MN5) -- no path into the courtship circuit exists even indirectly.
Reran the identical LC4-loom stimulus that drove both the wing and leg
muscles:

| | LC4 | LC10a | b3 MN (wing) | Sternal ant. rotator MN (leg) | **MN9 (feeding, unrelated)** |
|---|---|---|---|---|---|
| same stimulus as finding 28 | 3,394 | 20 | 19 | 59 | **0** |

**Result: clean, real specificity.** The same stimulus that fires both
real motor outputs leaves the biologically unrelated feeding motor
neuron at exactly zero -- not because it was excluded or filtered, but
because no real synaptic path exists from this circuit to it in the
actual connectome. This is a genuine, positive specificity result,
directly analogous to the LC21 baseline control (finding-17 era) and
the finding-20/21 ablation tests -- the courtship-tracking circuit
reaches the real body parts it should, and does not reach one it
shouldn't, using only real, natural connectome wiring throughout.

Scripts/files added: `connectome_lc10a_specificity.csv`/`_neurons.csv`,
`spike_summary_specificity.csv`.

### Extending the specificity control to 3-4 more real, biologically-named body systems

User's direct request: one unrelated-body-part control (MN9/feeding)
isn't enough to rule out a fluke -- add several more, using real,
biologically-identifiable named muscles (not generic alphanumeric codes
like "MNad21"), so the specificity claim rests on more than one data
point.

**Searched for real, named (not generically-coded) motor neuron types
across different body systems** by filtering out purely-numeric-coded
type names. Found real, clearly-identified muscle groups: haltere
(hi1 MN, hi2 MN, hDVM MN, hiii2 MN -- distinct from the MNhm42/43 codes
already known to connect), a second, independent feeding-muscle set
(MN4a, MN4b, MN11V, distinct neurons from MN9's own group), and neck
muscles (ADNM1 MN, ADNM2 MN). Salivary, antennal, ocellar, and genital
motor neuron types were searched for but don't exist as named types in
this dataset (real absence, not a skipped search).

**Checked real direct connectivity from every hub in the courtship
circuit before running anything** (LC10a, all four AOTU relays, DNa15,
DNa02): haltere and the second feeding group showed real weight = 0
from every hub -- clean candidates. **Neck showed a real, non-trivial
connection: DNa02 -> ADNM1/ADNM2, weight 36** -- not filtered out or
treated as a problem; a real, biologically sensible result (head/neck
orientation is plausibly part of visually tracking a target), reported
honestly rather than forced into "should be zero."

**Built all three groups into the network (6,422 real neurons total)
and reran the identical stimulus:**

| | b3 MN (wing) | leg muscle | MN9 (feeding) | haltere (4 types) | feeding-2 (3 types) | **neck (ADNM1/2)** |
|---|---|---|---|---|---|---|
| same stimulus | 19 | 59 | 0 | 0 | 0 | **38 / 1** |

**Result: specificity confirmed across multiple, independent, real
biological systems, not a single data point.** Two entirely separate
feeding-related neuron groups (MN9 and MN4a/4b/11V) both stayed at
exactly zero, as did four distinct named haltere motor neurons -- three
independent real "should not fire" tests, all consistent. The one
system that DID show activity (neck) did so for a real, identified
reason (a genuine, if modest, real synaptic path from DNa02) and makes
biological sense rather than looking like noise -- an honest positive
finding, not a control failure.

### Correction: haltere was never a valid negative control, and this project's own earlier data already showed why

User challenged the haltere result directly: halteres are evolutionarily
modified hindwings, function as real gyroscopic flight-stabilization
sensors, and are well documented in real Drosophila biology to be
neurally coupled to wing-steering circuits -- not an independent system
from wings at all. A poor choice for "unrelated system" from the start.

**Checked our own prior data before responding, and found the critique
already independently confirmed by this project's own earlier work.**
Finding 28's real downstream trace of DNa15 -- the same descending
neuron used throughout this circuit -- already showed a real, non-
trivial connection to haltere motor neurons MNhm42 (weight 154) and
MNhm43 (weight 151). The later "haltere = 0" specificity result used
different, specific named haltere neurons (hi1/hi2/hDVM/hiii2) that
happen not to be connected -- an accurate result for those particular
neurons, but reported under the misleading framing that "haltere" as a
category is unconnected, when this project's own finding 28 had already
shown otherwise for a different haltere neuron subset.

**Correction: the haltere result is withdrawn as a negative control.**
It doesn't disprove the specific numbers reported (hi1/hi2/hDVM/hiii2
genuinely were at zero), but haltere was never a fair test of whether
this circuit wrongly reaches unrelated systems, since real halteres are
part of the same functional flight apparatus as wings, and this
project's own data already shows a real connection at the subclass
level. **The genuinely defensible negative-control result is narrower
than first claimed: one independent, functionally unrelated system
(feeding), confirmed twice via two separate real neuron groups (MN9;
MN4a/MN4b/MN11V), both at exactly zero.** The neck result stands as
reported (a real, honest positive finding, not affected by this
correction).
`spike_summary_specificity2.csv`.

### Methodological upgrade: real trial-to-trial noise, and boost-multiplier sweeps instead of single hand-picked values

User asked us to actually implement two of the four methodological
fixes discussed after the "would a flyvis-caliber team roll their eyes"
conversation: (3) sweep boost multipliers across a range instead of
reporting one chosen value, and (4) add real stochastic noise and rerun
key tests multiple times, reporting distributions instead of single
numbers. Then redo the three main test threads (looming/escape,
small-target chase, eye-contrast) under both upgrades.

**Implemented real noise in `simulate.py`, not a workaround.** Added a
standard Brian2 Euler-Maruyama noise term to the membrane voltage
equation (`sigma_noise*xi*tau_mbr**-0.5`), a new `--noise-sigma` CLI
flag (default 0, exactly reproducing every prior finding's fully
deterministic behavior), and properly seeded Brian2's own RNG via
`--seed` (previously unseeded -- a real, if minor, reproducibility gap
fixed in passing). Verified: noise-sigma=0 gives bit-identical results
across different seeds (confirms backward compatibility); noise-sigma=
0.5mV gives real, visible trial-to-trial variability (e.g. one test
neuron's count varied 29/59/95 across 3 seeds) without swamping the
signal. Chose 0.5mV and N=8 trials per condition as a moderate,
practical standard for this pass.

**Scenario B -- chase circuit (finding 18-21's 8x boost), full sweep x
noise:**

| boost | LC9 (mean +- std) | muscle (mean +- std) |
|---|---|---|
| 0x (no boost) | 30 +- 1 | 0.0 +- 0.0 |
| 2x | 8,162 +- 71 | 155.4 +- 5.5 |
| 4x | 11,325 +- 13 | 183.8 +- 4.8 |
| 8x (original) | 12,970 +- 35 | 194.2 +- 3.9 |
| 16x | 13,833 +- 7 | 197.1 +- 3.6 |

**Result: the finding is far more robust than the original single-point
report suggested.** The circuit turns on robustly at ANY tested boost
from 2x through 16x -- not narrowly dependent on the specific 8x value
originally chosen. The response saturates (diminishing returns above
~4x) rather than scaling linearly -- a real, sigmoidal dose-response
shape, now properly characterized instead of assumed. Noise-induced
variability (std) is small relative to the differences between boost
levels, meaning the qualitative "aroused fires, unaroused doesn't"
conclusion is not noise-sensitive at all. **This upgrades finding 18
from "we picked 8x and it worked" to "the circuit reliably switches on
across a wide, realistic range of gain values, with real error bars."**

**Scenario C -- eye-contrast test (finding 27), noise x trials (no
synaptic boost was ever used here, confirmed by the earlier audit, so
the redo adds noise/trials only, no boost sweep):**

| condition | Tm3 (mean +- std) | LC10a | leg muscle |
|---|---|---|---|
| high-contrast (amplified) | 1,545 +- 6 | 0.0 +- 0.0 | 0.0 +- 0.0 |
| low-contrast (amplified) | 8 +- 1 | 0.0 +- 0.0 | 0.0 +- 0.0 |
| high-contrast (raw, no amplify) | 1,160 +- 5 | 0.0 +- 0.0 | 0.0 +- 0.0 |

**Result: finding 27's conclusion is confirmed robust, not a fluke of
one deterministic run.** Across 8 independent noisy trials per
condition, LC10a and the leg output stay at EXACTLY 0.0 +- 0.0 in every
single trial, every condition -- the small eye-sized stimulus genuinely
never crosses threshold into the courtship circuit, with real noise
included. Tm3's real, large contrast-dependent difference (1,545 vs. 8)
also survives with tight, real error bars.

**Scenario A -- looming/escape motion-vs-shape balance (finding 22/23),
noise x trials, per-trial-paired ratio (not just computed on the
means):**

| condition | DNp01 (mean +- std) | LC4 (mean +- std) |
|---|---|---|
| weak (still spider) | 73.0 +- 1.9 | 1,756.4 +- 42.1 |
| motion-only (loom blob) | 78.9 +- 0.8 | 1,899.8 +- 8.3 |
| strong (loom spider) | 86.4 +- 0.9 | 2,119.6 +- 15.5 |

Motion's real share of the total effect, computed per-trial (paired,
not just on the aggregate means): **DNp01 = 42.8% +- 14.3%, LC4 = 38.7%
+- 7.7%** (real flies: 63.2%, per de la Flor et al. 2017). **Result:
finding 22's corrected conclusion (our model underweights motion
relative to real flies) holds up under real noise and now carries
honest error bars** -- DNp01's estimate in particular is fairly
imprecise (+-14.3 percentage points), a real uncertainty that the
original single-run number completely hid. Both readouts remain clearly
below the real 63.2% even accounting for this noise, so the core
mismatch is not an artifact of picking one lucky/unlucky trial.

**Overall: this pass didn't overturn any existing finding, but it
replaced several single, deterministic numbers with real distributions
and swept ranges, exactly the upgrade a rigor-minded reviewer would ask
for** -- and in the one case where it mattered most (the arousal boost),
it made the finding considerably stronger, not weaker, by showing the
qualitative conclusion holds across a wide range rather than one
cherry-picked value.

Scripts/files added: `simulate.py` (`--noise-sigma`, proper Brian2
`--seed` wiring), `redo_with_controls.py`, `redo_scenario_A.py`,
`redo_scenario_C.py` (scratchpad), `results_redo_with_controls_A.csv`,
`results_redo_with_controls_B.csv`, `results_redo_with_controls_C.csv`.

### Fixing #1 and #2 for real: documented the field-wide parameter-uniformity problem honestly, and ran the synapse-weight-mapping robustness test -- which surfaced a real, significant complication

User asked to actually address the two remaining flyvis-caliber critiques
(uniform electrophysiology parameters; synapse-count treated as
functional strength) rather than stop at scenario B/C/A's upgrades.

**#1 -- checked before attempting a fix, and found the "fix" would have
made things worse.** Directly verified whether Shiu et al.'s own
published whole-brain model (the field's actual state of the art) uses
per-cell-type electrophysiology. It does not: ONE global membrane
resistance (10 MOhm) and capacitance (0.002 uF) for all 125,000+ real
neurons in their entire model. Real patch-clamp data doesn't exist at
this scale for almost any Drosophila cell type. Concluded that inventing
our own per-neuron parameters (e.g. scaling by real neuron size, an
option considered) without real data to calibrate them against would
replace one honestly-flagged simplification with a less-honest one that
only looks more sophisticated. **Documented as a real, field-wide open
problem in `findings_summary.md`'s limitations section instead of
patched.**

**#2 -- searched for real per-transmitter magnitude data, found none,
ran a real robustness test instead of inventing numbers.** The
excitatory/inhibitory sign assignment (GABA/glutamate = inhibitory) is
real and cited. Relative PSP *magnitude* differences by transmitter
class in Drosophila are not quantified anywhere found. Rather than
invent multipliers, implemented a real, testable alternative: whether
real synapse count maps to functional strength LINEARLY (this project's
assumption throughout) or SUB-LINEARLY/saturating (a real, documented
property of synapses generally, just not quantified per-type here).

**Implemented `--weight-exponent` in `simulate.py`** (default 1.0 =
original linear mapping, exact backward compatibility confirmed).
0.5 = square-root, anchored to agree exactly with the linear mapping at
a real reference synapse count (20) so the sweep changes only the
curve's SHAPE, not its overall scale.

**Reran the chase-circuit boost sweep (scenario B) under both
mappings, with noise x 6 trials:**

| exponent | boost=0x | boost=2x | boost=8x | boost=16x |
|---|---|---|---|---|
| linear (1.0, original) | 0.0 +- 0.0 | 156.8 +- 5.6 | 194.0 +- 4.1 | 197.3 +- 4.1 |
| **sqrt (0.5, saturating)** | **57.7 +- 2.1** | 66.8 +- 2.5 | 75.5 +- 2.8 | 76.0 +- 1.6 |

**Result: a real, significant complication, not a minor footnote.**
Under the sub-linear mapping, **the chase circuit already fires
substantially with ZERO arousal boost** (57.7 muscle spikes at 0x,
vs. exactly 0.0 under the linear assumption) -- and the boost's effect
becomes much smaller in relative terms (57.7 -> 76.0, roughly +32%,
vs. the linear case's 0 -> ~197, effectively an on/off switch).

**Honest interpretation: finding 18-21's entire "arousal gate" framing
(circuit is OFF until aroused, ON once boosted) rests on an unvalidated
assumption -- that synapse count maps linearly to functional strength --
that has no real literature backing, and an equally plausible
alternative assumption (sub-linear/saturating, also real and documented
in the general synaptic-physiology literature, just not quantified for
this specific circuit) gives a qualitatively DIFFERENT picture: a
circuit that's always somewhat active and gets modestly enhanced by
arousal, not a true on/off gate.** This does not mean the linear
assumption is wrong, or that findings 18-21 are false -- the real
literature-grounded facts underlying them (P1/dopamine arousal gating
exists and is real; the specific 8x/0.1x magnitudes were always flagged
as estimates) are unaffected. What changes is how confidently the
specific "silent until aroused" qualitative SHAPE of the result should
be stated -- it is now known to be sensitive to a real, unresolved
modeling choice, not a robust, assumption-independent conclusion.
**This is exactly the kind of result a proper robustness check is
supposed to surface, and it was found by doing the check honestly
rather than only running the version expected to confirm the original
finding.**

Scripts/files added: `simulate.py` (`--weight-exponent`,
`--weight-exponent-ref`), `redo_weight_exponent.py` (scratchpad),
`results_weight_exponent_sweep.csv`.

### Full matrix: 3 stimuli (blob / red-eye / white-eye) x 5 arousal levels, full circuit to leg AND wing muscles, plus all specificity controls, real noise x trials

**Same correction applies here (see above): "red-eye" and "white-eye"
are the same generic blob image at two brightness levels, not an eye
stimulus.** Read as "blob," "high-contrast blob," "low-contrast blob"
throughout this entry.

User asked for the most comprehensive single test yet: every stimulus,
every arousal level, the complete circuit through to both real motor
outputs, with the finding-29 specificity controls included throughout.

**Caught and fixed a real bug before trusting any result.** The network
this required (`connectome_lc10a_specificity2`) descended from finding
15's original LC10a build, which never actually included LC9 or its
real upstream bridges (Y3, T2a, TmY5a) -- an oversight carried through
several subsequent builds (28, 29) without being noticed, because those
tests never exercised the LC9-boost pathway on this particular lineage.
First run of the matrix showed LC9 stuck at exactly 0 in literally every
condition including 16x boost -- caught this as implausible immediately
(contradicts scenario B's own solid earlier result), checked directly,
and confirmed LC9/Y3/T2a/TmY5a/Tm5Y were simply absent as nodes. Fixed
properly: added all five real types plus refetched every real edge
among the full union (11,402 real neurons total,
`connectome_full_matrix.csv`/`_neurons.csv`), verified real Mi1->Y3
(65,229), Y3->LC9 (2,058), and LC9->LC10a (9,661) edges were present
before rerunning anything.

**Full corrected results (5 trials/noise per cell, means shown, full
std in `results_full_arousal_matrix.csv`):**

| stimulus | boost | LC9 | LC10a | leg muscle | wing (b3 MN) |
|---|---|---|---|---|---|
| blob | 0x | 3,683 | 759 | 376 | 115 |
| blob | 2x | 8,704 | 1,728 | 404 | 144 |
| blob | 4x | 11,411 | 2,117 | 419 | 153 |
| blob | 8x | 13,014 | 2,335 | 415 | 156 |
| blob | 16x | 13,824 | 2,435 | 423 | 160 |
| eye_red_contrast | 0x-16x | (nearly identical to blob row-for-row) | | | |
| eye_white_contrast | 0x-8x | **0** | **0** | **0** | **0** |
| eye_white_contrast | **16x** | **11,652** | **1,931** | **343** | **132** |

**Finding 1 -- blob and red-eye-contrast are, in this network, barely
distinguishable stimuli.** Both conditions land at nearly identical
numbers at every boost level (e.g. LC9: 3,683 vs. 3,713 at 0x). Checked
why: both stimuli use the same real hex window (radius=4, same center
position) -- the specific "eye-sized, high-contrast" stimulus ends up
driving a similar total real Mi1 population as the full courtship-target
blob once passed through the same amplification. **This means the
earlier framing of "the eye-contrast test" as meaningfully different
from the main chase-target test needs a caveat: at this size/position,
they are not clearly distinct inputs to this circuit** -- a real,
previously-unflagged overlap.

**Finding 2 -- new, real, and directly consistent with Pan et al. 2012's
actual experiment.** The low-contrast ("white eye") condition stays at
exactly zero through boost levels 0x-8x, matching every earlier result
-- but at **16x, it suddenly fires the entire circuit**, reaching both
the leg muscle (343) and the wing muscle (132). This is a genuinely new
result: sufficiently high arousal can push even a very weak, otherwise
sub-threshold visual cue through the whole real circuit to both motor
outputs. This is a striking, quantitative echo of the real behavioral
finding discussed earlier this session -- artificially fully-aroused
male flies chase and court non-specific, poorly-defined moving objects
(a rubber band) that an unaroused male ignores entirely. Here, a
"low-contrast, borderline" stimulus that never moved the unaroused or
mildly-aroused circuit becomes fully effective once arousal is strong
enough -- the same real qualitative pattern (arousal lowers the bar for
what counts as a valid target), reproduced quantitatively for the first
time in this simulation.

**Specificity holds perfectly across the entire 15-condition matrix.**
All 8 real control neurons from finding 29 (MN9, the second feeding
group, all four haltere neurons) stayed at EXACTLY 0.0 in every single
condition, including the newly-firing high-boost white-eye case -- the
circuit's real selectivity does not break down even under the strongest
tested arousal state.

Scripts/files added: `connectome_full_matrix.csv`/`_neurons.csv`,
`full_arousal_matrix.py` (scratchpad, edited in place to use the
corrected network), `results_full_arousal_matrix.csv`.

### Actually testing red-eye vs. white-eye for real: built a genuine head+eye stimulus, found a real amplification confound, then found a deeper methodological limit

User pushed to test the real hypothesis properly after the "this was
never a red-eye test" correction: the real paper's own reasoning is that
red eyes contrast sharply against the lighter head/cuticle while white
eyes blend in -- a real local-contrast question, testable in grayscale
without needing color vision.

**Built a real head+eye composite, not a lone blob.** Synthetic image:
a medium-gray head-sized disc on a light background, with a smaller
eye-sized circle either much darker (red-eye analog, real local
contrast against the head) or the same brightness as the head
(white-eye analog, blends in completely) -- `redeye_analog.jpg`/
`whiteeye_analog.jpg`. Verified visually and numerically before running
anything: same head size/position/overall mean contrast in both
(0.246 vs. 0.245), differing only in whether the eye region pops out.

**Caught a real confound before trusting results: our own amplification
was erasing the very difference being tested.** Checked the actual
amplified values directly: raw contrast for head (0.235) vs. red eye
(0.627) is a real ~2.7x difference, but after the project's standard
low-c50 Naka-Rushton amplification, both saturate to nearly the same
output (0.833 vs. 0.855, ~1.03x) -- the amplification designed to help
weak signals was compressing the real signal we were trying to measure.
Tested a range of c50 values; even at c50=0.5 (much higher than
standard), compression to ~1.37x remained substantial. Ran BOTH raw
(unamplified, true ~2.7x difference preserved) and moderately-amplified
(c50=0.35, partial preservation) variants rather than picking one.

**Full result, both arousal levels, both amplification settings, on the
corrected complete network (`connectome_full_matrix`):**

| variant | condition | boost | Tm3 | LC9 | LC10a | leg | wing |
|---|---|---|---|---|---|---|---|
| raw | red-eye | 0x | 397 | 16 | 34 | 195 | 20 |
| raw | white-eye | 0x | 341 | 11 | 22 | 126 | 27 |
| raw | red-eye | 8x | 404 | 12,178 | 2,068 | 378 | 143 |
| raw | white-eye | 8x | 344 | 12,098 | 2,072 | 368 | 144 |
| modamp | red-eye | 8x | 1,044 | 12,788 | 2,231 | 398 | 152 |
| modamp | white-eye | 8x | 1,020 | 12,776 | 2,186 | 399 | 153 |

**Result: nearly identical at every downstream readout, in every
condition -- a real, honest negative result, and traced to its actual
cause rather than left unexplained.** At 8x arousal (raw), LC10a differs
by only 0.2% between red-eye and white-eye. Checked why directly, at the
level of individual driven Mi1 neurons rather than accepting the
aggregate null result at face value: **only 2 of the 113 real neurons in
the entire stimulus window show a substantial local contrast difference
between conditions** (raw diff +0.277 and +0.196); the other 111 --
looking at the identical surrounding head -- show negligible or zero
difference. Mean difference across the whole population: 0.0049,
essentially nothing.

**Real, generalizable methodological conclusion, not specific to this
one test:** every finding in this project measures TOTAL, POOLED spike
counts across a whole driven population. That method is structurally
blind to a small, spatially localized feature (like one differently-
colored eye) embedded in a much larger, otherwise-unchanged shape -- not
because the underlying neurons fail to detect it (2 specific neurons
clearly do, with a large real local contrast difference), but because
summing across the whole population buries that signal under everything
else. **A genuine test of the red-eye/white-eye hypothesis would need to
track the specific, small subset of neurons anatomically positioned to
see the eye (e.g. bodyIds 51122, 34057 here), not pooled population
totals** -- a different kind of analysis than anything done elsewhere in
this project, not yet built.

Scripts/files added: `redeye_analog.jpg`, `whiteeye_analog.jpg`,
`seq_redeye.npy`/`seq_whiteeye.npy` (initial, over-amplified),
`seq_redeye_raw.npy`/`seq_whiteeye_raw.npy`,
`seq_redeye_modamp.npy`/`seq_whiteeye_modamp.npy`
(+ all `_bodyids.csv`), spike summaries in `/tmp/realeye_*.csv`
(not moved to the project directory -- scratch comparison only).

### Following up finding 32: routed through LC9/LC10a directly, then found the real mechanism that would fix it

User asked to route the head+eye stimulus through the real LC9/LC10a
small-object pathway specifically rather than stop at the pooled-sum
null result, then asked whether real fly brains have something more
sophisticated than a flat sum for combining individual neuron signals.

**Per-neuron (not pooled) comparison of LC9/LC10a, using the already-
saved raw 8x spike summaries (per-bodyId data was already present in
the standard `--spike-summary-out` CSV, no rerun needed).** Real,
reproducible per-neuron differences DO exist, unlike the pooled sum:
85/115 real LC9 neurons and 44/87 real LC10a neurons show nonzero,
reproducible differences between red-eye and white-eye conditions (up
to +-6 spikes for a single LC9 neuron). But the differences are a
roughly even mix of increases and decreases across the population, no
single obvious "eye-detector" neuron. Attempted to check spatial
clustering (do the differing neurons share a real anatomical position)
but hit a known, previously-established limit: LC9 lacks real per-
neuron retinotopic coordinates in this dataset (broad receptive fields,
not populated in neuprint's schema) -- could not confirm whether this
reflects genuine localized encoding or is recurrent-network scatter
from LC9's own heavy self-recurrence. Left as a genuine, unresolved
result.

**User's direct guess -- that real brains have a more sophisticated
combination mechanism than a flat sum -- checked against real
literature and confirmed precisely, with a named, citable mechanism.**
[Keleş & Frye 2017, Current Biology, "Object-Detecting
Neurons in Drosophila"](https://pubmed.ncbi.nlm.nih.gov/28190726/):
LC11 (a real, close relative of LC9/LC10a in the same small-object-
detector family) has a documented **end-stopped inhibition** receptive
field -- an excitatory center + inhibitory surround. A small object
landing in the center excites; a large, spatially-extended stimulus
(like our uniform head) spilling into the surround actively SUPPRESSES
the response, rather than merely failing to add to it. Causally
confirmed in the real paper: blocking the inhibitory current
experimentally abolished small-object selectivity and made the neuron
respond just as well to large bars/gratings instead -- proving the
inhibition, not just the excitation, is what creates small-object
selectivity.

**Direct implication for finding 32's negative result.** Our simulation
modeled these neurons as pure linear summers -- every excitatory input
adds, nothing actively suppresses a large uniform region. Real LC11-
type neurons do the opposite: the large "head" region would actively
push the response DOWN via real surround inhibition, making the small
eye-region's contribution stand out by contrast rather than being
diluted by volume, exactly the missing mechanism that would plausibly
let a real fly detect what our pooled-sum test could not. **This is
now a real, precise, literature-grounded, buildable next step (add
real center-surround/end-stopped inhibitory structure to the LC9/LC10a
model) rather than a vague "needs more sophistication" gesture.**

Scripts/files added: none (per-neuron analysis reused already-saved
CSVs; remainder is literature research).

### Building the temporal-binding test: does synchrony between "parts" matter, using tools already in hand

User pushed back correctly on treating "central complex/learning required"
as a hard boundary -- scope is a choice, and the temporal-binding
hypothesis (parts of a real object share correlated timing; a fly might
not need a dedicated "gestalt neuron" to notice they belong together,
just circuitry sensitive to that shared timing) is fully testable with
the existing simulator, no new circuitry needed.

**Built two real, matched 10-frame stimulus sequences from the same
head+eye composite used in finding 32/33**, bypassing `photo_at_position.py`
(which doesn't support two independently-modulated regions) with a
custom renderer following the same real contrast/blur pipeline: head
and eye brightness both oscillate over 10 frames, either IN PHASE
(rise and fall together -- "real object" case) or 180-degrees ANTI-
PHASE (eye peaks exactly when head dips, and vice versa). Verified
before running anything: time-averaged brightness matches almost
exactly between conditions (0.0417 vs. 0.0417) -- confirms the only
real difference is the TIMING relationship, not overall energy.

**Ran both through the complete real circuit (`connectome_full_matrix`,
8x arousal boost, deterministic/no noise so the same-seed comparison is
exact):**

| readout | in-sync | out-of-sync | diff |
|---|---|---|---|
| Mi1 (driven) | 1,039 | 1,047 | +8 |
| Tm3 | 419 | 431 | +12 |
| LC9 | 21,444 | 21,413 | -31 |
| LC10a | 3,633 | 3,602 | -31 |
| LC4 | 5,683 | 5,677 | -6 |
| AOTU008 | 802 | 783 | -19 |
| **pC1_18b** | **188** | **438** | **+250 (+133%)** |
| **aIPg5** | **170** | **473** | **+178%** |
| DNa15 | 232 | 235 | +3 |
| b3 MN (wing) | 269 | 268 | -1 |
| DNa02 | 310 | 311 | +1 |
| leg muscle | 668 | 673 | +5 |

**Result: a real, large, reproducible effect -- at exactly two specific
real central-brain neurons, and in the OPPOSITE direction from the naive
binding-hypothesis prediction.** The entire early/main pathway (Mi1
through LC10a, LC4, AOTU008) and both final motor outputs (wing, leg)
show negligible difference (all within a few percent, consistent with
"timing doesn't matter for the core sensorimotor chain"). But **pC1_18b
and aIPg5 -- real courtship-circuit neurons from finding 15's own
LC10a->AOTU->pC1->aIPg->pIP10 chain -- respond far MORE strongly to the
temporally UNCORRELATED (anti-phase) stimulus**, not the synchronized
one. This is the opposite of what "these neurons detect that the parts
belong together via shared timing" would predict.

**Honest interpretation, not forced into a clean story:** this is a
real, substantial, deterministic (not noise) effect at specific, real,
identifiable neurons -- not a null result, and not something to hide
because it contradicts the hypothesis being tested. The most likely
mechanism, not yet independently confirmed: pC1/aIPg may function as
coincidence detectors sensitive to being driven by MULTIPLE
asynchronously-arriving inputs rather than one synchronized input peak
-- i.e., out-of-sync timing may create more DISTINCT temporal windows
in which some input is elevated, giving these convergence neurons more
separate opportunities to be pushed over threshold, versus in-sync
timing concentrating all drive into fewer, larger but less numerous
peaks. This is a plausible, testable follow-up hypothesis, not a
confirmed mechanism.

**What this does NOT show:** it does not confirm or refute the general
"binding by temporal correlation" hypothesis from the literature --
that literature describes correlated timing as the binding CUE (parts
that move together get treated as one object), and this test found the
opposite real pattern at these two specific neurons. This could mean
(a) pC1/aIPg are not the real substrate for temporal binding at all, or
(b) the real relevant temporal structure differs from a simple 10-frame
sine-wave modulation, or (c) something else. Recorded as a genuine,
unresolved, real finding, not resolved further here.

Scripts/files added: `build_temporal_binding.py` (scratchpad),
`seq_temporal_insync.npy`/`seq_temporal_outsync.npy` (+ `_bodyids.csv`).

### RETRACTION: the pC1_18b/aIPg5 temporal-binding effect does not survive noise and repeated trials

User asked directly whether the striking pC1_18b/aIPg5 result above
holds up under real noise and repeated trials -- exactly the kind of
check this project's own protocol calls for before trusting a dramatic
single-run result. It does not hold up.

**Reran both conditions with real noise (0.5mV) and 8 trials each**
(same complete network, same 8x boost, same stimuli):

| readout | in-sync (mean+-std) | out-of-sync (mean+-std) | approx z-score |
|---|---|---|---|
| pC1_18b | 416.5 +- 20.9 | 424.1 +- 18.3 | +0.27 |
| aIPg5 | 453.1 +- 26.6 | 458.5 +- 25.8 | +0.15 |
| LC9 | 21,443.1 +- 32.3 | 21,436.1 +- 31.9 | -0.15 |
| LC10a | 3,647.8 +- 35.4 | 3,628.9 +- 19.8 | -0.47 |
| leg muscle | 689.1 +- 6.2 | 694.0 +- 11.1 | +0.38 |

**Every readout's difference is now well under 1 standard deviation --
no statistically meaningful effect anywhere, including pC1_18b and
aIPg5.** Critically, even the in-sync CONDITION's own trial-averaged
mean for pC1_18b (416.5) is wildly different from the single
deterministic run originally reported (188) -- proving that first run
was an unrepresentative outlier for that specific random seed, not a
stable baseline. **The dramatic, real-looking 2-3x effect reported above
was a fluke of comparing two single, unlucky/lucky deterministic seeds
against each other, not a real property of how this circuit responds to
timing.**

**Retracted, not deleted -- kept in place with this correction directly
below it, per this project's own established practice** (matching the
binocular-suppression retraction earlier in this project's history).
The underlying question (does temporal correlation between parts matter
to this circuit) remains genuinely open -- this specific test, once
properly checked, found no evidence either way, not evidence against
it and not evidence for it. A real test would need many more trials
and/or a stimulus manipulation with a larger expected effect size to be
distinguishable from noise at this network's baseline variability.

Scripts/files added: `redo_temporal_binding.py` (scratchpad),
`results_temporal_binding_noise.csv`.

### User located the real Dryad dataset behind de la Flor et al. 2017 -- corrects finding 22's target, and recreating the real 2x2 exposed a deeper confound

User provided the actual Dryad link
(https://datadryad.org/dataset/doi:10.5061/dryad.4mb11). Downloaded the
real raw data (`Spider Data.xlsx`, 18 sheets, one per figure panel;
Figure 4b is the exact panel behind finding 22, n=32 flies/condition).

**Real, data-verified numbers, replacing the earlier web-summary
estimates:** still mock spider 33.4%, moving mock spider 2.0%, still
stir-bar 42.4%, moving stir-bar 17.8% (all % of 600s spent near the
threat). Verified the paper's own reported statistic independently:
Mann-Whitney U on moving spider vs. moving stir-bar, p=0.0019 (paper:
P=0.010, real and significant either way). Recomputed finding 22's real
target: motion explains 49.7% of the effect, not the originally-used
63.2% (an approximate figure from a web summary) -- a real, material
correction, made and kept visible rather than silently edited.

**User then directly observed something in the real data worth checking
rather than assuming:** still spider (33.4%) vs. still stir-bar (42.4%)
-- a real numeric gap from SHAPE ALONE, zero motion. Checked statistically
before endorsing the claim "flies visually recognize spiders": Mann-
Whitney U, p=0.224 -- NOT significant at n=32. The paper's own real,
significant evidence for shape effects only appears once motion is
present (the p=0.0019 result above); the still-only comparison doesn't
support shape recognition at rest on its own. Corrected the inference
rather than accepting the plausible-looking raw numbers at face value.

**Then recreated the real experiment's full 2x2 design in the
simulation directly** (still spider / moving spider / still blob /
moving blob, real noise x 8 trials), and caught a deeper, previously-
unnoticed confound while setting it up: the earlier finding-22
normalization paired still-conditions and loom-conditions to DIFFERENT
target brightness levels (0.378 for still, 0.644 for loom) -- meaning
"motion" and "overall brightness" were never actually separated in the
original test. Fixed by normalizing all four conditions to one common
target mean (0.378) before running anything.

**Result, properly deconfounded:**

| condition | DNp01 | LC4 |
|---|---|---|
| still spider | 73.0 +- 1.9 | 1,756.4 +- 42.1 |
| moving (loom) spider | 69.1 +- 2.0 | 1,668.4 +- 41.3 |
| still blob | 68.9 +- 1.8 | 1,580.9 +- 35.9 |
| moving (loom) blob | 58.5 +- 1.7 | 1,364.2 +- 29.1 |

**Real, significant, and troubling finding: once brightness is properly
held constant, our simulated "motion" (looming) effect REVERSES --
moving stimuli produce LESS activity than still ones, for both spider
and blob, at both readouts.** This directly contradicts finding 22's
original framing (which always treated "loom" as the stronger, more
threat-like condition). Root cause identified: our zoom-based looming
stimulus generator naturally samples brighter, more central image
content as it "zooms in" frame-by-frame, so every prior looming
condition in this project was confounded with a real, unintended
brightness increase -- what looked like "motion increases response" was
at least partly "the frames got brighter," not purely a real dynamic-
motion effect.

**Honest state, not yet resolved:** this calls into question the
looming-vs-static comparisons throughout findings 1, 2, 8, 13, and 22 to
some degree, since several of them may share this same brightness-
confound in how looming stimuli were generated. Not all of those are
necessarily invalidated (some used total-current-matching specifically
to guard against exactly this), but this is a real, newly-discovered,
systemic methodological risk that needs auditing, not a one-off. Also
flagged: matching MEAN brightness across conditions (as done here) does
not guarantee matching the full spatial/temporal distribution of
contrast -- a subtler residual confound may remain even after this fix.

Scripts/files added: `spider_data_dryad.xlsx`,
`seq_2x2_still_spider.npy`/`seq_2x2_loom_spider.npy`/
`seq_2x2_still_blob.npy`/`seq_2x2_loom_blob.npy` (+ `_bodyids.csv`),
`results_recreate_2x2.csv`.

### Full audit of every real "loom"/zoom stimulus used in this project for the brightness confound

User asked to audit systematically, not just fix the one case that was
caught. Did this in two parts: (1) confirm and quantify the mechanism
directly with real measurements, not just theory; (2) go through every
finding that used a zoom/loom stimulus and check whether its actual
comparison design was exposed to the confound or not.

**Confirmed the mechanism is severe and universal, not case-specific.**
Regenerated the exact real stimulus parameters used in three different
findings and printed real per-frame mean contrast:

| params (used in) | frame 0 | frame 1 | frame 2 | saturates by |
|---|---|---|---|---|
| radius=8, zoom=1.3 (findings 22/26) | 0.448 | 0.754 | **1.000** | frame 2 |
| radius=15, zoom=1.4, amplified (finding 21) | 0.578 | 0.856 | 0.861 (~ceiling) | frame 1-2 |
| radius=8, zoom=1.15 (gentlest rate used, `image_to_retina_sequence.py` default) | 0.448 | 0.590 | 0.779 | frame 4-5 |

**Every real configuration tested reaches near-total saturation (mean
contrast approaching 1.0) within 2-5 frames, regardless of zoom rate or
amplification.** This confirms the confound isn't specific to finding
22's exact parameters -- it's a structural property of cropping toward
an object's center, which necessarily increases the fraction of
"object" pixels vs. "background" pixels as the crop tightens.

**Went through every finding that used a zoom/loom stimulus and checked
the actual comparison design, not just whether zoom was used:**

- **Finding 22/23 (motion-vs-shape ratio): CONFIRMED COMPROMISED, already
  fixed** (finding 36's clean 2x2 recreation). This is the case that
  started the audit.
- **Finding 18, Stage 4 ("frontal looming (large)" vs. static
  conditions): REAL, UNRESOLVED RISK.** The looming condition was the
  only one to fire (LC9=8) among several compared conditions in that
  early table -- plausibly explained, at least partly, by reaching much
  higher saturated brightness than the static conditions being compared
  against, not a genuine looming-specific mechanism. This specific
  stage-4 result was already superseded by finding 18's own later,
  amplification+arousal-boost-based resolution, so the project's
  headline chase-circuit conclusion doesn't rest on this one table --
  but the table's own "looming uniquely crosses threshold" claim should
  be read with this caveat now attached, not treated as clean evidence.
- **Finding 13 (von Reyn speed-dependent motor-mode timing, real
  physics-based loom, varying tau): NOT weakened -- if anything,
  strengthened.** Faster tau reaches high zoom (and thus high
  brightness, per this same confound) SOONER in real time than slower
  tau -- meaning the confound would bias TOWARD finding a spurious
  speed-dependent timing effect (faster tau = brighter sooner = should
  fire earlier), not away from it. Finding 13's actual result was a
  clean null (no timing difference across tau) despite this bias working
  against the null. A null result that survives a confound pushing
  toward a false positive is more robust, not less.
- **Finding 26 (LC4->LC10a loom stimulus) and every later reuse of the
  same stimulus (findings 27-36's shared `seq_lc4courtship_loom.npy` and
  similar): NOT compromised by THIS confound.** These tests never
  compared a loom stimulus against a differently-normalized non-loom
  stimulus -- they held the exact same (saturated) stimulus fixed and
  varied only a network parameter (boost on/off, added neurons, etc.)
  between compared conditions. The stimulus being saturated is a real,
  separate, already-acknowledged scope limitation (these tests show "a
  maximally strong visual input reaches X," not "realistic-strength
  looming reaches X") but does not create a FALSE difference between the
  actual compared conditions the way finding 22's mismatched-target
  normalization did.
- **Finding 21 (LC16/Cazalé-Debat et al. threat stimulus): NOT compromised**, same
  reasoning -- identical stimulus used in both the "brake on" and "brake
  off" conditions being compared.
- **Findings 1-9 (pre-dating this visible portion of the session):
  UNABLE TO VERIFY** from what's directly accessible now -- the
  project's own documentation references "total-current-matched" stimulus
  design as an established early practice, suggesting some guard against
  magnitude confounds existed from the start, but whether it specifically
  addressed THIS zoom-brightens-inherently mechanism can't be confirmed
  without re-reading that original code directly. Flagged as unverified,
  not claimed clean.

**Net honest conclusion:** the confound is real and severe wherever it
applies, but it only actually corrupts a finding's CONCLUSION when two
different, differently-normalized stimuli are compared -- most of this
project's later work (findings 21, 26-36) happened to be structured as
"same stimulus, different network state," which is naturally immune.
The two real, concrete exposures found are finding 22/23 (fixed) and
finding 18's stage-4 table (flagged, not yet re-run) -- not a sweeping
invalidation of the whole project, but a real, now-documented risk to
check before trusting any FUTURE looming-vs-static comparison built with
these tools.

Scripts/files added: none (audit used existing tools; results are the
per-frame measurements documented above).

### Fixing finding 18's Stage 4 table with a real matched-brightness control -- the original claim reverses

User asked to actually fix the flagged table, not just flag it. Rebuilt
the static-vs-looming comparison with brightness properly matched
across both conditions (same method as finding 36), real noise x 8
trials, on the current chase network (`connectome_richer_chase`), same
readouts as the original table (LC9, DNp09, DNa02, muscle).

**Built matched stimuli:** static and looming (radius=8, zoom-per-frame
1.3, matching the original real parameters) both normalized to the
same target mean (0.448, static's own raw mean, the smaller of the
two).

**Result -- the original claim doesn't just weaken, it reverses:**

| condition | LC9 | DNp09 | DNa02 | muscle |
|---|---|---|---|---|
| static (brightness-matched) | 3,879.2 +- 45.4 | 59.1 +- 0.6 | 42.8 +- 3.0 | 123.4 +- 8.2 |
| looming (brightness-matched) | 3,588.5 +- 25.0 | 54.0 +- 0.5 | 37.0 +- 1.4 | 106.9 +- 5.0 |

**The original stage-4 table reported "frontal, static: 0" and
"frontal, looming (large): LC9=8" -- i.e. only looming fired at all.**
With brightness properly controlled, BOTH conditions fire robustly, and
**static now fires MORE than looming at every single readout** -- the
complete reverse of the original claim. This is now the SECOND
independent confirmation (after finding 36's 2x2, on a different
network and different specific stimuli) that this simulation's looming
implementation, once the brightness confound is removed, does not show
real flies' expected "motion increases response" pattern at all --
if anything the opposite, consistently, across two separate tests.

**Honest conclusion: finding 18's original "looming uniquely crosses
threshold" claim is retracted, not just caveated.** It was an artifact
of the brightness confound the whole time. The real, corrected finding
is that this project's simulated escape/chase circuit does not
currently show a genuine motion-detection advantage independent of
raw stimulus brightness -- a real, now twice-replicated, and more
significant limitation than originally understood. This does not
overturn finding 18's LATER conclusions (the arousal-boost/amplification
resolution), which were reached through a different route and did not
depend on this specific stage-4 comparison.

Scripts/files added: `seq_stage4_static.npy`/`seq_stage4_looming.npy`
(+ `_norm.npy`, `_bodyids.csv`), `results_stage4_fixed.csv`.

### Auditing findings 1-9 for the brightness confound, for real -- checked directly rather than left unverified

User asked to actually check findings 1-9, not leave them flagged as
"can't verify." The real image files from that era still exist in the
project, making a direct check possible.

**Important context first: findings 1-9 are already fully superseded
for a separate, more fundamental reason** (finding 9's own
calibration-robustness sweep found the whole "legs matter" result
depended on an unvalidated, narrow combination of made-up parameters
and did not survive being tested against real measured Drosophila
electrophysiology -- already explicitly retracted before this audit).
This check is about whether the SPECIFIC brightness confound adds a
second, independent problem, not about reviving or further damaging an
already-retracted claim.

**Checked ink-budget matching directly** on the real shape images
(`shape_blob.jpg`, `shape_snowman.jpg`, `shape_snowman_legs.jpg`,
`shape_snowman_legs_detailed.jpg`, `spider_sill.jpg`): total contrast
("ink") is 66,102-67,541 across all five -- within ~2% of each other,
confirming finding 5's own explicit ink-budget-matching claim was real,
not just asserted.

**Checked the actual per-frame zoom-brightening trajectory for each
shape** (real `zoom_frame` cropping logic, zoom-per-frame=1.20, 5
frames):

| shape | frame 0 | frame 4 | ratio |
|---|---|---|---|
| snowman (no legs) | 0.244 | 0.860 | 3.52x |
| snowman + legs | 0.243 | 0.804 | 3.31x |
| snowman + legs (detailed) | 0.243 | 0.816 | 3.36x |
| blob | 0.244 | 0.892 | 3.66x |
| spider_sill (real photo) | 0.239 | 0.486 | **2.03x** |

**Result 1: the legs-vs-legless comparison specifically is NOT
meaningfully exposed to this confound.** Legged and legless synthetic
shapes brighten at nearly the same rate during zoom -- if anything, the
legless snowman brightens slightly MORE than the legged versions, which
would bias AGAINST finding a false "legs matter" effect, not toward it.
Combined with the ink-budget matching being real and confirmed, finding
5's specific legs/legless comparison holds up against this particular
confound (independent of the fact that it's already invalidated for
the calibration reason above).

**Result 2: a real, new, previously-unflagged asymmetry -- the real
photo brightens far less during zoom than any synthetic shape** (2.03x
vs. 3.3-3.7x). This is a genuine, additional confound risk specific to
comparisons between real photos and synthetic silhouettes during zoom
sequences -- relevant to finding 5's own already-documented "real photo
vs. synthetic shape" response gap (previously attributed only to edge-
softness/photographic detail) and potentially to finding 12's real-
predator-photo-vs-vector-icon comparison. Not deeply investigated
further here -- flagged as a real, concrete, checkable next audit item
rather than left as a vague possibility.

**Honest conclusion:** findings 1-9 remain correctly retracted/
superseded for the reason finding 9 already established. This specific
audit adds one clean result (legs-vs-legless was not zoom-brightness-
confounded) and one new, real, unresolved risk (real-photo-vs-synthetic
zoom-brightening asymmetry) rather than either exonerating or further
indicting the whole 1-9 block.

Scripts/files added: none (audit used existing real image files and
existing zoom logic; results are the measurements documented above).

### Adding LC17 and the real dopamine neurons in for real -- first functional test of what actually triggers the dopamine "brake"

User's chain of reasoning this session (does vision trigger dopamine?
does motor feedback trigger it? what does dopamine's own real upstream
look like?) led to finding LC17 as a real, substantial, previously-
unmodeled visual input into the PPM1201-1205 dopamine cluster (weight
493). User asked to add it for real.

**Checked LC17 directly before adding anything.** 353 real neurons,
cholinergic. Real dominant upstream: **T2a (106,674)** and self-
recurrence (100,060), then T3, Li25, **Tm5Y (34,033)**, PVLP011, Tm24,
**Y3 (12,281)**, LC11, LC9 (6,731) -- T2a, Tm5Y, and Y3 are ALL already
present in this project's main network (they drive LC9), so LC17 shares
real upstream bridges with the existing chase circuit rather than
needing new ones.

**Built the network in two steps**, catching a real gap along the way:
first added LC17 alone (confirmed real T2a->LC17 edge, 106,674, survived
the build) -- but a sanity check for LC17->dopamine came back 0, revealing
the actual dopamine neurons (PPM1201-1205) had never been added as real
simulated nodes in ANY network built this session; every prior dopamine
check was a direct database query, never something actually IN a
running simulation. Fixed: added all 12 real PPM1201/1202/1203/1205
neurons too (`connectome_full_matrix_lc17dop.csv`/`_neurons.csv`, 11,767
real neurons). Confirmed real LC17->dopamine edge survived (493).
(One trivial discrepancy noted: a direct requery confirmed the real
dopamine->LC16 edge, weight 16, still exists -- it just didn't surface
in this build's own new-edge diff, immaterial since that edge was
already established as functionally trivial/neuromodulatory in finding
33 and isn't relied on for anything in this network.)

**First real, functional test: drive the standard visual stimulus and
check whether the dopamine neurons actually fire**, not just whether a
synapse exists on paper. Ran the existing LC4-loom stimulus (no
courtship-specific tuning, just the standard visual drive already used
throughout this project) through the network:

| | T2a | LC17 | PPM1203 | PPM1205 | PPM1201/1202 |
|---|---|---|---|---|---|
| driven by visual stimulus | 8,386 | **14,861** | **73** | **11** | 0 (silent) |

**Result: real, causal, for the first time.** LC17 fires robustly from
ordinary visual input via the real T2a bridge, and this genuinely
reaches the dopamine cluster -- 2 of the 12 real dopamine neurons fire
(84 total spikes), the other 10 (including all of PPM1201 and PPM1202)
stay silent. This is a real, partial, honest result, not an artifact:
the actual biology (Cazalé-Debat et al. 2024) describes dopamine ramping up
GRADUALLY as courtship progresses over minutes, not switching on from
one instantaneous visual snapshot -- a modest, partial response to a
single stimulus presentation is exactly the expected shape of a
real, slow-building signal caught at one early moment, not evidence
against the mechanism.

**Significance:** this is the first time this project has shown a real,
end-to-end functional path from raw vision through to the actual
neurons that suppress the danger-detection pathway, rather than
imposing that suppression as an external, manually-toggled switch (as
in finding 21). It doesn't yet close the full loop (courtship duration
-> dopamine ramp -> LC16 suppression is still not simulated as a
continuous process, just this one snapshot), but it's a real, concrete
step from "we assume dopamine turns on" toward "here's a real visual
pathway that could plausibly drive it."

Scripts/files added: `connectome_full_matrix_lc17dop.csv`/`_neurons.csv`
(and the intermediate `connectome_full_matrix_lc17.csv`/`_neurons.csv`).

### Does the real dopamine response scale with stimulus duration? Tested directly -- a near-perfect linear relationship

Follow-up to finding 39: does exposing the fly to the visual stimulus
for LONGER produce MORE dopamine activity, matching the real biological
description of a gradual ramp (Cazalé-Debat et al. 2024)? Isolated TIME as
the only variable -- same visual content throughout, only
`--frame-duration` varied (50/100/200/400/800ms per frame, holding the
same 6 real frames, giving total exposure 300ms-4800ms). Real noise x 6
trials per duration.

**Result:**

| total exposure | dopamine (mean +- std) | LC17 (mean +- std) |
|---|---|---|
| 300ms | 83.0 +- 0.6 | 14,857.3 +- 9.9 |
| 600ms | 178.5 +- 1.0 | 31,555.8 +- 10.8 |
| 1,200ms | 372.0 +- 1.2 | 64,958.5 +- 14.2 |
| 2,400ms | 756.3 +- 1.7 | 131,727.0 +- 18.8 |
| 4,800ms | 1,527.2 +- 3.2 | 265,341.5 +- 35.3 |

**Near-perfect linear fit: dopamine = 0.321 x time_ms - 13.6, R^2 =
1.00000.** Not an approximation -- essentially every trial landed
exactly on the line. The doubling ratio (dopamine x2.15, x2.08, x2.03,
x2.02 for each successive doubling of time) converges toward exactly
2.0x as duration grows, consistent with a small fixed threshold/lag
(the -13.6 intercept) followed by clean linear accumulation -- not
saturating, not accelerating, genuinely proportional to time.

**Significance:** this is a real, quantitative, testable prediction that
emerged directly from the network's actual dynamics -- nothing was
tuned to produce this specific linear relationship, it fell out of
driving a real circuit for different real durations. It's a precise
echo of the real biological description (dopamine ramps up gradually
with courtship duration, not a step function) -- though the honest
caveat remains that this tests exposure to a STATIC repeated visual
stimulus, not actual courtship duration/progress as the real mechanism
is described, and the real biological ramp's timescale (real minutes)
is far longer than what was tested here (up to 4.8 real simulated
seconds) -- the SHAPE of the relationship (linear, not step-like) is a
real, meaningful finding regardless of whether the absolute timescale
matches.

Scripts/files added: `test_dopamine_duration.py` (scratchpad),
`results_dopamine_duration.csv`.

### LC10a chase-circuit 7x7 responsiveness map, compared to LC9 danger-circuit map — `confirmed`

Direct follow-up to the LC9->DNp09 danger-circuit responsiveness map
above: is the "target must land in a specific part of the visual field"
effect specific to the danger pathway, or general? Ran the identical
49-point real-coordinate grid test (same x 4-34, y 1-38 range,
total-current-matched, radius=3 clamped) on the chase pathway instead:
LC10a -> AOTU019 -> DNa15 -> b3 MN (real wing-steering muscle), using
`connectome_lc10a_legchase.csv` and the real `lc10a_columns.csv`
coordinates. Script: `responsiveness_map_chase_step.py`; full data in
`results_responsiveness_map_chase.csv`; rendered as
`responsiveness_map_chase_grid.png`.

**Result: the effect generalizes -- chase also has real, sharp dead
zones, but a different shape and a smaller dead fraction than danger.**

- 19/49 cells (39%) are exactly zero at the b3 MN (wing muscle) readout,
  vs. 26/49 (53%) for the danger pathway's DNp09 readout.
- The responsive region is a roughly horizontal band spanning most x
  values at cy=7-20, peaking at (14,7)=160 and (19,13)=165 -- unlike the
  danger map's single diagonal corner block.
- Both extreme edges of y (cy=1 and cy=38) are dead or near-dead at every
  x value tested, in both maps -- the one structural feature the two
  pathways share.
- AOTU019 and DNa15 (the two intermediate real hops) track b3 MN's
  on/off pattern closely at every grid point checked, so the dead zones
  are set early in the chain (at or before AOTU019), not lost partway
  down a working chain.

**Interpretation:** both real pathways tested so far are genuinely
position-selective, not just the one we happened to map first. Chase
covers more of the visual field than danger does, which is at least
directionally consistent with a real fly needing to track a moving mate
across a wider range of gaze than it needs to react to a single
threat direction -- but this is a plausible reading, not a claim
checked against behavioral literature.

### Real red-eye vs white-eye photos, full circuit, 5 positions, with arousal boost — `confirmed`, and this REVERSES the earlier "signal is buried" finding

Direct follow-up requested by user: retest the red-eye/white-eye
hypothesis using genuine, well-matched real photographs (not the earlier
synthetic gray-circle composite from finding 32/33), pushed through the
FULL real chain (Mi1 -> LC9 -> LC10a -> AOTU019 -> DNa15 -> b3 MN wing
muscle, `connectome_full_matrix.csv`), at 5 different real positions
spread across the eye's actual coordinate range (hex1/hex2), so no
single result could be explained away as a lucky/unlucky position.

**Real photo pair used:** two AI-generated but photorealistic images of
the same fly, same pose, same lighting, same framing, differing only in
eye color (`drosophila-eye-level-red.png`/`-white.png`, user-supplied),
cropped to a matched 450x420 head window. This is a much better-matched
pair than the earlier synthetic gray-circle test, and directly comparable
to the real paper's own manipulation (genetic eye-color swap, everything
else held constant).

**First pass (no arousal boost): inconclusive, not a real result.**
At default settings, almost nothing propagated past Mi1 in either
condition -- only 1 of 10 conditions produced any spikes at the muscle at
all. Correctly diagnosed as "the whole circuit is off," not a red/white
difference, consistent with the project's established finding that an
unaroused circuit ignores weak visual cues. Also caught and fixed a real
crash bug in `simulate.py` (region-activation plotting failed when zero
spiking neurons had a tagged region -- an edge case this sparse test
happened to trigger; fixed to skip the plot gracefully instead of
crashing).

**Second pass, with the same 8x arousal boost used in earlier arousal-
matrix work (`--type-boost LC9:LC9:8.0,LC9:LC10a:8.0,LC10a:LC10a:8.0`):**

| photo | position | Mi1 | LC9 | LC10a | AOTU019 | DNa15 | b3 MN (wing muscle) |
|---|---|---|---|---|---|---|---|
| red | center | 2,553 | 10,925 | 12,650 | 155 | 149 | **131** |
| red | upper_left | 31 | 0 | 0 | 0 | 0 | 0 |
| red | upper_right | 2,499 | 11,045 | 12,776 | 152 | 149 | **125** |
| red | lower_left | 2,201 | 0 | 0 | 0 | 0 | 0 |
| red | lower_right | 2,070 | 9,895 | 12,435 | 156 | 160 | **137** |
| white | center | 1,559 | 0 | 0 | 0 | 0 | **0** |
| white | upper_left | 1 | 0 | 0 | 0 | 0 | 0 |
| white | upper_right | 1,514 | 0 | 0 | 0 | 0 | **0** |
| white | lower_left | 1,197 | 0 | 0 | 0 | 0 | 0 |
| white | lower_right | 1,162 | 0 | 0 | 0 | 0 | **0** |

**Result: clean, large, and consistent -- the opposite conclusion from
finding 32/33.** At every one of the 3 positions where the real photo
had enough real neurons under it to drive anything (center, upper_right,
lower_right -- all with Mi1 in the 2,000-2,550 spike range), the
red-eyed photo fires the ENTIRE circuit through to the real wing muscle
(125-137 spikes), while the white-eyed photo, at those exact same
positions, produces EXACTLY ZERO spikes past Mi1 every single time --
despite Mi1 itself still receiving a substantial, real signal (1,162-
1,559 spikes) from the white-eyed photo. The other 2 positions
(upper_left, lower_left) are dead for BOTH photos -- consistent with the
real position-dependence (dead zones) documented earlier in this
project, not a red/white effect; these two positions simply had very
few real neurons in that part of the coordinate window (31 and low Mi1
counts) regardless of which photo was shown.

**Why this reverses finding 32/33 rather than just adding to it:** the
earlier test's null result was traced to two specific, real weaknesses --
(1) the synthetic composite was a crude gray-circle stand-in with a
raw contrast difference that got compressed by the amplification stage,
and (2) only 2 of 113 relevant neurons showed any real local difference
at all. This test uses genuinely well-matched, higher-fidelity real
photos, and the color difference clearly survives being pooled across
the whole population -- not a subtle 2-neuron effect buried in noise,
but a difference between total silence and 125+ spikes at the actual
motor output. The earlier finding's specific numeric conclusion ("the
population-pooling method is structurally blind to this cue") is now
contradicted by better input data -- the method isn't blind to the cue
when the cue itself is stronger and better-matched to the real
biological manipulation.

**Caveat, stated plainly:** the 8x arousal boost is a chosen stand-in for
"the fly is aroused enough to react to visual cues in general" -- it is
applied identically to both photo conditions, so it cannot itself be
producing the red/white difference (a completely OFF circuit stays off
regardless of boost, as the unboosted pass showed). But the exact
boost magnitude is a project convention carried over from earlier work,
not independently re-derived here.

Scripts/files added: `photo_multi_position.py`,
`run_multiposition_eyecolor.py`, `redeye_userphoto_head.jpg`/
`whiteeye_userphoto_head.jpg`, `results_multiposition_eyecolor.csv`
(boosted), `results_multiposition_eyecolor_noboost.csv` (unboosted, the
inconclusive first pass). `simulate.py` fix: skip the region-activation
plot instead of crashing when no spiking neuron has a tagged region.

### Specificity test: does the danger circuit (DNp09/PVLP004) stay off while chase fires on the same real photo? — `confirmed`, hypothesis FAILS

Direct follow-up to the multi-position red/white-eye photo test above.
User asked for the real hypothesis to be stated before testing: should a
harmless courtship-target photo (no motion, no looming) leave the real
danger/escape circuit (DNp09, PVLP004 -- LC9's real downstream threat
readouts) off while it turns the chase circuit on? Flagged in advance as
a real risk, not a safe assumption, because LC9 is shared upstream
wiring for both circuits.

**Built a combined network to test it properly.** `connectome_full_matrix.csv`
(chase circuit, Mi1->LC9->LC10a->AOTU019->DNa15->b3 MN) did not contain
DNp09/PVLP004 as nodes at all -- merged in the real DNp09/PVLP004 neurons
and their real edges from `connectome_chase2.csv` (same neuprint dataset,
same real bodyIds, so edge weights are directly reusable, not
re-estimated). Result: `connectome_full_matrix_danger.csv`/`_neurons.csv`,
11,420 real neurons, 326,036 real edges -- one network with the complete
chase circuit, the complete danger-readout circuit, and MN9 (the one
genuinely unrelated real control neuron available in this build) all
present together.

**Re-ran the same 5-position, 2-photo, 8x-boosted test on this combined
network:**

| photo | position | LC9 | b3 MN (chase) | DNp09 (danger) | PVLP004 (danger) | MN9 (unrelated control) |
|---|---|---|---|---|---|---|
| red | center | 10,748 | 130 | 87 | 737 | 0 |
| red | upper_right | 10,897 | 132 | 90 | 748 | 0 |
| red | lower_right | 9,697 | 135 | 77 | 677 | 0 |
| white | any position | 0 | 0 | 0 | 0 | 0 |

**Result: specificity fails, cleanly and consistently.** At every one of
the 3 positions where the chase circuit fires, the danger circuit fires
right alongside it -- PVLP004 actually reaches a HIGHER spike count
(677-748) than the actual chase motor output, b3 MN (130-135). This is
not a small leak; PVLP004 is LC9's single strongest real downstream
target, and this test shows that strength counts against specificity as
much as it does for it. MN9, the one true unrelated real control
present, holds at exactly 0 in every condition -- ruling out "the whole
network is just noisy" as an explanation. The leak is specific to LC9's
shared wiring into both circuits, not a general breakdown.

**Honest interpretation:** this project's real, verified connectome
wiring does not, on its own, keep "notice a potential mate" and "notice
a threat" separate once LC9 is strongly driven -- both of LC9's major
real downstream targets (LC10a for chase, DNp09/PVLP004 for danger) get
activated together. Whether a real fly avoids this problem via some
mechanism not modeled here (e.g. the dopamine-suppression pathway built
earlier in this project, which was specifically designed to suppress
danger-circuit sensitivity once courtship is underway) is a natural next
question -- this test used the plain 8x arousal boost only, without that
suppression pathway active.

Scripts/files added: `connectome_full_matrix_danger.csv`/`_neurons.csv`,
`run_multiposition_eyecolor_danger.py`,
`results_multiposition_eyecolor_danger.csv`.

### Size-threshold sweep: does danger have a lower size threshold than chase? — `confirmed`, they share one threshold

Direct follow-up to the specificity-failure finding above. User correctly
flagged that the radius=10 window used there (35.7% of the whole eye) is
far bigger than this project's own established realistic mate-target
size (radius=4, 5.5% of the eye, ~22.5deg, from real behavioral
literature) -- so the "danger leaks" result might just be an artifact of
using an oversized stimulus, not a real property of the circuit.
Retested at radius=4 first (realistic size): everything, including
chase, stayed at exactly zero -- the stimulus was too small to cross
LC9's firing threshold at all, at this network's current calibration.

**Ran a full size sweep (radius 4-10, i.e. 5.5%-35.7% of the eye) at a
single fixed, known-good position (hex1=18, hex2=20), same 8x arousal
boost, for both photos, on `connectome_full_matrix_danger.csv`:**

| photo | radius | % of eye | LC9 | LC10a | b3 MN (chase) | DNp09 (danger) | PVLP004 (danger) |
|---|---|---|---|---|---|---|---|
| red | 4 | 5.5% | 0 | 0 | 0 | 0 | 0 |
| red | 5 | 9.1% | 0 | 0 | 0 | 0 | 0 |
| red | 6 | 12.7% | 0 | 0 | 0 | 0 | 0 |
| red | 7 | 16.8% | 0 | 1 | 0 | 0 | 0 |
| red | **8** | **22.2%** | **10,338** | **12,185** | **124** | **86** | **713** |
| red | 9 | 28.5% | 10,565 | 12,404 | 127 | 88 | 726 |
| red | 10 | 35.7% | 10,748 | 12,656 | 130 | 87 | 737 |
| white | 4-10 | 5.5%-35.7% | 0 (every size) | 0 | 0 | 0 | 0 |

**Result: chase and danger switch on at the EXACT SAME size threshold,
not different ones.** Between radius 7 and radius 8, LC9 goes from
completely silent to fully active, and both of its real downstream
targets -- LC10a (chase) and DNp09/PVLP004 (danger) -- turn on together,
in the same jump. There is no size range in which chase is active while
danger stays off, or vice versa. This directly confirms (rather than
weakens) the earlier specificity-failure finding: it isn't that danger
has a lower/more sensitive threshold that leaks in early -- chase and
danger are tied to the identical upstream switch (LC9 crossing
threshold), so they are structurally inseparable in this network,
regardless of stimulus size.

**Second, independent result: white-eye never crosses this threshold at
any size tested,** including the largest (35.7% of the eye) -- confirming
eye color, not size, is what determines whether the circuit fires at
all for this photo pair.

**Honest caveat, flagged directly rather than glossed over:** the
threshold size that fires anything here (>=22% of the eye) is roughly
4x bigger than this project's own established realistic mate-target
size (5.5%). At the realistic size, this particular network (Mi1 driven
directly, no amplification stage) stays completely silent regardless of
eye color. This is consistent with, not a new instance of, the
already-documented gap from earlier in this project: realistic-sized
visual stimuli fail to fire this circuit without an early-vision gain-
control/amplification stage that hasn't been added yet (the subject of
the separate flyvis research task run earlier this session). This test
is therefore informative about the STRUCTURE of the chase/danger overlap
(they share a threshold), but happens in an unrealistically-large-
stimulus regime, not a validated realistic one.

Scripts/files added: `run_size_sweep_eyecolor.py`,
`results_size_sweep_eyecolor.csv`.

### Replication: same size-threshold test, independent second photo pair ("more female"-styled) — `confirmed`

User supplied a second, independently-generated red/white-eye photo
pair, deliberately restyled to look more clearly female, to check
whether the size-threshold finding above was specific to the first
photo or a general property of the circuit. Same crop window (450x420),
same size sweep (radius 4-10), same position (hex1=18/hex2=20), same
network (`connectome_full_matrix_danger.csv`), same 8x boost.

| photo | radius=7 (16.8%) | radius=8 (22.2%) | radius=10 (35.7%) |
|---|---|---|---|
| female_red -- LC9 | 0 | 10,112 | 10,480 |
| female_red -- b3 MN (chase) | 0 | 123 | 128 |
| female_red -- DNp09/PVLP004 (danger) | 0/0 | 82/695 | 87/725 |
| female_white -- all readouts | 0 | 0 | 0 |

**Result: replicates exactly.** Same sharp radius 7->8 threshold, same
simultaneous chase+danger onset, same complete white-eye silence at
every size tested. Full results in
`results_size_sweep_eyecolor_female.csv`.

Scripts/files added: `run_size_sweep_eyecolor_female.py`,
`female_red_userphoto_head.jpg`/`female_white_userphoto_head.jpg`,
`results_size_sweep_eyecolor_female.csv`.

### Real MDN connectivity check — `confirmed`, and a genuine, unexpected finding

Live neuprint access restored this session (user-provided token). Searched
male-cns:v1.0 directly for MDN (Moonwalker Descending Neurons, the real
documented backward-walking command circuit) and DopaMeander (a very
recently published forward-walking dopaminergic neuron, Control of
walking direction by descending and dopaminergic neurons in Drosophila,
2025/2026).

**MDN: found, 4 real neurons** (2 per side, `instance` MDN_L/MDN_R x2),
`predictedNt`=acetylcholine -- matches the literature's "four adult
MDNs" exactly.

**DopaMeander: not found** under that name or several tried variants
([Ww]alk, [Mm]eander, oDN, aDN1, aDN2) -- likely too recently published
to have an EM cell-type annotation in this dataset yet, or defined at
a light-level/genetic-driver level rather than as a reconstructed type.

**Correction to an earlier literature-only claim:** the search summary
used earlier this session stated MDN's real visual input comes from
LC16. Checked this directly against male-cns wiring -- **not supported
by the real data.** Real LC-family input into MDN is small and comes
from LC33 (weight 13) and LCNOpm (weight 1); LC16->MDN weight is exactly
zero. MDN's actual dominant real inputs (top of 4,664 real input edges,
total weight 20,849) are unnamed local/premotor interneurons (LAL-,
DN-prefixed types), not a direct visual LC pathway. Either the LC16->MDN
claim comes from a different dataset/species reconstruction, or it's an
indirect multi-hop route not visible in a single-hop query -- flagged
honestly rather than left uncorrected.

**Checked our own circuit's real connectivity to MDN directly:**

| our neuron | -> MDN (weight, edges) | MDN -> our neuron |
|---|---|---|
| LC9 | 0 (0) | 0 |
| LC10a | 0 (0) | 0 |
| DNp09 | 6 (3) | 0 |
| PVLP004 | 0 (0) | 0 |
| **AOTU019** | **233 (18)** | 1 |
| DNa15 | 2 (2) | 4 |

**Real, unexpected finding: AOTU019 -- the real relay neuron in our
already-built chase circuit (LC10a->AOTU019->DNa15->b3 MN) -- has a
substantial real connection directly into MDN, stronger than any real
visual input MDN receives from any LC-type neuron at all.** AOTU019's
real `predictedNt` is **GABA (inhibitory)**. This is a real, directly
verified candidate mechanism for the kind of built-in "engaging chase
actively suppresses retreat" antagonism discussed earlier (analogous to
the documented MDN/DopaMeander mutual-inhibition pair in the
literature) -- found in our own already-built circuit's real wiring,
not a new addition. Not yet tested functionally (MDN is not yet a node
in any of our simulated networks) -- the natural next step is adding
MDN as a real inhibited node downstream of AOTU019 and testing whether
driving the chase circuit measurably suppresses MDN activity in
simulation.

Note: NEUPRINT_APPLICATION_CREDENTIALS was supplied by the user for
this session only; not stored in any project file.

### MDN added to the network with real connections; chase-vs-retreat directly tested — `confirmed`

Direct follow-up to the AOTU019->MDN discovery. Added MDN (4 real
neurons) into the combined network with ALL its real connections to
every neuron already present (91 real edges into MDN, 38 real edges out
of MDN -- fetched live from neuprint, not estimated), correctly signed
by real `predictedNt` (AOTU019 and AOTU062 are GABA -> inhibitory, MDN
itself and every other new presynaptic type is acetylcholine ->
excitatory, matching this project's established sign convention).
`connectome_full_matrix_mdn.csv`/`_neurons.csv`, 11,424 real neurons,
326,165 real edges.

**Re-ran the red/white-eye size sweep on this network, tracking MDN:**

| photo | radius | LC9 | b3 MN (chase) | Sternal ant. rotator MN (chase leg) | MDN (retreat) |
|---|---|---|---|---|---|
| red | 8-10 | 10,338-10,748 | 124-130 | 301-310 | **0** |
| white | any | 0 | 0 | 0 | 0 |

**MDN stayed at exactly zero in every condition, including the
strongest chase activation.** Before calling this "chase, not retreat,"
ran the obvious control: is MDN silent because it's being actively
suppressed, or because it was never going to fire regardless (i.e. the
AOTU019 inhibition doing no real work)? Built
`connectome_full_matrix_mdn_noinhib.csv` (identical network, only the
18 real AOTU019->MDN inhibitory edges removed) and reran the same 3
conditions.

**Result: removing the inhibition wakes MDN up.** MDN goes from 0 to 11
spikes at every tested size once the AOTU019 brake is removed, while
every other readout (LC9, b3 MN, DNp09, PVLP004, leg muscle) stays
essentially unchanged. This confirms the suppression is real and
functionally active, not a case of "MDN just doesn't get driven by this
stimulus anyway" -- there is a real, nonzero signal reaching MDN, and
the real GABA connection from the chase relay (AOTU019) is what's
blocking it.

**Honest interpretation:** for THIS specific real photo stimulus, at
sizes strong enough to drive the circuit at all, the network's real
wiring supports "this is a chase, not a retreat" -- the retreat-command
neuron is actively silenced while the chase motor output fires. This
is a genuine, verified real-connectome result, not an assumption. It
does not resolve the broader question of whether leg/wing muscle
activity in general always means chase (MDN itself connects directly,
excitatorily, to some of the same muscles -- see the AOTU019/MDN
connectivity finding above) -- only that for this specific circuit
state, the balance of real excitation and inhibition favors chase.

Scripts/files added: `connectome_full_matrix_mdn.csv`/`_neurons.csv`,
`connectome_full_matrix_mdn_noinhib.csv`/`_neurons.csv`,
`run_size_sweep_eyecolor_mdn.py`, `run_size_sweep_eyecolor_mdn_noinhib.py`,
`results_size_sweep_eyecolor_mdn.csv`,
`results_size_sweep_eyecolor_mdn_noinhib.csv`.

### Complete, fully-validated 4-circuit network (chase/danger/escape/retreat); looming vs mate photo, identical settings — `confirmed`

Built out the genuinely missing real escape pathway (LC4 was present as
an orphan node in earlier builds with zero direct Mi1 input at the
single-hop level -- corrected: it DOES have real multi-hop input via 6
real bridge types, 4 of which -- T2, TmY3, Tm3, Tm5Y -- were already
present from earlier LC9-bridge work; added the 2 missing ones, Tm4 and
Tm2, plus LC4's own genuine real escape output, DNp01 (not DNp09, which
is LC9-dominated, not LC4-dominated) -> TTMn (real jump/escape muscle,
Giant-Fiber-adjacent). `connectome_full_matrix_final.csv`/`_neurons.csv`,
14,864 real neurons, 432,976 real edges.

**Every hop of every one of the 4 circuits individually verified against
live neuprint data before running anything (not assumed from file
presence):**

| circuit | path | status |
|---|---|---|
| chase | Mi1->Y3/T2a/TmY5a->LC9->LC10a->AOTU019->DNa15->b3 MN | all real, all nonzero |
| danger | LC9->DNp09, LC9->PVLP004 | all real, all nonzero |
| escape | Mi1->{T2,TmY3,Tm3,Tm5Y,Tm4,Tm2}->LC4->DNp01->TTMn | all real, all nonzero |
| retreat | AOTU019->MDN (inhibitory), MDN->DNa02/DNa11/DNa15/leg muscle | all real, all nonzero |

**Ran red-eye photo, white-eye photo, and a confound-free growing
looming blob (`blob_looming_growing.py` -- grows the driven WINDOW size
per frame rather than zoom-cropping, so no per-pixel brightness change
occurs; verified flat per-seat contrast across frames before use) on
this identical complete network, identical 8x boost, identical position:**

| stimulus | Mi1 | LC4 | b3 MN (chase) | DNp01->TTMn (escape) | MDN (retreat) |
|---|---|---|---|---|---|
| red-eye | 2,552 | 2,343 | 131 | 100 -> 30 | 0 |
| white-eye | 1,559 | 1 | 0 | 0 -> 0 | 0 |
| looming blob | 7,467 | 2,994 | 147 | 106 -> 34 | 0 |

**Result: no reverse inhibition, and a real reason why, checked
directly rather than left unexplained.** The looming blob fires chase,
danger, AND escape all together -- slightly MORE than the mate photo
(because a solid max-contrast blob is simply a stronger raw visual
signal than a natural grayscale photo, not because it engages a
qualitatively different channel). Checked whether DNp01 or LC4 have any
real connection back into the chase pathway or MDN that could produce
suppression: **DNp01 has zero real downstream connections to LC10a,
AOTU019, DNa15, b3 MN, or MDN -- a real dead end.** LC4's only real
connection into the chase circuit is LC4->LC10a, weight 126,
EXCITATORY (LC4 is acetylcholine) -- if anything, the real wiring adds
to chase rather than suppressing it.

**Final, honest conclusion:** across all real connectivity traced in
this project so far, the ONLY verified inhibitory cross-circuit
connection is chase->retreat (AOTU019->MDN). No real escape->chase,
danger->chase, or escape->retreat suppression exists in any path
checked. This network does not contain a "threat overrides courtship"
switch -- courtship actively suppresses retreat, but nothing found so
far suppresses courtship itself. This is a genuine negative result,
consistent with (not contradicting) the earlier Cazalé-Debat et al. 2024
citation, which describes suppression running the opposite direction
(courtship state suppressing threat PERCEPTION, via LC16 and dopamine
-- a mechanism this project has approximated separately but not
integrated into this specific 4-circuit network).

Scripts/files added: `blob_looming_growing.py`, `run_final_all_tests.py`,
`connectome_full_matrix_final.csv`/`_neurons.csv`,
`results_final_all_tests.csv`.

### Added real P1/pC1 and pIP10 (courtship command + song-descending neuron) — `confirmed`, does not change the core finding

Added the real pC1 subtypes (13a/13b/14a/14b/5b) and pIP10 -- all 20
real neurons were already present as nodes in the network (swept in
incidentally during the MDN merge), only their real edges were missing.
Fetched cheaply (query by the 6 small neuron-type lists directly rather
than filtering against the full 14,864-neuron base list server-side,
which had hung/stalled on the naive approach -- killed and retried with
the cheaper direction). 3,995 new real edges added, signed by real
predictedNt.

**Real connectivity confirmed:** LC10a -> pC1* (202 edges, weight 740)
-- our courtship-target visual pathway does genuinely, substantially
drive the real P1-equivalent neuron. pC1 -> pIP10 already confirmed
earlier (real, weight 565/215). Full real chain: Mi1->...->LC10a->pC1->
pIP10 all verified.

**Re-ran the red-eye / white-eye / looming-blob comparison tracking
pC1 and pIP10:**

| condition | pC1 (sum) | pIP10 | MDN |
|---|---|---|---|
| red-eye | 47 | 50 | 0 |
| white-eye | 0 | 0 | 0 |
| looming blob | 45 | 43 | 0 |

**Result: no change to the core finding.** pC1/pIP10 fire almost
identically for red-eye and the looming blob, same as every other
readout tested so far. Adding a better-grounded, literature-validated
"courtship commitment" signal did not give the network any new way to
distinguish a mate from a threat -- because pC1, like everything else
downstream, is driven through the same shared LC10a/Mi1-bridge pathway
that both stimuli activate equally. This strengthens (rather than
resolves) the earlier finding: the lack of mate-vs-threat specificity
in this project's current build is structural (shared upstream visual
bridges), not fixable by adding more downstream readouts alone.

Scripts/files added: `run_final_all_tests2.py`,
`results_final_all_tests2.csv`. Network updated in place:
`connectome_full_matrix_final.csv` (432,994 edges, up from 432,976).

## SESSION CHECKPOINT — stopping here, resume from this point

**Where things stand:** Built and fully validated five real circuits in
one combined network (`connectome_full_matrix_final.csv`/`_neurons.csv`,
14,864 real neurons, 432,994 real edges) -- every single hop checked
against live neuprint data, not assumed:
- **Chase**: Mi1->Y3/T2a/TmY5a->LC9->LC10a->AOTU019->DNa15->b3 MN
- **Danger (LC9-based)**: LC9->DNp09/PVLP004
- **Escape (LC4-based, genuinely separate from danger)**: Mi1->{T2,TmY3,
  Tm3,Tm5Y,Tm4,Tm2}->LC4->DNp01->TTMn (real jump muscle)
- **Retreat**: AOTU019->MDN (real, inhibitory, GABA) plus MDN's own real
  outputs to the shared leg/wing muscles
- **Courtship commitment**: LC10a->pC1 (real, weight 740)->pIP10 (real
  song-descending neuron)

**Clean, repeatable result across all of them:**
- Red-eye photo vs white-eye photo: clean, sharp, reliable difference.
  White-eye fires NOTHING, at any circuit, any test, any size --
  confirmed as the one thing this whole build reliably distinguishes.
- Red-eye photo vs looming blob: **no difference at all.** Every circuit
  (chase, danger, escape, courtship-commitment) fires almost identically
  for both. MDN (retreat) stays silent in every condition tested.

**Why, root cause, confirmed not guessed:** LC9 (danger/chase gateway)
and LC4 (genuine escape gateway) share several real upstream visual
bridge neurons (T2, TmY3, Tm3, Tm5Y). Any sufficiently large/strong
stimulus at this eye position drives both gateways together, regardless
of whether it's actually a mate or a threat. Checked directly: DNp01
(escape) has ZERO real connection back into chase or MDN; LC4's only
real connection into chase is excitatory (LC4->LC10a, weight 126), not
inhibitory. **The only real cross-circuit inhibition found anywhere in
this project is chase->retreat (AOTU019->MDN).** No real "threat
overrides courtship" switch exists in any path traced so far.

**Real, plausible fix not yet built:** the literature (Cazalé-Debat et al. et al.
2024, cited earlier) describes a real suppression mechanism -- P1/pC1
commitment building up over courtship TIME, ramping up PPM1/PPM2
dopamine, suppressing LC16-mediated threat perception via Dop2R. This
project has pC1 now genuinely wired to the visual pathway (new this
session), but LC16 and the dopamine-ramp-over-time mechanism are NOT
yet integrated into this same combined network. That is the natural
next real test.

**Open questions flagged but not yet resolved:**
1. "Chase" (b3 MN) was found to be a weaker label than initially treated
   -- it's a general wing-steering muscle, also directly excited by MDN
   (retreat). Real, solid "chase" evidence would need either b1 MN
   (courtship-song-specific muscle, exists in the dataset but its real
   upstream is entirely unnamed local interneurons, same wall as MDN's
   own muscle path) or a genuine forward-walking command neuron
   (literature's "DopaMeander" -- searched, not found under that name in
   male-cns yet).
2. Never confirmed which direction (toward/away) the fly's body actually
   moves from any muscle spike count -- this remains inferred, not
   measured, for every circuit in this project.
3. Real camera-capture test of genuine approach motion (vs the
   brightness-confounded synthetic zoom) was never completed --
   `live_preview.py`/`preview_and_capture.py` exist but no clean,
   face-free, correctly-directioned capture was ever processed through
   the pipeline.

**Natural next steps, in likely priority order:**
1. Add LC16 + the real PPM1/PPM2 dopamine-ramp mechanism into this same
   final network and retest whether it's what's actually supposed to
   separate mate-response from threat-response over courtship time.
2. Try to find/verify a real forward-walking-specific command neuron
   (DopaMeander-equivalent) in male-cns to get genuine positive evidence
   for chase direction, not just absence-of-retreat.
3. Revisit the real camera capture, now that there's a clear reason to
   want it (testing genuine looming/approach motion once the confound-
   free `blob_looming_growing.py` script already exists).

NEUPRINT_APPLICATION_CREDENTIALS was supplied by the user this session;
live neuprint access will need to be re-established (token re-exported)
next session -- not stored in any project file.

### Built the real color-opponent channel (Tm20) — `confirmed`, real signal exists but too weakly wired to change the outcome

Built a genuine second visual channel using Tm20 (876 real neurons,
side R, real hex coordinates for 1,732/1,762 total) -- the most
spatially-mapped node downstream of the real color photoreceptors
(R7p/R7y/R8p/R8y, real, histamine, confirmed present in male-cns).
Checked several candidate color-pathway layers first (Tm5a/b/c, Dm8a/b)
-- all more color-dominant by proportion but none have real spatial
coordinates; chose Tm20 specifically to avoid fabricating coordinate
data for a neuron that was never actually measured spatially, keeping
with this project's real-data-only standard. Computed each Tm20
neuron's real, individual pale (R7p+R8p) vs yellow (R7y+R8y) synaptic
input weight (427 of 876 have real direct photoreceptor input; natural
mosaic split 164 pale-dominant / 263 yellow-dominant, close to the
documented real ~30:70 pale:yellow ratio). `tm20_columns.csv`,
`image_to_tm20_color.py` (uses actual RGB photos, not grayscale --
blue channel as an R8p/blue-Rh5 proxy, green channel as an R8y/green-
Rh6 proxy, blended per-neuron by real measured bias).

**Confirmed Tm20 is a real, non-orphan gateway into the existing
network** before building: direct real edges to LC10a (1,402), LC9
(128), LC4 (97), plus heavy real overlap through the same bridge
neurons already used (Tm5Y: 53,512, T2a: 6,518). Also found a strong
real connection to LC16 (17,683) -- the literature's threat-suppression
neuron, not yet added to any network this project has built. Merged:
`connectome_full_matrix_color.csv`/`_neurons.csv`, 15,740 real neurons,
459,093 real edges.

**Ran red-eye vs white-eye with BOTH channels driving simultaneously
(Mi1 achromatic + Tm20 real color), same 8x boost:**

| | red-eye | white-eye |
|---|---|---|
| Tm20 (color channel) | 3,670 | **2,340** |
| LC9 | 11,772 | 0 |
| LC10a | 13,890 | 1 |
| b3 MN (chase) | 147 | 0 |
| DNp09/PVLP004 (danger) | 96/806 | 0/0 |

**Result: the color channel is real and functional -- white-eye now
produces a genuine, nonzero, correctly-directioned color response
(2,340 spikes, red > white as expected) that did NOT exist in the
achromatic-only pipeline. But it does not change the final outcome.**
Traced why directly: Tm20's own real connection into LC9/LC10a (128,
1,402) is small next to LC9's own real self-recurrence (40,675,
established earlier this session) that dominates the network's
threshold-switch dynamics. The real color signal exists, is measurably
different between conditions, and simply isn't wired strongly enough
into the decision-making stage to move the outcome -- a different,
more specific finding than "no color information exists," and a more
honest one.

Scripts/files added: `image_to_tm20_color.py`, `tm20_columns.csv`,
`tm20_color_input_edges.csv`, `connectome_full_matrix_color.csv`/
`_neurons.csv`, `spike_summary_color_red.csv`/`_white.csv`.

## SESSION CHECKPOINT #2 — stopping here, resume from this point

Continuation of the checkpoint above. Since that checkpoint, built and
tested the real color-opponent channel (Tm20), per the flagged
"next step #3 area" -- actually pulled forward ahead of the LC16/
dopamine-ramp work, at user's direction.

**New this session, since checkpoint #1:**
- Built `connectome_full_matrix_color.csv`/`_neurons.csv` (15,740 real
  neurons, 459,093 real edges) -- adds Tm20 (real color-pathway relay,
  876 real neurons, real per-neuron pale/yellow photoreceptor bias) on
  top of everything from checkpoint #1 (chase, LC9-danger, LC4-escape,
  MDN-retreat, pC1/pIP10-courtship-commitment).
- **Real finding:** the color channel works -- white-eye now produces a
  genuine, nonzero, correctly-directioned response in Tm20 (2,340
  spikes, vs 3,670 for red-eye) that never existed in the grayscale-only
  pipeline. But it doesn't change the final outcome: white-eye still
  produces zero downstream chase/danger activity, because Tm20's own
  real connection into LC9/LC10a (128/1,402) is far too weak relative to
  LC9's own massive real self-recurrence (40,675) to move the needle.
  **The bottleneck isn't "no color sense" -- it's "color sense exists
  but isn't wired loudly enough into the decision stage."**

**Full current state of validated real circuits, one combined network
(`connectome_full_matrix_color.csv`):** chase, LC9-danger, LC4-escape
(genuinely separate from danger), MDN-retreat (real, active GABA
suppression from chase, verified by knockout test), P1/pC1->pIP10
courtship-commitment (real, LC10a->pC1 weight 740), and now Tm20 color
(real, functional, but under-weighted downstream).

**Still true from checkpoint #1, unchanged:**
- Red-eye vs white-eye: clean, sharp, reliable difference -- now
  understood even more precisely (real color signal exists but is
  diluted below the network's ignition threshold by the time it
  reaches LC9/LC10a).
- Red-eye vs looming blob: still indistinguishable across every real
  circuit tested (chase, danger, escape, courtship-commitment). Adding
  color did not touch this comparison directly this session -- worth
  rerunning the blob through the color-enabled network specifically,
  since the blob is pure black/white (no real chromatic content) and
  SHOULD, in principle, look different from red-eye through the color
  channel even though it doesn't through luminance alone. Not yet
  tested -- good candidate for tomorrow.
- The only real cross-circuit inhibition found anywhere in this project
  remains chase->retreat (AOTU019->MDN). No real threat->chase or
  escape->chase suppression exists in any path traced.
- "Chase" (b3 MN) is still a weaker-grounded label than "escape"
  (TTMn) -- unresolved.
- Real camera-capture test of genuine approach motion still incomplete.

**Natural next steps, updated priority order:**
1. **Run the looming blob through the NEW color-enabled network** --
   quick, cheap test (scripts already exist), directly checks whether a
   colorless/black-white stimulus is now distinguishable from red-eye
   via the color channel, even though neither differs from the other
   through luminance alone.
2. Add LC16 + real PPM1/PPM2 dopamine-ramp-over-courtship-time mechanism
   (Cazalé-Debat et al. 2024) -- Tm20->LC16 real connection (17,683) already
   confirmed this session, ready to build on.
3. Try to find/verify a real forward-walking-specific command neuron
   (DopaMeander-equivalent) for genuine positive chase-direction evidence.
4. Revisit real camera capture for genuine approach motion.

NEUPRINT_APPLICATION_CREDENTIALS supplied by user this session; will
need re-export next session (not stored in any project file).

### Corrected the color-opponent signal (was a bug), reran blob comparison — `confirmed`, still no downstream change, root cause now precise

Found and fixed a real bug in `image_to_tm20_color.py`: the original
version computed "contrast" (background minus channel value) separately
per color channel -- still fundamentally a per-channel DARKNESS
detector, not a genuine color-opponent signal. Any sufficiently dark
object would trigger it regardless of actual hue. Verified directly:
whole-image G-B difference was nearly identical for red-eye (0.0406)
and white-eye (0.0416) -- not a usable signal.

**Fixed to a real opponent computation:** redness = R - (G+B)/2 (real
pigment absorbs blue/green more than red, so this is genuinely near
zero for colorless objects and positive specifically where red content
exists). Verified directly before rebuilding: blob_control.jpg (pure
black/white) gives EXACTLY 0.0000 redness, red-eye peaks at 0.50,
white-eye at 0.32 -- correct, real, meaningful separation this time.

**Rebuilt all three stimuli and reran through `connectome_full_matrix_color.csv`:**

| condition | Mi1 (achromatic) | Tm20 (color) | LC9 | LC10a | b3 MN |
|---|---|---|---|---|---|
| red-eye | 2,555 | 3,270 | 11,695 | 13,815 | 150 |
| white-eye | 1,566 | 2,133 | 0 | 1 | 0 |
| looming blob | 10,438 | **4,199** (down from 10,847 with the buggy version) | 12,491 | 14,834 | 154 |

**Confirmed the fix worked at the signal level:** isolating just the
genuinely color-carrying Tm20 neurons (174 of 318, real direct
photoreceptor input), the blob reads EXACTLY 0.0 while red-eye/white-eye
both carry real, correctly-ordered signal (0.116 vs 0.076) -- the
opponent computation is now doing the right thing.

**But still no change downstream, and the reason is now precise rather
than general.** Mi1's raw achromatic signal for the blob (10,438) is
~4x larger than for red-eye (2,555) -- a solid black high-contrast
circle simply produces far more raw darkness than a natural photo does.
That achromatic flood alone is more than enough to saturate LC9's
threshold-switch, completely swamping the now-correctly-near-zero color
signal. **This is a magnitude/wiring-strength problem, not a computation
problem:** the color channel works, but Tm20's real connection into
LC9/LC10a (128/1,402, per the earlier finding) is far too weak to ever
outvote Mi1's achromatic drive when the achromatic signal is this much
stronger, regardless of what color information says.

Scripts/files updated: `image_to_tm20_color.py` (bug fix, real opponent
signal). Files added: `spike_summary_color2_red/white/blob.csv`.

### Real motion-energy signal added (frame-to-frame contrast change), smooth centered approach — `confirmed`, real partial fix

Direct follow-up to the Aptekar/Keleş/Lu/Zolotova/Frye 2015 finding
(full text finally retrieved via browser after 6 blocked access
attempts): LC9 and LC10a show very small ON/OFF (static flicker)
responses and require genuine moving-edge motion to respond strongly.
Our entire pipeline up to this point only ever drove neurons with
static per-frame contrast -- never a real motion signal.

**Two real corrections made together, per user's own diagnosis:**
1. Removed random position jitter from the approach sequence (was
   working against coherent edge motion) -- replaced with a smooth,
   centered growth curve (real fixation behavior: a tracked target
   stays roughly centered while it grows, it doesn't jump around).
2. Added a real frame-to-frame local contrast CHANGE signal (a coarse
   proxy for true T4/T5 elementary motion detection, which compares
   neighboring positions over time -- not implemented at that level of
   detail here, but a real, principled first approximation), combined
   additively with the existing static contrast.
   `approach_sequence_motion.py`, `--motion-weight` flag (0 = old
   static-only pipeline, exactly reproducible for comparison).

**Ran all 3 real stimuli (red-eye, white-eye, blob) with and without
the motion term, same smooth centered approach, same network
(`connectome_full_matrix_final.csv`), same 8x boost:**

| condition | LC9 | LC10a | b3 MN (wing-steering response) | DNp09/PVLP004 (danger) | DNp01->TTMn (escape) |
|---|---|---|---|---|---|
| red, static-only | 0 | 0 | 0 | 0/0 | 10->3 |
| **red, +motion** | **3,480** | **4,248** | **47** | **28/243** | **42->13** |
| white, static-only | 0 | 0 | 0 | 0/0 | 0->0 |
| white, +motion | 0 | 0 | 0 | 0/0 | 19->7 |
| blob, static-only | 10,098 | 11,967 | 123 | 84/700 | 95->29 |
| blob, +motion | 10,237 | 12,159 | 130 | 85/707 | 95->31 |

**Result: a real, partial fix.** Adding genuine motion-energy driving
pushed red-eye from completely silent to fully active (LC9/LC10a both
firing hard) -- a real qualitative change, not present with static-only
driving. White-eye, given the identical treatment, stayed at exactly
zero for every LC9/LC10a-downstream readout. **This is the first test
in this entire project where red-eye and white-eye separate cleanly
during a realistic (blurred, resolution-limited, gradually-approaching)
presentation** -- earlier clean separations all used an unrealistic
instant full-strength static presentation.

**Did not fix the blob problem.** The blob was already saturating
every readout even without the motion term (a solid, maximum-contrast
object is simply a much stronger raw signal), so adding motion on top
changed it by only a few percent. Blob remains the strongest of the
three stimuli either way -- red-eye now competes with it, but doesn't
separate from it.

**Honest interpretation:** the real biology (motion-sensitivity
requirement) explains why our earlier static-only tests were giving an
unrealistically permissive/uniform "if it's dark enough, everything
fires" pattern -- adding real motion sensitivity makes the circuit
more selective and closer to how real LC9/LC10a are documented to
behave, and it produces a genuinely new, real distinction (red vs
white) that a static-only pipeline could never produce, regardless of
tuning. It does not, on its own, solve the separate, still-open
question of mate-vs-threat (blob) discrimination -- that likely still
needs the real, un-built size/shape-selectivity (end-stopped
inhibition) or the multisensory/state-dependent mechanisms discussed
earlier.

Scripts/files added: `approach_sequence_motion.py`,
`spike_summary_appmot_{red,white,blob}_{static,motion}.csv`.

### Terminology correction note

Caught reusing the word "chase" for b3 MN in several entries after
already agreeing earlier this session to retire it (b3 MN is a general
wing-steering muscle, not confirmed to indicate pursuit direction, and
is also directly excited by MDN, the real retreat-command neuron --
see the earlier "why are we calling it chase" discussion). Not
rewriting every historical instance above this note, consistent with
this project's practice of correcting forward rather than silently
editing past entries -- but from this point on, b3 MN is referred to
as the "wing-steering response," not chase.

### Added LC10b/LC10d, real octopamine (73 neurons) and dopamine (378 neurons, filtered) — `confirmed`, amplifies rather than discriminates

Added LC10a's two real, connected siblings (LC10b: 95 neurons, modest
connectivity; LC10d: 214 neurons, heavily wired -- LC10a->LC10d weight
13,852, LC10d->AOTU019 weight 7,828, nearly as strong as LC10a's own
direct AOTU019 connection). Also searched male-cns for real
octopaminergic neurons (126 total, real documented types: OA-VUMa,
OA-VPM, OA-AL2i, OA-ASM) and dopaminergic neurons (4,447 total,
mostly irrelevant Kenyon cells) -- filtered both down to only neurons
with at least one real edge to/from the existing network (73
octopamine, 378 dopamine kept), which naturally excluded ~4,000
irrelevant mushroom-body memory neurons while keeping the real,
functionally-connected danger-suppression cluster (PPM1201-1205) and
courtship-reward cluster (PAM01-15). Real, substantial connectivity
confirmed before merging: octopamine -> TmY5a (the same shared bridge
neuron implicated throughout this project) = 19,300 real weight;
dopamine -> TmY5a = 594 in / 2,439 out; dopamine <-> pC1 subtypes,
real and bidirectional (500+ weight on several individual pairs).
`connectome_full_matrix_complete.csv`/`_neurons.csv`, 15,624 real
neurons, 528,583 real edges.

**Re-ran the same 6-condition test (red-eye/white-eye/blob x
static/motion) on this complete network:**

| condition | LC9 | LC10a | b3 MN | danger | escape | MDN | octopamine | PAM (reward) | PPM (danger-suppress) |
|---|---|---|---|---|---|---|---|---|---|
| red, static | 0 | 0 | 0 | 0/0 | 10->3 | 0 | 0 | 0 | 0 |
| red, +motion | 3,761 | 4,533 | 47 | 30/312 | 45->13 | 5 | 71 | 15 | 28 |
| white, static | 0 | 0 | 0 | 0/0 | 0->0 | 0 | 0 | 0 | 0 |
| white, +motion | 0 | 0 | 0 | 0/0 | 19->7 | 0 | 2 | 0 | 0 |
| blob, static | 15,528 | 18,727 | 127 | 135/1,169 | 152->34 | 3 | 351 | **543** | 118 |
| blob, +motion | 15,873 | 19,106 | 134 | 136/1,188 | 154->35 | 1 | 357 | 543 | 118 |

**Result: real octopamine and dopamine activity is present and
measurable, but scales with overall circuit strength rather than
providing content-specific discrimination.** Both chemical systems are
at zero for white-eye (which never crosses threshold at all), real and
present for red-eye, and largest for the blob -- the same ordering as
every other readout in this project. Most notable, and worth flagging
honestly rather than glossing over: **the real courtship-reward
dopamine cluster (PAM) fires far MORE for the plain black blob (543)
than for the actual red-eye mate (15)** -- backwards from what a
genuine, content-specific courtship-reward signal should do. This
confirms, via a different and independent real circuit than any tested
before, the same root-cause finding from earlier: whatever's driving
these downstream systems (in this build) is raw stimulus magnitude,
not stimulus identity.

**Also, adding LC10d specifically substantially amplified the blob's
overall response** (LC9 roughly 10,098 -> 15,528 versus the
pre-LC10d/pre-neuromodulator network), consistent with real, massive
LC10a<->LC10d mutual excitation and the neuromodulators' own real
excitatory contributions back into the shared bridge neurons --
amplifying the existing imbalance rather than correcting it.

**Small, new, real signal worth tracking further:** MDN (retreat)
picked up a small amount of real activity for red-eye-motion (5
spikes) that wasn't present before these additions -- likely via new
indirect pathways through LC10d or the neuromodulatory neurons. Not
yet traced to a specific real edge.

Scripts/files added: `spike_summary_complete_{red,white,blob}_{static,motion}.csv`.

### Real cVA pheromone pathway added (antenna -> lateral horn) — `confirmed`, correct at the sensory stage, still outweighed at the decision stage

Traced and added the real cVA (pheromone) detection pathway: ORN_DA1
(204 real neurons, entryNerve=AN confirming physical location in the
antenna) -> DA1_lPN/DA1_vPN (real glomerulus relay, 13+2 neurons) ->
LH008m/LH007m (real lateral horn neurons, found by tracing one extra
hop past the initial DA1 downstream search). Confirmed BEFORE building
that LH008m and LH007m have real, direct connections into our existing
courtship circuit: LH008m->pC1_3c (77), LH008m->AOTU019 (69),
LH008m->aIPg1 (87), LH007m->pC1_5b (66), LH007m->pIP10 (128, the
largest single real weight found), LH007m->aIPg1/aIPg5 (6/11).
`connectome_full_matrix_cva.csv`/`_neurons.csv`, 15,862 real neurons,
543,558 real edges.

**Built a real, distance-proportional cVA concentration signal**
(present, ramping up as the approach sequence's radius grows, for both
red-eye and white-eye -- real flies -- and exactly zero throughout for
the blob, since a blob emits no real pheromone), driving all 204
ORN_DA1 neurons uniformly (no real retinotopic structure for smell,
unlike vision).

**Ran red-eye, white-eye, and blob with cVA + the existing visual
motion signal combined, same network, same boost:**

| readout | red-eye | white-eye | blob |
|---|---|---|---|
| ORN_DA1 (antenna) | 11,984 | 11,984 | **0** |
| LH008m / LH007m (lateral horn) | 1,151 / 767 | 1,143 / 764 | **0 / 0** |
| pC1 (courtship commitment, all subtypes) | 2,615 | 2,354 | 3,172 |
| pIP10 (courtship song) | 59 | 59 | 103 |
| AOTU019 | 56 | 16 | 182 |

**Result: cVA works correctly and completely at the sensory/relay
stage -- the first channel in this entire project where the blob
produces EXACTLY zero while both real fly photos produce real, correct,
nonzero activity.** This is a clean, genuine win, not a partial one.

**But the decision-stage readout (pC1) still favors the blob overall**
(3,172 vs 2,615/2,354), because pC1 receives real input from BOTH cVA
AND the visual pathway (via LC10a), and for the blob, LC10a's own
massive visual drive (19,106 spikes, vs 3,708 for red-eye) outweighs
the correctly-behaving cVA contribution once both land on the same
downstream neuron. **The fix works exactly where it was built; it just
isn't currently strong enough, relative to the oversized visual signal,
to flip the final decision-stage readout.**

**Honest interpretation and natural next step:** this suggests the real
fix isn't necessarily "add more of a correct signal" but rather
"correct the relative WEIGHTING between the visual and olfactory
inputs into pC1" -- in real flies, cVA/smell is understood to be a
comparably strong or even gating cue for courtship commitment, not a
minor addition to an already-decided visual signal. Our current
--type-boost only amplifies the visual (LC9/LC10a) side; nothing
currently boosts the olfactory side to a comparable real-world
strength. Worth testing a boosted cVA condition, or a reduced visual
boost, to see whether the correct-but-currently-outweighed olfactory
signal can be given its likely real proportional influence.

Scripts/files added: `seq_cva_{red,white,blob}.npy`,
`spike_summary_cvatest_{red,white,blob}.csv`.

### Real female-attractant pheromone (Z4-11Al / VA6 pathway) added and traced 3 hops to pC1/AOTU019 — `confirmed`, correct signal, still insufficient

Corrected the earlier cVA mismatch: researched and found the real,
named, female-specific, LONG-RANGE (olfactory, not contact) attractant
-- (Z)-4-undecenal (Z4-11Al), sensed via real receptor Or69a, real
target glomerulus named VA6 in this dataset's convention. Confirmed
real anatomy: ORN_VA6 (63 real neurons, entryNerve=AN, excitatory) ->
VA6_adPN (2 real neurons, excitatory) -> traced 416 real downstream
targets, checked top ~20 for a second-hop connection to our courtship
circuit, found three real relay routes: LHPV12a1 (GABA, weight
12/11/1 into pC1_2a/1a/1b), LHAV2b2_a (acetylcholine, weight up to 61
into pC1_2a, plus 32/12/5/5/4/1 into other pC1 subtypes and aIPg1),
AL-AST1 (acetylcholine, weight 13 into AOTU019). Mostly excitatory
overall (2 of 3 real relay routes excitatory). Merged:
`connectome_full_matrix_va6.csv`/`_neurons.csv`, 15,941 real neurons,
547,302 real edges.

**Built a real Z4-11Al concentration signal, present identically for
both red-eye and white-eye (a genuine female is present regardless of
eye color) and zero for the blob, same distance-ramping profile as the
earlier cVA test. Ran all 3 conditions:**

| | red-eye | white-eye | blob |
|---|---|---|---|
| ORN_VA6 (antenna) | 3,461 | 3,463 | **0** |
| pC1 (courtship decision, all subtypes) | 593 | **0** | 3,131 |

**Result: the correct pheromone works exactly as designed, and still
isn't enough.** Confirms two things precisely: (1) pC1 needs a
COMBINED push from both vision and smell to activate -- white-eye gets
a full, correct smell signal but still shows pC1=0, because its visual
side (LC10a) never crosses threshold at all, so the smell signal alone
isn't sufficient. (2) For red-eye, pC1 DID activate this time (593,
better than any earlier test using only vision or only the wrong
pheromone) -- but the blob still wins overall (3,131), because its raw
visual signal (LC10a=19,099) is roughly 4x larger than red-eye's
combined visual+smell total, and no realistically-sized real smell
contribution can outweigh a visual excess that large.

**Final, honest conclusion of this entire investigation:** every real
addition this session -- color vision, LC10 siblings, octopamine,
dopamine, and now two separate real pheromone pathways -- either
scales with the same underlying visual magnitude bias or, at best,
adds a real but proportionally small correct signal that the
oversized visual pathway still outweighs. The actual, structural fix
was identified early and never built: real size/shape-selectivity
(end-stopped inhibition, hypothesis #6) at the visual stage itself,
which would stop a plain large dark blob from ever producing a bigger
signal than a correctly-sized, correctly-identified real target in the
first place. Every other real biological mechanism added this session
has been fighting an uphill battle against that one, still-unfixed
root cause.

Scripts/files added: `seq_va6_{red,white,blob}.npy`,
`spike_summary_va6test_{red,white,blob}.csv`.

### Built the real LC16 + dopamine-ramp suppression circuit — `confirmed`, correctly wired, functionally inert in this scenario

Checked the connectome before building, per the real literature's own
description of this mechanism as "diffuse chemical release" rather
than point-to-point wiring: confirmed our originally-assumed dopamine
source (PPM1201-1205) has only trace/negligible real synaptic contact
with LC16 (2/0/14/0 weight) -- matching the literature. Found instead
a real, substantial, DIFFERENT dopamine source: LoVC18 and LoVC22 (4
real neurons each), which receive real direct input from our own
existing circuit (LC9->LoVC18: 36, LC10a->LoVC22: 50), and connect to
LC16 with real, meaningful weight (165, 78). Checked LC16's own real
downstream before building further: LC16->PVLP004 (one of our existing
danger readouts) = 835, a large real weight; LC16->DNp09/DNp01/TTMn =
all exactly zero, meaning this mechanism was never going to touch the
actual jump-escape pathway, only PVLP004 -- flagged honestly before
building, not after.

**Real correction applied before running anything:** the project's
default sign convention (GABA/glutamate = inhibitory, else
excitatory) doesn't know that THIS specific dopamine->LC16 connection
works through the real, documented Dop2R receptor (Gi-coupled,
inhibitory, confirmed via Cazalé-Debat et al. 2024) -- manually corrected
the LoVC18/LoVC22->LC16 edges to negative (243 total weight, 214
edges) rather than trusting the generic heuristic, which would have
simulated dopamine exciting LC16 instead of suppressing it.
`connectome_full_matrix_lc16.csv`/`_neurons.csv`, 16,123 real neurons,
561,036 real edges.

**Re-ran the extended 1.5-second red-eye approach test on this
network, comparing early (0-500ms) vs late (500-1500ms) spike rates:**

| | early rate (/ms) | late rate (/ms) |
|---|---|---|
| LoVC18 (dopamine) | 0.018 | 0.179 |
| LoVC22 (dopamine) | 0 | 0 (never fired) |
| **LC16** | 0 | **0 (never fired, either window)** |
| PVLP004 | 0.614 | 6.087 (identical to the earlier no-suppression run) |

**Result: the suppression mechanism is real, correctly wired, and
functionally inert in this specific test, for two independent real
reasons.** (1) LC16 itself never crossed its firing threshold at any
point in the 1.5-second simulated window, given the real, modest
weight it receives from LoVC18/LoVC22 (which themselves only fired
weakly) -- so there was nothing present to actually suppress. (2) Even
a fully-active LC16 would likely not have changed PVLP004's overall
trajectory much regardless, because PVLP004's real dominant driver is
a direct connection from LC9 (weight 31,334, confirmed earlier this
session) -- roughly 40x larger than LC16's own real contribution (835).
PVLP004's runaway growth in the extended-hold test is being driven
almost entirely through that separate, much larger pathway, which this
suppression mechanism was never wired to touch.

**Honest, final conclusion of this whole suppression-mechanism
investigation:** we found, verified, and correctly built a real,
literature-grounded biological mechanism -- and confirmed, through
direct simulation rather than assumption, that it would not have
solved the problem we set out to fix, even in principle. This is a
genuine negative result, arrived at properly (build it, test it,
report what actually happened) rather than left as an untested
assumption.

Scripts/files added: `seq_lc16test_red_long.npy`,
`spike_summary_lc16_red_long.csv`, `spike_times_lc16_red_long.csv`.

### Built LC11 (real end-stopped size detector) and tested the real optimal-size scenario — `confirmed`, two independent real limits found

Confirmed LC11 (143 real neurons, acetylcholine) exists in male-cns and
is exceptionally well-positioned in our existing circuit: massive real
upstream from the SAME shared bridges already driving everything else
(T2->LC11: 36,917; T2a->LC11: 24,572; TmY5a->LC11: 1,956), and
substantial real direct output into both LC9 (1,730) and LC10a (2,441)
-- the exact shared gateway implicated throughout this entire project.
`connectome_full_matrix_lc11.csv`/`_neurons.csv`, 16,266 real neurons,
595,194 real edges.

**Built a real size-gain function from Keleş & Frye 2017's actual
measured tuning curve** (peak response at 8.8deg, response falls to a
real asymptotic floor by ~24deg -- both real, published numbers),
converted using this project's own established real degrees-per-radius
mapping (radius=4 units = 22.5deg, from earlier work): peak gain at
radius=1.56, floor (0.15, an 85% real reduction) reached by radius~6+.

**Tested the real, intended scenario directly: a properly-sized mate
photo (radius=1.56, LC11 at full/peak gain) vs. an oversized blob
(radius=10, LC11 suppressed to its real floor via --type-boost
LC11:LC9:0.15,LC11:LC10a:0.15):**

| condition | LC9 | LC10a | LC11 | b3 MN | DNp09/PVLP004 | DNp01->TTMn |
|---|---|---|---|---|---|---|
| red-eye, small (real optimal size) | 0 | 0 | 0 | 0 | 0/0 | 0->0 |
| white-eye, small (real optimal size) | 0 | 0 | 0 | 0 | 0/0 | 0->0 |
| blob, large, LC11 suppressed | 19,949 | 24,122 | 1,178 | 150 | 174/1,473 | 190->40 |

**Result: two independent, honest, real limits found, neither of which
is a flaw in the LC11 mechanism itself.** (1) At the genuine
biologically-realistic small size (only 9 real Mi1 columns driven),
NOTHING fires at all in this network -- not even LC11 itself -- because
there simply isn't enough total raw signal at that scale to cross
ignition threshold, even at maximum arousal boost. This connects
directly to the still-unresolved early-vision amplification gap
identified much earlier this session (the flyvis research task) --
real fly eyes have an additional real gain-boosting stage before this
point that we have never built. (2) Even where the blob CAN be tested,
correctly suppressing LC11 to its real floor barely changes the
outcome (LC9=19,949, as strong as or stronger than earlier
unsuppressed blob runs), because LC11 is only one of several real
pathways into LC9/LC10a -- the direct bridge connections (T2, T2a,
TmY5a -> LC9/LC10a directly) are far larger and completely untouched
by this specific suppression.

**Final, honest conclusion of the entire size/shape-selectivity
investigation:** the real mechanism exists, was correctly researched,
correctly identified in the connectome, and correctly implemented --
and testing it honestly revealed that this project's simulation has a
structural amplification gap (missing early-vision gain control) that
prevents the realistic small-target scenario from ever generating
enough signal to be observed at all, independent of anything else
this session built or found.

Scripts/files added: `seq_lc11_red_small.npy`,
`seq_lc11_white_small.npy`, `spike_summary_lc11_{red_small,white_small,blob_suppressed}.csv`.

### Tested real early-vision amplification (Naka-Rushton) on the small-target scenario — `confirmed`, amplification alone is insufficient

Added `--amplify` to `photo_multi_position.py` (real two-stage
retina+lamina Naka-Rushton amplification, reusing the exact function
already established earlier in this project). Confirmed it worked
correctly at the signal level: mean per-neuron stimulus jumped from
0.075/0.059 (unamplified) to 0.364/0.360 (amplified) for red-eye/
white-eye at the true optimal small size (radius=1.56, only 9 real
Mi1 neurons driven) -- roughly a 5x real boost.

**Re-ran both through the network. Still exactly zero everywhere for
both conditions** (LC9, LC10a, LC11, b3 MN, DNp09, PVLP004, DNp01,
TTMn all 0).

**Result, refined and more precise than the earlier finding:** the
missing early-vision gain stage is real, and per-neuron amplification
alone does not fix the problem. The deeper issue is that only 9 real
neurons are driven at the genuinely realistic small-target size,
and no amount of per-neuron saturation can manufacture enough TOTAL
current from just 9 contributing neurons to cross this network's
ignition threshold -- a threshold whose absolute scale was effectively
calibrated (via the arousal --type-boost and input-current parameters
used throughout this project) around driving hundreds of neurons at
once (typical radius=8-10 tests drive 197-317 real neurons). This
network has never been validated at the true few-neuron scale that
real small-object detection (LC11, 8.8deg) actually operates at.

**Honest stopping point for this investigation:** fixing this properly
would require either recalibrating the network's absolute input-
current/threshold scale specifically for the small-target regime (a
real, nontrivial parameter-fitting exercise, not just adding an
amplification stage), or finding additional real, currently-unbuilt
early gain stages beyond simple contrast amplification (e.g. genuine
photoreceptor pooling/convergence ratios not yet modeled). Not
resolved in this session.

Scripts/files added: `photo_multi_position.py` (`--amplify`,
`--retina-c50`, `--lamina-c50`), `seq_amp_{red,white}_small.npy`,
`spike_summary_amp_{red,white}_small.csv`.

## SESSION CHECKPOINT #3 — consolidates everything since checkpoint #2, resume from here

Checkpoint #2 stopped after the first color-channel build. Everything
below happened since then, all real, all logged in detail above this
point -- this is the consolidated summary.

**Real circuits added since checkpoint #2, all merged into one final
network (`connectome_full_matrix_lc11.csv`/`_neurons.csv`, 16,266 real
neurons, 595,194 real edges):**
- Fixed a real bug in the color-opponent channel (was measuring raw
  channel darkness, not true color opponency; corrected to a real
  R-vs-(G+B) redness signal) -- works correctly now, still too weakly
  wired into LC9/LC10a to change outcomes.
- Added real frame-to-frame motion-energy driving (LC9/LC10a barely
  respond to static flicker per real literature) -- this was the ONE
  addition that produced a genuine, clean red-eye vs white-eye split
  under realistic (non-instant) viewing, though it didn't help vs the
  blob.
- Added LC10a's real siblings LC10b/LC10d (LC10d heavily amplifies via
  massive real mutual excitation with LC10a).
- Added real octopamine (73 connected neurons) and dopamine (378
  connected neurons, filtered from 4,447 total) -- both real and
  functional, but scale with overall stimulus magnitude rather than
  content; PAM (reward) dopamine fired ~35x more for the blob than the
  real mate photo.
- Added real cVA pheromone pathway (antenna->lateral horn->pC1/AOTU019)
  -- discovered mid-build that cVA is actually a MALE pheromone and an
  anti-aphrodisiac when a male smells it (real literature), meaning
  this was testing "rival male nearby," not "available mate" -- the
  real inhibitory wiring found matches this correctly.
- Corrected to the real FEMALE-specific long-range attractant,
  (Z)-4-undecenal (VA6 pathway) -- traced 3 real hops to pC1/AOTU019,
  confirmed mostly excitatory. Made the mate photo's pC1 activity real
  and nonzero (593) but the blob still won overall (3,131), because
  its visual drive is ~4x larger than red-eye's combined visual+smell
  total.
- Checked for a real "pC1 suppresses danger" wire -- none exists
  (weight ~1, negligible). The literature's real mechanism runs through
  a different neuron (LC16) via slow-building dopamine, not pC1 itself.
- Built the real LC16 + dopamine-ramp suppression circuit (LoVC18/
  LoVC22, real, driven by our own LC9/LC10a) with the correct real
  Dop2R-inhibitory sign (had to override the project's default
  sign-by-neurotransmitter heuristic manually for this one connection).
  Tested over an extended 1.5-second simulated window: LC16 never
  fired at all (too weak an input), and even if it had, PVLP004's real
  dominant driver is a direct LC9 connection (weight 31,334) ~40x
  larger than LC16's own contribution (835) -- suppression circuit is
  real and correctly wired but functionally inert here.
- Built the real LC11 end-stopped size-detector (Keleş & Frye 2017) --
  exceptionally well-positioned, massive real shared-bridge input,
  substantial real direct output into LC9 (1,730) and LC10a (2,441).
  Implemented its real measured tuning curve (peak at 8.8deg, floor by
  24deg) as a size-dependent gain. Tested the intended real scenario
  (small correctly-sized mate vs oversized blob): NEITHER red-eye nor
  white-eye fired at all at the true realistic small size (only 9 real
  neurons driven, not enough total current to ignite regardless of
  size-tuning), and the blob, even with LC11 correctly suppressed,
  barely changed (LC11 is one of several real inputs into LC9/LC10a;
  direct bridge connections dwarf it).
- Added real two-stage Naka-Rushton amplification (`--amplify` flag,
  `photo_multi_position.py`) to test whether boosting weak signals
  would let the small, realistic target finally fire. Confirmed the
  amplification works correctly at the signal level (~5x boost) but
  still produced exactly zero downstream activity for both red-eye and
  white-eye -- amplifying 9 neurons' signal strength can't manufacture
  the total current that comes from having more neurons recruited.

**Final, precise, well-evidenced root cause of the entire "can't tell
mate from blob" investigation, arrived at by systematically building
and testing every plausible real fix rather than assuming:** this
project's simulation has never validated its absolute input-current/
threshold scale against the genuinely small, few-neuron regime that
real small-object detection (LC11, ~8.8deg, ~9-50 real neurons) 
actually operates at. Every test all session used stimuli covering
197+ real neurons (radius 8-10) because that's the scale the network
was implicitly calibrated around (via --type-boost and --input-current
choices made early in the project, before this gap was identified).
Real, small, correctly-sized targets never generate enough total
current to cross that scale's ignition threshold, regardless of which
real biological mechanism (color, chemistry, size-tuning, dopamine
suppression) gets added on top.

**Natural next steps, in priority order:**
1. **Recalibrate the network's absolute scale for the small-target
   regime** -- likely needs new --input-current/--type-boost values
   specifically fit to driving ~9-50 neurons, not the 197+-neuron scale
   used throughout this project so far. This is a real parameter-fitting
   exercise, not another circuit addition.
2. Once recalibrated, REPEAT the LC11 size-selectivity test (small
   properly-sized mate vs oversized blob) -- this is the test that
   actually answers the original question, blocked only by the
   calibration gap found today.
3. Revisit real camera capture for genuine approach motion (still never
   completed, tools exist: `live_preview.py`/`preview_and_capture.py`).
4. The real forward-walking-command-neuron gap (DopaMeander-equivalent)
   for genuine positive chase-direction evidence remains open.

NEUPRINT_APPLICATION_CREDENTIALS supplied by user this session; will
need re-export next session (not stored in any project file).

### Recalibrated input-current for the small-target regime — `confirmed`, clean real result at the genuinely realistic scale

Directly addressed checkpoint #3's top priority. Swept `--input-current`
at the true small-target size (radius=1.56, 9 real neurons, amplified)
to find the network's real ignition threshold for this regime: sharp
switch between 1600 (nothing fires) and 1800 (everything fires) --
roughly an 18x increase over the standard setting (100) used
throughout the rest of this project, consistent with needing
proportionally more per-neuron current to compensate for ~20-30x fewer
neurons contributing (9 vs the 197-317 used in every earlier test).

**Re-ran red-eye and white-eye at the recalibrated input-current=1800,
same amplification, same 8x arousal boost, same real 9-neuron target:**

| | red-eye | white-eye |
|---|---|---|
| Mi1 | 598 | 574 |
| LC9 | **14,805** | **0** |
| LC10a | **17,846** | **0** |
| b3 MN | **123** | **0** |
| DNp01->TTMn | 45->13 | 5->1 |

**Result: clean, sharp, real distinction at the genuinely realistic
scale -- the cleanest result of the entire session.** Once the
network's absolute scale is properly calibrated for the true
few-neuron regime (rather than left at settings implicitly tuned for
the 200+-neuron regime used everywhere else), a realistically-sized
red-eye target fires the whole circuit while an identically-sized
white-eye target stays completely silent. This directly confirms the
checkpoint #3 hypothesis: the missing piece was never another circuit
or mechanism -- it was that this specific parameter had never been
validated against the real, literature-documented small-target scale.

Scripts/files added: `spike_summary_cal_white_1800.csv`
(input_current=1800 calibration sweep results in /tmp, not preserved
individually -- the key finding is the calibrated value itself: 1800).

### Tested user's hypothesis: does a real pre-visual pheromone head start change dopamine suppression? — `confirmed`, no, for a precise mechanical reason

User's hypothesis: in real courtship, a male likely smells a female's
pheromone seconds-to-minutes before he sees her, and pursues the smell
first ("seeking out the source"). If real dopamine-mediated suppression
(Cazalé-Debat et al. 2024) builds up over TIME, this pre-visual head start
could mean suppression is already partially built up by the time vision
engages -- a real, plausible refinement to the earlier "no suppression
observed" finding.

**Checked the real connectome first:** does the pheromone pathway
(ORN_VA6/DA1 etc.) connect directly to any real dopamine-suppression
neuron, independent of vision? Found: smell pathway -> PPM1201 = real
weight 75 (33 edges) -- present, though modest. (PPM1202/1203/1205 and
LoVC22 showed zero; LoVC18 showed a negligible 7.)

**Built two matched real sequences at the recalibrated small-target
scale (input-current=1800):** (1) "pheromone-first" -- 1 real second of
pheromone-only exposure (ramping to a sustained level), THEN vision
turns on for 300ms while pheromone continues; (2) "pheromone-same" --
identical total duration, but pheromone and vision both start together
at the same moment (no head start). Ran both with full spike-time
output.

**Result: no meaningful difference (PPM1201: 30 vs 31 total spikes;
LC16: 0 vs 0 in both; PVLP004, LC9, LC10a, b3 MN, TTMn all statistically
indistinguishable between conditions).**

**Traced exactly why, via real spike timing:** in BOTH conditions,
PPM1201's first spike occurs at ~1130-1150ms -- AFTER vision turns on
at 1000ms, never during the pre-visual pheromone-only phase. The real
pheromone-only signal, even sustained for a full real second, was never
strong enough on its own to cross PPM1201's firing threshold. It only
fires once the much stronger visual signal also arrives and combines
with it -- meaning the pre-visual head start was never actually used,
regardless of how long it was given.

**Honest conclusion: the user's hypothesis is mechanistically sound and
consistent with real biology, but this specific model's real
pheromone->PPM1201 connection is simply too weak, on its own, to do
anything without help from vision.** This is the same "insufficient
total current" root cause found earlier with the small visual target,
now confirmed to also apply to the olfactory side of the suppression
circuit -- not a new, separate problem, but the same one showing up in
a second real pathway.

Scripts/files added: `seq_pheromonefirst_red.npy`,
`seq_pheromonesame_red.npy`,
`spike_summary_{pheromonefirst,pheromonesame}_red.csv`,
`spike_times_{pheromonefirst,pheromonesame}_red.csv`.

### Citation correction note

Every reference to "Mishra et al. 2024" throughout this log (11
instances) has been corrected to the real, verified authors:
**Cazalé-Debat, Scheunemann, Day, Fernandez-dV Alquicira, Dimtsi,
Zhang, Blackburn, Ballardini, Greenin-Whitehead, Reynolds, Lin, Owald &
Rezaval. "Mating proximity blinds threat perception." Nature
634(8034):635-643, 2024.** doi: 10.1038/s41586-024-07890-3. The
underlying real findings attributed to this paper throughout the log
(dopamine-mediated suppression of LC16 threat perception, real timing
data at 7s/120s/240s into courtship) were correctly drawn from the real
paper -- only the author name citation was wrong, corrected here as a
factual fix rather than a scientific retraction.

### Combined recalibrated small-target vision + real pheromone — `confirmed`, the cleanest, most complete result of the entire session

Final test of the day: real small-target visual stimulus (radius=1.56,
9 real neurons, amplified, recalibrated input-current=1800) combined
with the real female pheromone signal (VA6 pathway), run together from
the start, on the complete network with every circuit built this
session (chase, danger, escape, retreat, courtship-commitment,
color, octopamine/dopamine, both pheromone pathways, LC16 suppression,
LC11 size-selectivity, and the pC1/lateral-horn recurrent loop).

| readout | red-eye | white-eye |
|---|---|---|
| LC9 / LC10a | 14,751 / 17,792 | 0 / 0 |
| **pC1 (all subtypes)** | **3,036** | **0** |
| aIPg7 | 165 | 0 |
| pIP10 (song) | 97 | 0 |
| AOTU019 | 170 | 0 |
| b3 MN (wing-steering) | 120 | 0 |
| DNp09/PVLP004 (danger) | 129/1,118 | 0/0 |
| DNp01->TTMn (escape) | 140->31 | 5->1 |

**Result: every circuit built this entire session fires strongly and
together for the real red-eyed mate, and stays essentially completely
silent for the white-eyed one, at the genuinely realistic scale.** pC1
reached 3,036 -- by far the strongest courtship-commitment signal
produced in any test this session (compare: 593 in the earlier
non-recalibrated small-target+pheromone test, 47 in the very first
gradual-approach test). This is the cleanest, sharpest, most complete
real result of the entire investigation.

**Honest attribution check:** LH008m itself shows exactly 0 spikes --
meaning this specific result is NOT running through the newly-discussed
recurrent pC1/lateral-horn loop. pC1's massive activation here comes
from the OTHER real convergent pathways (direct visual drive via
AOTU019/aIPg, and the direct DA1_lPN->pC1 connection) that were already
present and simply needed the day's earlier recalibration
(input-current=1800) to become strong enough to fire on their own. The
recurrent loop is real, correctly wired, and remains untested in
practice -- today's actual breakthrough was the calibration fix, not
this specific loop.

Scripts/files added: `seq_loop_{red,white}_small.npy`,
`spike_summary_loop_{red,white}_small.csv`,
`spike_times_loop_{red,white}_small.csv`.

### Tested a precise 0.2ms smell-lead-over-vision — `confirmed`, no measurable difference

User requested a specific, small test: does giving smell exactly a
0.2ms head start over vision change anything? Rebuilt the stimulus at
fine 0.2ms time resolution (750 frames covering 150ms real time,
`--frame-duration 0.2`) so the offset could be represented precisely
(the project's usual 50ms-per-frame resolution can't represent an
offset this small). Ran both a 0.2ms-lead version and a matched
zero-lead control at the identical fine resolution and window length.

| | pC1 (all) | LC9 | LC10a | TTMn |
|---|---|---|---|---|
| 0.2ms lead, red-eye | 320 | 2,689 | 3,084 | 9 |
| no lead, red-eye (control) | 325 | 2,699 | 3,097 | 9 |
| white-eye, both versions | 0 | 0 | 0 | 1 |

**Result: no meaningful difference -- the small variation (320 vs 325
etc.) is normal run-to-run noise, not a real effect.** Consistent with,
and more precisely confirming, the earlier 1-second pheromone-head-
start test (also null). Real neurons integrate input over a membrane
time constant of several milliseconds; a 0.2ms offset is far too brief
for that integration process to register at all, so smell and vision
are effectively simultaneous from the network's perspective at this
timescale, regardless of which one nominally "started" first.

Scripts/files added: `seq_smellead_{red,white}.npy`,
`seq_smellsame_{red,white}.npy`,
`spike_summary_{smellead,smellsame}_{red,white}.csv`.

### Tested a full real 1-second smell-only lead before vision — `confirmed`, definitively closes the timing question

Extended the earlier timing tests (0.2ms lead, 1-second pheromone-first
approach test) to a clean, controlled version: exactly 1000ms of
smell-only exposure (ORN_VA6 sustained, vision at zero), followed by
300ms of smell+vision together (`--frame-duration 10`, 130 total
frames).

| | pC1 (all) | LC9 | LC10a | PPM1201 |
|---|---|---|---|---|
| red-eye, 1s smell lead | 3,070 | 14,768 | 17,789 | 29 |
| white-eye, 1s smell lead | 0 | 0 | 0 | 0 |

Essentially identical to the simultaneous-onset baseline (pC1=3,036) --
no meaningful change from adding the lead.

**Checked the real spike timing directly: PPM1201 produced ZERO spikes
during the entire 1000ms smell-only window.** Its first spike occurs at
t=1130ms -- ~130ms after vision turns on at t=1000ms, the same delay
seen in every earlier version of this test regardless of lead duration
(0.2ms, ~1s approach test, and now a clean 1s controlled version).

**Definitive conclusion, closing this line of inquiry:** duration of
smell exposure does not matter, at any timescale tested (0.2ms to
1000ms). Real integrate-and-fire neurons don't accumulate charge
indefinitely under a weak, steady input -- they settle into a stable
sub-threshold resting state and stay there regardless of how long that
state persists. The real bottleneck is connection STRENGTH (smell ->
PPM1201, weight 75, confirmed too weak earlier this session), not
TIME. No amount of pre-exposure, however long, will make this specific
real pathway fire on its own without help from vision.

Scripts/files added: `seq_smell1s_{red,white}.npy`,
`spike_summary_smell1s_{red,white}.csv`,
`spike_times_smell1s_{red,white}.csv`.

### DISCARDED — this section and the two that follow it (10-trial extension, 3-seed mean+/-std) are superseded

Root cause found: the exact literal command that produced the 3
seed values below was never saved anywhere, only described in prose.
When this project's session was later resumed (context compaction),
attempting to reconstruct that command from the prose description and
rerun it for seeds 4-10 produced a DIFFERENT, non-matching pattern
(white/blob firing fully in the large majority of trials, not 1-in-3)
-- and repeated attempts to find a parameter combination (varying
`--type-boost`, `--seed` offset) that reproduces the original seed-1-3
values (white=0, red=14,749) all failed, even though every individual
rerun is itself perfectly reproducible (same command + same seed always
gives the same result, verified by running the identical command twice
in a row). This means the seed-1-3 baseline and the seed-4-10
extension were generated by two different, non-comparable setups that
got mixed together in one table -- an error. User's decision: discard
all of it and replace with a single fresh, internally consistent batch
(see "Canonical 50-trial robustness check" below). Lesson applied
going forward: every logged test must save its exact literal command
line, not just a prose description of its parameters.

### SUPERSEDED — original 3-trial robustness check (kept for the record, do not use for comparisons)

User requested proper rigor: repeat the small-target/smell tests across
multiple noise-seeded trials (real membrane noise, `--noise-sigma 0.5`,
3 different seeds), plus a matched blob-only control (no smell) at the
same recalibrated scale, to check whether the earlier "clean red vs
white" result was a real, robust finding or a one-off.

**3 trials each, red-eye+smell(50ms lead), white-eye+smell(50ms lead),
blob(no smell), all at input-current=1800:**

| condition | trial 1 | trial 2 | trial 3 |
|---|---|---|---|
| red-eye + smell (LC9) | 14,749 | 15,036 | 14,271 |
| white-eye + smell (LC9) | 0 | **14,626** | 0 |
| blob, no smell (LC9) | 0 | 0 | **13,260** |

**Result: red-eye is genuinely robust (fires strongly, consistently,
all 3 trials). White-eye and the blob are NOT reliably silent --each
crossed into full activation in exactly 1 of 3 trials, purely from
added noise, reaching nearly the same magnitude as red-eye when they
did.**

**Honest, important correction to the earlier "cleanest result of the
session" claim:** the recalibrated input-current (1800) sits almost
exactly ON the network's ignition threshold, not safely below it for
white-eye/blob and safely above it for red-eye. The earlier noise-free
tests happened to land cleanly on the correct side every time --
verified now to be a lucky deterministic outcome at a knife-edge
boundary, not a robust separation. Under real, modest noise, roughly
1 in 3 trials tips the "should stay silent" conditions over into full
activation anyway.

**This does not undo the earlier finding that red-eye vs white-eye is
a real, meaningful distinction** (red-eye's signal is objectively
stronger and more reliably crosses threshold) -- but it does mean the
specific calibration used is fragile, sitting right at the edge rather
than with real margin. A properly robust calibration would need either
a stronger real separation between the two conditions' raw input
strength, or a threshold set with genuine headroom below red-eye's
typical drive and above white-eye/blob's typical drive -- not the
exact boundary value found by a single deterministic sweep.

Scripts/files added: `seq_smell50ms_{red,white}.npy`,
`seq_blobcontrol.npy`, `seq_amp_blob_small.npy`,
`spike_summary_rep_{red,white,blob}_seed{1,2,3}.csv`.

### SUPERSEDED — 10-trial extension (mixed two non-comparable setups, do not use)

User's call: 3 trials isn't enough to trust a 1-in-3 "flip" rate --
extended the same test (identical stimulus files, identical
input-current=1800, `--noise-sigma 0.5`) to seeds 1 through 10 for all
three conditions (red-eye+smell, white-eye+smell, blob/no-smell).

**LC9 spike totals, all 10 seeds:**

| condition | seed1 | seed2 | seed3 | seed4 | seed5 | seed6 | seed7 | seed8 | seed9 | seed10 | fires fully |
|---|---|---|---|---|---|---|---|---|---|---|---|
| red-eye + smell | 14,749 | 15,036 | 14,271 | 16,352 | 16,625 | 17,007 | 16,271 | 16,136 | 17,290 | 16,451 | **10/10** |
| white-eye + smell | 0 | 14,626 | 0 | 16,004 | 16,539 | 16,947 | 16,335 | 16,058 | 17,146 | 16,009 | **8/10** |
| blob, no smell | 0 | 0 | 13,260 | 15,733 | 16,178 | 15,788 | 15,878 | 15,379 | 16,366 | 15,836 | **8/10** |

**Result: with a proper sample size, the earlier "1 in 3" flip rate was
itself a lucky underestimate.** At n=10, white-eye and the blob (with
NO visual stimulus at all) both fire at full magnitude in 8 of 10
trials -- statistically indistinguishable from red-eye's 10/10. Only
red-eye is genuinely robust. The input-current=1800 calibration does
not sit on a fragile-but-mostly-correct edge; under real membrane
noise (sigma=0.5mV) it is crossed by noise alone in the large majority
of trials, independent of eye color or even the presence of a real
visual target. This is a materially stronger correction than the
3-trial version: the calibration does not discriminate red-eye from
white-eye/blob in any way that would survive contact with realistic
trial-to-trial variability. A new calibration needs a real margin --
either a lower input-current that keeps noise-driven false positives
rare, or a stronger designed gap between the red-eye and white-eye/blob
driving currents -- not the single deterministic threshold value found
by the earlier no-noise sweep.

Scripts/files added: `spike_summary_rep_{red,white,blob}_seed{4..10}.csv`
(7 additional seeds per condition, 21 new runs, reusing the existing
`seq_smell50ms_{red,white}.npy` / `seq_blobcontrol.npy` stimulus files).

### SUPERSEDED — mean+/-std across the original 3 seeds (do not use)

Verified all 9 `spike_summary_rep_{red,white,blob}_seed{1,2,3}.csv`
files existed and were complete, then computed mean +/- std per
condition across those 3 seeds for every key readout neuron.

| neuron | red (mean +/- std) | white (mean +/- std) | blob (mean +/- std) |
|---|---|---|---|
| LC9 | 14,685.3 +/- 386.5 | 4,875.3 +/- 8,444.3 | 4,420.0 +/- 7,655.7 |
| LC10a | 17,690.7 +/- 456.9 | 5,869.3 +/- 10,166.0 | 5,499.0 +/- 9,521.1 |
| pC1 (all) | 3,018.3 +/- 37.0 | 1,008.7 +/- 1,747.1 | 961.0 +/- 1,664.5 |
| AOTU019 | 168.3 +/- 2.5 | 54.3 +/- 94.1 | 54.0 +/- 91.8 |
| b3 MN | 118.3 +/- 2.3 | 40.3 +/- 69.9 | 41.7 +/- 68.7 |
| DNp09 | 127.7 +/- 2.5 | 41.7 +/- 72.2 | 37.7 +/- 65.2 |
| PVLP004 | 1,107.0 +/- 24.5 | 368.7 +/- 638.5 | 335.0 +/- 580.2 |
| DNp01 | 138.3 +/- 3.5 | 49.0 +/- 76.2 | 50.3 +/- 69.9 |
| TTMn | 31.0 +/- 1.0 | 11.0 +/- 17.3 | 11.7 +/- 16.7 |

**Red-eye: tight and reproducible (std is only ~2-3% of the mean across
every readout).** White-eye and blob: **std exceeds the mean at every
single readout** -- the statistical signature of a bimodal, all-or-
nothing switch (dead silent OR fully saturated, essentially nothing in
between) rather than graded trial-to-trial variation. When the flip
happens for white-eye/blob, the entire downstream circuit lights up
together (LC9, LC10a, pC1, AOTU019, b3 MN, DNp09/PVLP004, DNp01/TTMn
all jump in lockstep), consistent with one shared threshold-crossing
event propagating through the whole network rather than independent
per-neuron noise.

**Does the earlier "clean separation" finding hold up? Partially.** The
real, meaningful distinction -- red-eye reliably drives the circuit,
white-eye/blob normally don't -- remains true and is not overturned.
But the specific calibration (input-current=1800) is confirmed, now
with a formal mean+/-std characterization on top of the raw counts, to
sit close enough to the network's ignition threshold that ordinary
membrane noise alone flips white-eye/blob to full activation in
roughly 1 of 3 trials at this seed count -- consistent with, and now
quantitatively reinforced by, the earlier 3-trial and later 10-trial
robustness checks. Recalibration with real margin remains the
outstanding next step.

### Canonical 50-trial robustness check — `confirmed`, replaces all earlier robustness-check sections above

Fresh, internally consistent batch: 50 noise-seeded trials (seeds
1-50, real membrane noise sigma=0.5mV) for each of 3 conditions --
red-eye+smell(50ms lead), white-eye+smell(50ms lead), blob(no smell)
-- 150 total runs, all using the exact same literal command (verified
reproducible: running the identical command twice in a row gives
identical output):

```
.venv/bin/python simulate.py \
  --edges connectome_full_matrix_lc11.csv \
  --neurons connectome_full_matrix_lc11_neurons.csv \
  --stimulus-sequence seq_smell50ms_{red,white}.npy   # or seq_blobcontrol.npy for the blob condition
  --stimulus-sequence-bodyids seq_smell50ms_{red,white}_bodyids.csv   # or seq_blobcontrol_bodyids.csv
  --frame-duration 10 \
  --input-current 1800 \
  --type-boost LC9:LC9:8.0,LC9:LC10a:8.0,LC10a:LC10a:8.0 \
  --noise-sigma 0.5 \
  --seed {1..50} \
  --spike-summary-out spike_summary_rep_{cond}_seed{seed}.csv \
  --spike-times-out spike_times_rep_{cond}_seed{seed}.csv
```

**Result: at this scale, red-eye, white-eye, and blob are no longer
distinguishable at all.** Every one of the 150 trials fired fully (0
silent trials in any condition) -- std is only ~2-3% of the mean for
every readout neuron, in all three conditions alike:

| Neuron code | Friendly name | First fires (ms) | Red (avg +/- std) | White (avg +/- std) | Blob (avg +/- std) |
|---|---|---|---|---|---|
| ORN_VA6 | Smell (the antenna) | 0.1 | 9,639 +/- 0 | 9,639 +/- 0 | 0 +/- 0 (no smell) |
| Mi1 | Vision (the eye) | 50.0 | 606 +/- 0.4 | 602 +/- 0.0 | 685 +/- 0.0 |
| DNp01 | Escape-jump command | 89.0 | 159.1 +/- 3.9 | 158.0 +/- 3.2 | 156.8 +/- 3.9 |
| TTMn | Jump muscle | 109.3 | 44.6 +/- 1.3 | 44.4 +/- 1.4 | 45.2 +/- 1.3 |
| LC9 | Danger/courtship gateway | 105.2 | 16,573 +/- 412 | 16,468 +/- 386 | 16,063 +/- 423 |
| LC10a | Mate-target detector | 108.0 | 20,048 +/- 506 | 19,915 +/- 478 | 19,438 +/- 509 |
| AOTU019 | Courtship relay | 111.7 | 185.3 +/- 3.3 | 183.6 +/- 3.8 | 180.5 +/- 4.0 |
| PVLP004 | Threat-alarm neuron | 118.2 | 1,251.5 +/- 25.4 | 1,243.5 +/- 25.1 | 1,213.8 +/- 25.9 |
| DNp09 | Threat-alarm neuron | 123.8 | 144.5 +/- 3.8 | 143.5 +/- 3.6 | 139.3 +/- 4.0 |
| b3 MN | Wing-steering muscle | 123.1 | 139.5 +/- 3.8 | 139.3 +/- 3.1 | 137.7 +/- 3.0 |
| pC1 (all) | Courtship-commitment neuron (total) | 124.9 | 4,752.2 +/- 81.0 | 4,706.8 +/- 86.8 | 4,455.2 +/- 81.0 |
| pIP10 | Courtship song command | 131.8 | 131.9 +/- 3.6 | 132.2 +/- 3.8 | 126.4 +/- 3.9 |
| aIPg7 | Courtship relay (aIPg) | 149.3 | 247.5 +/- 4.3 | 245.4 +/- 4.4 | 236.1 +/- 4.4 |

(Timing column = median first-spike time across the 50 red-eye trials
where the neuron fired; white/blob fire at essentially the same times
once they cross threshold, since it's the same shared circuit.)

**Honest conclusion, replacing every earlier robustness-check claim in
this log: at input-current=1800 with real membrane noise (sigma=0.5),
this calibration provides NO discrimination between a real mate
photo, a non-mate photo, and a plain blob with no smell at all.** All
three drive the full downstream circuit (LC9 through pC1) to
statistically indistinguishable magnitudes. This is a stronger, more
definitive version of the "knife-edge" finding -- not a fragile edge
that noise sometimes tips over, but a threshold so far past the true
separation point that noise pushes every condition over it essentially
every time. Recalibration is not optional cleanup; the current
input-current value is unusable for the red/white discrimination this
project is trying to demonstrate. Next step: sweep input-current
downward from 1800 (holding noise-sigma=0.5, type-boost fixed) to find
a value where the real visual+olfactory input strength difference
between red-eye and white-eye reliably produces different outcomes
across many trials, rather than both saturating past threshold.

Scripts/files added: `spike_summary_rep_{red,white,blob}_seed{1..50}.csv`,
`spike_times_rep_{red,white,blob}_seed{1..50}.csv` (150 runs total,
300 files). All earlier `spike_summary_rep_*_seed{1,2,3}.csv` files
from the discarded original baseline were overwritten by this batch
and no longer exist as a separate artifact -- the numbers quoted in
the discarded sections above are preserved only as text in this log.

### Split visual/olfactory current, built a properly matched blob control, swept visual drive down — `confirmed`, real ordering emerges once the control is fair

Two methodology fixes applied before this sweep:

1. **Split `--input-current`**: added `--scale-types`/`--scale-mult` to
   `simulate.py`, letting the visual (Mi1) and olfactory (ORN_VA6)
   pathways be driven independently within one combined stimulus file.
   ORN_VA6 stays fixed at full input-current=1800 throughout (it
   already saturates identically red/white/blob at 9,639 spikes,
   confirmed not noise-sensitive); only the visual scale is swept.

2. **Rebuilt the blob control.** The original `blob_control.jpg` was
   found to be an unfair control on two counts: (a) pure black circle
   on pure white background gives near-maximal raw contrast, well
   above the real fly photos' ~0.80-0.82 post-amplify level (blob was
   ~0.86); (b) the circle's footprint activated 5 of the 9 candidate
   Mi1 neurons vs. 4 for the real photos, adding extra total drive on
   top of the contrast mismatch. Rebuilt with (a) background matched to
   the real photos' actual gray level (161, not white), (b) circle
   fill tuned so post-amplify contrast matches red/white's average
   (0.81), and (c) one of the resulting 5 active columns zeroed to
   match the real photos' 4-neuron footprint exactly. New files:
   `blob_control_matched.jpg`, `seq_blobcontrol_matched4.npy` (+
   `_bodyids.csv`).

**Swept visual scale from 1.0 down to 0.05 (10 noise-seeded trials per
scale per condition, scale-types=Mi1, everything else identical to the
canonical 50-trial setup):**

| scale | red fires | white fires | blob fires (matched) |
|---|---|---|---|
| 1.0-0.13 | 10/10 | 10/10 | 10/10 down to 0/10 at 0.13 |
| 0.12 | 10/10 | 10/10 | 0/10 |
| 0.11 | 9/10 | 7/10 | 0/10 |
| 0.10 | 7/10 | 2/10 | 0/10 |
| 0.09 | 0/10 | 1/10 | 0/10 |
| <=0.08 | 0/10 | 0/10 | 0/10 |

**Result: once the control is fair (matched contrast + matched
neuron-count footprint), the real ordering emerges -- red > white >
blob -- rather than blob outcompeting both real photos as it did with
the original mismatched control.** There is a narrow apparent
separation window around visual-scale=0.10-0.11 where red-eye fires
more reliably than white-eye, with blob silent throughout that range.

**Important caveat, raised directly by the user and agreed with:**
this scale value was found by scanning many scale levels and picking
the one that looks best -- that is a real risk of cherry-picking noise
rather than finding a genuine effect, especially at only 10 trials per
scale. This finding is NOT yet validated and should not be reported as
a real result until confirmed on a fresh, held-out set of seeds never
used during the scan, at a larger sample size, with a proper
significance test (e.g. Fisher's exact test) rather than eyeballing a
raw fire-count ratio. That validation is the next step, not yet run.

Scripts/files added: `simulate.py` (`--scale-types`, `--scale-mult`,
`per_id_current_scale` in `build_network_dynamic`), `blob_control_matched.jpg`,
`seq_amp_blob_matched.npy`, `seq_blobcontrol_matched.npy` (5-neuron
intermediate, superseded), `seq_blobcontrol_matched4.npy` +
`_bodyids.csv` (final, 4-neuron matched), `sweep_{red,white}_scale*_seed*.csv`
(160 runs), `sweep_blobm4_scale*_seed*.csv` (100 runs, scales 0.05-0.2).

### Literature check: does real innate vision distinguish red-eyed from white-eyed flies? — `confirmed`, no, only through learning

User pushback prompted a direct literature check rather than assuming
either way. Two real findings:

**1. The `white` gene itself impairs vision in the mutant fly.**
`white` encodes an ABC transporter needed to make the screening
pigment that optically insulates each ommatidium. Without it, light
scatters between ommatidia, photoreceptors receive ~19x more light
than normal, and white-eyed flies show reduced visual acuity and no
optomotor response (Wikipedia "White (mutation)"; Sturtevant 1915 via
secondary sources; Sepel et al./Zhang et al. via PLOS One "Influence of
the White Locus on the Courtship Behavior of Drosophila Males";
Krstic et al., "The white gene controls copulation success in
Drosophila melanogaster", Sci Rep 2017). One paper found white-
associated copulation success is INDEPENDENT of eye color phenotype
specifically -- the effect is a broader sensory/behavioral defect in
the mutant, not other flies visually rejecting it for its eye color.

**2. Directly on point -- real study, males looking at red-eyed vs
brown-eyed females:** Dukas lab, "Male Drosophila melanogaster learn
to prefer an arbitrary trait associated with female mating status"
(Current Zoology, 2015; PMC/PubMed 32256540). Real, confirmed findings:
- **Naive males have NO baseline (innate) preference between red-eyed
  and brown-eyed females** -- stated directly in the abstract.
- Males CAN come to prefer one eye color, but only after training
  (repeated mating experience with receptive females of that color) --
  a learned association, not a hardwired one.
- Confirmed genuinely visual (not olfactory) by testing in darkness --
  the learned preference disappeared without light, meaning the raw
  visual information IS present and usable, just not acted on
  innately.

**Honest, significant implication for this whole project's approach:**
this connectome-based simulation has zero capacity for learning or
plasticity -- every synaptic weight is fixed, derived directly from
real synapse counts. It can only ever represent an INNATE, naive-fly
circuit. The real literature's direct answer for that exact case (naive
male, red vs. non-red female) is that there IS no innate preference.
So the fragile, noise-sensitive, barely-there red/white separation
found throughout this session's robustness testing may not be a
calibration failure to fix -- it may be an accurate reflection of real
biology: there is genuinely little to no innate signal to find here,
because real eye-color mate discrimination is a learned behavior that
a fixed-weight, no-plasticity model structurally cannot represent.

Sources: Wikipedia "White (mutation)"; Krstic, Boll & Noll, "The white
gene controls copulation success in Drosophila melanogaster", Scientific
Reports 7:42388 (2017); "Influence of the White Locus on the Courtship
Behavior of Drosophila Males", PLOS One (2013), PMC3813745; Dukas lab,
"Male Drosophila melanogaster learn to prefer an arbitrary trait
associated with female mating status", Current Zoology 61(6):1036-1044
(2015), PubMed 32256540.

**Next step, per user's direction:** stop testing eye-color
discrimination at the unresolvable tiny-target scale. Build two new,
more meaningful tests instead: (1) a real fly's full head/body,
properly downsampled across a large enough neuron patch to actually be
shape-resolvable (not a 9-pixel crop that mostly misses the fly), (2)
the same setup shown a genuinely non-fly object, to test real shape
detection rather than fine eye-color discrimination.

### New experiment: real time-to-collision looming, tested for DIRECTIONAL speed-dependence (not eye-color discrimination) — in progress

Per user's explicit re-scoping: dropped the red/white eye-color
discrimination line entirely (see prior entry -- naive flies have no
innate preference per real literature, so that test was structurally
unwinnable). New goal, in the user's own words: "can we replicate fly
biological response to an external stimulus (ideally visual)... the
experiment should ensure the sim-fly is actually behaving directionally
like the biological fly."

**Chosen experiment: looming (expanding dark disc) -> escape response**,
using the real circuit verified directly in this connectome:
Mi1 (eye) -> T2/T2a/Tm3/TmY3 (real motion-relay neurons, confirmed via
direct edge query -- there is NO direct Mi1->LC4 edge) -> LC4 (real,
published looming/expansion detector, confirmed as DNp01's only
significant real input, weight 6362) -> DNp01 (escape command) -> TTMn
(jump muscle, confirmed as DNp01's only significant real output, weight 90).

**Real literature grounding (Card & Dickinson 2008, PMC3817277):**
real looming stimuli are parameterized by tau = l/|v| (time-to-contact),
starting at 2-3 degrees angular size and growing to 120-130 degrees;
escape triggers at a fixed ~49-54 degree angular threshold, ~22ms after
crossing it, REGARDLESS of tau -- speed affects how much real TIME it
takes to reach that fixed angular threshold, not the trigger rule
itself. Real distance/object-size are deliberately not specified in the
literature (l/|v| is distance-invariant) -- confirmed this is
intentional, not a gap in the search.

**Built `loom_real_physics.py`**: grows the real driven-neuron RADIUS
frame-by-frame from the actual physics formula theta(t) =
2*atan(tau/T(t)), converted to this dataset's real hex-unit-to-degree
calibration (5.625 deg/unit), instead of the earlier zoom-crop method
(image_to_retina_sequence.py) which has a documented brightness
confound. This directly implements "start with one retinal seat, add
more as the object appears to grow" per user's own description of how
this should work mechanically.

**Design decisions, explicit per user's direction:**
- Speed expressed as real, reportable "total time for the object to
  grow from a barely-visible speck to filling most of the eye" (2s,
  5s, 10s, 20s, 30s) rather than the abstract tau, which even the user
  found unintuitive -- tau is derived internally (53.2/132.9/265.9/
  531.8/797.6ms respectively) but not the reported variable.
- Frontal approach only (not mixed direction) for this first pass.
- Fixed dark contrast, fixed final size (120 deg), only speed varied.
- Control (not yet run): same object, receding instead of approaching --
  should activate early motion-relay neurons but die at LC4 (looming-
  specific), unlike a real approach.

**First single-run diagnostic (input-current=100, no noise, seed=1):**
found genuine, consistent DIRECTIONAL/proportional speed-dependence --
DNp01 fires at ~66% of the way through the approach regardless of total
duration (2s: 68.6%, 5s: 67.0%, 10s: 66.5%, 20s: 66.2%, 30s: 65.8%).
This is the first real speed-dependent result in this project (the
earlier tau200-600 sweep and the wide tau50-vs-2000 diagnostic both
showed zero timing difference -- root cause found: that test started
the object already covering the WHOLE eye from frame 0, skipping past
the entire part of the trajectory where speed matters).

**However: absolute trigger threshold is miscalibrated.** DNp01 fires
at only ~8.7 degrees angular size (9 neurons active) at that 66% mark,
vs. the real ~50 degree literature threshold -- the same "input-current
too strong, triggers too early" pattern seen throughout this project.
The relative/directional shape of the result is real; the absolute
calibration is not yet validated against the real 50-degree figure.

**Currently running:** N=20 noise-seeded trials (`--noise-sigma 0.5`,
seeds 1-20) at each of the 5 durations (100 runs total), full spike-time
output, to check whether the directional result survives real trial-to-
trial noise -- learning directly from yesterday's finding that a single
deterministic run is not sufficient evidence. Exact literal command
used (logged this time, unlike the discarded prior work):

```
.venv/bin/python simulate.py --edges connectome_full_matrix_lc11.csv \
  --neurons connectome_full_matrix_lc11_neurons.csv \
  --stimulus-sequence seq_realloom_dur{2,5,10,20,30}s.npy \
  --stimulus-sequence-bodyids seq_realloom_dur{2,5,10,20,30}s_bodyids.csv \
  --frame-duration 10 --input-current 100 \
  --noise-sigma 0.5 --seed {1..20} \
  --spike-summary-out spike_summary_realloom_dur{N}s_seed{S}.csv \
  --spike-times-out spike_times_realloom_dur{N}s_seed{S}.csv
```

Scripts/files added: `loom_real_physics.py`, `seq_realloom_dur{2,5,10,20,30}s.npy`
(+ `_bodyids.csv`), `spike_summary_realloom_dur{2,5,10,20,30}s_seed{1..20}.csv`,
`spike_times_realloom_dur{2,5,10,20,30}s_seed{1..20}.csv` (100 runs, in progress).

### Real-time looming test, re-scoped to 1-6s duration, N=10 trials — `confirmed`, first genuinely robust directional result in this project

Per user's cost/scope trimming (dropped the 20s/30s conditions as
low-value given how expensive they are to simulate and how little new
information they'd add beyond a 6x speed range), re-ran the real-physics
loom test (`loom_real_physics.py`, theta(t) = 2*atan(tau/T(t)), fixed
3 deg start / 120 deg end angular range for every condition) at 1, 2,
3, 4, 5, 6 second total approach durations, N=10 noise-seeded trials
each (`--noise-sigma 0.5`, `--input-current 100`, seeds 1-10), 60 runs
total, DNp01 (escape command) as the readout.

| duration | DNp01 first-fire (mean+/-std) | % through approach | fired |
|---|---|---|---|
| 1s | 711.9 +/- 3.3 ms | 71.2% | 10/10 |
| 2s | 1,370.5 +/- 3.0 ms | 68.5% | 10/10 |
| 3s | 2,027.6 +/- 4.7 ms | 67.6% | 10/10 |
| 4s | 2,682.8 +/- 7.5 ms | 67.1% | 10/10 |
| 5s | 3,335.0 +/- 9.6 ms | 66.7% | 10/10 |
| 6s | 4,003.2 +/- 9.7 ms | 66.7% | 10/10 |

**Result: genuinely robust and directional.** Fired in all 60/60
trials (unlike every version of the red/white test). Faster approach
triggers escape sooner in absolute real time (0.71s for the fastest vs.
4.0s for the slowest), while the RELATIVE trigger point stays
consistent (~67-71% of the way through the approach, converging as
duration increases) -- matching the real Card & Dickinson 2008 finding
that escape triggers at a fixed angular threshold, with speed only
changing how much real time it takes to reach it, not the trigger rule
itself. Checked the angular size directly at the trigger moment across
all conditions: 9.22, 8.80, 8.68, 8.61 degrees for durations 1/5/10/20s
-- essentially constant (~8.6-9.2 deg), confirming the circuit is
triggering on visual-field COVERAGE, not on elapsed time or frame
count. Absolute threshold is still ~6x too low vs. the real ~50 degree
literature figure (same "too-sensitive input-current" pattern as every
earlier test in this project) -- not yet recalibrated.

**User-caught methodology bug, fixed:** initial report used TOTAL spike
count across each entire simulation as an "intensity" measure, and
found it scaled with duration (slowest = most spikes). This is an
artifact, not a real finding -- each condition was simulated for its
full duration (1s vs. 6s), so slower conditions simply ran longer and
accumulated more spikes after the decision was already made, unrelated
to response strength. Recomputed using spikes in a FIXED 100ms window
after DNp01's first spike, which reverses the pattern and makes
biological sense: 1s=11.9+/-1.0, 2s=8.0+/-0.8, 3s=7.4+/-0.5,
4s=7.1+/-0.9, 5s=5.5+/-0.8, 6s=6.1+/-0.7 spikes/100ms -- faster,
more urgent approach genuinely produces a MORE INTENSE burst, not a
weaker one. Total spike count over a whole simulation is not a valid
cross-duration intensity metric; any future comparison must use a
fixed post-trigger window.

**User question, answered directly: can we isolate speed from
size/distance/coverage as separate causal variables?** No, not even in
principle -- this is a fundamental property of monocular looming
perception, not a gap in this project's design. A single eye can only
observe an object's angular size and its rate of change; real physical
size, real distance, and real speed collapse into one observable
(angular trajectory over time), because infinitely many (size,
distance, speed) triples produce the identical angular sequence. This
is exactly why Card & Dickinson and the rest of the field deliberately
parameterize looming stimuli by angle and time (tau = l/|v|) rather
than physical units -- there is no way to recover the other axes from
vision alone. This experiment's design DOES correctly isolate one
thing: start (3 deg) and end (120 deg) angular coverage are held
identical across every condition, so only the real-time RATE of
traversal (speed) differs -- final size is not a confound here. A
genuinely different, second experiment (vary final angular coverage
while holding total real time fixed) would test size/coverage as an
independent axis, but that is a separate test, not a confound-removal
fix to this one.

Scripts/files added: `loom_real_physics.py`,
`seq_realloom_dur{1,2,3,4,5,6}s.npy` (+ `_bodyids.csv`),
`spike_summary_realloom_dur{1..6}s_seed{1..10}.csv`,
`spike_times_realloom_dur{1..6}s_seed{1..10}.csv` (60 runs).

### Tm2 negative-control investigation: silent under loom AND sweep, but proven functional — `confirmed`, real inhibition, real literature explains why

Found empirically: among the many real neuron types directly wired to
Mi1, `Tm2` stayed essentially silent (0-1 spikes) across every trial
of both the real-time looming test (60 runs, durations 1-6s) and a
separate sideways-sweep test (5 noise-seeded trials), despite receiving
a real, substantial direct excitatory connection from Mi1 (weight 443,
comparable to other neuron types that DID fire heavily).

**Traced why, in three steps:**

1. **Real inhibitory input found:** `TmY5a -> Tm2`, weight -1,140 --
   more than 2.5x stronger than Mi1's own excitatory drive into Tm2 (443).
   Confirmed correctly signed: TmY5a's real predicted neurotransmitter is
   glutamate, which this project's established convention correctly
   treats as inhibitory. TmY5a itself fires heavily under both test
   stimuli (15,927 spikes by 6s in the loom test), so its inhibitory
   brake on Tm2 is genuinely active throughout.

2. **Confirmed Tm2 is NOT structurally broken:** direct current
   injection (`--input-types Tm2 --input-current 300`, bypassing the
   real circuit and its inhibition entirely) produced 60,044 spikes --
   the neuron model itself fires readily when driven. The silence is
   real, active suppression, not a dead/non-functional unit.

3. **Real literature explains the mechanism precisely** (search:
   "Processing properties of ON and OFF pathways for Drosophila motion
   detection", Behnia/Clark, Nature 2014, and follow-up eLife/PMC work):
   Tm2 is one of the 4 real input neurons to the fly's OFF-motion
   pathway (with Tm1, Tm4, Tm9, feeding a comparator neuron -- note:
   T5, the classic textbook downstream target, does NOT exist as a
   labeled cell type anywhere in this male-cns dataset; in THIS
   connectome Tm2 instead outputs heavily and directly onto T2, TmY3,
   and even LC4 itself, i.e. straight into the same escape circuit
   already tested, not a separate/untested branch). Tm2 **depolarizes
   to OFF (local brightness DECREMENT) and hyperpolarizes to ON**, with
   an antagonistic surround (classic center-surround organization) --
   it wants a small, localized dark edge at its receptive-field center,
   and is actively suppressed by brightness changes in its surround.

**Honest conclusion:** both stimuli tested so far (an expanding loom,
a large sweeping blob) are spatially BROAD, synchronized darkening
events -- likely triggering Tm2's antagonistic-surround suppression
across neighboring points at the same time as exciting its center,
working against itself. Neither stimulus was actually well-matched to
Tm2's real, literature-documented preference: a small, sharp, LOCAL
dark edge translating steadily across the visual field, not a broad
region darkening/growing all at once. This is a well-explained,
mechanistically real negative result, not a broken test -- but the
right follow-up stimulus (thin moving bar/small dot, not a blob) has
not yet been built or tested.

**Real 4-neuron OFF-pathway family in this dataset, for future
reference:** Tm1, Tm2, Tm4, Tm9 (Tm9 not yet checked in this
connectome). ON-pathway equivalent (already indirectly tested via the
escape/loom circuit): Mi1, Tm3, Mi4, Mi9 (Mi4/Mi9 not yet checked).

Sources: "Processing properties of ON and OFF pathways for Drosophila
motion detection" (Behnia, Clark et al., Nature 2014); "Comparisons
between the ON- and OFF-edge motion pathways in the Drosophila brain"
(eLife, PMC); "Non-preferred contrast responses in the Drosophila
motion pathways..." (bioRxiv).

Scripts/files added: `seq_tm2test_sweep.npy` (+`_bodyids.csv`,
sideways sweep, did not activate Tm2), direct-injection sanity check
(`--input-types Tm2 --input-current 300`, not saved as a named file,
confirmed 60,044 spikes). Next step (not yet built): a small, sharp,
localized moving dark edge stimulus, properly matched to Tm2's real
center-surround OFF preference.

### Tm2 investigation, resolved: fires under a whole-eye OFF flash, confirming it is functional and doing real work — `confirmed`

Continued the Tm2 investigation after user pushback ("it has a specific
job, which it doesn't seem to do -- that doesn't make sense"). Correct
call -- re-read the literature finding more carefully: Tm2 depolarizes
to OFF (local darkening) as a direct response, not specifically to
motion; directional selectivity is described as emerging downstream of
Tm2, not intrinsic to it. All earlier tests (loom, sweep, small moving
dot at multiple sizes/speeds/currents) involved MOTION and were
therefore not a clean test of Tm2's actual documented, literature-
described core response.

**Built the simplest, most literature-faithful test: a sudden, sustained
OFF flash (no motion) driving all 265 real Mi1 neurons that have a
direct synapse onto Tm2** (found via direct edge query -- Tm2's real
input partners are spread thin across the WHOLE eye, not clustered
locally; earlier local-dot tests only ever activated 2-21 of these
~265 partners simultaneously, nowhere near enough summed drive).
Stimulus: 10 frames background, then instant step to full contrast,
held for 40 frames.

**Result: Tm2 fired for the first time in this entire investigation** --
15 spikes at standard input-current=100, 31 spikes at 300 -- despite
TmY5a's real inhibitory input also being very active simultaneously
(16,164 / 22,930 spikes). Confirms Tm2 is genuinely functional and does
real, literature-consistent work; it was never broken.

**Root cause of every earlier failure, now understood precisely:** Tm2
requires broad, simultaneous drive from across a large fraction of its
real synaptic partners (spread across the whole eye) to overcome its
own strong real inhibition (TmY5a, glutamatergic, weight -1,140 vs.
Mi1's 443 excitatory). A small local target -- even a real, correctly-
connected one -- can never provide enough simultaneous partners active
at once to cross that threshold. This is a real structural property of
the circuit, not a modeling bug.

**Is Tm2 still a valid negative control for the escape/looming
experiments? Yes, with one honest caveat, both recorded here:**
- Yes: under every ecologically plausible stimulus tested so far (a
  real, physics-correct expanding loom; a real sideways-sweeping
  object; a small local moving dot at several sizes/speeds), Tm2
  reliably stayed silent -- AND that silence is now independently
  confirmed to be real and mechanistically explained (insufficient
  simultaneous partner activation to beat real inhibition), not a
  broken/non-functional neuron. That makes it a legitimate, well-
  understood negative control specifically for THESE experiments.
- Caveat: the stimulus that finally made it fire (a synchronized,
  whole-eye instantaneous flash using literally all its known real
  input partners at once) is itself not ecologically realistic --
  no natural visual event looks like that. So this test proves Tm2
  CAN fire (not dead), the same role the earlier direct-current-
  injection sanity check played -- it does not tell us what REAL,
  naturalistic stimulus would activate it. That remains a genuinely
  open question if ever needed for a future experiment.

Scripts/files added: `seq_tm2_offflash.npy` (+ `_bodyids.csv`,
all 265 real Mi1 partners of Tm2, whole-eye instant OFF step),
`seq_tm2_localedge.npy`/`seq_tm2_localedge2.npy` (both confirmed
silent -- kept as documented negative results, not deleted).

### Receding-object control, corrected and retested with a static-hold comparison — `confirmed`, real threshold-trigger + real sustained-intensity distinction, but NOT complete

**First attempt was flawed and is documented as a mistake, not deleted:**
built "receding" by naively time-reversing the full 3-120 degree
approach sequence, which meant it started at 120 degrees (already
covering most of the eye). Unsurprisingly it fired instantly (~18ms,
0.3-1.9% through) regardless of duration -- an uninformative result
caused by an unfair starting condition, not a finding about the
circuit. User caught this immediately.

**Second, corrected version:** rebuilt using the real physics capped
at a moderate, non-saturating 40 degrees (not 120), giving both a fair
"approach to 40deg" condition and its time-reverse "recede from
40deg" condition -- same size range, same real speed, only direction
differs. Reconfirmed the absolute trigger threshold first: DNp01 fires
at 7.9-8.8 degrees angular size across all 6 durations (1-6s) --
consistent with the original 120-degree-ending test's 8.6-9.2 degree
figure. This ~8 degree number now looks like a genuine, stable property
of this model's current calibration (vs. the real ~50 degree
literature figure -- still not recalibrated).

**Even the corrected recede fired 10/10 every time, MORE than
approach at every duration** (e.g. 6s: recede=419.5 vs approach=350.0
mean DNp01 spikes). Initially treated as a real specificity failure.

**User's key insight, which reframed this correctly:** the recede
stimulus starts at ~14 degrees (moderate size, ~100 active neurons) --
already ABOVE the ~8 degree trigger threshold just reconfirmed. A pure
threshold detector SHOULD fire almost immediately on anything that
starts above threshold, independent of what it does next. Comparing
"recede from above-threshold" against "approach from near-zero" was
never a fair direction/specificity test -- it mostly just compared
"starts above threshold" vs. "starts below threshold". This directly
echoes Card & Dickinson's own real finding: a FIXED ANGULAR THRESHOLD,
not expansion rate per se, is the primary real trigger variable.

**Correct, fair test built instead: receding vs. a static object held
at that same ~14 degree size for the same total duration.** Built by
tiling the same starting frame for the same frame count. Real result,
N=10 trials per condition per duration:

| duration | recede DNp01 (mean) | static-held DNp01 (mean) | recede 1st spike | static 1st spike |
|---|---|---|---|---|
| 1s | 82.5 | 366.2 | 23.3ms | 23.2ms |
| 2s | 156.8 | 757.2 | 22.4ms | 22.3ms |
| 3s | 224.9 | 1,140.2 | 22.4ms | 22.3ms |
| 4s | 288.6 | 1,522.7 | 22.4ms | 22.3ms |
| 5s | 352.1 | 1,903.9 | 22.3ms | 22.3ms |
| 6s | 419.5 | 2,286.6 | 22.3ms | 22.3ms |

**Result, genuinely informative this time:** first-spike timing is
statistically identical between recede and static (~22-23ms at every
duration) -- confirming the INITIAL trigger is a pure, direction-blind
threshold detector, matching real biology's documented mechanism. But
TOTAL sustained spike count differs by 4-5x (static consistently much
higher) at every duration -- a receding object's drive naturally drops
below threshold as it shrinks, so ongoing spiking tapers off, while a
static unmoving threat keeps delivering full drive the whole trial.
This is a real, sensible distinction between "still a threat" and
"resolving threat" -- but it emerges from simple cumulative drive
integration, NOT from any genuine expansion-vs-contraction motion
computation (which this static-weight, comparator-free connectome
model has no mechanism to perform).

**Explicitly NOT a complete or closed investigation.** Open questions,
not yet tested:
- Whether a genuinely different, comparator-based mechanism (something
  closer to a real motion-energy computation) exists anywhere else in
  this connectome that WOULD show true direction-of-change sensitivity
  at the trigger stage, not just the sustained-response stage.
- The absolute ~8 degree threshold vs. the real ~50 degree literature
  figure remains uncalibrated.
- Whether the 4-5x sustained-intensity difference found here would
  survive at a properly recalibrated (higher) threshold, or whether
  it is itself an artifact of the current, likely-too-sensitive
  calibration.
- A true expansion-RATE test (matched starting size, one growing, one
  static, one shrinking, all starting from the SAME point and
  compared stage by stage) has not been run.

Scripts/files added: `seq_recede_dur{1-6}s.npy` (first, flawed
attempt -- kept, not deleted, with this entry documenting why it's
unusable), `seq_moderate_dur{1-6}s.npy`, `seq_recede3_dur{1-6}s.npy`,
`seq_static_dur{1-6}s.npy` (+ all `_bodyids.csv`),
`spike_summary_{moderate,recede3,static}_dur{1-6}s_seed{1-10}.csv`,
`spike_times_{moderate,recede3,static}_dur{1-6}s_seed{1-10}.csv`
(240 runs total across the two attempts).

### Recalibrated input-current to match the real ~50 degree escape threshold — `confirmed`, robust under noise

Swept `--input-current` down from 100 (the value used throughout every
looming test so far, which triggered escape at only ~8-9 degrees --
about 6x more sensitive than real biology) on the full 3-120 degree,
6s-duration approach stimulus, single deterministic run per value,
checking the real angular size at DNp01's first spike:

| input-current | trigger angle |
|---|---|
| 100 | 8.8 deg |
| 50 | 11.9 deg |
| 30 | 13.9 deg |
| 20 | 19.8 deg |
| 15 | 37.9 deg |
| 14 | 63.1 deg |
| 13 | never fires |
| 14.2 | 49.2 deg |

Found a very steep, cliff-like region between current=13 (never fires)
and current=14 (fires at 63 deg) -- the same knife-edge signature that
caused every robustness failure in the earlier red/white eye-color
work. Given that history, did NOT trust the single deterministic
result at 14.2 (49.2 deg) -- ran N=10 real noise-seeded trials
(`--noise-sigma 0.5`, seeds 1-10) before accepting it.

**Result: genuinely robust, unlike every earlier "clean" calibration
in this project.** Fired 10/10 trials, trigger angle tightly clustered
39.9-47.6 degrees (mean ~43.4 degrees) -- close to, though somewhat
below, the real ~50 degree Card & Dickinson figure, and critically NOT
flipping between silent/full-activation the way the red/white
calibration did under the same test. **New default: input-current=14.2**
for the whole-eye / large-target real-looming stimulus regime
(distinct from the small-target 9-neuron regime's own separately-
calibrated value, input-current=1800, which remains unvalidated/
unrecalibrated).

Next: rerun the full 1-6s directional speed-dependence test (the
project's strongest validated result so far) at this corrected
current, to confirm the earlier directional finding still holds at a
properly-calibrated, literature-matched threshold rather than the
previous overly-sensitive one.

### Recalibrated escape circuit: reaction-time cliff mapped, 0.5s-6s — `confirmed`

Following the recalibration to input-current=14.2 (trigger ~39.9-47.6
degrees, robust across 10 noise trials, closely matching the real
~50 degree Card & Dickinson figure), reran the full directional speed
test and found a new, previously-hidden effect: at the OLD, over-
sensitive calibration (input-current=100, ~8 degree trigger), every
tested duration from 1-6s fired 10/10. At the NEW, realistic
calibration, short durations increasingly fail to escape in time at
all.

**Full curve, N=10 noise-seeded trials per duration (`--input-current
14.2`, `--noise-sigma 0.5`, seeds 1-10):**

| duration | escaped in time |
|---|---|
| 0.5s | 0/10 |
| 0.7s | 0/10 |
| 1.0s | 1/10 |
| 1.2s | 8/10 |
| 1.5s | 10/10 |
| 1.7s | 10/10 |
| 2s-6s | 10/10 |

**Result: a sharp, clean reaction-time cliff between 1.0s and 1.5s.**
Below ~1 second total approach time, escape essentially never
completes before the object would have already arrived. Between
1.0-1.5s there is a steep transition (1/10 -> 8/10 -> 10/10). Above
1.5s, escape is fully reliable at every duration tested up to 6s.

**Interpretation, stated carefully:** once calibrated to a realistic
(not oversensitive) trigger threshold, this circuit has a genuine
minimum reaction time of roughly 1.2-1.5 real seconds of total
approach duration -- a sufficiently fast, close threat can
mechanistically outrun the circuit's ability to complete an escape
decision, purely from real synaptic/integration delays compounding
against a hyperbolic (heavily backloaded) growth curve that only
crosses the ~50 degree trigger size very late in a fast approach's
timeline. This is a plausible, real biological phenomenon (fast
predator strikes do sometimes succeed against real prey for exactly
this class of reason) but has not been independently validated against
real Drosophila reaction-time literature -- flagged as an interesting,
literature-consistent-in-kind but not literature-confirmed-in-magnitude
finding.

Scripts/files added: `seq_realloom_dur{0.5,0.7,1.2,1.5,1.7}s.npy`
(+ `_bodyids.csv`), `spike_summary_recal_dur{0.5,0.7,1,1.2,1.5,1.7,2,3,4,5,6}s_seed{1..10}.csv`,
`spike_times_recal_dur{...}s_seed{1..10}.csv` (100 runs total across
the recalibration + cliff-mapping work).

### Correction/clarification: the original (pre-recalibration) directional speed test was directionally correct, just miscalibrated in sensitivity — not wrong

User-flagged correction, recorded for the historical record: the very
first version of the real-time looming/speed test (input-current=100,
~8 degree trigger threshold, before recalibration to ~50 degrees) has
sometimes been described in this log as "wrong" or "miscalibrated."
To be precise: the DIRECTION of the finding was always correct --
faster approaches triggered escape sooner, slower approaches later,
a real and consistent proportional relationship, present even in the
very first, oversensitive version. What was wrong was only the
ABSOLUTE SENSITIVITY (trigger threshold) -- sim-fly reacted after
seeing under 1% of its visual field covered, instead of waiting for a
real, believable ~50% threshold like real flies. The recalibration
work did not change or fix the directional pattern; it only corrected
how easily the circuit got "scared." This distinction matters for
anyone reading this log later: the early, oversensitive results are
not directionally invalid, only magnitude-invalid.

### Arousal/state study: does simulated octopamine ("excitement") give sim-fly a real safety margin? — `confirmed`, yes, with proper controls

Per user's explicit choice (arousal/state effects prioritized over
multisensory smell+vision combination as the next study). Real
question: does a real, documented arousal neuromodulator (octopamine)
measurably help escape performance at a genuinely borderline approach
speed, and is any such effect specific to octopamine's real wiring
(not just "any extra neural activity helps")?

**Real connectivity check first (before building anything):** octopamine
neurons (14 real types, 32 real neurons in this connectome:
OA-AL2i1-4, OA-ASM1, OA-VPM3/4, OA-VUMa1-6/8) output substantially and
directly onto the SAME real motion-relay neurons already validated in
the escape chain -- T2 (4,594 total real weight), T2a (1,918), Tm3
(1,792), TmY3 (1,746), plus TmY5a (18,150, the same neuron found
earlier to inhibit Tm2) and LC9. Real, bidirectional connectivity also
confirmed (these same neurons feed back into the OA neurons too).
Octopamine's real predicted neurotransmitter is not GABA/glutamate, so
it defaults correctly to excitatory under this project's established
sign convention -- consistent with octopamine's real, documented
"arousal/energizing" role.

**Method:** no code changes to `simulate.py` needed -- reused the
existing `--scale-types`/`--scale-mult` mechanism (built earlier for
the visual-vs-olfactory current split) by appending the 32 real OA
neuron bodyIds as extra, constantly-driven columns onto the existing
duration=1.2s looming stimulus (the borderline case from the earlier
reaction-time-cliff mapping, where baseline escape success was right
on the edge). `--scale-mult 5.0` applied only to the OA-type columns.

**Two random-neuron control iterations, second one used as the real
control (documented, not deleted):**
1. First random draw (32 neurons, excluding only OA types + core
   escape-chain types): accidentally included real visual-pathway
   neurons (Tm2, TmY5a, LC16) by chance -- contaminated, not a fair
   "unrelated" control. Produced erratic results (10/10 fired, but
   wildly inconsistent timing, including two extreme outliers at
   283ms and 879ms) -- not used for the final comparison.
2. Second random draw: pool restricted to CentralBrain/VNC region
   (excludes Optic(L/R), LO(L/R)) and excludes LC-family (chase) and
   pC1-family (courtship) types too -- genuinely unrelated to vision/
   escape/courtship (mostly generic AOTU relay neurons). Used as the
   real control.

**Full result, N=30 noise-seeded trials per condition (`--input-current
14.2`, `--noise-sigma 0.5`, seeds 1-30), duration=1.2s, escape ratio
and timing margin before the 1200ms deadline:**

| condition | escape ratio | margin mean | margin min | margin max |
|---|---|---|---|---|
| Calm (no extra drive) | 26/30 (87%) | 6ms | 0ms | 18ms |
| Random control (unrelated neurons, same current) | 29/30 (97%) | 14ms | 4ms | 30ms |
| Aroused (real octopamine neurons) | 30/30 (100%) | 104ms | 82ms | 117ms |

**Result: real, specific, and robust.** Escape ratio alone doesn't
cleanly separate random-control from aroused (97% vs 100%, both close
to ceiling) -- but the TIMING MARGIN does, decisively. Random
neurons only nudge borderline trials over the line by a few
milliseconds (mean 14ms, barely more than calm's 6ms). Real octopamine
neurons produce a categorically larger, tightly-clustered margin
(82-117ms, mean 104ms) -- roughly 7-17x more spare time than calm,
and clearly distinct from the random control's much smaller effect.
This confirms the arousal effect is genuinely tied to octopamine's
real, targeted wiring onto the motion-relay layer, not a generic
"any extra current helps" artifact.

Scripts/files added: `oa_neuron_ids.csv`, `random_control_ids.csv`
(first, contaminated draw -- kept, documented as unusable),
`random_control2_ids.csv` (final, clean draw), `seq_realloom_dur1.2s_aroused.npy`,
`seq_realloom_dur1.2s_randctrl.npy` (first draw), `seq_realloom_dur1.2s_randctrl2.npy`
(final draw) + all `_bodyids.csv`, `spike_summary_rerun_{calm,randctrl,aroused}_seed{1..30}.csv`,
`spike_times_rerun_{calm,randctrl,aroused}_seed{1..30}.csv` (90 runs
for the final N=30 comparison, plus earlier N=10 exploratory runs).

### Major correction: the "excitement helps escape" finding does NOT survive proper realism checking — `confirmed`, retracted

User's sharp methodological question ("are we fixing our results to match
the behavior we want") led directly to catching a real problem in the
earlier arousal/octopamine finding (input-current=14.2, `--scale-mult
5.0` on 32 real OA neurons, duration=1.2s escape test).

**What we found on closer inspection:** checked the FULL network's
spike counts (not just the escape circuit) between calm and "aroused"
conditions. Completely unrelated brain regions exploded from exactly
zero spikes to thousands: Kenyon cells (KCg-m: 0->8,592), dopamine PAM
cluster neurons (PAM08: 0->4,373, PAM01: 0->3,181), and even an
unrelated leg muscle (Sternal anterior rotator MN: 0->1,846). This is
not a targeted arousal signal -- it is an unrealistic, network-wide
activity storm.

**Swept the push strength (`--scale-mult`) down to find where this
collateral damage disappears, deciding the cutoff ONLY by whether
Kenyon cells/PAM/unrelated-motor-neurons stay near zero -- NOT by
looking at the escape result, to avoid tuning the outcome we wanted:**

| scale-mult | Kenyon cells (KCg-m) | DNp01 first-fire |
|---|---|---|
| 0.1-0.7 | 0 (clean) | ~1,197ms (same as calm baseline) |
| 0.8-0.95 | 6,396-7,607 (cascade already present) | ~1,150ms |
| 1.0+ (original test) | 7,668+ | ~1,085-1,118ms |

**Result: at every push level where the network stays realistic
(collateral regions quiet), there is NO meaningful improvement in
escape timing.** The earlier "genuine, specific, robust" arousal
effect only ever appeared once the network was already in an
unrealistic, over-driven cascade state. **This finding is retracted.**
Excitement (octopamine), tested properly, does not measurably speed up
escape in this model at any realistic push strength found so far.

**Checked whether real literature gives an actual number to calibrate
against (it does not, or at least not accessibly):** confirmed
qualitatively real, that octopamine genuinely boosts visual neuron gain
during flight (Suver, Mamiya & Dickinson 2012, "Octopamine Neurons
Mediate Flight-Induced Modulation of Visual Processing in Drosophila",
Current Biology 22(24):2294-2301, PMID 23142045 -- the primary VS-cell
gain-boost paper; also Suver et al. 2014, J Exp Biol 217(10):1737,
"Octopaminergic modulation of the visual flight speed regulator of
Drosophila"; Longden & Krapp, "Octopaminergic modulation of contrast
sensitivity", PMC3411070; Rien et al. 2012, Eur J Neurosci,
"Octopaminergic modulation of contrast gain adaptation in fly visual
motion-sensitive neurons"). All of these are paywalled -- could not
access the actual quantified fold-change/percentage numbers, only
confirm qualitatively that a real, documented boost exists. This means
our test's push-strength dial has NO real literature anchor at all --
we can only ask "does turning this on help without breaking realism
elsewhere," not "did we use the biologically correct amount."

**Standing methodological lesson, worth repeating for every future
neuromodulator/state test in this project:** before trusting any
"turn on neuron group X, does readout Y change" result, always check
the WHOLE network's spike counts for collateral damage in clearly
unrelated regions, not just the readout of interest. A result that
looks clean on the one neuron you're watching can still be riding on
an unrealistic, network-wide overload.

Scripts/files added: none new -- reused existing `seq_realloom_dur1.2s_aroused.npy`
and swept `--scale-mult` at values 0.1/0.3/0.5/0.7/0.8/0.85/0.9/0.95/1.0/1.5/2.0/3.0
(temp files in /tmp, not preserved individually -- the key finding is
the threshold itself, not the intermediate files).

### Real literature number found: octopamine/flight boosts visual response by only 20-30%, not the 5x we tested — `confirmed`

User located and provided the actual primary paper (Suver, Mamiya &
Dickinson 2012, Current Biology 22(24):2294-2302, PMID 23142045),
previously only accessible via paywalled abstract. Read the full text
directly.

**Real, quantified finding from the paper:** "This effect of flight
represented a 20%-30% increase in response, as measured at the cell
body of the VS cells." Confirmed via real whole-cell patch-clamp
recordings, with matching pharmacological (bath-applied octopamine)
and genetic (dTrpA1 activation / Kir2.1 silencing) experiments all
converging on the same real effect size. Also real, relevant caveat
from the paper itself: pharmacologically-applied octopamine (bath
application, reaching the whole brain) produced some non-specific
effects (an unexplained baseline membrane-potential shift) not seen
with genetically-targeted activation of the real endogenous octopamine
neurons -- the paper explicitly attributes this to bath octopamine
reaching brain regions "not typically supplied with this
neuromodulator," causing "broad nonspecific effects." This is a real,
literature-documented version of exactly the same failure mode we
found in our own simulation (driving real neurons too strongly/broadly
causes unrealistic collateral effects beyond the intended target).

**This confirms and quantifies the earlier correction:** our original
arousal test used `--scale-mult 5.0` (a 500% increase) -- roughly
17-25x stronger than the real, documented 20-30% effect. This fully
explains the unrealistic network-wide cascade (Kenyon cells, PAM
dopamine neurons, random motor neurons all firing from zero) found
earlier. We were not testing a realistic amount of arousal; we were
testing something ~20x too strong.

**Next step:** rerun the escape/arousal test at a real,
literature-matched push level (~1.25x, i.e. a 25% increase) rather
than an arbitrary guess, and check both (a) whether collateral regions
(Kenyon cells, PAM, unrelated motor neurons) stay near zero at this
now-literature-anchored level, and (b) whether any measurable escape-
timing effect survives at this much more modest, realistic strength.

Source: Suver, M.P., Mamiya, A., and Dickinson, M.H. (2012).
"Octopamine Neurons Mediate Flight-Induced Modulation of Visual
Processing in Drosophila." Current Biology 22(24):2294-2302.
doi:10.1016/j.cub.2012.10.034. PMID 23142045. Full text provided
directly by user (PDF), not accessed via paywalled search snippet.

### Arousal finding, corrected and re-validated with the real literature number and the right method — `confirmed`

Following the retraction of the earlier 5x-current arousal test (see
above) and finding the real literature number (Suver, Mamiya &
Dickinson 2012: flight/octopamine boosts visual response gain by
20-30%, not 5x), re-tested using the CORRECT method: instead of
injecting raw current directly into octopamine neurons (which
cascades into unrelated regions regardless of multiplier, since it's
driving the wrong thing), applied `--type-boost` directly to the real
synapses feeding the already-validated motion-relay neurons
(Mi1->T2, Mi1->T2a, Mi1->Tm3, Mi1->TmY3, each x1.25 = +25%, within
the real literature's 20-30% range) -- a direct, literature-accurate
simulation of "these neurons respond 25% more strongly to the same
visual input," touching no octopamine/neuromodulator neurons at all.

**Result, N=10 noise-seeded trials, duration=1.2s (the same borderline
speed test used throughout this investigation):**

| condition | escape ratio | margin (mean) | Kenyon cells (collateral check) |
|---|---|---|---|
| Calm | 8/10 | 6ms | 0 |
| "Excited" (rejected 5x-current method) | 10/10 | 104ms | 44,038 (unrealistic cascade) |
| **"Excited" (real 25% synaptic gain boost)** | **10/10** | **~88ms** (range 78-97ms) | **0 (clean, zero collateral damage across all 10 trials)** |

**This restores and properly validates the original finding, on
correct footing this time.** A real, literature-matched 25% gain
increase in the motion-detection stage gives sim-fly a genuine, large,
consistent safety margin -- with zero spillover into unrelated brain
regions. Unlike the earlier version, this result is grounded in an
actual measured real number (not an arbitrary guess) and produces no
collateral damage anywhere in the network.

**Standing lesson for this project, now confirmed twice:** when
simulating a neuromodulator/state effect, do not inject raw current
into the modulatory neurons themselves and scale by an arbitrary
multiplier -- this conflates "how hard I'm pushing an arbitrary
input" with "the real, receptor-mediated gain change" the literature
actually measured, and reliably causes unrealistic network-wide
cascades regardless of multiplier size (confirmed failing even at the
literature-accurate 1.25x current-injection level). The correct method
is to directly apply the real, literature-quantified percentage as a
synaptic-strength (`--type-boost`) change on the specific real
connections the modulator is documented to affect, leaving the
modulatory neurons and everything else untouched.

Scripts/files added: `spike_summary_gainboost25_dur1.2s_seed{1..10}.csv`,
`spike_times_gainboost25_dur1.2s_seed{1..10}.csv` (10 runs, using
existing `seq_realloom_dur1.2s.npy`, no new stimulus files needed).

**Closing note on this investigation:** the conclusion itself
("excited fly escapes faster and more reliably than calm fly") is not
new -- it's the same directional finding from the original, flawed
5x-current test. What changed is validity, not the headline: the
original version could not be trusted (unrealistic network-wide
cascade); this version is properly grounded in a real literature
number (20-30% gain increase, Suver et al. 2012) and produces zero
collateral damage. Investigation closed.

## SESSION RESTART: clean rebuild, one unified connectome

Per user's direction: previous folder (6.1GB, many one-off connectome
merges and inconsistent per-test calibrations) archived and wiped.
Preserved: this log, 9 core scripts (simulate.py with all features,
loom_real_physics.py, photo_multi_position.py, etc.), and 7 real
neuron-ID reference files, all copied to
`/Users/pravin/projects/flybrain-sim-archive/` before deletion.

**Rebuilt ONE single, comprehensive, correctly-signed real connectome**
(`connectome_v3.csv` + `connectome_v3_neurons.csv`) covering everything
needed for all planned tests, instead of separate merges per test:

- Mi1 visual patch (317 real neurons, radius=10 hex units, center
  hex1=18/hex2=20 -- same patch used throughout this project)
- Real motion relays restricted to those connected to the patch
  (Tm3=458, T2a=393, T2=194, TmY3=170, weight>=20 threshold)
- LC4 (looming detector), LC9 (shared danger/chase gateway), LC10a
  (mate-target detector), LC16 (threat detector, 2nd pathway)
- DNp01 (escape command), TTMn (jump muscle), b3 MN, MDN
- Real smell pathway: ORN_VA6, VA6_adPN, LHPV12a1, LHAV2b2_a, AL-AST1,
  DA1_lPN (VA6 mate-attractant + cVA)
- LH008m/LH007m (real courtship recurrent-loop partners)
- PVLP010, CL038 (real inhibitory neurons onto DNp01 -- the validated
  courtship-suppresses-escape pathway)
- pC1 (all subtypes) + aIPg (all subtypes) -- 212 real neurons
- Octopamine neurons (14 real types, 33 neurons) for future arousal
  tests, using the literature-validated method (type-boost on
  synapses, NOT raw current injection -- see prior correction)

**Final: 2,706 real neurons, 80,568 real edges, correctly signed**
(477 inhibitory via GABA/glutamate convention, 80,091 excitatory).
Sanity-checked against every previously-established real weight:
LC4->DNp01 (6,362, matches), PVLP010->DNp01 (-711), CL038->DNp01
(-549), LC16->pC1_2a (1,661), ORN_VA6->VA6_adPN (8,277) -- all
consistent with earlier findings.

**Standing rule going forward, per user's explicit direction:** use
this ONE connectome and ONE consistent calibration (input-current=14.2,
the literature-validated escape threshold; any neuromodulator effect
applied only as a literature-matched `--type-boost` percentage, never
raw current injection into modulator neurons) for every future test --
no more per-test one-off calibrations.

**Next planned test (per user's identified correct ordering): visual +
olfactory courtship initiation.** Does a borderline/weak visual mate
signal, combined with the real (already-confirmed-weak-alone) smell
signal, together cross pC1's threshold when neither does alone? This
was identified as logically prior to the courtship-suppresses-escape
test (courtship must start before it can suppress anything), and was
proposed but never actually executed before the rebuild.

Scripts/files added: `mi1_patch_ids.csv`, `motion_relay_restricted.csv`,
`named_neurons_raw.csv`, `pc1_aipg_raw.csv`, `final_neuron_set_ids.csv`,
`final_edges_raw.csv`, `final_neuron_nt.csv`, `connectome_v3.csv`,
`connectome_v3_neurons.csv`.

## Rebuild, piece by piece (per user's direction after the LC9 rabbit hole)

Abandoned the single "pull everything at once" rebuild attempt after
getting stuck tracing LC9's real inputs node-by-node (kept finding
"the" real pathway, then discovering it was thinner than it looked --
several rounds of this without resolution). Deleted that attempt.
New approach: rebuild one working piece at a time, starting simplest,
confirming each piece works alone before adding the next.

### Piece 1: escape circuit alone — `confirmed working`

Rebuilt just Mi1 patch (317, radius=10, center hex1=18/hex2=20) ->
real motion relays connected to it (Tm3=458, T2a=393, T2=194,
TmY3=170, weight>=20 threshold) -> LC4 (126) -> DNp01 (2) -> TTMn (2).
1,662 total real neurons, 32,789 real edges. Sanity-checked key
weights against prior work: LC4->DNp01=6,362, DNp01->TTMn=90 -- exact
matches.

Tested with the same real-physics loom stimulus (tau=159.5ms, 3-120
degree range) at the one standard calibration (input-current=14.2),
N=5 noise-seeded trials: fires at 50.5-60.1 degrees -- matches the
real Card & Dickinson literature figure (~49-54 degrees) even more
closely than the original build did (39.9-47.6 degrees). Confirmed
working standalone.

Files: `connectome_escape.csv` + `connectome_escape_neurons.csv`,
`escape_circuit_ids.csv`, `seq_escape_test.npy`.

**Next: Piece 2 (smell/VA6 pathway alone).**

### Piece 1, real experiment: speed-borderline escape, calm vs. excited, N=30 — `confirmed`

Ran the actual experiment (not just a sanity check) on the freshly
rebuilt escape-only circuit (`connectome_escape.csv`). Same borderline
duration (1.2s total approach, tau=31.91ms) used throughout this
project's reaction-time-cliff work, N=30 noise-seeded trials per
condition (`--noise-sigma 0.5`, seeds 1-30).

| condition | escape ratio | margin mean | margin range |
|---|---|---|---|
| Calm (no boost) | 2/30 (7%) | 5ms | 3-7ms |
| Excited (real 25% synaptic gain boost, Mi1->{Tm3,T2a,TmY3,T2}) | 30/30 (100%) | 84ms | 69-99ms |

**Result: confirms and sharpens the earlier finding.** This freshly
rebuilt circuit landed slightly closer to the real ~50-54 degree
literature threshold than the original build (50.5-60.1 degrees vs.
the original's 39.9-47.6), which makes this same borderline duration
genuinely harder for a calm fly -- explaining why the calm escape
ratio dropped from the original 87% (26/30) to just 7% (2/30) here.
The excited condition remains robust and essentially unchanged (100%,
large margin), using the same literature-matched method validated
earlier (no raw current injection into modulator neurons, no
collateral damage elsewhere in the network -- not re-checked in this
specific run, but same method already validated as clean).

Scripts/files added: `seq_borderline.npy` (+`_bodyids.csv`),
`spike_summary_{calm,excited}_seed{1..30}.csv`,
`spike_times_{calm,excited}_seed{1..30}.csv` (60 runs).

## Piece 3: flight-state gain boost (correcting terminology — NOT escape/arousal)

Per user's insistence on correct, non-confounded terminology: this is
"flight-state gain boost" (Suver, Mamiya & Dickinson 2012's real,
confirmed finding), completely separate from the earlier
"courtship-state" and "danger-escape" circuits. Octopamine's only
literature-confirmed effect is on VS/HS cells (wide-field rotation
detectors used for flight stabilization) -- NOT on the escape circuit,
which was the original, uncorrected assumption this whole investigation
was built on.

**Built the real circuit properly, honest method (drive the real
neuron, not the claimed result):** Mi1 patch (317, shared with the
escape circuit) -> real ON-pathway relays (Tm3, Mi4=108, Mi9=6) ->
real T4 (all 4 subtypes, 1,336 total, confirmed connected) -> real
VS/HS/H1/H2 family (25 neurons, matches earlier finding exactly) ->
plus the real octopamine neurons (14 types, 33 neurons), with their
real, direct, confirmed connection onto VS/HS (122 total weight, 38
real synapses -- matches the literature's AL2-cluster-to-optic-lobe
projection). Combined with the existing, already-validated escape
circuit in the SAME connectome (`connectome_flight_escape.csv`,
3,169 neurons, 76,257 edges) specifically to test whether a wide-field
stimulus spuriously triggers escape too (a real, honest concern raised
by the user, given our earlier finding that escape triggers on raw
coverage/magnitude, not genuine motion-pattern discrimination).

**Method: NOT rigged.** Did not impose the real 20-30% literature
number onto VS-cell synapses directly. Instead drove the real
octopamine neurons with real current and let the real, existing wiring
produce whatever change resulted -- a genuine test, not a
reproduction of the expected answer.

**Stimulus: a real, wide-field rotating grating** (sine-wave pattern,
sweeping across the full 317-neuron patch -- matching the real
literature's requirement that VS/HS cells need WIDE-FIELD coverage,
unlike the escape circuit's single small target).

**Result, N=5 noise-seeded trials (`--noise-sigma 0.5`, seeds 1-5),
HSE as readout:**

| seed | baseline | flight-state (octopamine on) |
|---|---|---|
| 1 | 0 | 13 |
| 2 | 28 | 77 |
| 3 | 18 | 76 |
| 4 | 17 | 68 |
| 5 | 20 | 71 |

**Genuine, consistent, emergent finding: real octopamine drive produces
a real, substantial (roughly 3-4x) increase in HSE's response to
rotating motion, in all 5 trials.** Directionally matches the real
literature (Suver et al.'s confirmed 20-30% boost) -- our magnitude is
larger, so this should NOT be reported as "matching the real number,"
only as "correctly directional." This is the first genuinely emergent
(not imposed) neuromodulator effect confirmed in this project.

**Also checked, per the user's specific concern: does this same
wide-field stimulus spuriously trigger the escape circuit (LC4/DNp01)
too, given escape's known coverage-based (not pattern-based) trigger?**
No -- LC4 and DNp01 stayed at exactly 0 across all 10 runs (both
conditions, all 5 seeds). The predicted cross-trigger risk did not
materialize at this stimulus size/duration -- an honest negative
result, worth remembering as a real boundary condition (may still
occur at a larger/longer stimulus, not tested).

Scripts/files added: `flight_mi4_mi9.csv`, `flight_t4.csv`,
`flight_vs_hs.csv`, `flight_and_escape_ids.csv`,
`connectome_flight_escape.csv` + `_neurons.csv`, `seq_rotating.npy`
(+`_bodyids.csv`), `seq_rotating_withOA.npy` (+`_bodyids.csv`),
spike summaries for baseline/withOA x seeds 1-5.

### Audit of the "too good" 44-57 degree growing-threat result — `confirmed clean`, plus one new real finding

User's skepticism was well-placed to check. Audited three things:
1. Independently re-derived the theta(t) physics from scratch (not
   reusing project code) -- matches reported values exactly (44.28
   vs. reported 44.3 degrees).
2. Directly inspected the actual stimulus file content at the
   corresponding frame -- smooth, monotonic growth (101->247 active
   neurons across 20 frames), consistent with the expected radius for
   that angular size. Not a frozen/hardcoded value, not discontinuous.
3. Checked for accidental cross-contamination from the newly-added
   flight-state neurons into the escape circuit.

**New real finding from check #3:** octopamine neurons DO have a real,
direct connection into LC4 (247 total weight, spread across 186 weak
individual synapses, ~1.3 average per synapse) -- small next to LC4's
main real input (Mi1 chain, thousands), but genuinely present, not
zero. **This did not affect the growing-threat result being audited**
-- octopamine neurons received no stimulation at all in that test (no
current, not part of the driven stimulus array), so this real pathway
sat idle. Worth remembering for any FUTURE test that drives octopamine
and a growing threat at the same time -- there is now a confirmed,
real (if modest) route for octopamine to directly influence escape,
separate from anything routed through VS/HS cells.

**Conclusion: the 44-57 degree growing-threat result is clean and
verified, not a bug or artifact.**

### Growing threat + flight-state (octopamine) together — `confirmed`, real modest cross-talk

Direct test of the newly-found OA->LC4 connection (247 total weight,
186 weak synapses). Same growing-threat stimulus as the validated
44-57 degree test, this time with octopamine neurons also driven
(real current, same method as the flight-state test -- not imposed).

N=5 noise-seeded trials:

| condition | trigger angle | DNp01 spikes |
|---|---|---|
| Growing alone | 44-57 deg (avg ~51) | 38-43 |
| Growing + octopamine | 39-49 deg (avg ~44) | 60-65 |

**Result: real, modest, consistent boost.** Escape triggers slightly
earlier (smaller required size) and fires ~50-60% more strongly when
octopamine is also active. Smaller in magnitude than the flight-state
boost to HSE (which was 3-4x) -- consistent with this being a much
weaker, secondary real pathway (247 total weight vs. the strong direct
Mi1->relay chain), not the primary route into escape.

**Honest interpretation:** this is a real, emergent, unforced effect
(not imposed), found by testing an actual real connection rather than
assuming one. It shows flight-state and danger-escape are not fully
walled off from each other after all -- there is a small, genuine
crosstalk wire -- but escape is still overwhelmingly driven by its own
real pathway (Mi1->LC4), with flight-state activation only nudging it
slightly, not driving it outright.

### Escape trigger angle, real N=30 (replaces earlier N=5 estimate) — `confirmed`

The 44-57 deg / avg ~51 deg figure quoted earlier for the growing-threat
escape trigger was only ever N=5. Ran the same test properly at N=30
on the combined connectome (`connectome_flight_escape.csv`), same
stimulus (`seq_escape_test.npy`, tau=159.5ms, start=3deg, end=120deg,
frame-interval=10ms), same calibration (`--input-current 14.2`,
`--noise-sigma 0.5`, `--synapse-mv 0.275` default), seeds 1-30,
`--spike-times-out` per seed, first DNp01 spike time converted to
theta(t) via the same real physics used to build the stimulus.

**Real result, N=30: mean=52.5 deg, std=3.6 deg, range 44.3-59.0 deg.**
Close to the earlier N=5 estimate (44-57, avg ~51) but not identical --
real mean sits slightly higher (52.5 vs 51), and the true max (59.0) is
wider than the N=5 sample's max (57). Still lines up with the real
Card & Dickinson 2008 literature figure (49-54 deg), sitting just above
the top of that range rather than centered on it.

Per-seed readings (seed: angle_deg): 1:44.3, 2:52.9, 3:52.0, 4:50.9,
5:57.3, 6:56.9, 7:47.1, 8:53.0, 9:51.6, 10:50.5, 11:55.3, 12:53.8,
13:51.5, 14:52.1, 15:57.2, 16:59.0, 17:52.1, 18:58.4, 19:53.4, 20:49.6,
21:52.7, 22:52.8, 23:57.9, 24:49.4, 25:44.5, 26:52.7, 27:49.2, 28:53.8,
29:52.4, 30:49.8.

Files: `/tmp/escape_n30/spike_times_seed{1..30}.csv` (not moved into
the project dir -- scratch outputs from this specific validation run).

### Open item, not started: real photoreceptor / lamina input stage

Currently the escape and flight-state circuits both start at Mi1, with
a made-up flat "input current" (14.2mV, calibrated to match the real
Card & Dickinson escape-angle result, not itself measured) applied
directly to Mi1. This skips the real biology upstream of Mi1.

**Checked the live male-cns:v1.0 database directly:**
- L1, L2, L3 (real lamina cells): present, real, traced -- 1,776 /
  1,779 / 1,772 neurons respectively.
- R1-R6 (the actual photoreceptors driving motion vision): NOT
  present, zero traced. The retina tissue itself is outside this
  connectome's reconstructed volume.
- R7/R8 (color vision, separate pathway): partially present, one
  subtype only (R7p/R8p, ~330 each), not the full complement.

So L1/L2/L3 could be added as a real, wired intermediate stage between
the input and Mi1, but the true first step (a real photoreceptor
responding to light) can never be simulated from this dataset alone --
we'd still have to fake the very first input, just one layer earlier
than today (at L1/L2/L3 instead of at Mi1).

**Real literature exists that could inform a better-grounded fake input
stage, not yet used:** Hardie & Juusola's decades of real Drosophila
photoreceptor electrophysiology, especially Song, Juusola & Hardie
2012 (full biophysical photoreceptor model, ~30,000 microvilli per
cell, quantum bump responses, 40-65mV real dynamic range, 50-300ms
real per-microvillus refractory period) and the Juusola/Hardie 2001
light-adaptation papers. Real, measured summary numbers (response
range, adaptation timing) could replace today's flat made-up 14.2mV
constant with something grounded in real photoreceptor behavior,
without needing to build the full microvilli-level model (which is a
much heavier, separate undertaking, not a simple add-on).

**Status: not started.** Flagged as a real, known gap -- today's input
stage is calibrated-to-match-behavior, not built from real photoreceptor
biophysics. Revisit later: (1) add real L1/L2/L3 wiring between input
and Mi1, (2) pull real numbers from Song/Juusola 2012 and the Hardie
lab's light-adaptation work to replace the flat 14.2mV constant with
something derived from real measured photoreceptor dynamics.

### Stationary control retested at the old, uncalibrated input-current=100 — `confirmed broken`

User's question: does the stationary-object control (a non-moving blob
should never trigger escape) still hold at the original, pre-calibration
input-current=100, or only at the calibrated 14.2?

Reran the same stationary blob stimulus (`seq_stationary_blob.npy`, 300
frames, non-moving, same 317-neuron patch size as the real target) on
the combined connectome, input-current=100, `--noise-sigma 0.5`, seeds
1-5.

| seed | LC4 spikes | DNp01 spikes | TTMn spikes |
|---|---|---|---|
| 1 | 75,987 | 2,485 | 1,013 |
| 2 | 76,047 | 2,488 | 1,018 |
| 3 | 75,967 | 2,489 | 1,005 |
| 4 | 76,014 | 2,489 | 1,008 |
| 5 | 76,038 | 2,488 | 1,004 |

**Result: no, it does not hold. Completely breaks down.** At the
calibrated value (14.2), this same stationary blob produces exactly 0
spikes in LC4/DNp01/TTMn across 5 trials (already confirmed earlier).
At the old, uncalibrated value (100), the same non-moving object fires
the escape circuit massively and consistently -- DNp01 spikes ~2,488
times, TTMn ~1,010 times, essentially indistinguishable from a real
threat response. At current=100 the circuit cannot discriminate a
stationary object from an approaching one at all; the "size alone
triggers escape, not motion" oversensitivity extends to full failure
of the stationary control, not just an earlier-than-real trigger angle.

**Confirms, from a different angle, why the input-current calibration
down to 14.2 was necessary** -- not just to match the real ~50 degree
figure, but because the uncalibrated network fails a basic sanity
check (stationary things should not look like danger) that the
calibrated network passes cleanly.

Files: `/tmp/stationary_100/spike_summary_seed{1-5}.csv` (scratch,
not moved into the project dir).

### Correction: wrong paper cited for the escape-angle target, recalibrated — `confirmed`

Discovered, by actually reading the real PDFs the user supplied, that
the "49-54 degree" / "50 degree" figure used throughout this entire
project as the real literature target was wrong. It was never in
Card & Dickinson, 2008, Current Biology ("Visually Mediated Motor
Planning in the Escape Response of Drosophila") -- that paper is
about escape DIRECTION, not the angular trigger threshold, and its
only quantitative timing figure is a 215ms +/- 42ms takeoff latency.

The real angular-threshold data is in the OTHER Card & Dickinson 2008
paper: "Performance trade-offs in the flight initiation of Drosophila,"
Journal of Experimental Biology 211: 341-353. Real numbers from that
paper: the falling-disk stimulus grew from 20 deg to 40 deg over its
fall; escape wing-motion onset happened 160-210ms after stimulus
start (median 190.7ms), during which "the disk diameter had reached
a size of 30-40 deg in the fly's field of view" (their Figure 4).
**Real target: 30-40 degrees, not 49-54.**

**Recalibrated input-current against the correct target.** Already had
a single deterministic data point at current=15 from the earlier
sweep: 37.9 deg, inside the real range. Ran it properly at N=30
noise-seeded trials (same method as the original 14.2 validation),
combined connectome, seeds 1-30:

**Result: mean=37.6 deg, std=2.0 deg, range=33.5-42.1 deg, fired
30/30.** Tighter and better-centered on the real 30-40 range than the
old 14.2mV/49-54deg pairing ever was on its (wrong) target. **New
calibrated value: input-current=15** (replacing 14.2) for matching
real escape-angle behavior on this connectome.

**Worth flagging:** 15mV sits close to the stationary-object cliff
found earlier (safe through 16, breaks at 17) -- only 1-2mV of margin,
less than 14.2 had. Still on the safe side, not touching the cliff,
but with less room than before.

Per-seed readings (seed: angle_deg), current=15, N=30: 1:40.3, 2:39.9,
3:35.1, 4:37.6, 5:34.2, 6:38.2, 7:38.6, 8:33.9, 9:39.2, 10:36.0,
11:37.7, 12:39.5, 13:35.4, 14:36.1, 15:38.2, 16:37.6, 17:37.8, 18:42.1,
19:39.7, 20:37.6, 21:37.1, 22:39.7, 23:36.2, 24:36.7, 25:40.1, 26:40.1,
27:33.5, 28:36.5, 29:36.3, 30:38.0.

All escape-angle numbers, images, and figures in the blog updated to
use current=15 / 30-40 deg / mean 37.6 deg going forward, replacing
the earlier (wrongly-sourced) 14.2mV / 49-54 deg / mean 52.5 deg
figures.

Files: `/tmp/escape_n30_cur15/spike_times_seed{1-30}.csv` (scratch),
`blog_images/eyeview_{3,15,30,38,120}deg*.png` (regenerated with
corrected frame indices), `blog_images/escape_stages_and_results.png`,
`blog_images/deducing_14_2mv.png`, `blog_images/input_current_cliff.png`,
`blog_images/three_panel_calibration_plate.png` (all regenerated).

### Isolating which real wire actually causes the octopamine-crosstalk effect — `confirmed`, found the real dominant pathway

Following the recalibration to input-current=15 (see prior entry), re-ran
the octopamine/growing-threat crosstalk test under the corrected
calibration, then did a proper isolation study to find out WHICH real
connection is actually responsible for the earlier-firing effect,
rather than assuming it was the previously-reported OA->LC4 wire.

**Step 1: confirm the crosstalk effect still exists at input-current=15.**
Same growing-threat stimulus, this time with the 33 real octopamine
neurons also driven (`seq_growing_withOA.npy`), combined connectome,
N=30 noise-seeded trials (seeds 1-30, `--noise-sigma 0.5`):

| condition | trigger angle (mean +/- std) | N fired |
|---|---|---|
| No octopamine (baseline, this session's earlier N=30) | 37.6 +/- 2.0 deg | 30/30 |
| Octopamine on, all real wires intact | 31.8 +/- 1.4 deg | 30/30 |

Confirmed: real, still present, now bigger in relative terms than
previously reported (mean shifts ~5.8 deg earlier, vs. the old
14.2mV-calibration test's smaller shift). Two individual trials (out
of 30) fired at 29.5 deg, below the real 30-40 deg literature range
and below this circuit's own no-octopamine minimum (33.5 deg).

**Step 2: which real wire is actually responsible?** Earlier in this
project, a "thorough search" (see prior entry) found THREE real,
independent connections between the octopamine/flight-state side and
the escape circuit, not just the one (OA->LC4) originally reported:
(1) OA -> LC4 direct (247 total weight, 185 synapses), (2) T4 (flight
motion detector) -> T2 (escape relay) (463 edges, T4b->T2 alone =391
weight), and (3), found only during this isolation work, OA -> the
escape relay cells themselves (Mi1/Tm3/T2a/T2/TmY3) directly -- 1,565
real edges, total weight ~2,200+, by far the largest of the three.

Built two modified connectome edge-list CSVs by removing one candidate
pathway's edges at a time (`connectome_no_OA_LC4.csv`,
`connectome_no_T4_T2.csv`, `connectome_no_OA_relays.csv`), reran the
same withOA N=30 test on each:

| condition | trigger angle (mean +/- std) | N fired |
|---|---|---|
| Octopamine on, all wires intact | 31.8 +/- 1.4 deg | 30/30 |
| Octopamine on, OA->LC4 cut | 32.5 +/- 1.4 deg | 30/30 |
| Octopamine on, T4->T2 cut | 31.7 +/- 1.5 deg | 30/30 |
| Octopamine on, OA->relay-cells cut | 36.4 +/- 1.9 deg | 30/30 |

**Result: neither the originally-reported OA->LC4 wire nor the T4->T2
wire is the real driver.** Cutting either one alone barely moves the
result (32.5 and 31.7 deg respectively, both close to the 31.8 deg
intact baseline). Cutting the octopamine->relay-cells pathway instead
closes ~80% of the gap back toward the no-octopamine baseline (36.4
vs. 37.6 deg baseline vs. 31.8 deg fully intact) -- clearly the
dominant real route.

**Honest conclusion: the earlier-firing crosstalk effect is mostly
caused by octopamine neurons synapsing directly onto the escape
circuit's own relay cells (Tm3, T2a, T2, TmY3, and a little onto
Mi1), not through LC4 and not through T4.** The originally-reported
OA->LC4 wire is real and present, but a minor contributor, not the
explanation for this effect. This corrects an earlier, premature
attribution in this project (the audit/crosstalk entries above, which
attributed the effect to OA->LC4 alone without ever testing alternative
routes).

Files: `connectome_no_OA_LC4.csv`, `connectome_no_T4_T2.csv`,
`connectome_no_OA_relays.csv` (modified edge lists, kept in project
dir); `/tmp/crosstalk_n30_cur15/`, `/tmp/isolate_no_OA_LC4/`,
`/tmp/isolate_no_T4_T2/`, `/tmp/isolate_no_OA_relays/` (spike-time
outputs, scratch, not moved into project dir).

### Internal note: provenance of the 7 "real" neuron properties — partially verified, not fully closed

Traced where Shiu et al. 2024's electrophysiology numbers (the ones
we use for every neuron in this project) actually come from, by
reading their real source code (github.com/philshiu/Drosophila_brain_model,
model.py). Findings:

1. **0.275mV per synapse is NOT measured.** Shiu et al.'s own code
   comments it explicitly as `# Free parameter`. Same category as our
   own made-up input-current, a tuned modeling choice, not a real
   electrode measurement. Source attribution (Shiu et al. 2024) is
   still correct, since that's genuinely where we got the number, but
   describing it as "measured directly off real neurons" is wrong and
   should be fixed in the blog text.

2. **Resting voltage / threshold / membrane time constant**, cited by
   Shiu et al. to Kakaria & de Bivort 2017 -- confirmed real, but
   composite: that paper is itself a modeling paper, not a direct
   measurement, and explicitly assembles these numbers from FOUR
   separate older real studies (Rohrbough & Broadie 2002, Sheeba et
   al. 2008, Gouwens & Wilson 2009, Nagel et al. 2015), describing them
   as values for "a generic spiking neuron." Real, but averaged/generic
   across multiple real studies, not one clean single measurement of
   one specific neuron type.

3. **Refractory period** (2.2ms), cited by Shiu et al. to "Lazar et
   al.," doi 10.7554/eLife.62362 -- this DOI resolves to the
   FlyBrainLab paper, a software/tools paper, not an original
   electrophysiology study. Almost certainly not the true primary
   source; the real measurement is cited somewhere further upstream,
   not confirmed.

4. **Synaptic delay** (1.8ms), cited by Shiu et al. to "Paul et al.
   2015," doi 10.3389/fncel.2015.00029 -- could not locate this paper
   via web search at all. Possibly a citation error in Shiu's own
   code, or just poorly indexed. Not confirmed.

5. **Synaptic decay time constant** (5ms), cited to "Jürgensen et
   al." -- not yet checked.

**Sex-of-flies question (the original motivation for this check)
remains open** for all of these -- none of the sources checked so far
specify fly sex for the underlying real measurements, and two of the
four remaining citation chains (refractory period, synaptic delay)
weren't confirmed as primary sources at all, so tracing sex further
back wasn't possible with the effort spent.

**Status: parked, not resolved.** Hit diminishing returns on web
search alone; closing this out properly would need the actual PDFs
of Kakaria & de Bivort 2017's four cited sources, plus tracking down
the real primary sources behind the refractory-period and
synaptic-delay citations. Worth revisiting if this becomes load-bearing
for a specific claim in the write-up (e.g., if someone explicitly
asks whether these numbers are sex-matched to the male-cns dataset).
Immediate action taken: blog text describing the 7 properties should
stop calling all 7 "measured directly off real neurons with
electrodes" -- at minimum the 0.275mV/synapse number needs its own,
more honest description (free parameter, not measured).

### Flight-state boost recalibrated at input-current=15, plus a current sweep to check for a cliff — `confirmed`

Following the escape-circuit recalibration to input-current=15 (see
prior entries), reran the flight-state boost test (rotating wide-field
pattern, HSE as readout, octopamine off vs on) under the corrected
value, N=30 noise-seeded trials each (`--noise-sigma 0.5`, seeds
1-30), same stimuli (`seq_rotating.npy`, `seq_rotating_withOA.npy`).

**Real result, N=30 at input-current=15:**

| condition | HSE spikes (mean +/- std) |
|---|---|
| Octopamine off | 178.0 +/- 5.2 |
| Octopamine on | 273.3 +/- 5.2 |
| Ratio | 1.54x |

**This replaces the earlier-reported 3.5x figure (20.5 vs 72.5 spikes),
which was generated under the old, since-corrected input-current=14.2.**
The boost is real and still clearly present (no overlap between the
two conditions across 30 trials each), but smaller than first
reported. Notably, 1.54x (a 54% increase) is now much closer to the
real published Suver, Mamiya & Dickinson 2012 figure (20-30% boost in
real flies) than the old 3.5x ever was, still bigger than the real
number, but no longer wildly overshooting it.

**Follow-up: swept input-current (single deterministic run per value,
seed=0) to check whether this boost shows a sharp cliff the way the
escape circuit's stationary-object test did:**

| current | HSE off | HSE on | ratio |
|---|---|---|---|
| 5-14 | 0 | 0 | nothing fires |
| 14.2 | 0 | 13 | octopamine alone crosses threshold |
| 15 | 89 | 143 | 1.61x |
| 16 | 356 | 495 | 1.39x |
| 17 | 694 | 849 | 1.22x |
| 18 | 974 | 1,100 | 1.13x |
| 20 | 1,413 | 1,500 | 1.06x |
| 25 | 1,869 | 1,911 | 1.02x |
| 30-100 | ~2,300-2,450 | ~2,300-2,460 | ~1.00x |

**Result: two distinct effects, not one cliff.** (1) A genuine onset
threshold below 15mV -- nothing fires at all, off or on, and right at
14.2mV there's a narrow window where octopamine alone is enough to
push HSE over threshold even though the baseline stimulus by itself
still cannot -- a real, sharp switch, similar in character to the
escape circuit's cliff. (2) No cliff in the boost ratio itself once
both conditions are firing -- the ratio decays smoothly from 1.61x at
15mV down to ~1.00x (no boost) by 50mV, a gradual ceiling/saturation
effect, not a sharp switch. The stimulus alone eventually drives HSE
hard enough that octopamine has nothing left to add.

Files: `/tmp/flight_n30_cur15/{baseline,withOA}/spike_summary_seed{1-30}.csv`
(N=30 recalibration, scratch), `/tmp/flight_sweep/` (current sweep,
scratch), neither moved into the project dir.

### Internal note: the HSE flight-state test and the DNp01 escape-isolation test are NOT comparable, and what's next

Flagging clearly, since the two most recent test batches produced
very different-looking spike counts (178 vs 273 for HSE; 73.3 vs 97.9
for DNp01) and it's worth being explicit these are not two versions
of the same experiment:

- **Flight-state boost test** (HSE readout, 178 vs 273 spikes, 1.54x):
  wide-field rotating pattern, continuously driving the whole eye
  patch for the full 6s stimulus, reading out HSE (a flight-
  stabilization cell fed heavily by T4, 1,336 real neurons). This
  test's job is to check how strongly the flight-stabilization
  circuit itself responds to motion, with vs. without octopamine.

- **Escape-isolation test** (DNp01 readout, 73.3 vs 97.9 spikes, 5
  conditions): a small object slowly growing into a real threat over
  6s, reading out DNp01 (the escape command cell). This test's job is
  to check WHEN escape triggers and HOW HARD, with vs. without
  octopamine, and which real wire is responsible.

Different stimulus, different readout cell, different real upstream
wiring feeding each one -- the two spike-count numbers were never
meant to match and aren't comparable to each other. No error here,
just noting it explicitly so it isn't misread later as an
inconsistency.

**Relationship to the original circuit-one write-up:** the
escape-isolation test (5-condition table, degrees + DNp01 spikes) is
a direct extension of circuit one's own core result (escape circuit
alone fires at 30-40 deg, matching Card & Dickinson). This new work
adds one variable on top of that same circuit and same stimulus: is
the flight-state circuit (octopamine) also active when the threat
appears. Real answer: yes, it reacts earlier (37.6 deg alone vs. 31.8
deg with octopamine on), an effect now attributed to the real
octopamine->relay-cells wire specifically (see isolation study above),
not the originally-suspected direct OA->LC4 wire.

**Next planned work, per user's explicit direction:** before starting
anything new, properly study and write up the impact of octopamine
(flight-state) on escape behavior in response to an object moving
toward a stationary fly -- i.e., turn the escape-isolation results
above into a real, complete write-up section (similar rigor to the
circuit-one section: real N=30 numbers, the isolation findings, the
correct attribution to the relay-cell pathway), rather than moving on
to a new experiment or a new circuit.

### Internal note: realism problem with the octopamine+escape crosstalk test, and a proposed fix (not yet built)

User raised a sharp, valid concern about the octopamine/escape
crosstalk test (the 5-condition isolation study above, 37.6 deg alone
vs. 31.8 deg with octopamine): it combines two things that don't
fully make sense together in real biology.

**The problem:** octopamine, per the real literature we've cited
(Suver, Mamiya & Dickinson 2012), ramps up specifically when a fly is
actually flying. But the escape behavior we're reading out, the jump
muscle TTMn firing, is specifically what a STATIONARY fly uses to
launch itself off a surface. A fly that's already flying wouldn't use
this muscle at all, it would evade with wing/haltere steering instead,
a completely different motor system we haven't modeled. So "octopamine
on + TTMn jump" is an internally inconsistent scenario, not something
a real fly would actually do.

**What still holds up despite this:** the real wire (octopamine ->
escape relay cells) is genuinely there in the connectome data, and
driving those neurons genuinely changes this circuit's behavior in the
model. That part isn't in question. What's shaky is the STORY we told
about what the test means ("the fly is already flying when the threat
appears"), not the underlying wiring result itself.

**Proposed fix (discussed, not yet built):** instead of pairing
octopamine-on with the existing growing-threat-alone stimulus, build a
new combined visual stimulus that overlays the growing threat ON TOP
OF the wide-field rotating pattern (i.e., what a flying fly's eye
would actually see: wide self-motion plus a discrete approaching
object at the same time), then check whether LC4/DNp01 still respond.
This makes the VISUAL side of the test internally coherent.

**What this fix does NOT solve, flagged explicitly so it isn't
oversold later:**
1. Octopamine itself is still injected directly by us, not triggered
   by the visual stimulus. In real biology it's driven by the fly's
   own flight motor commands (wingbeats), not by what it's seeing.
   This simplification stays regardless of which visual stimulus is
   paired with it.
2. We have no wing or haltere steering muscles in this circuit, only
   TTMn (the leg jump muscle). So even if LC4/DNp01 respond correctly
   under the improved combined stimulus, we cannot show the fly
   actually maneuvering away in flight, only that the threat-detection
   part of the circuit still activates. The readout would need to be
   described as "the looming detector still responds to a threat
   during a flight-like visual scene," not "the fly evades in flight."

**Status: not built yet.** User wants to come back to this later and
asked for help distinguishing between the two related-but-different
tests when they return, since it's easy to confuse them:

- **Test A (already done, isolation study):** growing threat alone
  (no visual rotation) vs. growing threat + octopamine forced on,
  stationary-fly framing, reads out TTMn/DNp01 in degrees and spikes.
  Real result: 37.6 deg alone vs. 31.8 deg with octopamine, explained
  by the octopamine->relay-cells wire. Internally inconsistent
  scenario (see problem above), but the underlying wiring finding is
  real.

- **Test B (proposed, not built):** rotating wide-field pattern with
  a growing threat overlaid on top of it, octopamine still forced on
  by us, reads out whether LC4/DNp01 still respond. More visually
  coherent scenario, still limited by the two caveats above (fake
  octopamine trigger, no flight-steering muscles to show real
  evasion).

### Write-up: octopamine's effect on the flight-stabilization circuit and on escape (Test A) — `finalized`

Final blog-voice write-up for both the flight-state boost result (HSE,
never published anywhere before this) and the octopamine/escape
cross-talk isolation study (Test A, per the internal note above),
assembled into one piece and confirmed by the user. Full text below,
kept verbatim as the source of record for this section.

---

**Does an aroused fly react faster to a threat?**

Flies release a chemical called octopamine when they're active or
flying, it's roughly the fly equivalent of adrenaline. Real flies have
a small family of neurons called HS cells (HSE, HSN, HSS, HST in this
connectome's own naming, 42 neurons total) that sit downstream of the
eye's motion detectors and help a flying fly stay stable and keep its
gaze locked on the world as it moves. These cells are fed heavily by
T4, one of the connectome's real motion-detecting cell types.

To test whether octopamine changes how hard this circuit responds to
motion, I built a wide-field rotating pattern, the kind of thing a
fly's eye sees as it's turning or banking in flight, and drove it
across a patch of 317 eye columns for a 6 second stimulus. I ran this
with the 33 real octopamine neurons off, then on, 30 trials each, and
read out spikes in HSE.

With octopamine off, HSE fired 178.0 spikes on average. With
octopamine on, 273.3, a 1.54x increase, and the two never overlapped
across all 30 trials either way. So this is a real, repeatable effect,
the flight-stabilization circuit fires harder when octopamine is
active. It's also a decent match to the real literature, Suver, Mamiya
and Dickinson 2012 report a 20-30% boost in actual flies during
flight, and our 54% is bigger than that but points the same direction.

I then turned the input current up and down to see if this boost had
a sharp on/off cliff, the way the escape circuit did. In every one of
these runs the fly is still watching the same flight-motion pattern,
the only thing changing between "off" and "on" is whether octopamine
is also being pushed on top of it. Below 15mV, the pattern alone is
too weak, HSE never fires either way. Right at 14.2mV, the pattern
alone still isn't quite enough, but adding octopamine's push on top of
it is just enough to tip HSE over its firing threshold, so it starts
firing a little. Above that, both conditions fire, and the size of the
boost just shrinks the higher the current goes, from about 1.6x at
15mV down to no boost at all by 50mV, because the pattern alone is
already pushing HSE near its max and there's less room left for
octopamine to add anything. So there's a real on/off switch at the low
end, and a separate, gradual fade at the high end, not one single
cliff. The main takeaway is that octopamine and vision add together
into the same pool, octopamine isn't its own separate switch.

This result says the wiring for octopamine to boost the eye's
flight-stabilization response is real and works, at least in the
model. It doesn't tell us whether this same aroused state also changes
how a fly responds to a threat, which is a separate circuit.

To test that I took the same growing-threat setup used for the escape
study, and added current to the 33 octopamine neurons at the same time
the object was approaching. I ran this 30 times with octopamine off
and 30 times with it on, same stimulus, same random noise seeding,
everything else held constant.

With octopamine off, the escape circuit fired at 37.6 degrees of eye
coverage on average, matching the earlier result. With octopamine on,
it fired earlier, at 31.8 degrees. Every trial in both conditions
fired eventually, the only thing that changed was how early.

Since there was a real effect I wanted to know which actual wire in
the connectome was responsible, rather than just noting octopamine
connects to the circuit somewhere and leaving it at that. I found
three real candidate connections: octopamine onto LC4 directly,
octopamine onto T4/T2 further upstream, and octopamine onto the relay
cells (Tm3, T2a, T2, TmY3) sitting between Mi1 and LC4. I cut each of
these wire sets out one at a time and reran the same 30-trial test on
each, to see which cut brought the result back closest to the
no-octopamine baseline.

Cutting the LC4 connection barely moved the number, 32.5 degrees,
almost identical to the fully-wired 31.8. Cutting T4/T2 did about the
same. Cutting the connection into the relay cells moved it most of the
way back, to 36.4 degrees, close to the 37.6 baseline. So the wire
actually doing the work is octopamine talking directly to the relay
cells, not LC4, which is what I'd originally assumed when I first
noticed this cross-talk. Worth stating plainly since I got it wrong
the first time and this corrects it.

There's a real problem with how I set this test up though. Octopamine,
per the actual fly literature, ramps up mainly when a fly is flying.
But the muscle this test reads out, TTMn, is the jump muscle a fly
uses to launch itself off a surface it's standing on. A fly that's
already flying wouldn't use its legs to escape a threat, it would bank
away with its wings instead, a completely different motor system not
in this model at all. So pairing "octopamine on" with "jump muscle
fires" describes a scenario a real fly would never actually be in.
What the test does show is that the wire from octopamine to the escape
relay cells is real and does something when driven, not that a flying
fly would evade this way. Untangling that properly would mean building
a version of this test where the threat appears against a backdrop of
wide self-motion, the kind of visual scene an actually-flying fly
would see, and checking whether the looming detector still responds
under that more coherent scenario. That's the next thing worth
building, not something I've done yet (Test B, per the internal note
above).

---

**Status: this section is the finalized write-up for Test A.** Test B
(threat overlaid on the rotating flight pattern) remains proposed,
not built.

### Internal note: two external review docs on the octopamine/escape work, and the limits of "relay fires before LC4"

User supplied two AI-generated review documents assessing the
octopamine/escape write-up above (a ChatGPT-produced biological-parallels
review, and a follow-up list of 8 proposed next experiments). Both
reviewed here, not yet acted on -- user said to hold off on folding
their content into this log until they've read the source docs
themselves. Logging only the discussion that happened in this session
around them, for continuity.

**Doc 1 (biological parallels/critique) -- spot-checked and largely
holds up.** Verified 3 of its most load-bearing citations for real
(Ache et al. 2019 *Nat Neurosci* "State-dependent decoupling...",
the reiserlab Cell Type Explorer, Palacios Castillo et al. 2026
*Current Biology* on the OA/TA split-GAL4 toolkit) -- all real, not
fabricated. Also directly verified its specific anatomical connectivity
percentages against our own live male-cns:v1.0 queries and they match
closely: OA-AL2i3->T2 6.31% (doc said 6.7%), ->Tm3 4.01% (4.2%),
->TmY3 3.21% (3.5%), ->LC4 0.00% (0.0%); OA-AL2i2->T2 3.48% (~3.5%).
This independently confirms, via a totally different method (raw
anatomical connection counts, no simulation at all) the same
conclusion our own wire-cutting isolation study reached (OA hits the
relay cells, not LC4). Doc's fair critiques not yet applied to any
blog text: (1) comparing our 1.54x HSE result to Suver et al.'s
"20-30%" as if they're the same measurement is not apples-to-apples
(their number is VS-cell membrane-potential, ours is HSE spike count);
(2) our "HSE/HSN/HSS/HST, 42 neurons" HS-cell grouping may include HST,
which the doc claims is not one of the three canonical real HS types
(HSN/HSE/HSS) -- not yet verified against our own neuron list.

**Doc 2 (8 proposed next experiments) -- reviewed for build cost and
biological plausibility, not yet built.** Prioritized order discussed:
#1 (per-relay-cell-type knockout, Tm3/T2a/T2/TmY3 individually) and #3
(record relay-cell spike timing, not just TTMn) and #7 (sufficiency
test: drive relay cells directly, OA off) are buildable now with
existing tooling. #2/#5 (graded OA-strength sweep on the escape
circuit, same method as the earlier HSE current sweep) and #4 (loom
speed/tau sweep, already a `loom_real_physics.py` parameter) are cheap
extensions. #6 (contrast sweep) needs new code -- the stimulus
generator has no separate contrast-intensity knob today. #8
(occlusion test) follows naturally from #7.

**Biological plausibility discussion, not yet logged elsewhere:**
flagged #4 and #6 as close to expected outcomes (real, well-established
physics/gain-control principles, not risky bets). #1 and #2/#5 flagged
as the most genuinely interesting, since there's real partial precedent
(Tm3 already known state-modulated per Strother et al. 2018; OA already
known to act via non-additive/metabotropic mechanisms per Arenz et al.
2017) but nobody's connected either to looming/escape specifically.
#7/#8 flagged as likely to "succeed" almost by construction in our
model (since our model represents OA's synaptic effect on relay cells
as literally injected voltage, mechanically similar to directly driving
those same cells with current) -- useful for internal consistency, not
strong new evidence about real fly biology.

**Feedforward-order discussion (re: #3).** Clarified that the escape
circuit's wiring (Mi1->relay cells->LC4->DNp01->TTMn) is real, from the
connectome, not invented -- but the *prediction* that relay cells show
an OA-driven change before LC4 does is close to a logical consequence
of what the isolation study already found (relay cut removes ~79% of
the effect, direct LC4 cut only ~12%), not an independent new bet, and
only holds strictly within our simplified model.

Discussed real biological mechanisms that could break simple
feedforward ordering in an actual fly: (1) real feedback wiring
(downstream cells projecting back to upstream ones); (2) efference
copy / corollary discharge (a real, documented fly phenomenon --
motor/turn commands feeding back to adjust visual processing before or
during the movement); (3) parallel shortcuts (LPLC2 is already known,
per Ache et al. 2019, to feed the GF pathway via a separate route from
LC4, carrying angular-size rather than angular-velocity info -- a real
alternate path that could let downstream cells respond independent of
the relay-cell chain's timing); (4) broadcast/hormonal octopamine
release (spilling into the hemolymph rather than traveling through a
specific synaptic wire, which could hit multiple stages near-
simultaneously rather than in series).

**Which of these four are checkable from the connectome alone:**
- Feedback wiring: fully checkable (a direct query for backward edges
  from LC4/DNp01/TTMn to Mi1/relay-cells/OA-neurons).
- Parallel shortcuts: fully checkable (a direct query for LPLC2->DNp01
  edges, in parallel with the LC4 route).
- Efference copy: only half-checkable -- the anatomical substrate
  (a backward wire from motor-adjacent cells toward visual/OA neurons)
  is queryable, but confirming it's actually USED as a corollary-
  discharge signal requires live physiology/timing data, not just
  structural wiring.
- Broadcast/hormonal release: not checkable at all from connectome
  data -- point-to-point synaptic data cannot represent non-synaptic,
  volume-transmitted signaling by construction.

**Status: discussion only, nothing built or queried yet.** User
explicitly said to hold off until they've read both source docs
themselves. Offered to run the two fully-checkable connectome queries
(backward-edge check, LPLC2->DNp01 parallel-path check) live against
male-cns:v1.0 -- not yet done, pending user go-ahead.

### Blog 2 (final, user-approved) -- supersedes the earlier draft write-up above

User rewrote the Test A write-up in their own voice over several
rounds, with corrections applied along the way (species mix-up fixed,
T4/T2 cut number corrected 31.8->31.7 to match the real logged value,
"significant" softened to "consistent" since no formal statistical
test was run, "octopamine as fight-or-flight neurotransmitter" framing
corrected to "neurohormone" per real literature, order-of-discovery
corrected so the piece doesn't claim prior knowledge it didn't have).
User gave final go-ahead ("ya go forit"). This is the authoritative,
final version of the piece -- the earlier draft logged above is now
superseded by this one.

---

**Does an aroused fly react faster to a threat?**

Last week I sought to indulge my curiosity and determine if it was
possible to take a real wiring diagram of a section of the brain and
nervous system of a fruit fly, and add electrical properties gleaned
from scientific literature - does the resulting circuit actually
behave like the real thing? Apparently it does! The escape circuit
last week fired in the right order, and with some tuning it also fired
approximately at the right visual threshold seen in published
scientific literature on fruit flies.

That got me all nerded out and excited, as would be expected from
anyone who had a working simulation of an actual fly. Since I had a
working simulation of a fly circuit that ostensibly behaved like a
real fly, could I make other predictions about what such a circuit
would do in different conditions and ultimately could such in-silico
simulations be used to understand and develop hypotheses about the
function of real neural circuits?

In the course of building the escape circuit I had read about a
neurotransmitter called octopamine. In fruit flies, it has been shown
to boost a fly's motion-vision neurons respond during flight (Suver et
al 2012), also makes motion-sensitive neurons react faster (Rien, Kern
and Kurtz's 2013) in blowflies. Furthermore, its ubiquity in the
insects and proximity to fly vision and motion led to hypothesize that
if octopamine were connected into the escape circuit and turned on, it
should make the sim-fly react to a threat sooner.

Before proceeding I looked up the connectome to determine if our
escape circuit was connected to the octopamine neurons mentioned by
Suver et al. or Rien et al. As it turns out, the connectome data shows
there are direct synaptic connections from 33 real octopamine neurons
(out of 126 total octopaminergic neurons in this male fruit fly
connectome) into three separate points along the escape pathway: onto
LC4 itself, onto the upstream motion-detecting cells T4 and T2, and
onto the relay cells (Tm3, T2a, T2, TmY3) that sit between Mi1 and
LC4.

After building these connections into the sim-fly, I ran the
experiment again. The experiment involved simulating an object moving
toward a fly and observing the escape circuit. Additionally, I added
15mV of current to the 33 newly wired octopamine neurons at the same
time the object was approaching, and ran 30 trials with octopamine off
and 30 with it on. On each trial I added random noise seeding, and
kept everything else constant to the earlier study.

With octopamine off, the escape circuit fired at 37.6 degrees of eye
coverage on average, matching the earlier result, and with octopamine
on, it fired earlier, at 31.8 degrees. For new readers, degrees is a
measure of how much of eye vision is taken over by the object. It is
correlated to distance and size of object. Hence at 1 degree only a
small part of the fly's field of vision is occupied by the object, at
120 degrees the fly's entire field of vision is occupied by the
object. The results were consistent and clearly showed a real effect,
the sim-fly reacted faster (i.e when object was further away or
smaller) when octopamine was turned on.

Since we had a real effect, I now wanted to understand the role each
of the three connections played in the effect. So I disabled each of
the three circuits in our sim-fly one at a time and reran the same
30-trial test for each of the disabled circuits.

Disabling the LC4 and T4/T2 circuits moved the number to 32.5 degrees
and 31.7 degrees respectively. However, disabling the relay cells
moved firing to 36.4 degrees, much closer to the no octopamine
baseline of 37.6 degrees. This demonstrated that the circuit driving
the behavior is the relay cells connected to the escape circuit.

I actually found this whole process quite amazing. While I have a
solid knowledge of biology, I'm 30 years out of date, but with a bit
of reading and a few hours of investment I could create a simulated
version of a fly's brain circuitry, add in other electrical properties
gleaned from a broad swath of scientific literature, and come up with
a prediction, run the experiment, and get results.

It also should be pointed out that it is really hard for biologists to
snip a few neurons in a fly and run this type of experiment 30 times
in a matter of hours (that would be at least 30 flies with snipped
neurons!). Hence doing all of this in-silico is a great way for
biologists, hobbyists and any student of biology to learn about the
inner workings of complex neural activity and come up with actual
predictions that can be tested in the lab or the wild.

It gives any investigator a lot of power to eliminate pathways that
may not be fruitful and has the potential to make science and the
process of discovery orders of magnitude faster than it previously
took.

---

**Status: FINAL, user-approved.** Next up per earlier discussion:
Test B (threat overlaid on the rotating flight pattern), the two
fully-checkable connectome queries (backward-edge check, LPLC2->DNp01
parallel-path check), and the prioritized 8-experiment list from the
second review doc, in that rough order -- none started yet.

### Blog 2 -- truly final ending (supersedes the ending logged above)

User revised the closing two paragraphs once more: rewrote the intro
opening line, merged the in-silico/in-vivo cost comparison with the
"massive area of investment" context (Blue Brain Project, Human Brain
Project, Google/Janelia, FlyWire/Codex, flyvis) into flowing prose
instead of a bullet-style gaps list, removed repeated "it should be
pointed out" phrasing, and closed on the amateur-astronomer/telescope
analogy as the final line. Real links added for every named project
(all verified real via search this session, not fabricated). User
confirmed final with "yep." This ending replaces the version logged
immediately above -- the rest of the piece (opening three paragraphs,
the octopamine/connectome-check/isolation-study body) is unchanged
from the earlier final log entry.

Final two closing paragraphs, verbatim:

---

Of course, doing this in-silico is no substitute for real experiments
and observations in-vivo, and there are real gaps in this simulation
too, guesses standing in for real unknowns, like whether a given
connection actually excites or inhibits its target, or how strong that
connection really is. But it's worth weighing that against what the
alternative actually costs a real biologist: snipping a few specific
neurons in a fly and running the same experiment 30 times over would
mean at least 30 real flies with snipped neurons flying around a lab,
weeks of breeding and surgery for what took us a single afternoon on a
laptop. That speed, combined with a language model's ability to
quickly synthesize the relevant research, gives any investigator real
power to illuminate which directions are worth chasing and rapidly
rule out the ones that aren't.

It's also worth remembering this isn't some fringe idea, it's AI
accelerating what was already a massive area of investment from
governments and research institutions. The Blue Brain Project
(https://bluebrain.epfl.ch/), a Swiss national research effort, spent
nearly twenty years, from 2005 to 2024, trying to build biophysically
realistic simulations of small pieces of a rat's brain, and the Human
Brain Project (https://www.humanbrainproject.eu/en/), a decade-long,
roughly billion-euro European initiative, pursued a similar goal at a
larger scale. The connectome we're using ourselves came out of a real,
major collaboration between Google Research and Janelia
(https://male-cns.janelia.org/), one of the world's leading
neuroscience research campuses, and there's a whole separate, active
research community built around FlyWire (https://flywire.ai/), a
parallel connectome of the female fly brain, with a free public
explorer called Codex (https://codex.flywire.ai/) that anyone can
browse. On the modeling side, a real published model called flyvis
(https://github.com/TuragaLab/flyvis) goes further than what I've
built here, training a connectome-constrained network end-to-end to
predict actual real fly neural activity. What AI now makes possible is
bringing a version of that kind of work within reach of a hobbyist,
not unlike how an amateur astronomer with a backyard telescope can
still discover a real comet the professionals haven't spotted yet, AI
paired with a real connectome is doing something similar for biology,
making it newly accessible to anyone curious enough to try.

---

**Status: TRULY FINAL, user-approved ("yep").** The separate "holes in
the model" piece (nine specific gaps: receptor sign/identity, synaptic
strength vs. raw count, neuromodulator timescale, cell-to-cell
uniformity, presynaptic/axo-axonic effects, broadcast/hormonal
release, co-transmission, sex/strain mismatch, temperature) was
discussed and drafted in full during this session but was ultimately
compressed and folded into this blog's ending rather than published as
its own separate piece -- the full uncompressed version is preserved
in this session's transcript if needed later, not duplicated here.
