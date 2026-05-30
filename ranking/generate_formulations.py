"""Generate anti-entropy candidate formulations for Integrated Biostasis Chemistry.

This generator implements the central design logic of the project:
formulations should be assembled to cover complementary entropy-increase
pathways rather than by randomly mixing material classes.

Current strategy
----------------
1. Load the seed materials database.
2. Map each material to one or more entropy-control modules.
3. Enumerate 2- to 4-component candidate formulations.
4. Prefer formulations that cover multiple entropy pathways.
5. Penalize obvious assay risks and rule-based conflicts.
6. Output a ranked CSV of candidate anti-entropy programs.

The scores are expert-prior seed scores. They should be updated after
literature curation and experimental feedback.
"""

from __future__ import annotations

import argparse
import csv
import itertools
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple


Material = Dict[str, str]


ENTROPY_MAP: Dict[str, Set[str]] = {
    "trehalose": {"structural_entropy", "phase_entropy"},
    "sucrose": {"structural_entropy", "phase_entropy"},
    "ectoine": {"structural_entropy", "chemical_entropy"},
    "glycerol": {"structural_entropy", "phase_entropy"},
    "peg": {"diffusional_entropy", "phase_entropy"},
    "pvp": {"diffusional_entropy", "phase_entropy"},
    "dextran": {"diffusional_entropy", "structural_entropy"},
    "ficoll": {"diffusional_entropy"},
    "arginine": {"structural_entropy"},
    "proline": {"structural_entropy"},
    "catalase": {"chemical_entropy"},
    "glutathione": {"chemical_entropy"},
    "trolox": {"chemical_entropy"},
    "edta": {"enzymatic_entropy"},
    "egta": {"enzymatic_entropy"},
    "dtpa": {"enzymatic_entropy"},
    "silicic acid": {"confinement_entropy", "diffusional_entropy"},
    "calcium phosphate": {"confinement_entropy", "diffusional_entropy"},
    "alginate": {"diffusional_entropy", "confinement_entropy"},
    "agarose": {"diffusional_entropy", "confinement_entropy"},
    "zif-8": {"confinement_entropy", "diffusional_entropy"},
    "zinc acetate": {"confinement_entropy"},
    "2-methylimidazole": {"confinement_entropy"},
}


SYNERGY_BONUS: Dict[Tuple[str, str], float] = {
    tuple(sorted(("trehalose", "dextran"))): 2.0,
    tuple(sorted(("trehalose", "pvp"))): 1.5,
    tuple(sorted(("trehalose", "sucrose"))): 1.0,
    tuple(sorted(("sucrose", "dextran"))): 1.5,
    tuple(sorted(("glutathione", "trehalose"))): 1.0,
    tuple(sorted(("trehalose", "zif-8"))): 1.0,
    tuple(sorted(("silicic acid", "trehalose"))): 1.0,
    tuple(sorted(("calcium phosphate", "trehalose"))): 1.0,
}


CONFLICT_PENALTY: Dict[Tuple[str, str], float] = {
    tuple(sorted(("edta", "catalase"))): 3.0,
    tuple(sorted(("egta", "catalase"))): 2.0,
    tuple(sorted(("dtpa", "catalase"))): 2.0,
}


ASSAY_RISK_PENALTY = {
    "peg": 0.8,
    "zif-8": 1.0,
    "silicic acid": 0.8,
    "calcium phosphate": 0.5,
    "zinc acetate": 1.0,
    "2-methylimidazole": 1.0,
}


CORE_STATE_FIELDS = [
    "membrane_protection",
    "protein_protection",
    "nucleic_acid_protection",
    "oxidative_protection",
]


ASSAY_FIELDS = ["pcr_compatibility", "lcms_compatibility"]


def normalize_name(name: str) -> str:
    return name.strip().lower()


def read_materials(path: Path) -> List[Material]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_float(row: Material, field: str, default: float = 0.0) -> float:
    try:
        return float(row.get(field, default))
    except ValueError:
        return default


def material_entropy_modules(material: Material) -> Set[str]:
    return ENTROPY_MAP.get(normalize_name(material["material_name"]), set())


def pair_key(a: str, b: str) -> Tuple[str, str]:
    return tuple(sorted((normalize_name(a), normalize_name(b))))


def formulation_entropy_modules(formulation: Sequence[Material]) -> Set[str]:
    modules: Set[str] = set()
    for material in formulation:
        modules.update(material_entropy_modules(material))
    return modules


def average_state_score(formulation: Sequence[Material]) -> float:
    values = []
    for field in CORE_STATE_FIELDS:
        field_average = sum(as_float(m, field) for m in formulation) / len(formulation)
        values.append(field_average)
    return sum(values) / len(values)


