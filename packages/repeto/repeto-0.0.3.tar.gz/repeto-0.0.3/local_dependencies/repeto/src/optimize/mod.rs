use super::InvertedRepeat;

mod dynprog;
mod index;
mod trace;

pub type Score = i32;

pub fn run<'a, 'b>(dsrna: &'a [InvertedRepeat], scores: &'b [Score]) -> (Vec<&'a InvertedRepeat>, Score) {
    assert_eq!(dsrna.len(), scores.len());

    // Trivial solutions
    if dsrna.is_empty() || (dsrna.len() == 1 && scores[0] == 0) {
        return (vec![], 0);
    } else if dsrna.len() == 1 && scores[0] > 0 {
        return (vec![&dsrna[0]], scores[0]);
    }

    dynprog::DynProgSolution::new().solve(dsrna, scores)
}

#[cfg(test)]
mod tests {
    use std::ops::Range;

    use itertools::Itertools;

    use super::*;

    #[derive(Debug)]
    struct TestCase {
        pub dsrna: Vec<(Score, Vec<(Range<usize>, Range<usize>)>)>,
        pub expdsrna: Vec<usize>,
    }

    fn dotest(tcase: TestCase) {
        let mut transformed = Vec::with_capacity(tcase.dsrna.len());
        let mut scores = Vec::with_capacity(tcase.dsrna.len());
        let msg = format!("{tcase:?}");

        for (score, segments) in tcase.dsrna {
            scores.push(score);
            let segments = segments.into_iter().map(|x| x.into()).collect();
            transformed.push(InvertedRepeat::new(segments));
        }

        let expscore = tcase.expdsrna.iter().map(|x| scores[*x]).sum();
        let (mut result, score) = run(&transformed, &scores);
        debug_assert!(score == expscore, "{msg}\nScore: {expscore} vs {score}");

        let mut expected = tcase
            .expdsrna
            .iter()
            .map(|x| &transformed[*x])
            .collect_vec();
        let key = |x: &&InvertedRepeat| (x.brange().start, x.brange().end);
        result.sort_by_key(key);
        expected.sort_by_key(key);
        debug_assert!(
            expected == result,
            "Test case: {msg}\n{expected:?}\n{result:?}"
        );
    }

    #[test]
    fn empty() {
        dotest(TestCase {
            dsrna: vec![],
            expdsrna: vec![],
        })
    }

    #[test]
    fn single() {
        let workloads = [
            TestCase {
                dsrna: vec![(12, vec![(0..10, 20..30)])],
                expdsrna: vec![0],
            },
            TestCase {
                dsrna: vec![(12, vec![(0..10, 20..30), (12..15, 16..19)])],
                expdsrna: vec![0],
            },
        ];
        for w in workloads {
            dotest(w);
        }
    }

    #[test]
    fn no_overlap_no_complex() {
        let workloads = [
            TestCase {
                dsrna: vec![
                    (1, vec![(0..2, 3..5)]),
                    (2, vec![(6..8, 9..11)]),
                    (3, vec![(15..30, 45..60)]),
                ],
                expdsrna: vec![0, 1, 2],
            },
            TestCase {
                dsrna: vec![(1, vec![(0..2, 3..5)]), (2, vec![(5..8, 9..12)])],
                expdsrna: vec![0, 1],
            },
        ];
        for w in workloads {
            dotest(w);
        }
    }

    #[test]
    fn no_overlap_complex() {
        let workloads = [TestCase {
            dsrna: vec![
                (1, vec![(0..2, 3..5), (6..8, 9..11)]),
                (3, vec![(15..30, 45..60), (35..37, 40..42)]),
            ],
            expdsrna: vec![0, 1],
        }];
        for w in workloads {
            dotest(w);
        }
    }

    #[test]
    fn all_zeros() {
        let workloads = [
            TestCase {
                dsrna: vec![(0, vec![(0..10, 20..30)])],
                expdsrna: vec![],
            },
            TestCase {
                dsrna: vec![
                    (0, vec![(0..4, 5..9)]),
                    (0, vec![(9..12, 15..19)]),
                    (0, vec![(1..5, 7..10)]),
                ],
                expdsrna: vec![],
            },
        ];
        for w in workloads {
            dotest(w);
        }
    }

