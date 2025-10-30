# Declarative Floorplan - Module Structure Plan

## Overview
A Python library for declarative floorplan generation using constraint-based positioning and SVG rendering.

## Core Design Principles
1. **Declarative API**: Users describe what they want, not how to build it
2. **Constraint-based positioning**: Use constraints to define vertex positions
3. **Context manager pattern**: Floorplan as a context manager for automatic registration
4. **Type safety**: Full type hints for better IDE support
5. **Extensibility**: Easy to add new element types and constraints

---

## Module Structure

```
src/declarative_floorplan/
├── __init__.py              # Public API exports
├── core/
│   ├── __init__.py
│   ├── floorplan.py         # Floorplan context manager and coordinator
│   ├── registry.py          # Element registration and tracking
│   └── solver.py            # Constraint solving logic
├── geometry/
│   ├── __init__.py
│   ├── vertex.py            # Vertex class with constraint support
│   ├── constraints.py       # HorizontalConstraint, VerticalConstraint
│   └── utils.py             # Geometric calculations (distance, angles, etc.)
├── elements/
│   ├── __init__.py
│   ├── base.py              # Base class for all floorplan elements
│   ├── wall.py              # Wall element
│   ├── door.py              # Door element
│   ├── window.py            # Window element
│   └── opening.py           # Base class for Door/Window (shared behavior)
├── positioning/
│   ├── __init__.py
│   ├── position.py          # Position enum (CENTERED, START, END, etc.)
│   └── calculator.py        # Calculate positions along walls
├── rendering/
│   ├── __init__.py
│   ├── svg.py               # SVG generation engine
│   ├── styles.py            # Style definitions for different elements
│   └── templates.py         # SVG templates and patterns
└── utils/
    ├── __init__.py
    ├── validation.py        # Input validation
    └── exceptions.py        # Custom exceptions
```

---

## Detailed Module Descriptions

### 1. `core/` - Core Framework

#### `core/floorplan.py`
**Purpose**: Main coordinator and context manager for floorplan creation

**Classes**:
- `Floorplan`: Context manager that tracks all elements and orchestrates generation

**Key Methods**:
```python
class Floorplan:
    def __init__(self, name: str, units: str = "px")
    def __enter__(self) -> "Floorplan"
    def __exit__(self, exc_type, exc_val, exc_tb)
    def register_element(self, element: FloorplanElement)
    def generate_svg(self, output_path: str) -> None
    def solve_constraints(self) -> None
```

#### `core/registry.py`
**Purpose**: Track and manage all elements in a floorplan

**Classes**:
- `ElementRegistry`: Stores vertices, walls, doors, windows by type
- Maintains relationships between elements (e.g., which doors are on which walls)

**Key Methods**:
```python
class ElementRegistry:
    def register(self, element: FloorplanElement)
    def get_by_type(self, element_type: Type) -> List[FloorplanElement]
    def get_vertices(self) -> List[Vertex]
    def get_walls(self) -> List[Wall]
    def get_openings(self) -> List[Opening]
```

#### `core/solver.py`
**Purpose**: Resolve constraints to determine final vertex positions

**Classes**:
- `ConstraintSolver`: Evaluates constraints and resolves vertex positions

**Key Methods**:
```python
class ConstraintSolver:
    def solve(self, vertices: List[Vertex]) -> Dict[Vertex, Tuple[float, float]]
    def validate_constraints(self, vertex: Vertex) -> bool
```

---

### 2. `geometry/` - Geometric Primitives

#### `geometry/vertex.py`
**Purpose**: Define vertices with constraint-based positioning

**Classes**:
- `Vertex`: A point in 2D space defined by constraints

**Key Attributes**:
```python
class Vertex:
    name: str
    constraints: List[Constraint]  # HC and VC instances
    _position: Optional[Tuple[float, float]]  # Resolved position
```

**Key Methods**:
```python
def get_position(self) -> Tuple[float, float]
def add_constraint(self, constraint: Constraint)
```

