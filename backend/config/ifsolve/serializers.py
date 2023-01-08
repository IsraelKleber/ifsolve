from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (Alternativa, Aluno, Area, Avaliacao,
                     Elaborador, Item, ItemAvaliacao, Resposta, Tag, Usuario)
from datetime import datetime


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    extra_data = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'extra_data']

    def get_extra_data(self, obj):
        tipo_usuario = ''
        if hasattr(obj.usuario, 'aluno'):
            tipo_usuario = 'aluno'
        elif hasattr(obj.usuario, 'elaborador'):
            tipo_usuario = 'elaborador'
        return {
            'tipo_usuario': tipo_usuario,
        }

    def get_id(self, obj):
        return obj.usuario.elaborador.id if hasattr(obj.usuario, 'elaborador') else obj.usuario.aluno.id


class AlunoSerializer(serializers.ModelSerializer):
    data_nascimento = serializers.DateField()
    nome_completo = serializers.CharField(max_length=100)

    def create(self, validated_data):
        username = UsuarioSerializer.__getitem__(self, "username").value
        nome_completo = UsuarioSerializer.__getitem__(self, "nome_completo").value
        senha = UsuarioSerializer.__getitem__(self, "password").value
        email = UsuarioSerializer.__getitem__(self, "email").value
        nascimento = UsuarioSerializer.__getitem__(
            self, "data_nascimento").value
        
        user = User.objects.create_user(
            username=username,
            password=senha,
            email=email,
        )
        aluno = Aluno()
        aluno.user = user
        aluno.data_nascimento = nascimento
        aluno.nome_completo = nome_completo
        aluno.save()
        return Response(UsuarioSerializer.data)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'data_nascimento', 'nome_completo']

class ElaboradorSerializer(serializers.ModelSerializer):
    data_nascimento = serializers.DateField()
    verificado = serializers.BooleanField()
    nome_completo = serializers.CharField(max_length=100)

    def create(self, validated_data):
        username = UsuarioSerializer.__getitem__(self, "username").value
        nome_completo = UsuarioSerializer.__getitem__(self, "nome_completo").value
        senha = UsuarioSerializer.__getitem__(self, "password").value
        email = UsuarioSerializer.__getitem__(self, "email").value
        nascimento = UsuarioSerializer.__getitem__(
            self, "data_nascimento").value
        verificado = UsuarioSerializer.__getitem__(self, "verificado").value
        user = User.objects.create_user(
            username=username,
            password=senha,
            email=email,
        )
        elaborador = Elaborador()
        elaborador.verificado = verificado
        elaborador.user = user
        elaborador.data_nascimento = nascimento
        elaborador.nome_completo = nome_completo
        elaborador.save()
        return Response(UsuarioSerializer.data)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'data_nascimento', 'verificado', 'nome_completo']

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class AlternativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    alternativa_a = AlternativaSerializer(required=False)
    alternativa_b = AlternativaSerializer(required=False)
    alternativa_c = AlternativaSerializer(required=False)
    alternativa_d = AlternativaSerializer(required=False)
    alternativa_e = AlternativaSerializer(required=False)
    data_publicacao = serializers.DateTimeField(required=False)
    tags = TagSerializer(required=False, many=True)

    def create(self, validated_data):
        item = Item.objects.create(
            elaborador=get_object_or_404(Elaborador, id=ItemSerializer.__getitem__(self, "elaborador").value),
            visibilidade=ItemSerializer.__getitem__(self, "visibilidade").value,
            area=Area.objects.get(id=ItemSerializer.__getitem__(self, "area").value),
            assunto=ItemSerializer.__getitem__(self, "assunto").value,
            titulo=ItemSerializer.__getitem__(self, "titulo").value,
            data_publicacao=datetime.now(),
            enunciado=ItemSerializer.__getitem__(self, "enunciado").value,
        )

        tipo = ItemSerializer.__getitem__(self, "tipo").value
        item.tipo = tipo

        if (tipo == "ME"):
            obj_a = ItemSerializer.__getitem__(self, "alternativa_a")
            obj_b = ItemSerializer.__getitem__(self, "alternativa_b")
            obj_c = ItemSerializer.__getitem__(self, "alternativa_c")
            obj_d = ItemSerializer.__getitem__(self, "alternativa_d")
            obj_e = ItemSerializer.__getitem__(self, "alternativa_e")

            alt_a = Alternativa.objects.create(texto=obj_a.__getitem__("texto").value, justificativa=obj_a.__getitem__("justificativa").value)
            alt_b = Alternativa.objects.create(texto=obj_b.__getitem__("texto").value, justificativa=obj_b.__getitem__("justificativa").value)
            item.alternativa_a = alt_a
            item.alternativa_b = alt_b

            if(obj_c):
                alt_c = Alternativa.objects.create(texto=obj_c.__getitem__("texto").value, justificativa=obj_c.__getitem__("justificativa").value)
                item.alternativa_c = alt_c
            
            if(obj_d):
                alt_d = Alternativa.objects.create(texto=obj_d.__getitem__("texto").value, justificativa=obj_d.__getitem__("justificativa").value)
                item.alternativa_d = alt_d
            
            if(obj_e):
                alt_e = Alternativa.objects.create(texto=obj_e.__getitem__("texto").value, justificativa=obj_e.__getitem__("justificativa").value)
                item.alternativa_e = alt_e

            item.alternativa_correta = ItemSerializer.__getitem__(
                self, "alternativa_correta").value

        elif (tipo == "DI"):
            item.expectativa_resposta = ItemSerializer.__getitem__(
                self, "expectativa_resposta").value

        id_coelaboradores = ItemSerializer.__getitem__(
            self, "co_elaboradores").value
        lista_tags = ItemSerializer.__getitem__(self, "tags").value
        texto_base = ItemSerializer.__getitem__(self, "texto_base").value

        for tag in lista_tags:
            if (Tag.objects.filter(nome=tag["nome"]).exists()):
                obj_tag = Tag.objects.get(nome=tag["nome"])
            else:
                obj_tag = Tag.objects.create(nome=tag["nome"])
            item.tags.add(obj_tag)

        if (id_coelaboradores != None):
            item.co_elaboradores.add(*id_coelaboradores)

        if (texto_base != None):
            item.texto_base = texto_base

        item.save()
        return Response(ItemSerializer.data)

    class Meta:
        model = Item
        fields = "__all__"

class ItemAvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemAvaliacao
        fields = "__all__"

class AvaliacaoSerializer(serializers.ModelSerializer):

    itens = ItemAvaliacaoSerializer(required=False, many=True)

    def create(self, validated_data):
        avaliacao = Avaliacao.objects.create(
            titulo = AvaliacaoSerializer.__getitem__(self, "titulo").value,
            descricao = AvaliacaoSerializer.__getitem__(self, "descricao").value,
            nota = AvaliacaoSerializer.__getitem__(self, "nota").value,
            visibilidade = AvaliacaoSerializer.__getitem__(self, "visibilidade").value,
            elaborador = get_object_or_404(Elaborador, id = AvaliacaoSerializer.__getitem__(self, "elaborador").value),
        )

        id_coelaboradores = AvaliacaoSerializer.__getitem__(self, "co_elaboradores").value
        if(id_coelaboradores != None):
            avaliacao.co_elaboradores.add(*id_coelaboradores)
        
        data_inicio = AvaliacaoSerializer.__getitem__(self, "data_inicio").value
        if(data_inicio != None):
            avaliacao.data_inicio = data_inicio
        
        data_fim = AvaliacaoSerializer.__getitem__(self, "data_fim").value
        if(data_fim != None):
            avaliacao.data_fim = data_fim
        
        id_alunos = AvaliacaoSerializer.__getitem__(self, "alunos").value
        if(id_alunos != None):
            avaliacao.alunos.add(*id_alunos)

        lista_itens = AvaliacaoSerializer.__getitem__(self, "itens").value

        for item in lista_itens:
            id_item = item["item"]
            obj_item = get_object_or_404(Item, id = id_item)
            item_avaliacao = ItemAvaliacao.objects.create(
                item = obj_item,
                avaliacao = avaliacao,
                numero_item = item["numero_item"],
                nota_item = item["nota_item"]
            )
            item_avaliacao.save()
        avaliacao.save()
        return Response(AvaliacaoSerializer.data)
        
    class Meta:
        model = Avaliacao
        fields = "__all__"


class RespostaSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

        resposta = Resposta.objects.create(
            aluno=Aluno.objects.get(
                id=RespostaSerializer.__getitem__(self, "aluno").value),
            resposta=RespostaSerializer.__getitem__(self, "resposta").value,
            data_hora=RespostaSerializer.__getitem__(self, "data_hora").value
        )

        item = Item.objects.get(
            id=RespostaSerializer.__getitem__(self, "item").value)
        item_avaliacao = RespostaSerializer.__getitem__(
            self, "item_avaliacao").value
        nota_obtida = RespostaSerializer.__getitem__(self, "nota_obtida").value

        if (item != None):
            resposta.item = item

        if (item_avaliacao != None):
            resposta.item_avaliacao = item_avaliacao

        if (nota_obtida != None):
            resposta.nota_obtida = nota_obtida

        resposta.save()
        return Response(RespostaSerializer.data)

    class Meta:
        model = Resposta
        fields = "__all__"