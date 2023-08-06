from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.apps import apps

from df_permission.permissions import DFMethods
from df_permission.variables import prefix


class Command(BaseCommand):
    @staticmethod
    def get_fields(model):
        fields = model._meta.get_fields()
        return fields

    def handle(self, *args, **options):
        models = apps.get_models()
        permission_objects = []
        actions = [DFMethods.CREATE, DFMethods.UPDATE, DFMethods.RETRIEVE, DFMethods.LIST, DFMethods.DESTROY]

        for model in models:
            # get app name
            app_label = model._meta.app_label

            # get model name
            model_name = model._meta.model_name

            content_type = ContentType.objects.get(app_label=app_label, model=model_name)

            fields = self.get_fields(model)

            if Permission.objects.filter(content_type=content_type, name__startswith=prefix).exists():
                """
                Joriy model uchun custom permissionlar bazada qo'shilganligini tekshiradi
                """
                codenames = list(
                    Permission.objects.filter(content_type=content_type, name__startswith=prefix).values_list(
                        'codename', flat=True))
                for action in actions:
                    for field in fields:
                        codename = f'{action}--{model_name}--{field.name}'
                        name = f'{prefix} {action.capitalize()} {str(model_name).capitalize()} {field.name}'
                        if codename not in codenames:
                            permission_objects.append(
                                Permission(codename=codename, name=name, content_type=content_type))

                    codename = f'{action}--{model_name}'
                    name = f'{prefix} {action.capitalize()} {str(model_name).capitalize()}'
                    if codename not in codenames:
                        permission_objects.append(Permission(codename=codename, name=name, content_type=content_type))
            else:
                for action in actions:
                    for field in fields:
                        codename = f'{action}--{model_name}--{field.name}'
                        name = f'{prefix} {action.capitalize()} {str(model_name).capitalize()} {field.name}'
                        permission_objects.append(Permission(codename=codename, name=name, content_type=content_type))

                    codename = f'{action}--{model_name}'
                    name = f'{prefix} {action.capitalize()} {str(model_name).capitalize()}'
                    permission_objects.append(Permission(codename=codename, name=name, content_type=content_type))

        if len(permission_objects) > 0:
            Permission.objects.bulk_create(permission_objects)
