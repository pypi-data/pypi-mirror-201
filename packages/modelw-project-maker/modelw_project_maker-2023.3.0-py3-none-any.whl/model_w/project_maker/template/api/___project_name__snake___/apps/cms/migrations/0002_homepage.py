# Generated by Django 4.1.2 on 2022-10-21 00:20
import django.db.models.deletion
from django.apps import AppConfig
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import migrations, models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def forward(apps: AppConfig, schema_editor: BaseDatabaseSchemaEditor):
    """
    By default the root page of Wagtail will be a plain Page object, which is
    a tiny bit annoying since we might want to add some fields there. Since we
    define a HomePage model in our cms app, here we hijack that root page's
    DB representation to switch it into a HomePage.

    This way you get an easy way to start coding your Wagtail site without
    having to subvert the root page manually!

    Drawback is of course that all fields of the home page will have to be
    nullable or have a default. If you don't like it well feel free to drop
    this migration and do whatever you want.
    """

    WagtailSite = apps.get_model("wagtailcore.Site")  # noqa
    Page = apps.get_model("wagtailcore.Page")  # noqa
    HomePage = apps.get_model("cms.HomePage")  # noqa

    site = WagtailSite.objects.get()
    root = site.root_page

    ct = ContentType.objects.get_for_model(HomePage)
    Page.objects.filter(pk=root.pk).update(
        content_type_id=ct.pk,
        title=settings.WAGTAIL_SITE_NAME,
    )

    with schema_editor.connection.cursor() as cur:
        cur.execute("insert into cms_homepage (page_ptr_id) values (%s)", [root.pk])


def backward(apps: AppConfig, _):
    """
    Revert our HomePage into a normal Page.
    """

    WagtailSite = apps.get_model("wagtailcore.Site")  # noqa
    Page = apps.get_model("wagtailcore.Page")  # noqa

    site = WagtailSite.objects.get()
    root = site.root_page

    ct = ContentType.objects.get_for_model(Page)
    Page.objects.filter(pk=root.pk).update(content_type_id=ct.pk)


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0077_alter_revision_user"),
        ("cms", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.RunPython(forward, backward),
    ]
