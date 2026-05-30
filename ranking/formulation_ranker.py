def composite_biostasis_score(evidence, mechanism, compatibility, assay, weights=None):
    if weights is None:
        weights = {
            'evidence':0.25,
            'mechanism':0.35,
            'compatibility':0.20,
            'assay':0.20
        }

    return (
        evidence*weights['evidence'] +
        mechanism*weights['mechanism'] +
        compatibility*weights['compatibility'] +
        assay*weights['assay']
    )


if __name__ == '__main__':
    score = composite_biostasis_score(8.0,9.0,7.5,8.5)
    print(f'Composite biostasis score: {score:.2f}')
