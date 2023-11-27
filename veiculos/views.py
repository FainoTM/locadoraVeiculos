from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView
from django.contrib import messages
from veiculos.forms import CadUsuarioForm
from veiculos.models import Veiculo, TipoVeiculo
from django.contrib.auth.models import User

class HomeView(ListView):
    template_name = 'index.html'
    queryset = TipoVeiculo.tipoquery.all()
    context_object_name = 'cars'


class CadUsuarioView(FormView):
    template_name = 'usuario/cadastro.html'
    form_class = CadUsuarioForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, message='Usuario Cadastrado!!!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível cadastrar')
        redirect('cadusuario')


class LoginUserView(FormView):
    template_name = 'usuario/login.html'
    model = User
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        senha = form.cleaned_data['password']
        usuario = authenticate(self.request, username = username, password = senha)
        if usuario is not None:
            login(self.request, usuario)
            return redirect('listarposts')
        messages.error(self.request, 'Usuário não cadastrado')
        return redirect('loginuser')

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível logar')
        return redirect('loginuser')


class LogoutUserView(LoginRequiredMixin, LogoutView):

    def get(self, request):
        logout(request)
        return redirect('home')
