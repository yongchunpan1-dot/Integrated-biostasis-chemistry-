# Benchmark Experiment Workflow (v1)

## Objective

Evaluate candidate anti-entropy formulations using a minimal but information-rich preservation benchmark.

The benchmark is intentionally simple:

- Biological structure preservation
- Protein functionality preservation
- Nucleic-acid preservation
- Assay accessibility after storage

The goal is not to maximize a single readout but to preserve integrated biological-state information.

---

## Stress Condition

Primary accelerated benchmark:

- Storage temperature: 37°C
- Duration: 3 days

Future expansion:

- 25°C (ambient)
- 4°C
- Freeze-thaw cycles

---

## Readout 1: Membrane / Structural Integrity

Suggested model systems:

- Extracellular vesicles
- Liposomes
- Cells

Suggested measurements:

- Flow cytometry viability staining
- Flow cytometry membrane integrity staining
- NTA particle recovery
- NTA size distribution

Output:

Structural Fidelity Score (SFS)

Range: 0–10

---

## Readout 2: Protein Functionality

Suggested model systems:

- HRP
- Catalase
- Other benchmark enzymes

Suggested measurements:

- Relative enzymatic activity

Output:

Protein Fidelity Score (PFS)

Range: 0–10

---

## Readout 3: Nucleic Acid Amplifiability

Suggested model systems:

- Purified DNA
- Purified RNA
- EV-associated nucleic acids

Suggested measurements:

- qPCR Ct shift
- PCR amplification success

Output:

Nucleic Acid Fidelity Score (NFS)

Range: 0–10

---

## Cleanup Assessment

A preservation formulation is only useful if downstream assays remain accessible.

Each formulation should therefore receive an Assay Accessibility Score (AAS).

Assessment criteria:

- Cleanup required? (Yes/No)
- Cleanup difficulty (Easy/Medium/Hard)
- Sample loss during cleanup
- Assay interference after cleanup

Output:

Assay Accessibility Score (AAS)

Range: 0–10

---

## Composite Scores

Temporal Fidelity Score (TFS)

TFS =
0.34 × Structural Fidelity Score +
0.33 × Protein Fidelity Score +
0.33 × Nucleic Acid Fidelity Score

Integrated Biostasis Score (IBS)

IBS = TFS × (AAS / 10)

IBS rewards formulations that both preserve biological states and remain compatible with downstream analysis.
