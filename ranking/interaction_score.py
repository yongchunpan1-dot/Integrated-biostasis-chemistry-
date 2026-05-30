import yaml


def interaction_score(formulation_components, synergy_bonus=0.0, conflict_penalty=0.0):
    return synergy_bonus - conflict_penalty


# Future implementation roadmap:
# 1. Load compatibility_rules.yaml
# 2. Load incompatibility_rules.yaml
# 3. Detect matching component pairs
# 4. Sum synergy bonuses
# 5. Sum conflict penalties
# 6. Return normalized interaction score


if __name__ == '__main__':
    example = ['trehalose', 'dextran', 'catalase']
    score = interaction_score(example, synergy_bonus=2.0, conflict_penalty=0.0)
    print('Interaction score:', score)
