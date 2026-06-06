# Integrated Biostasis Chemistry

**Integrated Biostasis Chemistry (IBC)** is a knowledge-guided framework for discovering chemical microenvironments that preserve biological-state information over time.

Rather than preserving a single molecule or assay signal, IBC focuses on maintaining **temporal fidelity** across three fundamental biological information layers:

1. Membrane state
2. Protein state
3. Nucleic-acid state

Together, these layers capture much of the structural, functional, and informational content contained within biological samples.

## Motivation

Biological samples begin to drift immediately after collection. Membranes reorganize, particles aggregate or rupture, proteins denature, enzymes lose activity, and nucleic acids fragment. These changes introduce hidden temporal bias into diagnostics, liquid biopsy, extracellular vesicle analysis, proteomics, molecular testing, and biobanking.

Most preservation methods optimize a single endpoint.

```text
Traditional preservation:
    Preserve a molecule or assay signal.

Integrated biostasis:
    Preserve biological-state information over time.
```

## Entropy-control perspective

The theoretical foundation of IBC is that biological-state degradation is driven by progressive increases in disorder, molecular mobility, chemical damage, and information loss.

Accordingly, IBC views preservation as an entropy-control problem.

The objective is not to eliminate entropy, but to slow the processes that drive biological-state drift.

```text
Entropy Control
        ↓
State Preservation
        ↓
Temporal Fidelity
```

## Three-layer state framework

```text
Membrane State
      ↓
Protein State
      ↓
Nucleic-Acid State
```

These correspond approximately to:

```text
Structure
      ↓
Function
      ↓
Information
```

### Membrane state

- membrane integrity
- particle integrity
- aggregation state
- membrane protein retention
- membrane permeability
- stability of extracellular vesicles, liposomes, viral envelopes, and cellular membranes

### Protein state

- protein recovery
- protein conformation
- enzymatic activity
- protein-complex stability
- functional binding capability

### Nucleic-acid state

- DNA integrity
- RNA integrity
- qPCR amplifiability
- sequencing compatibility
- nucleic-acid recovery

## Entropy-control mechanisms

IBC currently groups preservation strategies into three primary mechanism classes.

### 1. Structural Stabilization

Reduces molecular mobility and structural reorganization.

Examples:

- trehalose
- dextran
- PEG
- PVP
- glycerol
- cholesterol
- poloxamers

### 2. Chemical Stabilization

Suppresses chemical reactions that cause information loss.

Examples:

- Trolox
- glutathione
- catalase
- EDTA
- EGTA
- DTPA

### 3. Physical Encapsulation

Restricts accessibility and configurational freedom through physical confinement.

Examples:

- silica
- calcium phosphate
- hydrogels

## Biological State Vector

```text
S(t) = [
    membrane state,
    protein state,
    nucleic-acid state
]
```

The objective is to maximize similarity between the initial state and preserved state.

```text
Temporal Fidelity = similarity(S0, St)
```

## Framework

```text
Literature and database mining
      ↓
Material knowledgebase
      ↓
Entropy-control mechanism ontology
      ↓
State ontology
      ↓
Mechanism-to-state mapping
      ↓
Compatibility and assay-risk rules
      ↓
Temporal Fidelity scoring
      ↓
Formulation ranking
      ↓
Experimental validation
      ↓
Active learning
```

## Core architecture

```text
Material
      ↓
Entropy-Control Mechanism
      ↓
Membrane / Protein / Nucleic-Acid State
      ↓
Temporal Fidelity Index (TFI)
```

## Repository structure

```text
Integrated-biostasis-chemistry-
├── docs/
├── ontology/
├── descriptors/
├── knowledgebase/
├── interactions/
├── ranking/
├── workflows/
├── validation/
└── active_learning/
```

## Scoring layers

1. Evidence score
2. Mechanism score
3. State-coverage score
4. Compatibility score
5. Assay-risk score
6. Temporal Fidelity score

A high-ranking formulation should preserve all three state layers simultaneously rather than optimize a single endpoint.

## Example validation framework

### Membrane state
- particle recovery
- size distribution
- aggregation state
- membrane marker retention

### Protein state
- protein recovery
- HRP or model enzyme activity
- functional protein retention

### Nucleic-acid state
- DNA/RNA recovery
- qPCR amplifiability
- Ct-shift analysis

These measurements can be integrated into a composite **Temporal Fidelity Index (TFI)**.

## Current status

This repository is an early-stage scaffold intended to develop a state-centric and entropy-informed preservation framework.

## Working definitions

**Integrated biostasis** refers to preservation of biological-state information across membrane, protein, and nucleic-acid layers over time.

**Integrated Biostasis Chemistry** refers to rational design of chemical microenvironments that preserve this temporal fidelity.

**Temporal Fidelity** refers to similarity between the biological state at collection and the biological state after storage, transport, processing, or stress.

**Temporal Fidelity Index (TFI)** refers to a composite preservation score derived from membrane, protein, and nucleic-acid state measurements.