#### `geometry/constraints.py`
**Purpose**: Define positioning constraints

**Classes**:
- `Constraint`: Abstract base class
- `HorizontalConstraint`: Fixes Y coordinate (horizontal line)
- `VerticalConstraint`: Fixes X coordinate (vertical line)
- Future: `DistanceConstraint`, `AngleConstraint`, etc.

**Usage Pattern**:
```python
class HorizontalConstraint(Constraint):
    def __init__(self, value: float)
    def apply(self, vertex: Vertex) -> float  # Returns Y coordinate

class VerticalConstraint(Constraint):
    def __init__(self, value: float)
    def apply(self, vertex: Vertex) -> float  # Returns X coordinate
```

#### `geometry/utils.py`
**Purpose**: Geometric calculations and utilities

**Functions**:
```python
def distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float
def angle_between(p1: Tuple[float, float], p2: Tuple[float, float]) -> float
def point_along_line(start, end, distance_or_ratio: float) -> Tuple[float, float]
def midpoint(p1: Tuple[float, float], p2: Tuple[float, float]) -> Tuple[float, float]
```

---

### 3. `elements/` - Floorplan Elements

#### `elements/base.py`
**Purpose**: Base class for all floorplan elements

**Classes**:
- `FloorplanElement`: Abstract base with common behavior

**Key Attributes**:
```python
class FloorplanElement(ABC):
    name: str
    element_type: str  # "wall", "door", "window", etc.

    @abstractmethod
    def validate(self) -> bool

    @abstractmethod
    def to_svg(self) -> str
```

#### `elements/wall.py`
**Purpose**: Wall element connecting two vertices

**Classes**:
- `Wall`: Linear element between two vertices

**Key Attributes**:
```python
class Wall(FloorplanElement):
    start_vertex: Vertex
    end_vertex: Vertex
    thickness: float = 15.0  # Default wall thickness
    style: WallStyle = WallStyle.INTERNAL  # or EXTERNAL

    def length(self) -> float
    def angle(self) -> float
    def midpoint(self) -> Tuple[float, float]
    def point_at_position(self, position: Union[float, Position]) -> Tuple[float, float]
```

#### `elements/opening.py`
**Purpose**: Base class for elements that create openings in walls (doors, windows)

**Classes**:
- `Opening`: Abstract base for Door and Window

**Key Attributes**:
```python
class Opening(FloorplanElement):
    wall: Wall
    position: Union[float, Position]  # Numeric position or Position enum
    width: float

    def get_absolute_position(self) -> Tuple[float, float]
    def get_start_end_points(self) -> Tuple[Tuple[float, float], Tuple[float, float]]
```

#### `elements/door.py`
**Purpose**: Door element

**Classes**:
- `Door`: Opening with door-specific rendering (swing arc, panel, etc.)
- `DoorStyle`: Enum for different door types

**Enums**:
```python
class DoorStyle(Enum):
    SWING_LEFT = "swing_left"
    SWING_RIGHT = "swing_right"
    SLIDING = "sliding"
    DOUBLE = "double"
    POCKET = "pocket"
```

**Key Attributes**:
```python
class Door(Opening):
    style: DoorStyle = DoorStyle.SWING_LEFT
    swing_angle: float = 90.0  # Degrees
```

#### `elements/window.py`
**Purpose**: Window element

**Classes**:
- `Window`: Opening with window-specific rendering (panes, frame, etc.)
- `WindowStyle`: Enum for different window types

**Enums**:
```python
class WindowStyle(Enum):
    REGULAR = "regular"
    CASEMENT = "casement"
    SLIDING = "sliding"
    BAY = "bay"
```

**Key Attributes**:
```python
class Window(Opening):
    style: WindowStyle = WindowStyle.REGULAR
    panes: int = 1
```

---

### 4. `positioning/` - Position Calculations

#### `positioning/position.py`
**Purpose**: Define standard positions along walls

**Enums**:
```python
class Position(Enum):
    CENTERED = "centered"
    START = "start"
    END = "end"
    # Future: QUARTER, THREE_QUARTERS, etc.
```

