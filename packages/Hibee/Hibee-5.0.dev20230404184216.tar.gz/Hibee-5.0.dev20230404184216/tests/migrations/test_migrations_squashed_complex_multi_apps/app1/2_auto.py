from hibeedb import migrations


class Migration(migrations.Migration):
    dependencies = [("app1", "1_auto")]

    operations = [migrations.RunPython(migrations.RunPython.noop)]
