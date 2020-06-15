# ccf-widget

[![Binder](http://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/NeurodataWithoutBorders/ccf-widget/master?urlpath=lab/tree/examples%2FStructureTreeNavigation.ipynb)

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