    #[test]
    fn overlap_no_complex_no_embedded() {
        let workloads = [
            TestCase {
                dsrna: vec![
                    (1, vec![(0..4, 5..9)]),
                    (2, vec![(9..12, 15..19)]),
                    (3, vec![(1..5, 7..10)]),
                    (4, vec![(10..12, 17..20)]),
                    (5, vec![(5..9, 15..19)]),
                    (10, vec![(20..25, 30..35)]),
                ],
                expdsrna: vec![2, 3, 5],
            },
            TestCase {
                dsrna: vec![
                    (1, vec![(0..4, 5..9)]),
                    (2, vec![(9..12, 15..19)]),
                    (3, vec![(1..5, 7..10)]),
                    (4, vec![(10..12, 17..20)]),
                    (15, vec![(5..9, 15..19)]),
                    (10, vec![(20..25, 30..35)]),
                ],
                expdsrna: vec![4, 5],
            },
        ];
        for w in workloads {
            dotest(w);
        }
    }

    #[test]
    fn overlap_no_complex_embedded() {
        let workloads = [
            TestCase {
                dsrna: vec![
                    (1, vec![(0..1, 19..20)]),
                    (1, vec![(2..3, 8..9)]),
                    (1, vec![(4..5, 6..7)]),
                    (1, vec![(11..12, 17..18)]),
                    (1, vec![(13..14, 15..16)]),
                    (1, vec![(9..10, 19..20)]),
                ],
                expdsrna: vec![0, 1, 2, 3, 4],
            },
            TestCase {
                dsrna: vec![
                    (1, vec![(0..1, 19..20)]),
                    (1, vec![(2..3, 17..18)]),
                    (1, vec![(4..5, 15..16)]),
                    (1, vec![(6..7, 13..14)]),
                ],
                expdsrna: vec![0, 1, 2, 3],
            },
        ];
        for w in workloads {
            dotest(w);
        }
    }

    #[test]
    fn overlap_complex_embedded_v1() {
        let workloads = [
            TestCase {
                dsrna: vec![
                    (1, vec![(0..2, 30..32), (7..9, 25..27)]),
                    (1, vec![(3..4, 5..6)]),
                    (1, vec![(10..12, 19..21), (15..16, 18..19)]),
                    (1, vec![(12..13, 14..15)]),
                    (1, vec![(22..23, 31..32), (24..25, 29..30)]),
                ],
                expdsrna: vec![0, 1, 2, 3],
            },
            TestCase {
                dsrna: vec![
                    (1, vec![(0..2, 30..32), (7..9, 25..27)]),
                    (1, vec![(3..4, 5..6)]),
                    (1, vec![(10..12, 19..21), (15..16, 18..19)]),
                    (1, vec![(12..13, 14..15)]),
                    (10, vec![(22..23, 31..32), (24..25, 29..30)]),
                ],
                expdsrna: vec![1, 2, 3, 4],
            },
            TestCase {
                dsrna: vec![
                    (1, vec![(0..2, 30..32), (7..9, 25..27)]),
                    (1, vec![(3..4, 5..6)]),
                    (1, vec![(10..12, 19..21), (15..16, 18..19)]),
                    (1, vec![(12..13, 14..15)]),
                    (1, vec![(22..23, 31..32), (24..25, 29..30)]),
                    (10, vec![(20..22, 30..32), (24..26, 27..29)]),
                ],
                expdsrna: vec![1, 3, 5],
            },
        ];
        for w in workloads {
            dotest(w);
        }
    }

    #[test]
    fn overlap_complex_embedded_v2() {
        let workloads = [
            TestCase {
                dsrna: vec![
                    (1, vec![(0..2, 38..40), (3..5, 35..37), (6..8, 32..34)]),
                    (1, vec![(9..12, 28..31), (13..14, 26..27)]),
                    (1, vec![(2..3, 4..5)]),
                    (1, vec![(7..8, 12..13)]),
                    (1, vec![(16..20, 21..25)]),
                    (1, vec![(27..30, 34..37)]),
                ],
                expdsrna: vec![2, 3, 4, 5],
            },
            TestCase {
                dsrna: vec![
                    (3, vec![(0..2, 38..40), (3..5, 35..37), (6..8, 32..34)]),
                    (3, vec![(9..12, 28..31), (13..14, 26..27)]),
                    (1, vec![(2..3, 4..5)]),
                    (1, vec![(7..8, 12..13)]),
                    (2, vec![(16..20, 21..25)]),
                    (1, vec![(27..30, 34..37)]),
                ],
                expdsrna: vec![0, 1, 4],
            },
        ];
        for w in workloads {
            dotest(w);
        }
    }
}
