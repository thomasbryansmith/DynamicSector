#!/usr/bin/env python3

"""
DynamicSector provides a suite of functions that help construct dynamic star (sector) maps for science fiction roleplaying games.
"""

def flatten(xss):
    """Flattens a list of list into a list."""
    return [x for xs in xss for x in xs]


def random_yellow_hex(red_range=(210, 255), green_range=(210, 255)):
    """Generates a random hex color code that falls within the yellow range."""

    # Load dependency
    import random
    
    # Generate random values for red and green components, ensuring a yellow hue
    red = random.randint(*red_range)
    green = random.randint(*green_range)

    # Keep blue component low to maintain yellow hue
    blue = random.randint(100, 255)

    # Format as hex code
    return "#{red:02X}{green:02X}{blue:02X}".format(red, green, blue)


def random_earthy_hex(red_range=(150, 255), green_range=(150, 255), blue_range=(75, 255)):
    """Generates a random hex color code with an earthy tone."""

    # Load dependency
    import random 
    
    # Generate random RGB values within the earthy ranges
    red = random.randint(*red_range)
    green = random.randint(*green_range)
    blue = random.randint(*blue_range)

    # Format as hex code
    return "#{:02x}{:02x}{:02x}".format(red, green, blue)


def set_color_shape_image(type_vector):
    """Based on the type attribute of input system data, each node in the sector is assigned either a clip art sun or an earthy tone."""

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


def set_edge_color_type(type_vector):
    """Based on the type attribute of input data, each edge in the sector map is assigned a color and type."""
    
    # Generate empty lists to populate    
    color = []
    updbl = []
    
    # If / else statement that identifies regular and unpredictable routes
    # This also hides within-system edges
    for n in type_vector:
        if n=='Regular':
            color.append('rgba(27, 235, 124, 0.7)')
            updbl.append(False)
        elif n=='Unpredictable':
            color.append('rgba(255, 0, 132, 0.7)')
            updbl.append(True)
        else:
            color.append('rgba(0, 0, 0, 0)')
            updbl.append(False)
    return {'color': color,
            'updbl': updbl}
        
def wrap_description(description_vector):
    """Wraps the description text using markdown and html syntax."""
        
    # Import wrap function from textwrap library
    from textwrap import wrap 
    
    # Generate empty lists to populate
    wrapped_md = []
    wrapped_html = []
    
    # Wrap the descriptions
    for n in description_vector:
        wrapped_md.append('\n'.join(wrap(n, width=50)))
        wrapped_html.append('<br>'.join(wrap(n, width=50)))
    
    return {'md': wrapped_md,
            'html': wrapped_html}
    
    
def dynamic_sector_2d(system_data, sector_map):
    """Generates 2D sector map based on data provided by the user."""
    
    # Load dependencies
    import pandas as pd
    import tkinter as tk
    import networkx as nx
    from pyvis.network import Network
    from IPython.display import HTML
    
    # Identify user screen size
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Update data ready for visualization
    system_data['color'] = set_color_shape_image(system_data['type'])['color']
    system_data['shape'] = set_color_shape_image(system_data['type'])['shape']
    system_data['image'] = set_color_shape_image(system_data['type'])['image']

    system_data['description_html'] = wrap_description(system_data['description'])['html']
    system_data['description_md'] = wrap_description(system_data['description'])['md']
        
    sector_map['color'] = set_edge_color_type(sector_map['type'])['color']
    sector_map['dashes'] = set_edge_color_type(sector_map['type'])['updbl']

    # Create networkx graph object from sector_map input
    G = nx.from_pandas_edgelist(sector_map, 'source', 'target', edge_attr=['weight', 'type', 'color', 'dashes'])

    # Set attributes of astronomical objects
    for _, row in system_data.iterrows():
        nx.set_node_attributes(G, {row['label']: {'value': row['value'], 
                                                'type': row['type'], 
                                                'threat level': row['threat level'], 
                                                'x': row['x']*50, 
                                                'y': row['y']*-50, 
                                                'title': row['label'] + "\n" + row['description'], 
                                                'color': row['color'],
                                                'shape': row['shape'],
                                                'image': row['image'],
                                                'font': {'color': '#8bad6b', 'face': 'Serif'}
                                                }})
        
    # Invert edge weights
    for u, v, data in G.edges(data=True):
        data['weight'] = 1 / data['weight']
        
    # Create pyvis network object with screen height and width to match user
    nt = Network(str(screen_height*0.75)+'px', str(screen_width*0.85)+'px', bgcolor="#031101")
    nt.from_nx(G)
    
    ## Set edge width to 2
    ## [Note: will not be applicable for all sector sizes, 
    # #       need to set relative sizes based on input features]
    for edge in nt.edges:
        edge['width'] = 2   
        
    ## Set visualization options
    nt.set_options("""
        var options = {
            "nodes": {
            "physics": false
            },
            "layout": {
            "hierarchical": false
            }
        }
        """)
    
    # Return html object
    html_string = nt.generate_html()
    return HTML(html_string)
