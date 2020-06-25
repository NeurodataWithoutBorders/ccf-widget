# ccf-widget

Jupyter [ipywidget](https://ipywidgets.readthedocs.io/en/stable/) to
interactively explore the [Allen Mouse Brain Common Coordinate Framework
v3](https://doi.org/10.1016/j.cell.2020.04.007), plot dynamic markers, or cell
representations.  Couple with the
[nwb-jupyter-widgets](https://github.com/NeurodataWithoutBorders/nwb-jupyter-widgets)
for an understanding of electrophysiology.

[![Binder](http://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/NeurodataWithoutBorders/ccf-widget/master?filepath=examples%2FStructureTreeNavigation.ipynb)

![ccfwidget](https://i.imgur.com/Q4VY5du.gif)

## Installation

```
pip install ccfwidget
```

## Usage

In Jupyter:

```
from ccfwidget import CCFWidget
ccf = CCFWidget()
ccf
```

Examples on Binder:

- [Explore the structure tree](https://mybinder.org/v2/gh/NeurodataWithoutBorders/ccf-widget/master?filepath=examples%2FStructureTreeNavigation.ipynb)
- [Use markers to represent neuropixels](https://mybinder.org/v2/gh/NeurodataWithoutBorders/ccf-widget/master?filepath=examples%2FNeuropixelProbes.ipynb)

Additional examples:

- [Add a cell type morphology](./examples/CellTypes.ipynb)

## Troubleshooting

With the error:

```
[...]
IOPub message rate exceeded.
[...]
```

Start `jupyter` with the flag:

```
jupyter notebook --NotebookApp.iopub_msg_rate_limit=1e12
```

## Hacking

Contributions are welcome and appreciated.

To install an editable build:

```
python3 -m pip install flit
flit install --symlink
```
