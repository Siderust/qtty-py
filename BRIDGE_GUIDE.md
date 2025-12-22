# Usando qtty-py como Bridge en tu Proyecto Rust

## Descripción General

`qtty-py` proporciona un módulo `bridge` que permite reutilizar sus bindings de PyO3 en tus propios proyectos Rust. De esta manera, cualquier estructura con cantidades físicas puede ser fácilmente exportada a Python.

## Setup

En tu `Cargo.toml`:

```toml
[dependencies]
pyo3 = { version = "0.22", features = ["extension-module"] }
qtty-py = { path = "../qtty-py" }
qtty-ffi = { version = "0.2", path = "../qtty/qtty-ffi" }

# Tu library con tipos de cantidad
my_project = { path = "../my_project" }
```

## Implementar ToQuantity en tu Código Rust

Supongamos que tienes una estructura así:

```rust
// En my_project/src/lib.rs
use qtty_ffi::UnitId;

pub struct MyDistance {
    value: f64,
    unit: UnitId,
}

impl MyDistance {
    pub fn new(value: f64, unit: UnitId) -> Self {
        Self { value, unit }
    }
}
```

### Opción 1: Implementar el trait `ToQuantity`

```rust
use qtty_py::bridge::ToQuantity;

impl ToQuantity for MyDistance {
    fn value(&self) -> f64 {
        self.value
    }
    
    fn unit(&self) -> UnitId {
        self.unit
    }
}
```

### Opción 2: Usar directamente en PyClass

```rust
use pyo3::prelude::*;
use qtty_py::PyQuantity;

#[pyclass]
pub struct MyObject {
    distance: MyDistance,
}

#[pymethods]
impl MyObject {
    #[getter]
    fn distance(&self) -> PyQuantity {
        PyQuantity::from_quantity(self.distance.value(), self.distance.unit())
    }
}
```

### Opción 3: Si ya implementas ToQuantity

```rust
use pyo3::prelude::*;
use qtty_py::bridge::ToQuantity;

#[pyclass]
pub struct MyObject {
    distance: MyDistance,
}

#[pymethods]
impl MyObject {
    #[getter]
    fn distance(&self) -> PyQuantity {
        self.distance.to_py_quantity()  // Directo!
    }
}
```

## Ejemplo Completo

```rust
// my_project/src/lib.rs
use pyo3::prelude::*;
use qtty_ffi::UnitId;
use qtty_py::bridge::ToQuantity;
use qtty_py::PyQuantity;

pub struct Distance {
    value: f64,
    unit: UnitId,
}

impl Distance {
    pub fn new(value: f64, unit: UnitId) -> Self {
        Self { value, unit }
    }
}

impl ToQuantity for Distance {
    fn value(&self) -> f64 {
        self.value
    }
    
    fn unit(&self) -> UnitId {
        self.unit
    }
}

#[pyclass]
pub struct Satellite {
    name: String,
    altitude: Distance,
}

#[pymethods]
impl Satellite {
    #[new]
    fn new(name: String, altitude_value: f64, altitude_unit: UnitId) -> Self {
        Self {
            name,
            altitude: Distance::new(altitude_value, altitude_unit),
        }
    }

    #[getter]
    fn name(&self) -> String {
        self.name.clone()
    }

    #[getter]
    fn altitude(&self) -> PyQuantity {
        self.altitude.to_py_quantity()
    }
}

#[pymodule]
fn my_project(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Satellite>()?;
    Ok(())
}
```

## Uso en Python

```python
from qtty import Unit
from my_project import Satellite

# Crear un satélite con altitud en metros
sat = Satellite("ISS", 408000, Unit.Meter)

# Acceder a la altitud como PyQuantity
altitude = sat.altitude
print(f"Altitud: {altitude.value} {altitude.unit}")

# Convertir a kilómetros
altitude_km = altitude.to(Unit.Kilometer)
print(f"Altitud en km: {altitude_km.value}")

# Operaciones en Python
doubled = altitude_km * 2
print(f"Doblada: {doubled.value} {doubled.unit}")
```

## Características del Bridge

✅ **Conversión transparente**: `Quantity<Unit>` → `PyQuantity`  
✅ **Sin boilerplate**: Usa el trait `ToQuantity`  
✅ **Totalmente type-safe**: Los tipos se validan en Rust  
✅ **Reutilizable**: Una sola implementación para muchos campos  
✅ **Compatible**: Funciona con todas las unidades de qtty-ffi  

## Notas Importantes

- El módulo `bridge` es público en qtty-py (`pub mod bridge`), así que puedes importarlo
- `PyQuantity` es clonable y se puede pasar libremente entre Python y Rust
- Las conversiones son zero-copy (solo se pasan referencias de f64 y UnitId)
- El trait `ToQuantity` es extensible para tus propios tipos de cantidad
