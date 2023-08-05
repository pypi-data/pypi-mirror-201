use std::fmt::{Display, Formatter};

use pyo3::prelude::*;

use repeto;

#[pyclass(get_all, set_all)]
#[derive(Clone, Debug)]
pub struct Range {
    pub start: usize,
    pub end: usize,
}

#[pymethods]
impl Range {
    fn __repr__(&self) -> String {
        format!("[{}, {})", self.start, self.end)
    }
}

#[pyclass(get_all, set_all)]
#[derive(Clone, Debug)]
pub struct InvertedRepeatSegment {
    pub left: Py<Range>,
    pub right: Py<Range>,
}


#[pymethods]
impl InvertedRepeatSegment {
    fn __repr__(&self) -> String {
        Python::with_gil(|py| {
            format!(
                "RepeatSegment {{ {} <-> {} }}",
                self.left.borrow(py).__repr__(),
                self.right.borrow(py).__repr__()
            )
        })
    }
}

#[pyclass(get_all, set_all)]
#[derive(Clone, Debug)]
pub struct InvertedRepeat {
    pub segments: Vec<Py<InvertedRepeatSegment>>,
}

impl InvertedRepeat {
    pub fn unbox(self, py: Python) -> repeto::InvertedRepeat {
        let segments: Vec<_> = self.segments.iter().map(|x| {
            let x = x.borrow(py);
            let (left, right) = (x.left.borrow(py), x.right.borrow(py));
            repeto::Segment::new(left.start..left.end, right.start..right.end)
        }).collect();
        repeto::InvertedRepeat::new(segments)
    }

    pub fn boxr(ir: &repeto::InvertedRepeat, py: Python) -> PyResult<Self> {
        let segments: PyResult<Vec<Py<InvertedRepeatSegment>>> = ir.segments().iter().map(|s| {
            Py::new(py, InvertedRepeatSegment {
                left: Py::new(py, Range {
                    start: s.left().start,
                    end: s.left().end,
                })?,
                right: Py::new(py, Range {
                    start: s.right().start,
                    end: s.right().end,
                })?,
            })
        }).collect();
        Ok(InvertedRepeat { segments: segments? })
    }
}

#[pyfunction]
pub fn predict(seq: &[u8], min_score: i64, min_matches_run: usize) -> PyResult<Vec<InvertedRepeat>> {
    let results = repeto::predict(seq, min_score, min_matches_run);

    // Convert to Py-wrappers
    Python::with_gil(|py| -> PyResult<Vec<InvertedRepeat>>{
        results.into_iter().map(|ir| InvertedRepeat::boxr(&ir, py)).collect()
    })
}


#[pyfunction]
pub fn optimize(ir: Vec<InvertedRepeat>, scores: Vec<i32>) -> PyResult<(Vec<InvertedRepeat>, i32)> {
    let ir = Python::with_gil(|py| -> Vec<repeto::InvertedRepeat> {
        ir.into_iter().map(|x| { x.unbox(py) }).collect()
    });

    let (result, total_score) = repeto::optimize(&ir, &scores);

    let ir = Python::with_gil(|py| -> PyResult<Vec<InvertedRepeat>> {
        result.into_iter().map(
            |x| InvertedRepeat::boxr(x, py)
        ).collect()
    })?;
    return Ok((ir, total_score));
}


#[pymodule]
#[pyo3(name = "repeto")]
fn py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Range>()?;
    m.add_class::<InvertedRepeatSegment>()?;
    m.add_class::<InvertedRepeat>()?;
    m.add_function(wrap_pyfunction!(predict, m)?)?;
    m.add_function(wrap_pyfunction!(optimize, m)?)?;
    Ok(())
}