import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("financeiro", "0002_update_categoria_constraint"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Conta",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=100)),
                ("tipo", models.CharField(choices=[("corrente", "Conta corrente"), ("poupanca", "Poupanca"), ("carteira", "Carteira"), ("investimento", "Investimento")], default="corrente", max_length=20)),
                ("saldo_inicial", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("ativa", models.BooleanField(default=True)),
                ("criada_em", models.DateTimeField(auto_now_add=True)),
                ("atualizada_em", models.DateTimeField(auto_now=True)),
                ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["nome"],
            },
        ),
        migrations.AddField(
            model_name="categoria",
            name="atualizada_em",
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="categoria",
            name="criada_em",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="transacao",
            name="atualizada_em",
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="transacao",
            name="conta",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="financeiro.conta"),
        ),
        migrations.AddField(
            model_name="transacao",
            name="criada_em",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="transacao",
            name="observacao",
            field=models.TextField(blank=True, default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="transacao",
            name="recorrente",
            field=models.BooleanField(default=False),
        ),
        migrations.AddConstraint(
            model_name="conta",
            constraint=models.UniqueConstraint(fields=("nome", "usuario"), name="unique_conta_por_usuario"),
        ),
    ]
