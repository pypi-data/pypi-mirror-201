from typing import Sequence, ByteString, List, Tuple


class Range:
    """
    Half-open interval, i.e. [), in sequence coordinates.
    """
    start: int
    end: int

    def __repr__(self) -> str: ...


class InvertedRepeatSegment:
    """
    Complementary sequence segments that are part of a larger inverted repeat.

    It's guaranteed that:
     * left segment doesn't overlap the right segment
     * left segment coordinates < right segment coordinates
    """
    left: Range
    right: Range

    def __repr__(self) -> str: ...


class InvertedRepeat:
    """
    Inverted repeats composed of complementary segments separated by variable gaps.

    In terms of alignment scores, inverted repeat is locally optimal. That is, it can't be extended or shrunk to
    get a higher alignment score.
    """
    segments: Sequence[InvertedRepeatSegment]


def predict(seq: ByteString, min_score: int, min_matches_run: int) -> List[InvertedRepeat]:
    """
    Predict inverted repeats in the given nucleic acid sequence.

    :param seq: raw ASCII string, DNA or RNA sequence
    :param min_score: min self-alignment score for predict inverted repeats
    :param min_matches_run: min number of continuous matches (complementary base pairs) in predicted inverted repeats
    :return: list of inverted repeats satisfying given constraints
    """
    pass


def optimize(ir: List[InvertedRepeat], scores: List[int]) -> Tuple[List[InvertedRepeat], int]:
    """
    Find score-maximal and coherent set of inverted nucleic acid repeats.

    Here, coherent matching means that there are no "interfering" inverted repeats in the final set.
    That is, there are no i and j where:
        left(i) <= left(j) < right(i) <= right(j)
    Visually (- is gap, * is matched nucleotide):
        *****--------*****
               ****---------****

    The following combinations are allowed:
        left(i) < right(i) < left(j) < right(j)
        *****--------*****    ****---------****

        left(i) < left(j) < right(j) < right(i)
        *****----------------------*****
               ****---------****

    Such coherent matching also represents a valid RNA secondary structure.

    :param ir: list of InvertedRepeat objects
    :param scores: numerical score for each InvertedRepeat
    :return: Tuple containing an optimal set of inverted repeats and the associated total score
    """
    pass
