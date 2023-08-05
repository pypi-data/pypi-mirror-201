from django.urls import path
from django.utils.translation import pgettext_lazy as _
from djangocms_blog.settings import get_setting
from djangocms_blog.urls import urlpatterns as original_patterns

from .views import AgendaAndPostListView, AgendaDetailView, AgendaPreviousEventsListView


def get_agenda_urls():
    urls = get_setting("PERMALINK_URLS")
    details = []  # noqa: FURB138
    for urlconf in urls.values():
        details.append(
            path(urlconf, AgendaDetailView.as_view(), name="agenda-detail"),
        )
    return details


agenda_detail_urls = get_agenda_urls()

# Here are the patched urls that still includes the original urlpattern of djangocms_blog.
# But it also adds an AgendaDetailView and a AgendaAndPostListView (that replace the original PostListView).

urlpatterns = (
    [
        path(
            _("past/", "agenda_view_url"),
            AgendaPreviousEventsListView.as_view(),
            name="agenda-previous-events",
        ),
        path("", AgendaAndPostListView.as_view(), name="agenda-coming-soon"),
    ]
    + agenda_detail_urls
    + original_patterns
)
