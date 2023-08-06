# pyplotbrookings <img src="figures/logo.png" align="right" width="120"/>

## Overview

`pyplotbrookings` is a `matplotlib` extension which implements the Brookings
Institution style guide. It offers several color palettes, a custom theme, and a few
helper functions. `pyplotbrookings` is a python implementation of `ggbrookings`, 
an R extension for `ggplot`.

## Installation

`pyplotbrookings` is now a python package! It downloaded from PyPI with `pip` (https://pypi.org/project/pyplotbrookings/0.1.0/)!
```
pip install pyplotbrookings==0.1.0
```

The accepted alias for `pyplotbrookings` is `ppb`. For example,
```python
import pyplotbrookings.pyplotbrookings as ppb
```

## Usage

The `pyplotbrookings` package has a few simple user facing functions:

-   `set_theme()` overrides the default `matplotlib` theme for a
    custom one which adheres to the Brookings style guide.

-   `get_palette()` returns the colors for a valid Brookings brand 
    palettes.

-   `set_palette()` sets the `matplotlib` color cycler to one of
    the Brookings brand palettes.

-   `get_cmap()` returns a continuous palette (or color map) using one of
    the color Brookings color palettes.

-   `view_palette()` helper function that previews a color palette
    showing the color, order, and the appropriate text color 
    that can be applied on top of each color.

-   `add_title()` adds titles and subtitles to a figure that are consistent 
    with Brookings brand guidelines. 

-   `add_notes()` adds notes to the bottom of a figure also consistent 
    with Brookings brand guidelines.

-   `add_logo()` adds a program/center logo to a figure.

-   `figure()` creates a `matplotlib` figure in one of the standard 
    Brookings sizes.

-   `save()` saves a figure in the Brookings advised dpi values depending
     on content type.


## Examples
Let's create a figure plot using `pyplotbrookings`. First we'll need some data

```python
import matplotlib.pyplot as plt
import pyplotbrookings.pyplotbrookings as ppb
import seaborn as sns

# Brookings plot theme for all plots
ppb.set_theme()

# Getting data
penguins = sns.load_dataset("penguins")
```

Now we can create a figure using the following 
```python
# Reversing data to get the correct z-order ordering of plots
ax = sns.histplot(data=penguins.iloc[::-1], 
                  x='bill_depth_mm', 
                  hue='species', 
                  # Setting the plot palette to Brookings brand2
                  palette=ppb.get_palette('brand2'), 
                  bins=20)

# Moving the legend in seaborn to the top
sns.move_legend(ax, "lower center", bbox_to_anchor=(.5, 1.05), ncol=3, title=None, frameon=False)
plt.xlabel('Bill Depth (mm)')

# Adding Brookings titles
ppb.add_title(title='Penguin Bill Depth', 
              subtitle='Bill Depth in mm of Adelie and Gentoo Penguins at Palmer Station LTER', 
              tag='FIGURE 1B')

# Adding notes
ppb.add_notes('Source: Palmer Station Antarctica LTER', 
              'Notes: Figure made using matplotlib')

ppb.add_logo('hc')
```

`pyplotbrookings` is designed to work with many different plots. Let's try creating a scatter plot that uses a colormap

```python
# Getting the Brookings sequential2 color map
cmap = ppb.get_cmap('sequential2', reverse=True)
# Creating a scatter plot
plt.scatter(data=penguins, x='bill_length_mm', y='bill_depth_mm', c='flipper_length_mm', cmap=cmap)

# Adding matplotlib legend/labels
plt.xlabel('Bill Length (mm)')
plt.ylabel('Bill Depth (mm)')

# Adding color bar
cbar = plt.colorbar(cmap=cmap)
cbar.set_label('Flipper Length (mm)')
cbar.outline.set_visible(False)

# Adding Brookings titles
ppb.add_title(title='Penguin Bills and Flippers', 
              subtitle='Bill length vs. Bill Depth vs. Flipper Length of Penguins at\nPalmer Station', 
              tag='FIGURE 2')

# Adding notes
ppb.add_notes('Source: Palmer Station Antarctica LTER',
              'Example: Here is some extra long text that\ngoes on and on and needs a linefeed.',
              'Notes: Figure made using matplotlib')

# Adding a CRM logo
ppb.add_logo('crm', scale=0.35, offsets=(-0.1, 0))
```

We could also create a box plot. Note that titles and notes auto-align to the left margin of the figure.
```python
# Creating a boxplot
sns.boxplot(data=penguins, x='bill_depth_mm', y='island', palette=ppb.get_palette('misc'))


# Adding Brookings titles
ppb.add_title(title='Penguin Bills Depth', 
              subtitle='Length of Penguin Bills on each Island', 
              tag='FIGURE 3')

# Adding notes
ppb.add_notes('Source: Palmer Station Antarctica LTER', 
              'Notes: Figure made using matplotlib')


# Adding matplotlib legend/labels
plt.xlabel('Bill Depth (mm)')
plt.ylabel('Island')

ppb.add_logo('crm', scale=0.35, offsets=(-0.1, 0))
```
