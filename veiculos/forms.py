from datetime import datetime
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

from veiculos.models import Veiculo, Automovel, Onibus, TipoVeiculo


class DateInput(forms.DateInput):
    pass


class VeiculoForm(forms.ModelForm):
    placa = forms.CharField(max_length=7, required=True)
    dataProxManut = forms.DateField(required=True, label='Data da próxima manutenção',
                                    widget=forms.DateInput(attrs={'type': 'date', 'value': datetime.now().date}))
    disponivel = forms.BooleanField(initial=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            veiculo = Veiculo.objects.get(tipoVeiculo=self.instance)

            self.fields['placa'].initial = veiculo.placa
            self.fields['dataProxManut'].initial = veiculo.dataProxManut.strftime('%Y-%m-%d')
            self.fields['disponivel'].initial = veiculo.disponivel

    def clean(self):
        errors = {}
        data = self.cleaned_data
        placa = data.get('placa', None)
        dataProxManut = data.get('dataProxManut', None)

        if placa:
            if len(placa) != 7:
                errors['placa'] = 'Placa deve possuir 7 dígitos'

            if Veiculo.objects.filter(placa=placa).exists():
                errors['placa'] = 'Essa placa já está cadastrada'

        if dataProxManut and (dataProxManut - (datetime.now().date())).days <= 0:
            errors['dataProxManut'] = 'A data não deve ser igual a hoje, ou antiga'

        if len(errors.keys()) > 0:
            raise forms.ValidationError(errors)

        return data


class AutomovelForm(VeiculoForm):
    class Meta:
        model = Automovel
        fields = '__all__'

    def clean(self):
        data = super().clean()

        errors = {}
        nome = data.get('nome', None)

        if not (self.instance and self.instance.pk):
            if nome and TipoVeiculo.objects.filter(nome=nome.strip()).exists():
                errors['nome'] = 'Nome já existe'

        if len(errors.keys()) > 0:
            raise forms.ValidationError(errors)

        return data

    def save(self, commit=True):
        data = self.cleaned_data
        veiculo = super().save(commit=False)

        if not veiculo.id:
            automovel = Automovel.objects.create(
                nome=veiculo.nome.strip(),
                arCond=veiculo.arCond,
                numPortas=veiculo.numPortas,
                dirHidraulica=veiculo.dirHidraulica,
                cambioAuto=veiculo.cambioAuto,
            )

            veiculoObject = Veiculo.objects.create(
                tipoVeiculo=automovel,
                placa=data['placa'],
                dataProxManut=data['dataProxManut'],
                disponivel=data['disponivel'],
            )

            automovel.save()
            veiculoObject.save()

            return automovel
        else:
            veiculoObject = Veiculo.objects.get(tipoVeiculo=veiculo)

            veiculoObject.placa = data['placa']
            veiculoObject.dataProxManut = data['dataProxManut']
            veiculoObject.disponivel = data['disponivel']

            veiculo.save()
            veiculoObject.save()

            return veiculo


class OnibusForm(VeiculoForm):
    class Meta:
        model = Onibus
        fields = '__all__'

    def clean(self):
        data = super().clean()

        errors = {}
        nome = data.get('nome', None)

        if not (self.instance and self.instance.pk):
            if nome and TipoVeiculo.objects.filter(nome=nome.strip()).exists():
                errors['nome'] = 'Nome já existe'

        if len(errors.keys()) > 0:
            raise forms.ValidationError(errors)

        return data

    def save(self, commit=True):
        data = self.cleaned_data
        veiculo = super().save(commit=False)

        if not veiculo.id:
            onibus = Automovel.objects.create(
                nome=veiculo.nome.strip(),
                arCond=veiculo.arCond,
                numPortas=veiculo.numPassageiros,
                dirHidraulica=veiculo.leito,
                cambioAuto=veiculo.sanitario,
            )

            veiculoObject = Veiculo.objects.create(
                tipoVeiculo=onibus,
                placa=data['placa'],
                dataProxManut=data['dataProxManut'],
                disponivel=data['disponivel'],
            )

            onibus.save()
            veiculoObject.save()

            return onibus

        else:
            veiculoObject = Veiculo.objects.get(tipoVeiculo=veiculo)

            veiculoObject.placa = data['placa']
            veiculoObject.dataProxManut = data['dataProxManut']
            veiculoObject.disponivel = data['disponivel']

            veiculo.save()
            veiculoObject.save()

            return veiculo


class CadUsuarioForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']