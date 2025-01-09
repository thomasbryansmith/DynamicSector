#!/usr/bin/env python3

"""
DynamicSector provides a suite of functions that help construct dynamic star (sector) maps for science fiction roleplaying games.
"""

def random_yellow_hex(red_range=(210, 255), green_range=(210, 255)):
    """Generates a random hex color code that falls within the yellow range."""

    # Generate random values for red and green components, ensuring a yellow hue
    red = random.randint(*red_range)
    green = random.randint(*green_range)

    # Keep blue component low to maintain yellow hue
    blue = random.randint(100, 255)

    # Format as hex code
    return f"#{red:02X}{green:02X}{blue:02X}".format(red, green, blue)


def random_earthy_hex(red_range=(150, 255), green_range=(150, 255), blue_range=(75, 255)):
    """Generates a random hex color code with an earthy tone."""

    # Generate random RGB values within the earthy ranges
    red = random.randint(*red_range)
    green = random.randint(*green_range)
    blue = random.randint(*blue_range)

    # Format as hex code
    return f"#{:02x}{:02x}{:02x}".format(red, green, blue)


def set_color_shape_image(type_vector):
    """Based on the type variable of input system data, each node in the sector is assigned either a clip art sun or an earthy tone."""

    # Generate empty lists to populate
    color = []
    shape = []
    image = []
    
    # If / else statement that identifies suns
    for n in type_vector: 
        if n=='Sun':
            color.append("rgba(0, 0, 0, 0)")
            shape.append('circularImage')
            image.append('https://png.pngtree.com/png-clipart/20230518/ourmid/pngtree-realistic-sun-illustration-png-image_7096994.png')
        else: 
            color.append(random_earthy_hex())
            shape.append('dot')
            image.append('')
    return {'color': color, 
            'shape': shape, 
            'image': image}
        
    
    
    
    
    
        
system_data['color'] = set_color_shape_image(system_data['type'])['color']
system_data['shape'] = set_color_shape_image(system_data['type'])['shape']
system_data['image'] = set_color_shape_image(system_data['type'])['image']
