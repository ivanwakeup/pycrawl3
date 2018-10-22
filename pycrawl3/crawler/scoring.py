
def score_blogger(blogger):
    creator_score = 15
    if blogger.found_ads:
        creator_score += 25
    if blogger.found_current_year:
        creator_score += 25

    if blogger.seed and blogger.seed.weighted_terms:
        terms = set([x.lower().strip() for x in blogger.seed.weighted_terms])
        for term in terms:
            if term in blogger.scrubbed_tags:
                creator_score += 10
                break

    return creator_score if creator_score <= 100 else 100