# Integrated Biostasis Chemistry

**Integrated Biostasis Chemistry (IBC)** is a knowledge-guided framework for discovering chemical environments that preserve biological states across multiple molecular and cellular hierarchies.

The central goal is not simply to preserve one biomolecule or one assay signal, but to maintain **temporal fidelity** across biological information layers, including extracellular vesicle membrane integrity, protein functionality, enzymatic activity, nucleic-acid amplifiability, and potentially cellular phenotypes.

## Concept

Biological samples continue to drift after collection. Membranes reorganize, vesicles aggregate or rupture, proteins denature, enzymes lose activity, nucleic acids fragment, and cellular phenotypes shift. These changes introduce hidden temporal bias into diagnostics, biobanking, liquid biopsy, extracellular vesicle analysis, and multi-omic workflows.

IBC treats preservation as a chemistry search problem:

```text
Literature mining
      ↓
Preservation material knowledgebase
      ↓
Descriptor ontology
      ↓
Compatibility and assay-risk rules
      ↓
Composite biostasis scoring
      ↓
Formulation ranking
      ↓
Experimental validation
      ↓
Active learning
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

## Core idea

IBC is designed to integrate evidence from formulation science, cryopreservation, lyophilization, vaccine stabilization, extracellular vesicle preservation, protein stabilization, nucleic acid preservation, biomaterials, mineral encapsulation, and regulatory/safety-associated excipient databases.

The platform prioritizes candidates using four major scoring layers:

1. **Evidence score** — literature and prior-use support.
2. **Mechanism score** — predicted ability to protect relevant biological-state layers.
3. **Compatibility score** — likelihood that components work together without functional conflict.
4. **Assay score** — likelihood that the formulation remains compatible with downstream assays such as PCR, LC-MS, flow cytometry, imaging, and EV analysis.

## Current status

This repository is an early-stage scaffold. Initial files define the ontology, descriptor schema, scoring logic, and seed database required to convert preservation literature into a searchable and rankable biostasis chemistry space.

## Working definition

**Integrated biostasis** refers to the preservation of biological-state information across multiple molecular and cellular hierarchies over time.

**Integrated Biostasis Chemistry** refers to the rational design of chemical microenvironments that preserve this temporal fidelity.
