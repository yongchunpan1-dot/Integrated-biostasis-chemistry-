# Integrated Biostasis Chemistry

**Integrated Biostasis Chemistry (IBC)** is a knowledge-guided framework for discovering chemical microenvironments that preserve biological-state information over time.

The goal is not simply to preserve a single biomolecule, cell type, vesicle population, or assay signal. IBC aims to preserve **temporal fidelity** across multiple biological information layers, including extracellular vesicle membrane integrity, particle stability, protein structure and activity, enzymatic function, nucleic-acid amplifiability, and potentially cellular phenotypes.

## Motivation

Biological samples begin to drift immediately after collection. Membranes reorganize, vesicles aggregate or rupture, proteins denature, enzymes lose activity, nucleic acids fragment, metabolites shift, and cellular phenotypes can change. These post-collection changes introduce hidden temporal bias into diagnostics, liquid biopsy, extracellular vesicle analysis, multi-omic profiling, biobanking, and translational sample handling.

Most preservation strategies are optimized for a single object or endpoint, such as cell viability, RNA recovery, protein stability, or cryosurvival. IBC reframes preservation as a **state-preservation problem**:

```text
Traditional preservation:
    Preserve a molecule, particle, cell, or assay readout.

Integrated biostasis:
    Preserve biological-state information across time.
```

## Core concept

IBC treats preservation as a chemistry search problem in biological-state space. A sample at a given time can be represented as a **biological state vector**:

```text
S(t) = [
    membrane integrity,
    vesicle recovery,
    aggregation state,
    protein abundance,
    protein activity,
    enzymatic activity,
    nucleic-acid amplifiability,
    cellular phenotype,
    assay compatibility
]
```

The central optimization target is **Temporal Fidelity**: the degree to which the preserved state remains similar to the initial or reference state after storage, transport, processing, or stress.

```text
Temporal Fidelity = similarity(S0, St)
```

Accordingly, IBC does not only ask whether a formulation preserves one endpoint. It asks whether a chemical environment can preserve an integrated biological state across multiple layers simultaneously.

## Framework

```text
Literature and database mining
      ↓
Preservation material knowledgebase
      ↓
Descriptor ontology
      ↓
State-layer ontology
      ↓
Mechanism-to-state mapping
      ↓
Compatibility and assay-risk rules
      ↓
Temporal Fidelity / biostasis scoring
      ↓
Formulation ranking
      ↓
Experimental validation
      ↓
Active learning and closed-loop refinement
```

## Repository structure

```text
Integrated-biostasis-chemistry-
├── docs/                 Concept, definitions, roadmap
├── ontology/             Material, mechanism, assay, and state ontologies
├── descriptors/          Descriptor schema and field dictionary
├── knowledgebase/        Seed material and evidence tables
├── interactions/         Compatibility, incompatibility, and assay-risk rules
├── ranking/              Composite scoring and formulation-ranking code
├── workflows/            Literature mining and formulation-generation workflows
├── validation/           Experimental validation design
└── active_learning/      Closed-loop optimization scaffold
```

## Scoring layers

IBC prioritizes candidate chemical environments using multiple linked scoring layers:

1. **Evidence score** — literature support, prior formulation use, regulatory familiarity, and experimental precedent.
2. **Mechanism score** — predicted ability to protect relevant biological-state layers, such as membrane stabilization, vitrification, osmoprotection, protein anti-aggregation, nuclease inhibition, antioxidant protection, or mineral encapsulation.
3. **State-coverage score** — the extent to which a formulation is expected to preserve multiple state layers rather than a single endpoint.
4. **Compatibility score** — likelihood that components work together without chemical, physical, or functional conflict.
5. **Assay-risk score** — likelihood that the formulation remains compatible with downstream assays such as PCR/qPCR, LC-MS, flow cytometry, imaging, EV analysis, enzymatic assays, and sequencing.
6. **Temporal Fidelity score** — experimental or predicted similarity between the initial biological state and the preserved state after defined stress or storage conditions.

## Example validation logic

A minimal experimental validation branch may evaluate three representative state layers:

```text
Extracellular vesicle / membrane state:
    particle recovery, size distribution, aggregation, membrane marker retention

Protein / enzyme state:
    protein recovery, HRP or model enzyme activity, denaturation-sensitive readouts

Nucleic-acid state:
    DNA/RNA recovery, qPCR amplifiability, inhibition risk
```

These readouts can be combined into a composite **Temporal Fidelity Index (TFI)** for formulation ranking and active learning.

## Current status

This repository is an early-stage scaffold. Initial files define the ontology, descriptor schema, compatibility logic, scoring structure, and seed database required to convert preservation literature into a searchable and rankable biostasis chemistry space.

The near-term development goal is to move from formulation ranking alone toward explicit modeling of:

```text
Material → mechanism → state layer → assay risk → temporal fidelity
```

## Working definitions

**Integrated biostasis** refers to the preservation of biological-state information across multiple molecular, vesicular, and cellular hierarchies over time.

**Integrated Biostasis Chemistry** refers to the rational design of chemical microenvironments that preserve this temporal fidelity.

**Temporal Fidelity** refers to the similarity between the biological state at collection or baseline and the biological state after storage, stress, transport, or processing.

**Temporal Fidelity Index (TFI)** refers to a composite experimental or computational score that summarizes preservation performance across multiple biological-state layers.