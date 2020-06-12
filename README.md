# ccf-widget

## Installation

```
pip install ccf-widget
```

## Usage

In Jupyter:

```
from ccfwidget import CCFWidget
ccf = CCFWidget()
ccf
```

### Troubleshooting

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