def assay_score(formulation: Sequence[Material]) -> float:
    values = []
    for field in ASSAY_FIELDS:
        values.append(sum(as_float(m, field) for m in formulation) / len(formulation))
    return sum(values) / len(values)


def synergy_score(formulation: Sequence[Material]) -> float:
    score = 0.0
    for a, b in itertools.combinations(formulation, 2):
        score += SYNERGY_BONUS.get(pair_key(a["material_name"], b["material_name"]), 0.0)
    return score


def conflict_penalty(formulation: Sequence[Material]) -> float:
    penalty = 0.0
    for a, b in itertools.combinations(formulation, 2):
        penalty += CONFLICT_PENALTY.get(pair_key(a["material_name"], b["material_name"]), 0.0)
    return penalty


def assay_risk_penalty(formulation: Sequence[Material]) -> float:
    return sum(ASSAY_RISK_PENALTY.get(normalize_name(m["material_name"]), 0.0) for m in formulation)


def class_diversity_bonus(formulation: Sequence[Material]) -> float:
    classes = {m["class"] for m in formulation}
    return 0.3 * len(classes)


def anti_entropy_score(formulation: Sequence[Material]) -> Dict[str, object]:
    modules = formulation_entropy_modules(formulation)
    module_coverage = len(modules)
    state = average_state_score(formulation)
    assay = assay_score(formulation)
    synergy = synergy_score(formulation)
    conflict = conflict_penalty(formulation)
    assay_risk = assay_risk_penalty(formulation)
    diversity = class_diversity_bonus(formulation)

    total = (
        1.8 * module_coverage
        + 0.45 * state
        + 0.20 * assay
        + synergy
        + diversity
        - conflict
        - assay_risk
    )

    return {
        "score": round(total, 3),
        "entropy_modules": ";".join(sorted(modules)),
        "module_coverage": module_coverage,
        "state_score": round(state, 3),
        "assay_score": round(assay, 3),
        "synergy_bonus": round(synergy, 3),
        "conflict_penalty": round(conflict, 3),
        "assay_risk_penalty": round(assay_risk, 3),
        "class_diversity_bonus": round(diversity, 3),
    }


def valid_formulation(formulation: Sequence[Material]) -> bool:
    names = {normalize_name(m["material_name"]) for m in formulation}

    # Avoid precursor-only mineral/MOF suggestions as final preservation formulations.
    precursor_names = {"zinc acetate", "2-methylimidazole"}
    if names and names.issubset(precursor_names):
        return False

    # Require at least two entropy modules for meaningful anti-entropy design.
    if len(formulation_entropy_modules(formulation)) < 2:
        return False

    # Avoid formulations with very poor global PCR compatibility at this stage.
    if assay_score(formulation) < 4.5:
        return False

    return True


def generate_formulations(materials: List[Material], min_size: int, max_size: int) -> Iterable[Sequence[Material]]:
    for size in range(min_size, max_size + 1):
        yield from itertools.combinations(materials, size)


def write_ranked_formulations(rows: List[Dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "rank",
        "formulation_id",
        "components",
        "component_classes",
        "score",
        "entropy_modules",
        "module_coverage",
        "state_score",
        "assay_score",
        "synergy_bonus",
        "conflict_penalty",
        "assay_risk_penalty",
        "class_diversity_bonus",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate anti-entropy biostasis formulation candidates.")
    parser.add_argument("--materials", default="knowledgebase/materials.csv")
    parser.add_argument("--output", default="outputs/candidate_formulations.csv")
    parser.add_argument("--min-size", type=int, default=2)
    parser.add_argument("--max-size", type=int, default=4)
    parser.add_argument("--top", type=int, default=100)
    args = parser.parse_args()

    materials = read_materials(Path(args.materials))
    candidates: List[Dict[str, object]] = []

    for formulation in generate_formulations(materials, args.min_size, args.max_size):
        if not valid_formulation(formulation):
            continue
        score_info = anti_entropy_score(formulation)
        names = [m["material_name"] for m in formulation]
        classes = [m["class"] for m in formulation]
        candidates.append(
            {
                "components": " + ".join(names),
                "component_classes": ";".join(classes),
                **score_info,
            }
        )

    ranked = sorted(candidates, key=lambda row: row["score"], reverse=True)[: args.top]
    for idx, row in enumerate(ranked, start=1):
        row["rank"] = idx
        row["formulation_id"] = f"AEF{idx:04d}"

    write_ranked_formulations(ranked, Path(args.output))
    print(f"Wrote {len(ranked)} ranked formulations to {args.output}")


if __name__ == "__main__":
    main()
