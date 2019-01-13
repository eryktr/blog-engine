"""
Create permission groups
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


class Command(BaseCommand):
    help = 'Creates read only default permission groups for users'

    def handle(self, *args, **options):
        normal_users_group, _ = Group.objects.get_or_create(name="normal_users")
        permissions = Permission.objects.all()
        normal_user_permissions = permissions.filter(codename__in=[
            "view_post",
            "view_tag",
            "view_comment",
            "add_post",
            "add_comment"
        ])
        normal_users_group.permissions.set(normal_user_permissions)
        moderators_group, _ = Group.objects.get_or_create(name="moderators")
        moderator_permissions = permissions.filter(codename__in=[
            "change_post",
            "change_comment",
            "delete_comment",
            "add_tag",
            "change_tag",
            "delete_tag"
        ])
        moderators_group.permissions.set(moderator_permissions)
