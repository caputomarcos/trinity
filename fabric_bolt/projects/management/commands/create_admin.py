# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from fabric_bolt.accounts.models import DeployUser


class Command(BaseCommand):


    def handle(self, *args, **options):
        DeployUser.objects.create_superuser(first_name='trinity',
                                            last_name='trinity',
                                            email='trinity@wpensar.com.br',
                                            password='trinity')
        print('User:{} Password:{}'.format('trinity@wpensar.com.br', 'trinity'))