#### `positioning/calculator.py`
**Purpose**: Calculate actual positions from Position enums or numeric values

**Functions**:
```python
def calculate_position_on_wall(
    wall: Wall,
    position: Union[float, Position],
    element_width: float
) -> Tuple[float, float]:
    """Returns the center point of the element on the wall"""

def calculate_opening_bounds(
    wall: Wall,
    center_position: Tuple[float, float],
    width: float
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Returns (start_point, end_point) of the opening"""
```

---

### 5. `rendering/` - SVG Generation

#### `rendering/svg.py`
**Purpose**: Main SVG generation engine

**Classes**:
- `SVGRenderer`: Converts floorplan elements to SVG markup

**Key Methods**:
```python
class SVGRenderer:
    def __init__(self, floorplan: Floorplan)

    def render(self) -> str:
        """Generate complete SVG document"""

    def render_walls(self) -> str
    def render_openings(self) -> str
    def render_vertices(self, debug: bool = False) -> str

    def calculate_viewbox(self) -> Tuple[float, float, float, float]
```

#### `rendering/styles.py`
**Purpose**: Define visual styles for different elements

**Classes**:
```python
@dataclass
class ElementStyle:
    fill: str
    stroke: str
    stroke_width: float
    fill_opacity: float = 1.0
    stroke_opacity: float = 1.0

class StyleSheet:
    WALL_INTERNAL: ElementStyle
    WALL_EXTERNAL: ElementStyle
    DOOR: ElementStyle
    WINDOW: ElementStyle
    VERTEX_DEBUG: ElementStyle
```

#### `rendering/templates.py`
**Purpose**: SVG templates and reusable patterns

**Functions**:
```python
def svg_document_template(viewbox: str, content: str) -> str
def wall_polygon(points: List[Tuple[float, float]], style: ElementStyle) -> str
def door_swing_arc(center, radius, start_angle, end_angle, style: ElementStyle) -> str
def window_panes(bounds, panes: int, style: ElementStyle) -> str
```

---

### 6. `utils/` - Utilities

#### `utils/validation.py`
**Purpose**: Input validation

**Functions**:
```python
def validate_vertex_constraints(vertex: Vertex) -> bool:
    """Ensure vertex has exactly one HC and one VC"""

def validate_wall(wall: Wall) -> bool:
    """Ensure wall has valid start and end vertices"""

def validate_opening(opening: Opening) -> bool:
    """Ensure opening fits within wall bounds"""
```

#### `utils/exceptions.py`
**Purpose**: Custom exceptions

**Classes**:
```python
class FloorplanError(Exception):
    """Base exception"""

class ConstraintError(FloorplanError):
    """Constraint validation failed"""

class GeometryError(FloorplanError):
    """Geometric validation failed"""

class RenderingError(FloorplanError):
    """SVG rendering failed"""
```

---

## Public API (`__init__.py`)

The main `__init__.py` exports a clean, simple API:

```python
from declarative_floorplan.core.floorplan import Floorplan
from declarative_floorplan.geometry.vertex import Vertex
from declarative_floorplan.geometry.constraints import (
    HorizontalConstraint,
    VerticalConstraint,
)
from declarative_floorplan.elements.wall import Wall
from declarative_floorplan.elements.door import Door, DoorStyle
from declarative_floorplan.elements.window import Window, WindowStyle
from declarative_floorplan.positioning.position import Position

__all__ = [
    "Floorplan",
    "Vertex",
    "HorizontalConstraint",
    "VerticalConstraint",
    "Wall",
    "Door",
    "DoorStyle",
    "Window",
    "WindowStyle",
    "Position",
]
```

---

## Usage Patterns from Examples

