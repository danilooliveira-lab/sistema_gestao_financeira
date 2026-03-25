from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("financeiro", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="categoria",
            options={"ordering": ["nome"]},
        ),
        migrations.AlterModelOptions(
            name="transacao",
            options={"ordering": ["-data", "-id"]},
        ),
        migrations.AlterUniqueTogether(
            name="categoria",
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name="categoria",
            constraint=models.UniqueConstraint(fields=("nome", "usuario"), name="unique_categoria_por_usuario"),
        ),
    ]
