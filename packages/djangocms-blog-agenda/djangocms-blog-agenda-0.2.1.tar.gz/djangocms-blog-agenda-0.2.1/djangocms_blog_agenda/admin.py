from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import djangocms_blog.admin as blog_admin
from djangocms_blog.admin import PostAdmin
from djangocms_blog.models import Post

from .misc import get_inline_instances as patched_get_inline_instances
from .models import PostExtension


# replace PostAdmin get_inlines function in order to hide event_start_date on
# regular blog posts
PostAdmin.get_inline_instances = patched_get_inline_instances


class PostExtensionInline(admin.StackedInline):
    model = PostExtension
    fields = ["event_start_date", "event_end_date"]
    classes = []
    extra = 1
    can_delete = False
    verbose_name = _("Event infos")
    verbose_name_plural = _("Event infos")
    min_num = 1
    max_num = 1


blog_admin.register_extension(PostExtensionInline)


admin.site.unregister(Post)


@admin.register(Post)
class AgendaPostAdmin(PostAdmin):
    """Better layout of Post admin form"""

    _fieldsets = [
        (None, {"fields": ["title", "subtitle", "slug", "publish", "categories"]}),
        (
            _("Info"),
            {
                "fields": [
                    ["tags"],
                    ["date_published", "date_published_end"],
                    "app_config",
                ],
                "classes": ("collapse",),
            },
        ),
        (
            _("Images"),
            {
                "fields": [["main_image", "main_image_thumbnail", "main_image_full"]],
                "classes": ("collapse",),
            },
        ),
        (
            _("SEO"),
            {
                "fields": [["meta_description", "meta_title", "meta_keywords"]],
                "classes": ("collapse",),
            },
        ),
    ]
    _fieldset_extra_fields_position = {
        "sites": [0, 1],
        "abstract": [0, 1],
        "post_text": [0, 1],
        "author": [0, 1],
        "enable_liveblog": None,
        "related": [1, 1, 0],
    }
