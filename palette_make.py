import math

BASE_PALETTE = [(169, 139, 124), (202, 146, 97), (221, 204, 166), (176, 133, 101), (183, 178, 157)]


def composite_colors(palette, weights):
    """
    Given nonnegative "weight" values, returns a color that is a composite of the palette in a particular way
    """
    color = [0, 0, 0]
    for i in range(len(palette)):
        for j in range(3):
            color[j] += (weights[i]) / sum(weights) * palette[i][j]
    return (int(color[0]), int(color[1]), int(color[2]))


def create_expanded_palette(palette, bonusweights=None):
    new_palette = []
    if bonusweights is None:
        bonusweights = [0 for _ in range(len(palette))]
    for i in range(1, 2**len(palette)):
        weights = []
        quotient = i
        for j in range(len(palette)):
            weights.append(quotient % 2 + bonusweights[j])
            quotient //= 2
        new_palette.append(composite_colors(palette, weights))
    return new_palette