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
    import networkx as nx
    from pyvis.network import Network
    from IPython.display import HTML
    from pyautogui import size

    # Update data ready for visualization
    system_data['color'] = set_color_shape_image(system_data['type'])['color']
    system_data['shape'] = set_color_shape_image(system_data['type'])['shape']
    system_data['image'] = set_color_shape_image(system_data['type'])['image']

    system_data['description_md'] = wrap_description(system_data['description'])['md']
        
    sector_map['color'] = set_edge_color_type(sector_map['type'])['color']
    sector_map['dashes'] = set_edge_color_type(sector_map['type'])['updbl']

    # Create networkx graph object from sector_map input
    G = nx.from_pandas_edgelist(sector_map, 'source', 'target', edge_attr=['weight', 'type', 'color', 'dashes'])

    # Set attributes of astronomical objects, generate layout if not provided
    if 'x' and 'y' in system_data.columns:
        for _, row in system_data.iterrows():
            nx.set_node_attributes(G, {row['label']: {'value': row['value'], 
                                                    'type': row['type'], 
                                                    'x': row['x']*50, 
                                                    'y': row['y']*-50, 
                                                    'title': row['label'] + "\n" + row['description_md'], 
                                                    'color': row['color'],
                                                    'shape': row['shape'],
                                                    'image': row['image'],
                                                    'font': {'color': '#8bad6b', 'face': 'Serif'}
                                                    }})
    else:
        pos = nx.spring_layout(G, dim=2)
        system_data['x'] = [x[0] for x in pos.values()]
        system_data['y'] = [y[1] for y in pos.values()]
        for _, row in system_data.iterrows():
            nx.set_node_attributes(G, {row['label']: {'value': row['value'], 
                                                    'type': row['type'], 
                                                    'x': row['x']*50, 
                                                    'y': row['y']*-50, 
                                                    'title': row['label'] + "\n" + row['description_md'], 
                                                    'color': row['color'],
                                                    'shape': row['shape'],
                                                    'image': row['image'],
                                                    'font': {'color': '#8bad6b', 'face': 'Serif'}
                                                    }})
        
    # Invert edge weights
    for u, v, data in G.edges(data=True):
        data['weight'] = 1 / data['weight']
       
    # Create pyvis network object with screen height and width to match user
    wid, hei= size()
    nt = Network(width='{}px'.format(wid), height='{}px'.format(hei), bgcolor="#031101")
    nt.from_nx(G)
    
    ## Set edge width to 2
    ## [Note: will not be applicable for all sector sizes, 
    ##        need to set relative sizes based on input features]
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


def dynamic_sector_3d(system_data, sector_map):
    """Generates 3D sector map based on data provided by the user."""
    
    # Load dependencies
    import pandas as pd
    import networkx as nx
    import plotly.graph_objects as go
    from PIL import Image
    from IPython.display import HTML
    
    # Update data ready for visualization
    system_data['shape'] = set_color_shape_image(system_data['type'])['shape']
    system_data['image'] = set_color_shape_image(system_data['type'])['image']

    system_data['description_html'] = wrap_description(system_data['description'])['html']
        
    sector_map['color'] = set_edge_color_type(sector_map['type'])['color']
    sector_map['dashes'] = set_edge_color_type(sector_map['type'])['updbl']
    
    # Create networkx graph object from sector_map input
    G = nx.from_pandas_edgelist(sector_map, 'source', 'target', edge_attr=['weight', 'type', 'color'])

    # Set attributes of astronomical objects
    if 'x' and 'y' and 'z' in system_data.columns:
        for _, row in system_data.iterrows():
            nx.set_node_attributes(G, {row['label']: {'value': row['value'], 
                                                     'type': row['type'], 
                                                     'x': row['x']*50, 
                                                     'y': row['y']*-50, 
                                                     'z': row['z']*50,
                                                     'title': row['description_html'], 
                                                     'shape': row['shape'],
                                                     'font': {'color': '#8bad6b', 'face': 'Serif'}
                                                    }})
    else:
        for _, row in system_data.iterrows():
            nx.set_node_attributes(G, {row['label']: {'value': row['value'], 
                                                     'type': row['type'], 
                                                     'title': row['description_html'], 
                                                     'shape': row['shape'],
                                                     'font': {'color': '#8bad6b', 'face': 'Serif'}
                                                    }})
        
    # Invert edge weights
    for u, v, data in G.edges(data=True):
        data['weight'] = 1 / data['weight']
        
    # Resize astronomical objects to vaguely resemble relative size of sun and planets
    # [Note: will not be applicable for all sector sizes, 
    #        need to set relative sizes based on input features]
    sizes = []
    for n in G.nodes:
        if G.nodes[n]['type']=='Sun':
            sizes.append(G.nodes[n]['value'] * 2000)
        else:    
            sizes.append(G.nodes[n]['value'] * 140000)
            
    # If / else statement that extracts layout from data or automatically generates layout
    if 'x' and 'y' and 'z' in system_data.columns:
        tmp = [{n:[G.nodes[n]['x'], G.nodes[n]['y'], G.nodes[n]['z']]} for n in G.nodes]
        pos = {}
        for d in tmp:
            pos.update(d)
    else:
        pos = nx.spring_layout(G, dim=3)
           
    # Generate colors for astronomical objects
    colors = []
    for n in G.nodes: 
        if G.nodes[n]['type']=='Sun':
            colors.append(random_yellow_hex())
        else: 
            colors.append(random_earthy_hex())
            
    # Extract edge colors
    edge_cols = flatten([[G.edges[edge]['color'], 
                          G.edges[edge]['color'], 
                          G.edges[edge]['color']] for edge in G.edges])
    
    # Create plotly graph object
    x_nodes = [G.nodes[n]['x'] for n in G.nodes]
    y_nodes = [G.nodes[n]['y'] for n in G.nodes]
    z_nodes = [G.nodes[n]['z'] for n in G.nodes]
    
    edge_x = []
    edge_y = []
    edge_z = []
    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])
        
    edge_trace = go.Scatter3d(x=edge_x, y=edge_y, z=edge_z,
                              mode='lines',
                              line=dict(color=edge_cols,
                                        width=5),
                              opacity=0.3,
                              hoverinfo='none')
    
    node_trace = go.Scatter3d(x=x_nodes, y=y_nodes, z=z_nodes,
                              mode='markers',
                              marker=dict(size=sizes, 
                                          color=colors),
                              hoverinfo='text',
                              text=["<b>" + str(x) + "</b> (" + str(G.nodes[x]['type']) + ")<br><br>" + G.nodes[x]['title'] for x in G.nodes]
                              )

    layout = go.Layout(scene=dict(xaxis=dict(visible=False,
                                             range=[min(x_nodes), max(x_nodes)]),
                                  yaxis=dict(visible=False,
                                             range=[min(y_nodes), max(y_nodes)]),
                                  zaxis=dict(visible=False,
                                             range=[min(z_nodes), max(z_nodes)])),
                       paper_bgcolor='rgba(0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)')
    
    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    fig.update(layout_showlegend=False) 
    fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False)
    fig.update_layout(autosize=True,
                      width=None,
                      height=None,
                      hoverlabel=dict(bgcolor="#000d03",
                                      font_size=16,
                                      font_family="Courier New"))
    
    # Convert plotly graph object to html and return html object
    html_string = fig.to_html(full_html=False)
    
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Nyxal's Reach</title>
    </head>
    <body style="background-color:black;">
    <div style="display: flex; justify-content: center;">
        {plot_div}
    </div>
    </body>
    </html>
    """
    return html_template.format(plot_div=html_string)