### Simple Room Pattern
```python
from declarative_floorplan import (
    Floorplan, Vertex, Wall, Door, Window,
    Position as Pos,
    HorizontalConstraint as HC,
    VerticalConstraint as VC
)

with Floorplan("Room Name") as fp:
    # 1. Define constraints (reusable positioning)
    h_constraint = HC(100)
    v_constraint = VC(50)

    # 2. Create vertices using constraints
    vertex = Vertex(name="Corner", constraints=[h_constraint, v_constraint])

    # 3. Create walls connecting vertices
    wall = Wall(name="Wall", start_vertex=v1, end_vertex=v2)

    # 4. Add openings (doors/windows) to walls
    door = Door(name="Door", wall=wall, position=50, width=30)
    window = Window(name="Window", wall=wall, position=Pos.CENTERED, width=40)

    # 5. Generate output
    fp.generate_svg("output.svg")
```

### Complex Floorplan Pattern (model_svg.py)
- Reuse constraints across multiple vertices
- Build complex polygon shapes with 5+ vertices
- Share constraints to ensure alignment
- Add multiple doors and windows with precise positioning

---

## Implementation Phases

### Phase 1: Core Geometry
- [ ] `geometry/constraints.py` - HC, VC classes
- [ ] `geometry/vertex.py` - Vertex with constraint support
- [ ] `core/solver.py` - Basic constraint solver
- [ ] `geometry/utils.py` - Basic geometric utilities

### Phase 2: Basic Elements
- [ ] `elements/base.py` - FloorplanElement base class
- [ ] `elements/wall.py` - Wall implementation
- [ ] `core/registry.py` - Element registration
- [ ] `core/floorplan.py` - Basic Floorplan context manager

### Phase 3: Openings
- [ ] `positioning/position.py` - Position enum
- [ ] `positioning/calculator.py` - Position calculations
- [ ] `elements/opening.py` - Opening base class
- [ ] `elements/door.py` - Door implementation
- [ ] `elements/window.py` - Window implementation

### Phase 4: Rendering
- [ ] `rendering/styles.py` - Style definitions
- [ ] `rendering/templates.py` - SVG templates
- [ ] `rendering/svg.py` - SVG renderer

### Phase 5: Polish
- [ ] `utils/validation.py` - Input validation
- [ ] `utils/exceptions.py` - Custom exceptions
- [ ] Type hints throughout
- [ ] Documentation and docstrings
- [ ] Unit tests

---

## Key Design Decisions

### 1. Constraint System
- Vertices defined by constraints, not direct coordinates
- Allows declarative positioning and automatic layout
- Easy to maintain alignment across multiple elements
- Extensible to new constraint types (distance, angle, etc.)

### 2. Context Manager Pattern
- `with Floorplan() as fp:` automatically registers elements
- Clean, Pythonic API
- Ensures proper resource management
- Clear scope for floorplan definitions

### 3. Type Safety
- Full type hints using modern Python (3.12+)
- Better IDE support
- Catch errors early
- Self-documenting code

### 4. Positioning Flexibility
- Support both numeric positions and Position enums
- `position=50` for exact placement
- `position=Position.CENTERED` for semantic positioning
- Easy to extend with more semantic positions

### 5. Extensibility
- Base classes make it easy to add new element types
- Constraint system can be extended
- Rendering is pluggable (could add PNG, PDF, etc.)
- Style system is separate from logic

---

## Future Enhancements

1. **Additional Elements**: Furniture, fixtures, dimensions, labels
2. **Advanced Constraints**: Distance, angle, parallel, perpendicular
3. **Room Detection**: Automatically identify enclosed spaces
4. **Measurements**: Auto-generate dimension lines
5. **Multiple Floors**: Support for multi-story buildings
6. **Export Formats**: PNG, PDF, DXF, etc.
7. **Interactive Editing**: Integration with web viewers
8. **Parametric Design**: Variables and formulas in constraints
9. **Library of Components**: Pre-built room templates
10. **Validation**: Check for overlapping elements, impossible constraints

---

## Dependencies

Based on the examples, minimal external dependencies:
- **Core**: Python 3.12+ (uses modern type hints)
- **Optional**:
  - `cairosvg` - For PNG/PDF export
  - `pydantic` - For data validation
  - `pytest` - For testing
