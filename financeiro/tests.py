from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import OrcamentoMensalForm, TransacaoForm
from .models import Categoria, Conta, MetaFinanceira, OrcamentoMensal, Transacao
from .selectors import filtrar_transacoes, paginar_queryset, resumo_dashboard


class FinanceiroViewsTests(TestCase):
    def setUp(self):
        self.today = timezone.localdate()
        self.user = User.objects.create_user(username="alice", password="senha-segura123")
        self.other_user = User.objects.create_user(username="bob", password="senha-segura123")
        self.conta_user = Conta.objects.create(nome="Nubank", tipo="corrente", saldo_inicial="500.00", usuario=self.user)
        self.conta_other = Conta.objects.create(nome="Inter", tipo="corrente", saldo_inicial="300.00", usuario=self.other_user)
        self.categoria_user = Categoria.objects.create(nome="Salario", usuario=self.user)
        self.categoria_other = Categoria.objects.create(nome="Mercado", usuario=self.other_user)
        self.transacao_user = Transacao.objects.create(
            usuario=self.user,
            conta=self.conta_user,
            descricao="Pagamento",
            valor="1000.00",
            data=date(self.today.year, self.today.month, 1),
            tipo="receita",
            categoria=self.categoria_user,
        )
        self.transacao_other = Transacao.objects.create(
            usuario=self.other_user,
            conta=self.conta_other,
            descricao="Compra",
            valor="200.00",
            data=date(self.today.year, self.today.month, 2),
            tipo="despesa",
            categoria=self.categoria_other,
        )
        self.orcamento = OrcamentoMensal.objects.create(
            usuario=self.user,
            categoria=self.categoria_user,
            ano=self.today.year,
            mes=self.today.month,
            limite="300.00",
        )
        self.meta = MetaFinanceira.objects.create(
            usuario=self.user,
            nome="Reserva de emergencia",
            valor_alvo="5000.00",
            valor_atual="1000.00",
            status="ativa",
        )

    def test_dashboard_exige_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_lista_transacoes_mostra_apenas_dados_do_usuario_logado(self):
        self.client.login(username="alice", password="senha-segura123")

        response = self.client.get(reverse("lista_transacoes"))

        self.assertEqual(response.status_code, 200)
        transacoes = list(response.context["transacoes"])
        self.assertEqual(transacoes, [self.transacao_user])

    def test_dashboard_exibe_patrimonio_com_saldo_inicial(self):
        self.client.login(username="alice", password="senha-segura123")

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["saldo_inicial_total"], self.conta_user.saldo_inicial)
        self.assertEqual(response.context["patrimonio_total"], self.conta_user.saldo_inicial + self.transacao_user.valor)

    def test_selector_resumo_dashboard_retorna_planejamento_e_metas(self):
        resumo = resumo_dashboard(self.user)

        self.assertEqual(resumo["total_receitas"], self.transacao_user.valor)
        self.assertEqual(len(resumo["orcamentos_resumo"]), 1)
        self.assertEqual(len(resumo["metas_resumo"]), 1)

    def test_categoria_duplicada_exibe_erro_amigavel(self):
        self.client.login(username="alice", password="senha-segura123")

        response = self.client.post(reverse("gerenciar_categorias"), {"nome": "salario"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Voce ja possui uma categoria com esse nome.")
        self.assertEqual(Categoria.objects.filter(usuario=self.user).count(), 1)

    def test_conta_duplicada_exibe_erro_amigavel(self):
        self.client.login(username="alice", password="senha-segura123")

        response = self.client.post(
            reverse("gerenciar_contas"),
            {"nome": "nubank", "tipo": "corrente", "saldo_inicial": "10.00", "ativa": True},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Voce ja possui uma conta com esse nome.")
        self.assertEqual(Conta.objects.filter(usuario=self.user).count(), 1)

    def test_orcamento_form_mostra_apenas_categorias_do_usuario(self):
        form = OrcamentoMensalForm(user=self.user)

        self.assertEqual(list(form.fields["categoria"].queryset), [self.categoria_user])

    def test_transacao_form_mostra_apenas_contas_e_categorias_do_usuario(self):
        form = TransacaoForm(user=self.user)

        self.assertEqual(list(form.fields["conta"].queryset), [self.conta_user])
        self.assertEqual(list(form.fields["categoria"].queryset), [self.categoria_user])

    def test_selector_filtra_transacoes_por_conta_tipo_e_recorrencia(self):
        Transacao.objects.create(
            usuario=self.user,
            conta=self.conta_user,
            descricao="Assinatura",
            valor="50.00",
            data=date(self.today.year, self.today.month, 5),
            tipo="despesa",
            categoria=self.categoria_user,
            recorrente=True,
        )

        queryset, filtros = filtrar_transacoes(
            self.user,
            {"conta": str(self.conta_user.id), "tipo": "despesa", "recorrente": "true", "q": "Assina"},
        )

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.first().descricao, "Assinatura")
        self.assertEqual(filtros["recorrente"], "true")

    def test_paginacao_de_transacoes_limita_resultados(self):
        for indice in range(12):
            Transacao.objects.create(
                usuario=self.user,
                conta=self.conta_user,
                descricao=f"Extra {indice}",
                valor="10.00",
                data=date(self.today.year, self.today.month, 10),
                tipo="receita",
                categoria=self.categoria_user,
            )

        queryset, _ = filtrar_transacoes(self.user, {})
        page_obj = paginar_queryset(queryset, page_number=2, per_page=8)

        self.assertEqual(page_obj.number, 2)
        self.assertGreaterEqual(page_obj.paginator.num_pages, 2)
        self.assertLessEqual(len(page_obj.object_list), 8)

    def test_deletar_categoria_aceita_apenas_post(self):
        self.client.login(username="alice", password="senha-segura123")

        response = self.client.get(reverse("deletar_categoria", args=[self.categoria_user.id]))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Categoria.objects.filter(id=self.categoria_user.id).exists())

    def test_usuario_nao_remove_transacao_de_outro_usuario(self):
        self.client.login(username="alice", password="senha-segura123")

        response = self.client.post(reverse("deletar_transacao", args=[self.transacao_other.id]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Transacao.objects.filter(id=self.transacao_other.id).exists())

    def test_adicionar_transacao_sem_conta_redireciona_para_contas(self):
        User.objects.create_user(username="charlie", password="senha-segura123")
        self.client.login(username="charlie", password="senha-segura123")

        response = self.client.get(reverse("adicionar_transacao"))

        self.assertRedirects(response, reverse("gerenciar_contas"))
