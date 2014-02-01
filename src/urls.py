"""
urls
"""

from webapp2 import Route, SimpleRoute

ROUTES = [
    #Foosball Ladder
    Route('/', handler='app.views.root.MainView'),
    Route('/about', handler='app.views.root.AboutView'),
    Route('/contact', handler='app.views.root.ContactView')
]