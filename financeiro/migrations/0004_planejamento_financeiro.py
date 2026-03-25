import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("financeiro", "0003_expandir_dominio_financeiro"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MetaFinanceira",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=120)),
                ("valor_alvo", models.DecimalField(decimal_places=2, max_digits=12)),
                ("valor_atual", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("prazo", models.DateField(blank=True, null=True)),
                ("status", models.CharField(choices=[("ativa", "Ativa"), ("concluida", "Concluida"), ("pausada", "Pausada")], default="ativa", max_length=12)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
                ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["status", "prazo", "nome"],
            },
        ),
        migrations.CreateModel(
            name="OrcamentoMensal",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ano", models.PositiveIntegerField()),
                ("mes", models.PositiveSmallIntegerField()),
                ("limite", models.DecimalField(decimal_places=2, max_digits=10)),
                ("observacao", models.CharField(blank=True, max_length=255)),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
                ("categoria", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="financeiro.categoria")),
                ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-ano", "-mes", "categoria__nome"],
            },
        ),
        migrations.AddConstraint(
            model_name="orcamentomensal",
            constraint=models.UniqueConstraint(fields=("usuario", "categoria", "ano", "mes"), name="unique_orcamento_categoria_periodo"),
        ),
    ]
