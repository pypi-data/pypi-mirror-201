from django.contrib.auth.models import User
from django.db import models


class NovadataModel(models.Model):
    data_criacao = models.DateTimeField(
        verbose_name="Data de criação",
        auto_now_add=True,
    )

    data_atualizacao = models.DateTimeField(
        verbose_name="Data de atualização",
        auto_now=True,
    )

    usuario_criacao = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Usuário de criação",
        blank=True,
        null=True,
    )

    usuario_atualizacao = models.ForeignKey(
        User,
        related_name="%(class)s_requests_modified",
        verbose_name="Usuário de atualização",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        """Sobrescrita do método save para realizarmos ações personalizadas."""
        from crum import get_current_user

        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.usuario_criacao = user
        self.usuario_atualizacao = user

        super(NovadataModel, self).save(*args, **kwargs)
