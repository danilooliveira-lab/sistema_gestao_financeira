from .models import Categoria, Conta, MetaFinanceira, OrcamentoMensal, Transacao


CATEGORIAS_INICIAIS = [
    "Moradia e contas",
    "Alimentacao",
    "Transporte",
    "Saude",
    "Lazer",
    "Educacao",
    "Salario",
    "Freelance e extras",
    "Investimentos",
    "Outros",
]


def criar_conta_para_usuario(form, usuario):
    conta = form.save(commit=False)
    conta.usuario = usuario
    conta.save()
    return conta


def criar_categoria_para_usuario(form, usuario):
    categoria = form.save(commit=False)
    categoria.usuario = usuario
    categoria.save()
    return categoria


def obter_ou_criar_categoria_para_usuario(nome, usuario):
    categoria, _ = Categoria.objects.get_or_create(
        usuario=usuario,
        nome__iexact=nome,
        defaults={"nome": nome, "usuario": usuario},
    )
    if categoria.nome != nome and categoria.nome.lower() == nome.lower():
        return categoria
    return categoria


def garantir_categorias_iniciais(usuario):
    if Categoria.objects.filter(usuario=usuario).exists():
        return Categoria.objects.filter(usuario=usuario), False

    categorias = [
        Categoria(usuario=usuario, nome=nome)
        for nome in CATEGORIAS_INICIAIS
    ]
    Categoria.objects.bulk_create(categorias)
    return Categoria.objects.filter(usuario=usuario), True


def criar_orcamento_para_usuario(form, usuario):
    orcamento = form.save(commit=False)
    orcamento.usuario = usuario
    orcamento.save()
    return orcamento


def criar_meta_para_usuario(form, usuario):
    meta = form.save(commit=False)
    meta.usuario = usuario
    meta.save()
    return meta


def criar_transacao_para_usuario(form, usuario):
    transacao = form.save(commit=False)
    transacao.usuario = usuario
    nova_categoria = form.cleaned_data.get("nova_categoria")
    if nova_categoria:
        transacao.categoria = obter_ou_criar_categoria_para_usuario(nova_categoria, usuario)
    transacao.save()
    return transacao


def usuario_possui_conta_ativa(usuario):
    return Conta.objects.filter(usuario=usuario, ativa=True).exists()


def remover_recurso_do_usuario(model_class, recurso_id, usuario):
    recurso = model_class.objects.get(id=recurso_id, usuario=usuario)
    recurso.delete()
    return recurso
