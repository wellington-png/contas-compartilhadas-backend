from django.core.management.base import BaseCommand
from apps.accounts.models import Membership
from apps.finances.models import Expense
from apps.groups.models import Group
from apps.reports.models import FinancialReport
from faker import Faker
from datetime import date
import random
import decimal

from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with fake data using Faker'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Criando alguns usuários
        users = []
        for _ in range(5):  # cria 5 usuários
            user = User.objects.create_user(
                password='password123',
                name=fake.first_name(),
                email=fake.email(),
            )
            users.append(user)

        # Criando grupos
        groups = []
        for _ in range(3):  # cria 3 grupos
            group = Group.objects.create(
                name=fake.company(),
                owner=random.choice(users)
            )
            groups.append(group)

        # Adicionando membros aos grupos
        for user in users:
            group = random.choice(groups)
            Membership.objects.create(user=user, group=group)

        # Criando despesas
        for _ in range(10):  # cria 10 despesas
            user = random.choice(users)
            group = random.choice(groups)
            Expense.objects.create(
                user=user,
                group=group,
                amount=round(random.uniform(10.00, 500.00), 2),
                description=fake.catch_phrase(),
                date_spent=fake.date_this_year(),
                is_fixed=random.choice([True, False])
            )

        # Gerando relatórios financeiros
        for group in groups:
            total_expenses = group.total_expenses()
            FinancialReport.objects.create(
                group=group,
                report_data={"total_expenses": float(total_expenses)}
            )

        self.stdout.write(self.style.SUCCESS('Database populated with fake data successfully!'))
