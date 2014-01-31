from webapp2 import Route
from keys import KEY

routes = [
    Route(KEY.URL_ROOT, 'app.views.root.IndexView', KEY.URL_NAME_ROOT),
    Route(KEY.URL_SITEMAP_XML, 'app.views.meta.SitemapXmlHandler', KEY.URL_NAME_SITEMAP_XML),
]