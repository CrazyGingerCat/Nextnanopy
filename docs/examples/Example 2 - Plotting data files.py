#!/usr/bin/env python
# coding: utf-8

# # Welcome to nextnanopy !
# 
# ## About this example: load a data file and make a simple plot
# 
# Our starting point is that there is no need for the user to know how the raw data is structure in the different data files like bandedges.dat or potential.fld. 
# 
# Therefore, our goal is to achieve the most user-friendly way to load all the information stored in any data file generated by nextnano products (nextnano++, nextnano3, nextnano.NEGF or nextnano.MSB).
# 
# Note: loading for nextnano.MSB data files is not implemented yet.
# 
# 
# ## How to load a data file?
# 
# The simplest way is to use an universal class, ```nextnanopy.DataFile``` for any data file, like the following case:
# 
# 
# ```python
# datafile = nextnanopy.DataFile(path_to_file, product = 'nextnano++')
# ```
# 
# This object contains all the relevant information of the data file:
# - coordinates (or independent variables) like x, y, z, position
# - variables (or dependent variables) like bandedges, electric field, density of electrons, energy levels, etc
# - product (str): nextnano++, nextnano3, nextnano.NEGF or nextnano.MSB
# 
# In the case shown above, ```datafile``` was created by specifying ```product = 'nextnano++'```. This helps the class to look for the best loading routine for files generated by nextnano++. It will detect the dimension of the simulation (1D, 2D, 3D) and the file format (.dat, .fld, .txt), so it will choose the proper loading routine.
# 
# For example:
# 
# ```python
# datafile_1d = nextnanopy.DataFile('bandedges_1d.dat', product = 'nextnano++') # 1D .dat file
# datafile_2d = nextnanopy.DataFile('bandedges_2d.fld', product = 'nextnano++') # 2D .fld file
# ```
# 
# In the case of ```bandedges_1d.dat```, there is one coordinate (x) and there are several variables (gamma band, electron fermi level, hole fermi level, etc). The structure in this file is a set of columns with a tabulator as delimiter.
# 
# On the other hand, ```bandedges_2d.fld```, there are two coordinates (x and y) and also with several variables. Moreover, the structure of the raw data is organized in a totally different way than ```bandedges_1d.dat```. 
# 
# The user-friendlyness relies on the fact that in spite of the differences in the file formats, an unique class is used to load the information: ```nextnanopy.Datafile```.
# 
# As a remark, you can omit the argument ```product```. In this case, it will try to detect automatically the nextnano product (nextnano++, nextnano3, nextnano.NEGF or nextnano.MSB), and then look for the best loading routine. This can be dangerous since it is not garanteed that the loaded data is correct. So, we recommend to always specify ```product```.
# 

# ## Example of a 1D nextnano++ simulation

# In[1]:


import nextnanopy as nn

datafile_1d = nn.DataFile(r'E:\junliang.wang\datafiles\nextnano++\bandedges_1d.dat',product='nextnano++')


# ## How to access to the coordinates?
# 
# You can access to the coordinates in ```datafile.coords```. It will return a dictionary of ```Coord``` objects.
# 
# ```Coord``` objects contains information about:
# - name (str)
# - value (numpy.array)
# - unit (str)
# - dim (int)
# - label (str, optional)
# - metadata (dict, if there is any)
# 
# Each information is an attribute. For example, if you want to get the unit a coordinate:
# 
# ```python
# datafile.coords['x'].unit
# ```

# In[2]:


print(f"List of coordinates in the current datafile: {datafile_1d.coords}")


# In[3]:


x = datafile_1d.coords['x']
print(f"coord 'x' - name: {x.name}")
print(f"coord 'x' - value (shape): {x.value.shape}")
print(f"coord 'x' - unit: {x.unit}")
print(f"coord 'x' - dim: {x.dim}")
print(f"coord 'x' - label: {x.label}")
print(f"coord 'x' - metadata: {x.metadata}")


# In[4]:


print(f"coord 'x' - value:")
print(x.value)


# ## How to access to the variables?
# 
# Similarly, you can access to the dependent variables in ```datafile.variables```. It will return a dictionary of ```Variables``` objects.
# 
# ```Variables``` objects contains information about:
# - name (str)
# - value (np.array)
# - unit (str)
# - label (str, optional)
# - metadata (dict, if there is any)
# 
# As for ```Coords```, each information is an attribute. For example, if you want to get the unit:
# 
# ```python
# datafile.varaibles['Gamma'].unit
# ```

# In[5]:


print(f"List of variables in the current datafile: {datafile_1d.variables}")


# In[6]:


key = 'Gamma'
var = datafile_1d.variables[key]
print(f"variables '{key}' - name: {var.name}")
print(f"variables '{key}' - value (shape): {var.value.shape}")
print(f"variables '{key}' - unit: {var.unit}")
print(f"variables '{key}' - label: {var.label}")
print(f"variables '{key}' - metadata: {var.metadata}")


# In[7]:


print(f"variables '{key}' - value:")
print(var.value)


# ## Simple plot
# 
# As an example, we are going to plot together the gamma band and the electron fermi level. In this example, the data corresponds to a simulation of a GaAs heterostructure.
# 
# For this example, we will you ```matplotlib```, but you can use any other package!

# In[8]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'notebook')

fig, ax = plt.subplots(1)
x = datafile_1d.coords['x']
gamma = datafile_1d.variables['Gamma']
efermi = datafile_1d.variables['electron_Fermi_level']

ax.plot(x.value,gamma.value,label=gamma.name)
ax.plot(x.value,efermi.value, label=efermi.name)

ax.set_xlabel(f"{x.name} ({x.unit})")
ax.set_ylabel(f"Energy ({gamma.unit})")
ax.legend()
fig.tight_layout()


# ## Example of data file from a 2D simulation
# 
# By using the same methods, we can access to the coordinates and the variables of a totally different data file.
# 
# Here, the data also corresponds to a GaAs heterostructure, but now we will plot the gamma band in the x and the y directions.

# In[9]:


datafile_2d = nn.DataFile(r'E:\junliang.wang\datafiles\nextnano++\bandedges_2d.fld',product='nextnano++')


# ## Now there will be two coordinates: x and y

# In[10]:


print(f"List of coordinates in the current datafile: {datafile_2d.coords}")


# ## Variables can be accessed by the same method

# In[11]:


print(f"List of variables in the current datafile: {datafile_2d.variables}")


# ## You can verify that the number of points are correct

# In[12]:


print(f"coord 'x' - value (shape): {datafile_2d.coords['x'].value.shape}")
print(f"coord 'y' - value (shape): {datafile_2d.coords['y'].value.shape}")
print(f"variables 'Gamma' - value (shape): {datafile_2d.variables['Gamma'].value.shape}")


# ## Let's make a simple color map!

# In[13]:


x=datafile_2d.coords['x']
y=datafile_2d.coords['y']
z=datafile_2d.variables['Gamma']

fig, ax = plt.subplots(1)
pcolor = ax.pcolormesh(x.value,y.value,z.value.T)
cbar = fig.colorbar(pcolor)
cbar.set_label(f"{z.name} ({z.unit})")

ax.set_xlabel(f"{x.name} ({x.unit})")
ax.set_ylabel(f"{y.name} ({y.unit})")

fig.tight_layout()


# Please, contact python@nextnano.com for any issue with this example.
