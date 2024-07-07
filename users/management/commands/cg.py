from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from service_customer.models import Mailing, MailingAttempt
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Создание группы manager и назначение прав'

    def handle(self, *args, **kwargs):
        manager_group, created = Group.objects.get_or_create(name='manager')

        permissions = [
            {'codename': 'view_mailing', 'model': Mailing},
            {'codename': 'deactivate_mailing', 'model': Mailing},
            {'codename': 'view_all_mailings', 'model': Mailing},
            {'codename': 'view_mailing', 'model': MailingAttempt},
            {'codename': 'view_user', 'model': get_user_model()},
            {'codename': 'change_user', 'model': get_user_model()},
            {'codename': 'deactivate_user', 'model': get_user_model()},
            {'codename': 'view_all_users', 'model': get_user_model()},
        ]

        for perm in permissions:
            try:
                content_type = ContentType.objects.get_for_model(perm['model'])
                permission = Permission.objects.get(codename=perm['codename'], content_type=content_type)
                manager_group.permissions.add(permission)
                self.stdout.write(self.style.SUCCESS(f'Право "{permission.name}" добавлено в группу "manager"'))
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Право с codename {perm["codename"]} и content_type {content_type} не найдено'))

        self.stdout.write(self.style.SUCCESS('Группа manager успешно создана и права назначены'))
