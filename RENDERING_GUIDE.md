# Rendering Architecture Guide

## Overview

The `declarative_floorplan` library uses a **separation of concerns** approach where:
- **Elements** handle geometry and spatial logic
- **SVGRenderer** handles all visual rendering and styling

This design gives you complete control over how floorplans are rendered without modifying element classes.

---

## Architecture

### 1. Elements (Geometry Layer)

Elements like `Wall`, `Door`, and `Window` focus on **geometry**:
- Position calculations
- Constraint solving
- Spatial relationships

**What they DON'T do:**
- Generate SVG markup
- Define colors or styles
- Handle rendering logic

### 2. SVGRenderer (Rendering Layer)

The `SVGRenderer` class:
- Takes a `Floorplan` and optional `RenderConfig`
- Handles all SVG generation
- Applies styles consistently
- Can be extended for different rendering styles

---

## Using RenderConfig for Custom Styling

### Basic Usage (Default Styling)

```python
from declarative_floorplan import Floorplan

with Floorplan("My Room") as fp:
    # ... define walls, doors, windows ...
    fp.generate_svg("output.svg")  # Uses default styling
```

### Custom Styling

```python
from declarative_floorplan import (
    Floorplan,
    RenderConfig,
    ElementStyle,
)

# Create custom configuration
config = RenderConfig(
    # Wall styles
    wall_internal=ElementStyle(
        fill="#1a1a3e",
        stroke="#0f0f23",
        stroke_width=1.5,
    ),

    # Door styling
    door_fill="#ffffff",
    door_stroke="#cc0000",
    door_stroke_width=2.0,
    door_arc_stroke="#990000",
    door_arc_stroke_width=1.5,

    # Window styling
    window_fill="#c0ffc0",
    window_stroke="#00aa00",
    window_stroke_width=1.5,
    window_glass_stroke="#006600",
    window_glass_stroke_width=1.0,

    # Viewbox settings
    viewbox_padding=30.0,
)

with Floorplan("Styled Room") as fp:
    # ... define elements ...
    fp.generate_svg("output.svg", config=config)
```

---

## RenderConfig Reference

### Wall Styling

```python
wall_internal: ElementStyle = ElementStyle(
    fill="#000000",           # Wall fill color
    stroke="#000000",         # Wall outline color
    stroke_width=0.5,         # Wall outline width
    fill_opacity=1.0,         # Fill transparency (0-1)
    stroke_opacity=1.0,       # Stroke transparency (0-1)
)

wall_external: ElementStyle = ElementStyle(...)  # For external walls (future)
```

### Door Styling

```python
door_fill: str = "#ffffff"              # Door opening line color
door_stroke: str = "#000000"            # Door panel line color
door_stroke_width: float = 1.0          # Door panel line width
door_arc_stroke: str = "#000000"        # Door swing arc color
door_arc_stroke_width: float = 1.0      # Door swing arc width
```

### Window Styling

```python
window_fill: str = "#e0e0ff"            # Window frame fill color
window_stroke: str = "#000000"          # Window frame outline
window_stroke_width: float = 1.0        # Window frame outline width
window_glass_stroke: str = "#000000"    # Glass pane line color
window_glass_stroke_width: float = 0.5  # Glass pane line width
```

### Viewbox Settings

```python
viewbox_padding: float = 20.0  # Padding around the floorplan (in units)
```

---

## ElementStyle Class

The `ElementStyle` dataclass defines visual properties:

```python
@dataclass
class ElementStyle:
    fill: str = "#000000"
    stroke: str = "#000000"
    stroke_width: float = 1.0
    fill_opacity: float = 1.0
    stroke_opacity: float = 1.0

    def to_svg_attrs(self) -> str:
        """Converts to SVG attribute string"""
```

### Usage Examples

```python
# Solid black wall
wall_style = ElementStyle(
    fill="#000000",
    stroke="#000000",
    stroke_width=1.0
)

# Semi-transparent blue
transparent_style = ElementStyle(
    fill="#0000ff",
    stroke="#000088",
    stroke_width=0.5,
    fill_opacity=0.5
)

# Just outline, no fill
outline_only = ElementStyle(
    fill="none",
    stroke="#000000",
    stroke_width=2.0
)
```

---

## Advanced: Extending the Renderer

### Custom Renderer Class

You can subclass `SVGRenderer` to add custom rendering logic:

