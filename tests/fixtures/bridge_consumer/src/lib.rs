use pyo3::prelude::*;
use qtty_py::bridge::{quantity_from_python, quantity_to_python_raw};

/// Build through the public bridge using only primitive cross-module data.
#[pyfunction]
fn make_quantity(py: Python<'_>, value: f64, unit_id: u32) -> PyResult<Py<PyAny>> {
    quantity_to_python_raw(py, value, unit_id)
}

/// Extract through the public bridge, returning primitive data to Python.
#[pyfunction]
fn extract_quantity(value: &Bound<'_, PyAny>) -> PyResult<(f64, u32)> {
    let parts = quantity_from_python(value)?;
    Ok((parts.value, parts.unit as u32))
}

/// Exercise both bridge directions in the independent extension.
#[pyfunction]
fn round_trip(py: Python<'_>, value: &Bound<'_, PyAny>) -> PyResult<Py<PyAny>> {
    let parts = quantity_from_python(value)?;
    qtty_py::bridge::quantity_to_python(py, parts.value, parts.unit)
}

#[pymodule]
fn qtty_bridge_consumer(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(make_quantity, m)?)?;
    m.add_function(wrap_pyfunction!(extract_quantity, m)?)?;
    m.add_function(wrap_pyfunction!(round_trip, m)?)?;
    Ok(())
}
