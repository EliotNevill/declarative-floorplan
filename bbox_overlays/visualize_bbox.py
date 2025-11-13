import json
from pathlib import Path
from PIL import Image, ImageDraw

# Original bbox coordinate system dimensions
ORIGINAL_WIDTH = 1000
ORIGINAL_HEIGHT = 1000

# Define colors for different labels
COLORS = {
    'wall': 'blue',
    'window': 'green',
    'door': 'red'
}

def process_json_file(json_path: Path, bbox_dir: Path):
    """Process a single JSON file and its corresponding image."""
    # Get the base name without extension
    base_name = json_path.stem

    # Look for corresponding image file
    image_extensions = ['.png', '.jpeg', '.webp', '.jpg']
    image_path = None

    for ext in image_extensions:
        potential_path = bbox_dir / f"{base_name}{ext}"
        if potential_path.exists():
            image_path = potential_path
            break

    if not image_path:
        print(f"Warning: No image found for {json_path.name}")
        return

    # Load the bounding boxes
    with open(json_path, 'r') as f:
        bboxes = json.load(f)

    # Load the image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Get actual image dimensions
    img_width, img_height = img.size

    # Calculate scaling factors
    scale_x = img_width / ORIGINAL_WIDTH
    scale_y = img_height / ORIGINAL_HEIGHT

    print(f"\nProcessing: {base_name}")
    print(f"  Image: {image_path.name} ({img_width}x{img_height})")
    print(f"  Scaling: x={scale_x:.3f}, y={scale_y:.3f}")
    print(f"  Bboxes: {len(bboxes)}")

    # Draw each bounding box
    for item in bboxes:

        if 'bbox_2d' not in item or 'label' not in item:
            print(f"  Warning: Invalid bbox item in {json_path.name}: {item}")
            continue

        bbox = item['bbox_2d']
        label = item['label']
        color = COLORS.get(label, 'yellow')

        # Scale bbox coordinates to actual image size
        scaled_bbox = [
            bbox[0] * scale_x,
            bbox[1] * scale_y,
            bbox[2] * scale_x,
            bbox[3] * scale_y
        ]

        # Draw rectangle
        draw.rectangle(scaled_bbox, outline=color, width=3)

        # Draw label
        draw.text((scaled_bbox[0], scaled_bbox[1] - 15), label, fill=color)

    # Save the result
    output_path = bbox_dir / f"{base_name}_bbox.png"
    img.save(output_path)
    print(f"  Saved: {output_path.name}")

def main():
    """Process all JSON files in the bbox directory."""
    bbox_dir = Path('bbox')

    if not bbox_dir.exists():
        print(f"Error: {bbox_dir} directory not found")
        return

    # Find all JSON files
    json_files = list(bbox_dir.glob('*.json'))

    if not json_files:
        print("No JSON files found in bbox directory")
        return

    print(f"Found {len(json_files)} JSON file(s)")

    # Process each JSON file
    for json_path in json_files:
        process_json_file(json_path, bbox_dir)

    print("\nDone!")

if __name__ == '__main__':
    main()