```python
from declarative_floorplan.rendering.svg import SVGRenderer

class CustomRenderer(SVGRenderer):
    def _render_wall(self, wall):
        """Override to add custom wall rendering"""
        # Your custom logic here
        svg = super()._render_wall(wall)
        # Add annotations, labels, etc.
        return svg

    def _render_door(self, door):
        """Override to change door appearance"""
        # Custom door rendering
        pass

# Use custom renderer
from declarative_floorplan.core.floorplan import Floorplan

with Floorplan("My Room") as fp:
    # ... define elements ...

    # Manually use custom renderer
    renderer = CustomRenderer(fp, config=my_config)
    svg = renderer.render()

    with open("output.svg", "w") as f:
        f.write(svg)
```

---

## Style Presets

You can create reusable style presets:

```python
# presets.py
from declarative_floorplan import RenderConfig, ElementStyle

BLUEPRINT_STYLE = RenderConfig(
    wall_internal=ElementStyle(
        fill="#0f3460",
        stroke="#16213e",
        stroke_width=1.0,
    ),
    door_fill="#ffffff",
    door_stroke="#1a1a2e",
    window_fill="#e4f1ff",
    window_stroke="#16213e",
    viewbox_padding=25.0,
)

MINIMALIST_STYLE = RenderConfig(
    wall_internal=ElementStyle(
        fill="none",
        stroke="#000000",
        stroke_width=2.0,
    ),
    door_fill="none",
    door_stroke="#000000",
    door_stroke_width=1.5,
    window_fill="none",
    window_stroke="#000000",
    window_stroke_width=1.5,
)

COLORFUL_STYLE = RenderConfig(
    wall_internal=ElementStyle(fill="#ff6b6b", stroke="#ee5a6f"),
    door_fill="#ffffff",
    door_stroke="#4ecdc4",
    door_arc_stroke="#44a8a3",
    window_fill="#ffe66d",
    window_stroke="#f4d35e",
)
```

### Using Presets

```python
from declarative_floorplan import Floorplan
from presets import BLUEPRINT_STYLE

with Floorplan("Office") as fp:
    # ... define elements ...
    fp.generate_svg("office_blueprint.svg", config=BLUEPRINT_STYLE)
```

---

## Benefits of This Architecture

### 1. **Separation of Concerns**
- Elements handle geometry
- Renderer handles visualization
- Easy to understand and maintain

### 2. **Flexibility**
- Change styles without modifying element classes
- Create multiple visual representations of the same floorplan
- Easy to add new rendering backends (PNG, PDF, etc.)

### 3. **Reusability**
- Style configurations can be saved and shared
- Same elements can be rendered in different styles
- Renderer can be extended without touching elements

### 4. **Testability**
- Geometry logic tested independently
- Rendering logic tested independently
- Mock renderers for unit tests

---

## Migration from Old `to_svg()` Methods

### Before (Old Approach)

```python
class Wall:
    def to_svg(self) -> str:
        # Hardcoded styles
        return f'<polygon ... fill="#000000" stroke="#000000"/>'
```

**Problems:**
- Styles hardcoded in elements
- Can't customize without modifying classes
- Mixing geometry and rendering concerns

### After (New Approach)

```python
class Wall:
    # Only geometry methods
    def length(self) -> float: ...
    def angle(self) -> float: ...
    def point_at_distance(self, d: float) -> Tuple[float, float]: ...

class SVGRenderer:
    def _render_wall(self, wall: Wall) -> str:
        # Uses config for styling
        style = self.config.wall_internal
        return f'<polygon ... {style.to_svg_attrs()}/>'
```

**Benefits:**
- Clean separation
- Flexible styling
- Easier to extend

---

## Future Enhancements

### Planned Features

1. **External Wall Detection**
   - Automatically distinguish internal/external walls
   - Apply different styles automatically

2. **Theme System**
   - Named themes (blueprint, modern, sketch, etc.)
   - Easy theme switching

3. **Export to Other Formats**
   - `PNGRenderer` using Cairo
   - `PDFRenderer` for print
   - `DXFRenderer` for CAD software

4. **Advanced Styling**
   - Gradients and patterns
   - Shadows and effects
   - Text labels and dimensions

5. **Per-Element Styling**
   - Style individual elements differently
   - Style based on properties (e.g., room type)

---

## Examples

See the `examples/` directory:
- `simple_room.py` - Basic room with default styling
- `styled_room.py` - Custom styling demonstration
- `model_svg.py` - Complex apartment layout

---

## Questions?

For more information, see:
- `MODULE_STRUCTURE.md` - Overall architecture
- Source code in `src/declarative_floorplan/rendering/`
- Example files in `examples/`
