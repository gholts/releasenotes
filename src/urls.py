"""
urls
"""

from webapp2 import Route, SimpleRoute

ROUTES = [
    #Foosball Ladder
    Route('/', handler='app.views.root.MainView'),
]