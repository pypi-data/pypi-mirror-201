from hibeedb import migrations


class Migration(migrations.Migration):
    operations = [migrations.RunPython(migrations.RunPython.noop)]
