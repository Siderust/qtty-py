# qtty-py Bridge - Quick Reference

## TL;DR - 3 Pasos

### 1. Implementa `ToQuantity` en tu tipo:

```rust
use qtty_py::bridge::ToQuantity;
use qtty_ffi::UnitId;

impl ToQuantity for MyDistance {
    fn value(&self) -> f64 { self.value }
    fn unit(&self) -> UnitId { self.unit }
}
```

### 2. Usa `.to_py_quantity()` en tu getter PyO3:

```rust
#[pymethods]
impl MyObject {
    #[getter]
    fn distance(&self) -> qtty_py::PyQuantity {
        self.distance.to_py_quantity()
    }
}
```

### 3. Ahora en Python tienes un `Quantity` completo:

```python
obj = MyObject()
qty = obj.distance              # Es un qtty PyQuantity

qty.to(Unit.Kilometer)          # Conversión
qty * 2.5                       # Aritmética
qty + otra_cantidad             # Dimensional safety
```

---

## API Mínima

| En Rust | Descripción |
|---------|-------------|
| `ToQuantity::value()` | Retorna f64 con el valor |
| `ToQuantity::unit()` | Retorna `UnitId` con la unidad |
| `to_py_quantity()` | Convierte a `PyQuantity` |
| `PyQuantity::from_quantity(f64, UnitId)` | Crea desde valores |
| `PyQuantity::get_value()` | Lee valor desde Rust |
| `PyQuantity::get_unit()` | Lee unidad desde Rust |

---

## Ejemplo Mínimo

```rust
// Cargo.toml
[lib]
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.22", features = ["extension-module"] }
qtty-py = { path = "../qtty-py" }
qtty-ffi = "0.2"
```

```rust
// src/lib.rs
use pyo3::prelude::*;
use qtty_ffi::UnitId;
use qtty_py::bridge::ToQuantity;

#[derive(Clone)]
struct Distance(f64);

impl ToQuantity for Distance {
    fn value(&self) -> f64 { self.0 }
    fn unit(&self) -> UnitId { UnitId::Meter }
}

#[pyclass]
struct Object {
    dist: Distance,
}

#[pymethods]
impl Object {
    #[new]
    fn new(meters: f64) -> Self {
        Self { dist: Distance(meters) }
    }

    #[getter]
    fn dist(&self) -> qtty_py::PyQuantity {
        self.dist.to_py_quantity()
    }
}

#[pymodule]
fn my_lib(_py: Python, m: &Bound<PyModule>) -> PyResult<()> {
    m.add_class::<Object>()?;
    Ok(())
}
```

```python
from qtty import Unit
from my_lib import Object

obj = Object(1000)
print(obj.dist.to(Unit.Kilometer))  # 1.0 Kilometer
```

---

## Troubleshooting

### Error: `method unit is private`
→ Usa `PyQuantity::from_quantity()` o implementa `ToQuantity`

### Error: `cannot find type UnitId`
→ Agrega: `use qtty_ffi::UnitId;`

### Error: `failed to resolve bridge`
→ Verifica que `pub mod bridge` está en `lib.rs` de qtty-py

### Python: `AttributeError: quantity is None`
→ Asegúrate que el getter retorna `PyQuantity`, no `PyResult<PyQuantity>`

---

## Para Más Detalles

Ver [BRIDGE_GUIDE.md](./BRIDGE_GUIDE.md) para:
- Ejemplos completos
- Patrones avanzados
- Notas de rendimiento
