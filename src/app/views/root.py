"""
root
"""
import logging

from app.views import TemplatedView
from app.domain.process_csv import parse_csv
from app.domain.format import format_email_text
from app.domain.salutations import clever_greeting, clever_farewell

class MainView(TemplatedView):
    """
    Main entry point for the app
    """

    def get(self, **context):
        self.render_response("index.html", **context)

    def post(self, **context):
        subject = self.request.POST.get("subject")
        issues = self.request.POST.get("issues")
        projects = self.request.POST.get("projects")
        chosen_font = self.request.POST.get("chosen_font")

        issue_list = parse_csv(issues)

        project_list = [project.strip() for project in projects.split(',')]

        email_html = format_email_text(issue_list, project_list)

        context["email_subject"] = subject
        context["email_html"] = email_html
        context["clever_greeting"] = clever_greeting()
        context["clever_farewell"] = clever_farewell()
        context["font"] = chosen_font or "Tahoma"
        self.get(**context)
