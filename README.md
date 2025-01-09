<hr>
<body>
<h1><img src="https://github.com/thomasbryansmith/DynamicSector/blob/main/assets/logo_white.png?raw=true" 
  style="width:50%;display: block; margin: auto;"
  alt="Dynamic Sector Logo"></h1>

The DynamicSector python library is intended as a support module for science fiction or otherwise intergalactic roleplaying games. It takes topological 'network' data, presently in the form of vector attribute and edge list Pandas data frames, converts the data into a NetworkX object, and visualizes the results as either a 2D or 3D 'star map'. The resulting visualizations are navigable using a mouse and keyboard and includes tooltips describing each of the planets and stars - assuming the descriptions are provided.

<hr>

Input data describing the astronomical objects in your system should adhere to the following data structure:  

<img src="https://github.com/thomasbryansmith/DynamicSector/blob/main/assets/system_data_example.png?raw=true" 
  style="width:75%;display: block; margin: auto;"
  alt="Dynamic Sector Logo">
  
+ <i><b>label</b></i> indicates the name of the astronomical object.
+ <i><b>type</b></i> encodes the type of astral body (and currently accepts 'Sun' or 'Planet').
+ <i><b>value</b></i> encodes the size of the planet in Astronomical Units.
+ <i><b>threat level</b></i> indicates the dangerousness of the planet.
+ <i><b>x</b></i>, <i><b>y</b></i>, and <i><b>z</b></i> are the coordinates of each planet.
  + These parameters are optional, and can be automatically inferred by a network layout algorithm if necessary.
+ <i><b>description</b></i> should be a string containing a brief description  of the astronomical object.

<hr>

Input data describing the sector map (i.e., the traversible pathways between the astronomical objects) should adhere to an edge list structure:

<img src="https://github.com/thomasbryansmith/DynamicSector/blob/main/assets/sector_map_example.png?raw=true" 
  style="width:55%;display: block; margin: auto;"
  alt="Dynamic Sector Logo">
  
<hr>
