from .models import Categoria, Conta, MetaFinanceira, OrcamentoMensal, Transacao


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
    transacao.save()
    return transacao


def usuario_possui_conta_ativa(usuario):
    return Conta.objects.filter(usuario=usuario, ativa=True).exists()


def remover_recurso_do_usuario(model_class, recurso_id, usuario):
    recurso = model_class.objects.get(id=recurso_id, usuario=usuario)
    recurso.delete()
    return recurso
