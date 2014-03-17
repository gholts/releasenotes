"""
urls
"""

from webapp2 import Route, SimpleRoute

ROUTES = [
    Route('/', handler='app.views.root.MainView'),
    Route('/about', handler='app.views.root.AboutView'),
    Route('/contact', handler='app.views.root.ContactView'),

    # APIs
    Route('/api/v1/issues/format/', handler='app.views.api.v1.issues.FormatApi')
]