from django.shortcuts import render, redirect
from django.views import View
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
from . import models, forms
from django.contrib import messages


class ListaTesourosView(View):
    def get(self, request):
        lista_tesouros = models.Tesouro.objects.annotate(
            total=ExpressionWrapper(
                F('preco') * F('quantidade'),
                output_field=DecimalField(
                    max_digits=10,
                    decimal_places=2,
                    blank=True
                )
            )
        ).all()
        return render(
            request,
            template_name='lista_tesouros.html',
            context=dict(
                lista_tesouros=lista_tesouros,
                total_geral=lista_tesouros.aggregate(Sum('total'))['total__sum']
            )
        )


class SalvarTesouroView(View):
    def get(self, request):
        return render(
            request,
            template_name='salvar_tesouro.html',
            context=dict(
                form=forms.TesouroForm
            )
        )

    def post(self, request):
        form = forms.TesouroForm(request.POST, request.FILES)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Tesouro criado com sucesso!')
            form.save()
            return redirect('list')
        messages.add_message(request, messages.ERROR, 'Ocorreu um erro ao criar o tesouro!')
        return render(
            request,
            template_name='salvar_tesouro.html',
            context=dict(
                form=form
            )
        )
