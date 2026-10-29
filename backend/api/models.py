from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'clientes'

    def __str__(self):
        return f'{self.nome} ({self.cpf})'


class Veiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    cor = models.CharField(max_length=30)
    # init.sql: REFERENCES clientes(id) ON DELETE CASCADE
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    class Meta:
        db_table = 'veiculos'

    def __str__(self):
        return self.placa


class Vaga(models.Model):
    TIPO_CHOICES = [
        ('CARRO', 'Carro'),
        ('MOTO', 'Moto'),
    ]
    STATUS_CHOICES = [
        ('LIVRE', 'Livre'),
        ('OCUPADA', 'Ocupada'),
    ]

    numero = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=5, choices=TIPO_CHOICES)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='LIVRE')

    class Meta:
        db_table = 'vagas'

    def __str__(self):
        return self.numero


class Permanencia(models.Model):
    STATUS_CHOICES = [
        ('ABERTO', 'Aberto'),
        ('FINALIZADO', 'Finalizado'),
    ]

    # init.sql: FKs sem ON DELETE, ou seja, o banco bloqueia a exclusão
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT)
    vaga = models.ForeignKey(Vaga, on_delete=models.PROTECT)
    data_hora_entrada = models.DateTimeField()
    data_hora_saida = models.DateTimeField(null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ABERTO')

    class Meta:
        db_table = 'permanencias'

    def __str__(self):
        return f'Permanência {self.pk} - {self.status}'
