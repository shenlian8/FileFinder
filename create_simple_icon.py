"""
Simple icon creator for FileFinder - 3S Lab
Uses tkinter (built-in) to create an icon
"""
import tkinter as tk
from tkinter import Canvas
import os

def create_icon_png():
    """Create a PNG icon using tkinter"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Create canvas
    size = 256
    canvas = Canvas(root, width=size, height=size, bg='white', highlightthickness=0)
    
    # Draw gradient background (blue to purple)
    for i in range(size):
        r = int(66 + (138 - 66) * i / size)
        g = int(135 + (43 - 135) * i / size)
        b = int(245 + (226 - 245) * i / size)
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, size, i, fill=color)
    
    # Draw magnifying glass
    center_x, center_y = size // 2 - 20, size // 2 - 20
    radius = 50
    
    # Glass circle
    canvas.create_oval(
        center_x - radius, center_y - radius,
        center_x + radius, center_y + radius,
        outline='white', width=8, fill=''
    )
    
    # Handle
    handle_x1 = center_x + radius - 10
    handle_y1 = center_y + radius - 10
    handle_x2 = size - 40
    handle_y2 = size - 40
    canvas.create_line(handle_x1, handle_y1, handle_x2, handle_y2, fill='white', width=12)
    
    # Add "3S" text
    canvas.create_text(
        center_x, center_y,
        text="3S",
        font=("Arial", 40, "bold"),
        fill='white'
    )
    
    # Save as PostScript then convert to PNG
    ps_file = "temp_icon.ps"
    canvas.postscript(file=ps_file, colormode='color')
    
    # Try to convert using PIL if available, otherwise just inform user
    try:
        from PIL import Image
        img = Image.open(ps_file)
        img.save("filefinder_icon.png", "PNG")
        os.remove(ps_file)
        print("Icon created: filefinder_icon.png")
        print("To convert to .ico, you can use an online converter or install PIL:")
        print("  pip install Pillow")
        print("  Then run: python create_icon.py")
    except ImportError:
        print(f"PostScript file created: {ps_file}")
        print("Please install Pillow to convert to PNG/ICO:")
        print("  pip install Pillow")
        print("Or use an online converter to convert the PS file to ICO")
    
    root.destroy()

if __name__ == "__main__":
    print("Creating 3S Lab FileFinder icon...")
    create_icon_png()
