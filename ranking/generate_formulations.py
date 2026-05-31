"""Generate anti-entropy candidate formulations for Integrated Biostasis Chemistry.

Generator v2 implements a diversity-aware discovery strategy.

The goal is not to repeatedly select the single highest-scoring material
(e.g., trehalose) into every formulation. Instead, the generator prioritizes:

1. Coverage of complementary entropy-increase pathways.
2. Balanced preservation of membrane/EV, protein, and nucleic-acid layers.
3. Component diversity across the top-ranked experimental set.
4. Avoidance of known conflicts and excessive assay-accessibility burden.

The output is designed for a first-round discovery screen, not final formulation
optimization. Therefore, diversity and mechanistic coverage are intentionally
rewarded.
"""

from __future__ import annotations

import argparse
import csv
import itertools
from collections import Counter
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
]


ASSAY_FIELDS = ["pcr_compatibility", "lcms_compatibility"]


DISCOVERY_STRATA = [
    "structural_entropy",
    "chemical_entropy",
    "enzymatic_entropy",
    "diffusional_entropy",
    "confinement_entropy",
    "balanced_mixed",
]


def normalize_name(name: str) -> str:
    return name.strip().lower()


def read_materials(path: Path) -> List[Material]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return rows


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


def formulation_names(formulation: Sequence[Material]) -> List[str]:
    return [normalize_name(m["material_name"]) for m in formulation]


def formulation_classes(formulation: Sequence[Material]) -> List[str]:
    return [m["class"] for m in formulation]


def state_layer_scores(formulation: Sequence[Material]) -> Dict[str, float]:
    return {
        "membrane_score": sum(as_float(m, "membrane_protection") for m in formulation) / len(formulation),
        "protein_score": sum(as_float(m, "protein_protection") for m in formulation) / len(formulation),
        "nucleic_acid_score": sum(as_float(m, "nucleic_acid_protection") for m in formulation) / len(formulation),
    }


def integrated_state_score(formulation: Sequence[Material]) -> float:
    scores = state_layer_scores(formulation)
    return sum(scores.values()) / len(scores)


def state_balance_bonus(formulation: Sequence[Material]) -> float:
    """Reward formulations that protect all three layers instead of only one."""
    scores = list(state_layer_scores(formulation).values())
    spread = max(scores) - min(scores)
    return max(0.0, 2.0 - 0.25 * spread)


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
    return 0.4 * len(classes)


def redundancy_penalty(formulation: Sequence[Material]) -> float:
    """Penalize formulations where multiple components cover the same narrow module set."""
    module_counts: Counter[str] = Counter()
    for material in formulation:
        module_counts.update(material_entropy_modules(material))
    repeated_modules = sum(max(0, count - 1) for count in module_counts.values())
    return 0.35 * repeated_modules


def novelty_bonus(formulation: Sequence[Material]) -> float:
    names = set(formulation_names(formulation))
    bonus = 0.0
    if names & {"zif-8", "silicic acid", "calcium phosphate"}:
        bonus += 0.8
    if names & {"edta", "egta", "dtpa"} and names & {"glutathione", "trolox"}:
        bonus += 0.5
    if "trehalose" not in names:
        bonus += 0.7
    return bonus


def base_anti_entropy_score(formulation: Sequence[Material]) -> Dict[str, object]:
    modules = formulation_entropy_modules(formulation)
    module_coverage = len(modules)
    state = integrated_state_score(formulation)
    balance = state_balance_bonus(formulation)
    assay = assay_score(formulation)
    synergy = synergy_score(formulation)
    conflict = conflict_penalty(formulation)
    assay_risk = assay_risk_penalty(formulation)
    diversity = class_diversity_bonus(formulation)
    redundancy = redundancy_penalty(formulation)
    novelty = novelty_bonus(formulation)

    total = (
        2.8 * module_coverage
        + 0.25 * state
        + 0.75 * balance
        + 0.12 * assay
        + 0.55 * synergy
        + diversity
        + novelty
        - conflict
        - assay_risk
        - redundancy
    )

    layer_scores = state_layer_scores(formulation)
    return {
        "base_score": round(total, 3),
        "entropy_modules": ";".join(sorted(modules)),
        "module_coverage": module_coverage,
        "membrane_score": round(layer_scores["membrane_score"], 3),
        "protein_score": round(layer_scores["protein_score"], 3),
        "nucleic_acid_score": round(layer_scores["nucleic_acid_score"], 3),
        "state_score": round(state, 3),
        "state_balance_bonus": round(balance, 3),
        "assay_score": round(assay, 3),
        "synergy_bonus": round(synergy, 3),
        "conflict_penalty": round(conflict, 3),
        "assay_risk_penalty": round(assay_risk, 3),
        "class_diversity_bonus": round(diversity, 3),
        "redundancy_penalty": round(redundancy, 3),
        "novelty_bonus": round(novelty, 3),
    }


def valid_formulation(formulation: Sequence[Material]) -> bool:
    names = set(formulation_names(formulation))

    # Avoid precursor-only mineral/MOF suggestions as final preservation formulations.
    precursor_names = {"zinc acetate", "2-methylimidazole"}
    if names and names.issubset(precursor_names):
        return False

    # Avoid free MOF precursor mixtures being suggested as preservation formulations.
    if "zinc acetate" in names or "2-methylimidazole" in names:
        return False

    # Require at least two entropy modules for meaningful anti-entropy design.
    if len(formulation_entropy_modules(formulation)) < 2:
        return False

    # Avoid formulations with very poor global assay compatibility at this stage.
    if assay_score(formulation) < 4.5:
        return False

    return True


