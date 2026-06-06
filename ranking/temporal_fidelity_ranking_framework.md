# Temporal Fidelity Ranking Framework (v0.1)

## Purpose

This ranking framework provides a prior (pre-experimental) estimate of formulation quality.

It is intended to prioritize formulations for experimental screening, not to predict final preservation performance.

---

## State Coverage Score

For each formulation:

Coverage Score = Mean(Membrane, Protein, Nucleic Acid)

where component scores are derived from the State Coverage Matrix.

---

## State Balance Score

Balanced preservation is preferred over highly skewed preservation.

Examples:

Good:

Membrane = 8
Protein = 8
NA = 8

Poor:

Membrane = 10
Protein = 10
NA = 0

Balance score is inversely related to variance among state layers.

---

## Mechanism Diversity Score

Reward formulations that combine complementary entropy-control mechanisms.

Structural Stabilization
Chemical Stabilization
Physical Encapsulation

Higher diversity increases robustness.

---

## Assay Risk Penalty

Apply penalties for known risks:

- PCR inhibition
- LC-MS interference
- enzyme inhibition
- excessive polymer carryover
- cleanup complexity

---

## Predicted TFI

Predicted_TFI =
0.45 × Coverage
+
0.30 × Balance
+
0.15 × Mechanism_Diversity
-
0.10 × Assay_Risk

---

## Experimental Update

After experimental measurements become available:

Membrane Score
Protein Score
Nucleic Acid Score

will replace prior estimates.

Real_TFI =
weighted combination of measured state preservation values.

The State Coverage Matrix should then be updated using experimental observations.

---

## Design Philosophy

Traditional preservation optimization:

Find the best stabilizer.

IBC optimization:

Find the chemical environment that most completely preserves biological-state information.
