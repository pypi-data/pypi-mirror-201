use std::borrow::Borrow;
use std::collections::BTreeMap;
use std::ops::Range;

use super::trace::TraceCell;
use super::inv;
use itertools::Itertools;

use super::Score;
use super::{index, trace};

// General rules:
// 1. If a hypothesis is included -> the best subset of its embedded hypothesis is also included
// 2. If a hypothesis is excluded -> some of its embedded hypothesis might be included
// Hypothesis => predicted InvertedRepeat
//
// We need to consdider the matrix with start/ends and the following recursive equation:
// f(s,e) = max of the following
// * f(s, e - 1)
// * max of the following:
//   * f(s, start(RNA)) + weight(RNA) + sum[f(start(gap_i), end(gap_i)) for all gaps in RNA where end(RNA) == e]
struct Workload<'a, T: Borrow<inv::Repeat>> {
    pub index: index::Index,
    pub invrep: &'a [T],
    pub scores: &'a [Score],
}

pub struct DynProgSolution {
    pub tracer: trace::Tracer,
    pub cache: Vec<BTreeMap<usize, Score>>,
}

impl DynProgSolution {
    pub fn new() -> Self {
        Self {
            tracer: trace::Tracer::new(0, 0),
            cache: vec![],
        }
    }

    pub fn solve<'a, 'b, T: Borrow<inv::Repeat>>(
        &mut self, invrep: &'a [T], scores: &'b [Score]
    ) -> (Vec<&'a T>, Score) {
        debug_assert!(invrep.len() == scores.len());
        let w = Workload {
            index: index::Index::new(invrep),
            invrep: invrep,
            scores,
        };

        // Prepare caches & the tracer
        self.cache
            .resize(w.index.starts().len(), Default::default());
        self.tracer
            .reset(w.index.starts().len(), w.index.ends().len());

        // Solve in a limited fashion to reduce the total number of recursive calls
        for i in 0..w.index.ends().len() {
            self.subsolve(&w, 0, i);
        }
        let score = self.subsolve(&w, 0, w.index.ends().len() - 1);
        let optimum = self
            .tracer
            .trace(0, w.index.ends().len() - 1)
            .into_iter()
            .map(|x| &invrep[x])
            .collect();

        (optimum, score)
    }

    fn subsolve<T: Borrow<inv::Repeat>>(&mut self, w: &Workload<T>, sind: usize, eind: usize) -> Score {
        // Sanity check
        debug_assert!(sind <= w.index.starts().len() && eind <= w.index.ends().len());

        // Prevent recursion for incorrect intervals
        if w.index.starts()[sind].pos >= w.index.ends()[eind].pos {
            return Score::default();
        }

        // Cached lookup
        if let Some(score) = self.cache[sind].get(&eind) {
            return *score;
        }

        let mut bestt = None;

        // DP equation
        // * We skip the current end <- the best option is to use the previous end
        if eind > 0 {
            let score = self.subsolve(w, sind, eind - 1);
            if score > 0 {
                bestt = Some((
                    trace::TraceCell {
                        rnaid: None,
                        included: vec![(sind, eind - 1)],
                    },
                    score,
                ))
            }
        }

        // * We look for the best rnafold here
        // TODO: please borrow checker without doing clone here
        for &rnaid in &w.index.ends()[eind].repeats.clone() {
            let (rnasind, rnaeind) = w.index.revmap(rnaid);
            // Skip rnas that are not inside the current region
            if rnasind < sind {
                continue;
            }

            let rna = &w.invrep[rnaid];
            let mut score = w.scores[rnaid];

            debug_assert!(
                rnasind >= sind
                    && rnaeind == eind
                    && w.index.starts()[sind].pos <= rna.borrow().brange().start
                    && w.index.ends()[eind].pos >= rna.borrow().brange().end
            );

            // Include the best combination of 'embeddable' RNAs
            let (gscore, mut trace) = self.gapsolve(w, w.index.blocks(rnaid), rnasind, rnaeind);
            score += gscore;

            // Find the closest end that doesn't contain the current rnafold
            let mut preeind = index::bisect::right(w.index.ends(), rna.borrow().brange().start, 0, eind);
            if preeind != 0 {
                preeind -= 1;
                debug_assert!(rna.borrow().brange().start >= w.index.ends()[preeind].pos);

                // Can we include it?
                if w.index.ends()[preeind].pos > w.index.starts()[sind].pos {
                    let pscore = self.subsolve(w, sind, preeind);
                    if pscore > 0 {
                        score += pscore;
                        trace.push((sind, preeind));
                    }
                }
            }

            if score > 0 && (bestt.is_none() || bestt.as_ref().unwrap().1 < score) {
                bestt = Some((
                    TraceCell {
                        rnaid: Some(rnaid),
                        included: trace,
                    },
                    score,
                ));
            }
        }

        return match bestt {
            None => {
                // No traces scored > 0
                self.cache[sind].insert(eind, 0);
                0
            }
            Some(bestt) => {
                self.tracer.update(sind, eind, bestt.0);
                self.cache[sind].insert(eind, bestt.1);
                bestt.1
            }
        };
    }

    fn gapsolve<T: Borrow<inv::Repeat>>(
        &mut self,
        w: &Workload<T>,
        blocks: &[Range<isize>],
        mut minsind: usize,
        maxeind: usize,
    ) -> (Score, Vec<(usize, usize)>) {
        // Blocks are sorted and for each start-end gap between adjacent blocks we need to find
        // the best possible sind/eind so that: minsind < start(sind) <= start < end <= end(eind) < maxend

        let mut traces = Vec::new();
        let (mut score, mut minend) = (0, 0);

        for (prv, nxt) in blocks.iter().tuple_windows() {
            debug_assert!(prv.end <= nxt.start);

            // No gap
            if prv.end == nxt.start {
                continue;
            }
            let gap = Range {
                start: prv.end,
                end: nxt.start,
            };

            // Find the closest known interval inside the gap
            let sind =
                index::bisect::left(w.index.starts(), gap.start, minsind, w.index.starts().len());
            let mut eind = index::bisect::right(w.index.ends(), gap.end, minend, maxeind);
            debug_assert!(eind < w.index.ends().len() && sind <= w.index.starts().len());

            // No rnas inside the gap
            if eind == 0 || sind == w.index.starts().len() {
                continue;
            }
            eind -= 1;

            let (start, end) = (w.index.starts()[sind].pos, w.index.ends()[eind].pos);
            debug_assert!(gap.start <= start && end <= gap.end);

            // No valid matches
            if start >= end {
                continue;
            }

            // Find the best combination
            let addition = self.subsolve(w, sind, eind);
            if addition > 0 {
                score += addition;
                traces.push((sind, eind));
            }

            // Since the gaps will only move right, we can be sure that:
            // * next gaps will end after the current one
            // * next gaps will start after the current one
            minsind = sind;
            minend = eind;
        }
        debug_assert!(score == 0 && traces.len() == 0 || score > 0 && traces.len() > 0);
        (score, traces)
    }
}
