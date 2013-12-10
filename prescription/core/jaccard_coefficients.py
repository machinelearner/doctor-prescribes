class JaccardCoefficient():
    def compute(self, tokens, other_tokens):
        setA = set(tokens)
        setB = set(other_tokens)

        intersection = setA.intersection(setB)
        union = setA.union(setB)

        if len(union) == 0:
            return 0
        return round((len(intersection) / float(len(union))), 4)
