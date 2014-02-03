"""
root
"""

from app.views import TemplatedView
from app.domain.process_csv import parse_csv
from app.domain.format import format_email_text

class MainView(TemplatedView):
    """
    Main entry point for the app
    """

    def get(self, **context):
        """
        Get route for the main view
        """
        self.render_response("index.html", **context)

    def post(self, **context):
        """
        Post route for the main view
        """

        issues = self.request.POST.get("issues")
        projects = self.request.POST.get("projects")
        chosen_font = self.request.POST.get("chosen_font")
        chosen_font_size = self.request.POST.get("chosen_font_size")
        output_style = self.request.POST.get("format-choice")

        issue_list = parse_csv(issues)

        project_list = [project.strip() for project in projects.split(',')]

        email_html = format_email_text(issue_list, project_list, issue_format=output_style)

        context["email_html"] = email_html
        context["font"] = chosen_font
        context["font_size"] = chosen_font_size
        self.get(**context)


class AboutView(TemplatedView):
    """
    View for the about page
    """
    def get(self, **context):
        """
        Get route for the about view
        """
        self.render_response("about.html", **context)


class ContactView(TemplatedView):
    """
    View for the contact page
    """
    def get(self, **context):
        """
        Get route for the contact view
        """
        self.render_response("contact.html", **context)