def generate_formulations(materials: List[Material], min_size: int, max_size: int) -> Iterable[Sequence[Material]]:
    for size in range(min_size, max_size + 1):
        yield from itertools.combinations(materials, size)


def assign_stratum(formulation: Sequence[Material]) -> str:
    modules = formulation_entropy_modules(formulation)
    if len(modules) >= 4:
        return "balanced_mixed"
    for stratum in DISCOVERY_STRATA:
        if stratum != "balanced_mixed" and stratum in modules:
            return stratum
    return "balanced_mixed"


def material_frequency_penalty(formulation: Sequence[Material], selected_counts: Counter[str], max_fraction_count: int) -> float:
    penalty = 0.0
    for name in formulation_names(formulation):
        if selected_counts[name] >= max_fraction_count:
            penalty += 4.0 + 0.5 * (selected_counts[name] - max_fraction_count)
    return penalty


def select_diverse_ranked_candidates(
    candidates: List[Dict[str, object]],
    top_n: int,
    max_material_fraction: float,
) -> List[Dict[str, object]]:
    """Greedy diversity-aware selection.

    This prevents one material, such as trehalose, from dominating the discovery set.
    """
    selected: List[Dict[str, object]] = []
    selected_counts: Counter[str] = Counter()
    max_fraction_count = max(1, int(top_n * max_material_fraction))

    # Stratified target allocation across entropy pathways.
    target_per_stratum = max(1, top_n // len(DISCOVERY_STRATA))
    stratum_counts: Counter[str] = Counter()

    pool = sorted(candidates, key=lambda row: row["base_score"], reverse=True)

    while pool and len(selected) < top_n:
        best_idx = None
        best_adjusted = None
        for idx, candidate in enumerate(pool):
            names = candidate["component_names"]
            stratum = candidate["discovery_stratum"]
            dominance_penalty = material_frequency_penalty(
                [candidate["materials_by_name"][name] for name in names],
                selected_counts,
                max_fraction_count,
            )
            stratum_penalty = 0.0
            if stratum_counts[stratum] >= target_per_stratum and len(selected) < int(top_n * 0.75):
                stratum_penalty = 1.5
            adjusted = float(candidate["base_score"]) - dominance_penalty - stratum_penalty
            if best_adjusted is None or adjusted > best_adjusted:
                best_adjusted = adjusted
                best_idx = idx

        if best_idx is None:
            break

        chosen = pool.pop(best_idx)
        chosen["score"] = round(float(best_adjusted), 3)
        selected.append(chosen)
        selected_counts.update(chosen["component_names"])
        stratum_counts.update([chosen["discovery_stratum"]])

    return selected


def write_ranked_formulations(rows: List[Dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "rank",
        "formulation_id",
        "discovery_stratum",
        "components",
        "component_classes",
        "score",
        "base_score",
        "entropy_modules",
        "module_coverage",
        "membrane_score",
        "protein_score",
        "nucleic_acid_score",
        "state_score",
        "state_balance_bonus",
        "assay_score",
        "synergy_bonus",
        "conflict_penalty",
        "assay_risk_penalty",
        "class_diversity_bonus",
        "redundancy_penalty",
        "novelty_bonus",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            cleaned = {key: row.get(key, "") for key in fieldnames}
            writer.writerow(cleaned)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate diversity-aware anti-entropy biostasis candidates.")
    parser.add_argument("--materials", default="knowledgebase/materials.csv")
    parser.add_argument("--output", default="outputs/top48_formulations.csv")
    parser.add_argument("--min-size", type=int, default=2)
    parser.add_argument("--max-size", type=int, default=4)
    parser.add_argument("--top", type=int, default=48)
    parser.add_argument(
        "--max-material-fraction",
        type=float,
        default=0.35,
        help="Maximum approximate fraction of selected candidates that should contain any one material.",
    )
    args = parser.parse_args()

    materials = read_materials(Path(args.materials))
    material_by_name = {normalize_name(m["material_name"]): m for m in materials}
    candidates: List[Dict[str, object]] = []

    for formulation in generate_formulations(materials, args.min_size, args.max_size):
        if not valid_formulation(formulation):
            continue
        score_info = base_anti_entropy_score(formulation)
        names_original = [m["material_name"] for m in formulation]
        names_normalized = [normalize_name(m["material_name"]) for m in formulation]
        classes = formulation_classes(formulation)
        candidates.append(
            {
                "components": " + ".join(names_original),
                "component_classes": ";".join(classes),
                "component_names": names_normalized,
                "materials_by_name": material_by_name,
                "discovery_stratum": assign_stratum(formulation),
                **score_info,
            }
        )

    ranked = select_diverse_ranked_candidates(
        candidates,
        top_n=args.top,
        max_material_fraction=args.max_material_fraction,
    )
    for idx, row in enumerate(ranked, start=1):
        row["rank"] = idx
        row["formulation_id"] = f"AEF{idx:04d}"

    write_ranked_formulations(ranked, Path(args.output))
    print(f"Wrote {len(ranked)} diverse ranked formulations to {args.output}")


if __name__ == "__main__":
    main()
