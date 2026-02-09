from PIL import Image, ImageDraw, ImageFont
import os

def create_simple_icon(output_path="icon.ico"):
    size = (256, 256)
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)

    # Draw generic "document" shape
    doc_color = (200, 200, 200) # Light grey
    draw.rectangle([50, 20, 206, 236], fill=doc_color, outline='black', width=3)
    
    # Draw "magnifying glass" shape
    glass_color = (50, 100, 255) # Blue
    draw.ellipse([80, 80, 180, 180], outline=glass_color, width=10)
    draw.line([160, 160, 220, 220], fill=glass_color, width=10)

    # Add text "FF"
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except IOError:
        font = ImageFont.load_default()
        
    draw.text((100, 100), "FF", fill="black", font=font)
    
    img.save(output_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print(f"Icon saved to {output_path}")

if __name__ == "__main__":
    create_simple_icon()
