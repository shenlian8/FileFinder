"""
Icon creator for FileFinder - 3S Lab
This script creates a simple icon from an image file or generates a basic icon.
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_3s_lab_icon(output_path="icon.ico"):
    """
    Creates a modern icon for 3S Lab FileFinder
    """
    # Create a 256x256 image with transparency
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw gradient background circle
    for i in range(100):
        alpha = int(255 * (100 - i) / 100)
        color = (
            int(66 + (138 - 66) * i / 100),   # Blue gradient
            int(135 + (43 - 135) * i / 100),  # Purple gradient  
            int(245 + (226 - 245) * i / 100), # 
            alpha
        )
        radius = int(size * 0.45 * (100 - i) / 100)
        draw.ellipse(
            [size//2 - radius, size//2 - radius, 
             size//2 + radius, size//2 + radius],
            fill=color
        )
    
    # Draw magnifying glass circle
    circle_center = (size // 2 - 20, size // 2 - 20)
    circle_radius = 50
    draw.ellipse(
        [circle_center[0] - circle_radius, circle_center[1] - circle_radius,
         circle_center[0] + circle_radius, circle_center[1] + circle_radius],
        outline=(255, 255, 255, 255), width=8
    )
    
    # Draw magnifying glass handle
    handle_start = (circle_center[0] + circle_radius - 10, circle_center[1] + circle_radius - 10)
    handle_end = (size - 40, size - 40)
    draw.line([handle_start, handle_end], fill=(255, 255, 255, 255), width=12)
    
    # Try to add "3S" text
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    text = "3S"
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Draw text in center of magnifying glass
    text_pos = (circle_center[0] - text_width // 2, circle_center[1] - text_height // 2)
    draw.text(text_pos, text, fill=(255, 255, 255, 255), font=font)
    
    # Save as ICO with multiple sizes
    img.save(output_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print(f"Icon created successfully: {output_path}")
    return output_path

def convert_image_to_icon(image_path, output_path="icon.ico"):
    """
    Converts an existing image to ICO format
    """
    try:
        img = Image.open(image_path)
        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Resize to square if needed
        size = max(img.size)
        square_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        square_img.paste(img, ((size - img.width) // 2, (size - img.height) // 2))
        
        # Save as ICO
        square_img.save(output_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
        print(f"Icon created from {image_path}: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error converting image: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Convert existing image
        image_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else "icon.ico"
        convert_image_to_icon(image_path, output_path)
    else:
        # Create default 3S Lab icon
        create_3s_lab_icon("filefinder_icon.ico")
