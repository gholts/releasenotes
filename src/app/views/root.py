"""
root
"""

from app.views import TemplatedView


class MainView(TemplatedView):
    """
    Yep
    """

    def get(self, **context):
        self.render_response("index.html", **context)