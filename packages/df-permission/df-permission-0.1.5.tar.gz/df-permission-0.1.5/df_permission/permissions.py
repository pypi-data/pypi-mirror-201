from django.contrib.auth.models import Permission
from django.db import models
from django.db.models import Q
from rest_framework.permissions import BasePermission


class DFMethods:
    CREATE = 'create'
    UPDATE = 'update'
    RETRIEVE = 'retrieve'
    LIST = 'list'
    DESTROY = 'destroy'


def get_user_perms(request):
    """
    Get all user permissions
    """
    user = request.user
    user_perms = list(
        Permission.objects.filter(Q(user=user) | Q(group__user=user)).values_list('codename', flat=True))

    return user_perms


def has_perms(user_perms, required_perms):
    """
    Check user has required perms
    """
    return all(perm in user_perms for perm in required_perms)


class DFPermission(BasePermission):
    def _get_model_fields(self, view):
        """
        Get model fields
        """
        model = self._get_model(view)
        fields = [field.name for field in model._meta.get_fields()]
        return fields

    def _get_fields(self, view):
        """
        Fields is permission required and available in df_model
        """
        if hasattr(view, 'df_fields'):
            fields = view.df_fields
        elif hasattr(view, 'get_serializer'):
            serializer = view.get_serializer()
            serializer_fields = list(serializer.fields.keys())

            model_fields = self._get_model_fields(view)

            # get fields only available in model
            fields = [field for field in serializer_fields if field in model_fields]
        else:
            raise AttributeError('df_fields is required')

        return fields

    @staticmethod
    def _get_method(view):
        """
        Get and check method is valid
        """
        if not hasattr(view, 'df_method'):
            raise AttributeError('df_method is required')

        method = str(view.df_method).lower()

        if method not in [DFMethods.CREATE, DFMethods.UPDATE, DFMethods.RETRIEVE, DFMethods.LIST, DFMethods.DESTROY]:
            raise ValueError('df_method must be valid value')

        return view.df_method

    @staticmethod
    def _get_model(view):
        """
        Get and check model is valid
        """
        if not hasattr(view, 'df_model'):
            raise AttributeError('df_model is required')

        model = view.df_model

        if not issubclass(model, models.Model):
            raise ValueError('df_model is not model class')

        return model

    def _get_model_name(self, view):
        """
        Get model name
        """
        model = self._get_model(view)

        return str(model._meta.model_name).lower()

    def _get_required_perms(self, view, fields):
        """
        Required permissions for view
        """
        df_method = self._get_method(view)
        df_model = self._get_model_name(view)

        required_perms = [f'{df_method}--{df_model}--{field}' for field in fields]
        return required_perms

    @staticmethod
    def _get_user_perms(request):
        return get_user_perms(request)

    @staticmethod
    def _validate_perms(perms):
        assert type(perms) in [list, tuple, str], 'Type of df_permissions must be list, tuple or str'

    def has_permission(self, request, view):
        if request.user.is_superuser:
            if getattr(view, 'df_allow_superuser', False):
                return True

        # all permission of request user
        user_perms = self._get_user_perms(request)

        # check df_permissions exists
        if hasattr(view, 'df_permissions'):
            df_permissions = view.df_permissions
            self._validate_perms(df_permissions)
            if type(df_permissions) == str:
                return has_perms(user_perms, [df_permissions])
            return has_perms(user_perms, df_permissions)
        elif hasattr(view, 'get_df_permissions'):
            df_permissions = view.get_df_permissions()
            self._validate_perms(df_permissions)
            if type(df_permissions) == str:
                return has_perms(user_perms, [df_permissions])
            return has_perms(user_perms, df_permissions)

        fields = self._get_fields(view)

        # required permissions for view
        required_perms = self._get_required_perms(view, fields)

        return has_perms(user_perms, required_perms)
