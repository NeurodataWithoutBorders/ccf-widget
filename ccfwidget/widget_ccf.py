__all__ = ['CCFWidget']

from ipywidgets import Widget

class CCFWidget(Widget):
    """A Jupyter widget for the Allen Common Coordinate Framework (CCF)
    Mouse Brain Atlas."""

    def __init__(self, **kwargs):
        super(CCFWidget, self).__init__(**kwargs)
