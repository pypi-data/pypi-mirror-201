try:
    from hibeecontrib.gis import admin
except ImportError:
    from hibeecontrib import admin

    admin.GISModelAdmin = admin.ModelAdmin
