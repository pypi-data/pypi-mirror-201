from hibee.apps import apps as hibee_apps
from hibee.contrib.sitemaps import Sitemap
from hibee.core.exceptions import ImproperlyConfigured


class FlatPageSitemap(Sitemap):
    def items(self):
        if not hibee_apps.is_installed("hibee.contrib.sites"):
            raise ImproperlyConfigured(
                "FlatPageSitemap requires hibee.contrib.sites, which isn't installed."
            )
        Site = hibee_apps.get_model("sites.Site")
        current_site = Site.objects.get_current()
        return current_site.flatpage_set.filter(registration_required=False)
