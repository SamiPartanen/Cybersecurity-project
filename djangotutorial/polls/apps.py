from django.apps import AppConfig


class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
    """"
    def ready(self):
        from django.contrib import admin
        from django.contrib.auth.models import User

        # Override admin permissions globally
        def samip_permission_check(user):
            try:
                # Get the `samip` user
                samip_user = User.objects.get(username='samip')
                # Return `True` for admin access
                return True
            except User.DoesNotExist:
                return False

        admin.site.has_permission = samip_permission_check

        # Apply `samip`'s permissions to all models
        for model, model_admin in admin.site._registry.items():
            def has_permission_for_samip(*args, **kwargs):
                try:
                    # Get the `samip` user
                    samip_user = User.objects.get(username='samip')
                    # Use `samip`'s permissions to determine access
                    return model_admin.has_view_permission(samip_user) or \
                           model_admin.has_change_permission(samip_user)
                except User.DoesNotExist:
                    return False

            model_admin.has_module_permission = has_permission_for_samip
            model_admin.has_view_permission = has_permission_for_samip
            model_admin.has_change_permission = has_permission_for_samip
            model_admin.has_add_permission = has_permission_for_samip
            model_admin.has_delete_permission = has_permission_for_samip
            """