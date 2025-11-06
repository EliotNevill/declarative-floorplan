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
│   ├── floorplan.py         # ✅ Floorplan context manager and coordinator
│   └── registry.py          # ✅ Element registration and tracking
├── geometry/
│   ├── __init__.py
│   ├── vertex.py            # ✅ Vertex class with constraint support
│   └── constraints.py       # ✅ HorizontalConstraint, VerticalConstraint
├── elements/
│   ├── __init__.py
│   ├── base.py              # ✅ Base class for all floorplan elements
│   ├── wall.py              # ✅ Wall element
│   ├── door.py              # ✅ Door element
│   ├── window.py            # ✅ Window element
│   └── opening.py           # ✅ Base class for Door/Window (shared behavior)
├── positioning/
│   ├── __init__.py
│   └── position.py          # ✅ Position enum (CENTERED, START, END, etc.)
└── rendering/
    ├── __init__.py
    ├── svg.py               # ✅ SVG generation engine
    ├── raster.py            # ✅ PNG/raster rendering (CairoSVG + Pillow)
    └── styles.py            # ✅ Style definitions (RenderConfig, ElementStyle)

examples/
├── simple_room/             # ✅ Basic room example
├── real_apartment/          # ✅ Complex apartment layout
└── gemeni_pro_2025_11_03/   # ✅ AI-generated floorplan example

mcp-servers/
└── visual-cot/              # ✅ MCP server for constraint visualization

render_examples.py           # ✅ Batch rendering script for all examples
```

**Legend:**
- ✅ = Implemented
- ⏸️ = Planned but not yet implemented

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

**Key Attributes**:
```python
class Door(Opening):
    wall: Wall              # Wall the door is placed on
    position: float | Position  # Position along the wall
    width: float            # Door width
    # Future: style, swing_angle, hinge_side
```

**Rendering**:
- Draws door opening line across the wall
- Renders door panel as a line
- Draws 90-degree swing arc to show door clearance

#### `elements/window.py`
**Purpose**: Window element

**Classes**:
- `Window`: Opening with window-specific rendering (panes, frame, etc.)

**Key Attributes**:
```python
class Window(Opening):
    wall: Wall              # Wall the window is placed on
    position: float | Position  # Position along the wall
    width: float            # Window width
    # Future: style, panes, sill_depth
```

**Rendering**:
- Draws window frame as a rectangle
- Renders glass pane with center line
- Uses distinct styling from walls and doors

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

#### `rendering/raster.py`
**Purpose**: Convert floorplans to raster formats (PNG, etc.)

**Classes**:
- `RasterRenderer`: Converts SVG to PNG/raster formats

**Key Methods**:
```python
class RasterRenderer:
    def __init__(self, floorplan: Floorplan, config: Optional[RenderConfig] = None)

    def render_to_png(self, output_path: str, dpi: int = 300) -> None:
        """Generate PNG file from floorplan"""

    def render_to_bytes(self, format: str = "PNG", dpi: int = 300) -> bytes:
        """Generate raster image as bytes"""
```

**Implementation Details**:
- Uses SVGRenderer to generate SVG first
- Converts SVG to PNG using CairoSVG
- Uses Pillow (PIL) for additional image processing
- Supports high-DPI rendering for print quality

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
from declarative_floorplan.elements.door import Door
from declarative_floorplan.elements.window import Window
from declarative_floorplan.positioning.position import Position
from declarative_floorplan.rendering.styles import ElementStyle, RenderConfig

__version__ = "0.1.0"

__all__ = [
    "Floorplan",
    "Vertex",
    "Wall",
    "Door",
    "Window",
    "HorizontalConstraint",
    "VerticalConstraint",
    "Position",
    "RenderConfig",
    "ElementStyle",
]
```

**Note**: Door/Window styles (DoorStyle, WindowStyle) are not yet implemented and are currently planned for future enhancement.

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

### Complex Floorplan Pattern
- Reuse constraints across multiple vertices (efficient and maintains alignment)
- Build complex polygon shapes with 5+ vertices
- Share constraints between rooms to ensure proper alignment
- Add multiple doors and windows with precise positioning
- Use numeric positions for exact placement, Position enums for semantic placement

See `examples/real_apartment/model.py` for a complete example of a multi-room apartment.

---

## Implementation Status

### ✅ Phase 1: Core Geometry (COMPLETED)
- ✅ `geometry/constraints.py` - HC, VC classes
- ✅ `geometry/vertex.py` - Vertex with constraint support
- ⏸️ `core/solver.py` - Constraint solving (currently inline in vertex)
- ⏸️ `geometry/utils.py` - Geometric utilities (currently inline in elements)

