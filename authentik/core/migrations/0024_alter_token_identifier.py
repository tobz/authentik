# Generated by Django 3.2.3 on 2021-06-03 09:33

from django.apps.registry import Apps
from django.db import migrations, models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.models import Count


def fix_duplicates(apps: Apps, schema_editor: BaseDatabaseSchemaEditor):
    db_alias = schema_editor.connection.alias
    Token = apps.get_model("authentik_core", "token")
    identifiers = (
        Token.objects.using(db_alias)
        .values("identifier")
        .annotate(identifier_count=Count("identifier"))
        .filter(identifier_count__gt=1)
    )
    for ident in identifiers:
        Token.objects.using(db_alias).filter(identifier=ident["identifier"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("authentik_core", "0023_alter_application_meta_launch_url"),
    ]

    operations = [
        migrations.RunPython(fix_duplicates),
        migrations.AlterField(
            model_name="token",
            name="identifier",
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
