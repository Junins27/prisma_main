import django.db.models.deletion
from django.db import migrations, models


def ensure_all_projects_are_classified(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    unclassified = list(
        Project.objects.filter(front__isnull=True)
        .order_by("pk")
        .values_list("pk", "title")[:20]
    )
    if unclassified:
        cases = ", ".join(f"#{pk} {title!r}" for pk, title in unclassified)
        raise RuntimeError(
            "Há cases legados sem uma frente reconhecível: "
            f"{cases}. Aplique primeiro até portfolio.0002_editorial_content, "
            "classifique esses cases como Marketing ou Tecnologia e então aplique "
            "portfolio.0003_project_front_required."
        )


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0002_editorial_content")]

    operations = [
        migrations.RunPython(
            ensure_all_projects_are_classified,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="project",
            name="front",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="projects",
                to="portfolio.businessfront",
                verbose_name="frente",
            ),
        )
    ]