### ✅ Phase 2: Basic Elements (COMPLETED)
- ✅ `elements/base.py` - FloorplanElement base class
- ✅ `elements/wall.py` - Wall implementation
- ✅ `core/registry.py` - Element registration
- ✅ `core/floorplan.py` - Floorplan context manager

### ✅ Phase 3: Openings (COMPLETED)
- ✅ `positioning/position.py` - Position enum
- ✅ `elements/opening.py` - Opening base class
- ✅ `elements/door.py` - Door implementation with swing arcs
- ✅ `elements/window.py` - Window implementation
- ⏸️ `positioning/calculator.py` - Position calculations (currently inline in opening)

### ✅ Phase 4: Rendering (COMPLETED)
- ✅ `rendering/styles.py` - RenderConfig and ElementStyle classes
- ✅ `rendering/svg.py` - Complete SVG renderer
- ✅ `rendering/raster.py` - PNG/raster rendering (CairoSVG + Pillow)

### 🚧 Phase 5: Polish (IN PROGRESS)
- ⏸️ `utils/validation.py` - Input validation (basic validation inline)
- ⏸️ `utils/exceptions.py` - Custom exceptions
- ✅ Type hints throughout
- 🚧 Documentation and docstrings (partially complete)
- ⏸️ Unit tests

### ✅ Additional Features (COMPLETED)
- ✅ `examples/` - Multiple working examples
- ✅ `render_examples.py` - Batch rendering script
- ✅ `mcp-servers/visual-cot/` - MCP server for constraint visualization
- ✅ `RENDERING_GUIDE.md` - Comprehensive rendering documentation
- ✅ `VVLM_PROMPT.md` - AI-assisted generation prompt template

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

## Tools and Utilities

### render_examples.py
A batch rendering script that automates the process of rendering all example floorplans.

**Features**:
- Automatically discovers all `model.py` files in `examples/`
- Imports the Floorplan object from each model
- Generates both SVG and PNG outputs
- Optionally creates visualization overlays:
  - **Constraint overlays**: Draws HC/VC lines on the original image
  - **Floorplan overlays**: Renders the generated floorplan over the original image

**Usage**:
```bash
uv run python render_examples.py
```

**Use Cases**:
- Batch processing of all examples
- Visual comparison with source images
- Debugging constraint placement
- Creating presentation materials

### MCP Server (visual-cot)
An MCP (Model Context Protocol) server that provides visual debugging tools.

**Location**: `mcp-servers/visual-cot/`

**Tools Provided**:

1. **draw_constraints**
   - Extracts HC/VC constraints from a model file
   - Draws constraint lines overlaid on the original image
   - Useful for verifying constraint placement accuracy
   - Helps visualize the "invisible" constraint grid

2. **overlay_floorplan**
   - Renders a floorplan model
   - Overlays the rendered result on the original image
   - Allows visual comparison between generated and source
   - Supports adjustable overlay opacity

**Integration**:
- Automatically available in Claude Code when working in this project
- Used by `render_examples.py` for overlay generation
- Can be called programmatically from Python code

**Benefits**:
- Debug constraint placement visually
- Compare generated floorplans with source images
- Verify model accuracy before finalizing
- Educational tool for understanding constraint-based design

---

## Future Enhancements

1. **Additional Elements**: Furniture, fixtures, dimensions, labels
2. **Advanced Constraints**: Distance, angle, parallel, perpendicular constraints
3. **Room Detection**: Automatically identify enclosed spaces
4. **Measurements**: Auto-generate dimension lines
5. **Multiple Floors**: Support for multi-story buildings
6. **Export Formats**: PDF, DXF, etc. (PNG already supported via `raster.py`)
7. **Interactive Editing**: Integration with web viewers
8. **Parametric Design**: Variables and formulas in constraints
9. **Library of Components**: Pre-built room templates
10. **Validation**: Check for overlapping elements, impossible constraints (via `utils/`)
11. **External Wall Detection**: Automatically distinguish internal/external walls
12. **Theme System**: Named style presets (blueprint, modern, sketch, etc.)

---

## Dependencies

**Required**:
- **Python 3.12+**: Uses modern type hints and language features
- **CairoSVG** (>=2.8.2): SVG to PNG conversion in `rendering/raster.py`
- **Pillow** (>=10.0.0): Image processing and manipulation

**Development**:
- **uv**: Fast Python package manager and dependency resolver
- **visual-cot-mcp**: MCP server for constraint visualization (dev dependency)
- **ruff**: Code formatting (recommended)

**Future**:
- **pytest**: Unit testing framework (not yet implemented)
- **pydantic**: Data validation (not yet implemented)
