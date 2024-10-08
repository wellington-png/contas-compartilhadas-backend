from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
import qrcode
import io
import base64
from django.db.models import Sum
from django.utils.timezone import now
from django.db.models import Sum, F, Q
from apps.core.viewsets import BaseModelViewSet
from apps.groups.models import Group, GroupInvite, generate_invite_token
from apps.groups.serializers import (
    GroupSerializer,
    InviteEmailSerializer,
    GroupDetailsSerializer,
)
from datetime import datetime
from apps.finances.models import Expense
from apps.finances.serializers import ExpenseSerializer
from apps.accounts.models import Membership
from apps.accounts.serializers import (
    MembershipSerializer,
    AddMemberSerializer,
    MembershipDetailsSerializer,
)
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model

User = get_user_model()


class FinancialSummarySerializer(serializers.Serializer):
    total_expense = serializers.DecimalField(max_digits=18, decimal_places=2)
    balance = serializers.DecimalField(max_digits=18, decimal_places=2)


class GroupViewSet(BaseModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self):
        user = self.request.user
        if self.action == "join":
            return Group.objects.all()
        return Group.objects.filter(members=user)

    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            raise ValidationError(
                {"detail": "Você não tem permissão para editar este grupo."},
                code=status.HTTP_403_FORBIDDEN,
            )

        updated_group = serializer.save()

        # Serialize the updated instance with GroupDetailsSerializer
        details_serializer = GroupDetailsSerializer(updated_group)

        # Return a response with the serialized data
        return Response(details_serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise ValidationError(
                {"detail": "Você não tem permissão para excluir este grupo."},
                code=status.HTTP_403_FORBIDDEN,
            )

        instance.delete()

    def perform_create(self, serializer):
        group_name = serializer.validated_data.get("name")

        group = serializer.save(owner=self.request.user)
        Membership.objects.create(group=group, user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Verifica se o usuário é o proprietário do grupo
        if instance.owner != request.user:
            raise ValidationError(
                {"detail": "Você não tem permissão para editar este grupo."},
                code=status.HTTP_403_FORBIDDEN,
            )

        # Cria o serializer com os dados do request
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        # Salva a instância atualizada
        updated_group = serializer.save()

        # Serializa a instância atualizada com GroupDetailsSerializer
        details_serializer = GroupDetailsSerializer(updated_group)

        # Retorna a resposta com os dados serializados
        return Response(details_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="details", name="details")
    def details(self, request, pk=None):
        group = self.get_object()
        serializer = GroupDetailsSerializer(group)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GroupDetailsSerializer
        if self.action == "add_expense":
            return ExpenseSerializer
        if self.action == "expenses":
            return ExpenseSerializer
        if self.action == "financial_summary":
            return FinancialSummarySerializer
        if self.action == "add_member":
            return AddMemberSerializer
        if self.action == "members":
            return MembershipSerializer
        if self.action == "invite_email":
            return InviteEmailSerializer
        if self.action == "invite_qrcode":
            return serializers.Serializer

        return GroupSerializer

    @action(
        detail=True, methods=["post"], url_path="invite-qrcode", serializer_class=None
    )
    def invite_qrcode(self, request, *args, **kwargs):
        group = self.get_object()

        data = {
            "group_id": group.id,
            "group_name": group.name,
        }

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_code_image = buffer.getvalue()

        qr_code_base64 = base64.b64encode(qr_code_image).decode("utf-8")

        return Response({"qr_code": qr_code_base64})

    @action(
        detail=True,
        methods=["post"],
        url_path="invite-email",
        serializer_class=InviteEmailSerializer,
    )
    def invite_email(self, request, *args, **kwargs):
        group = self.get_object()
        email = request.data.get("email")

        if not email:
            return Response(
                {"detail": "E-mail é obrigatório."}, status=status.HTTP_400_BAD_REQUEST
            )
        user = user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {"detail": "E-mail não está registrado no sistema."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invite_token = generate_invite_token()
        GroupInvite.objects.create(group=group, token=invite_token, user=user)
        invite_link = (
            f"https://wellington2.thunder.dev.br/join/{group.id}/{invite_token}/"
        )
        button_text = "<a href='{invite_link}'>Clique aqui para se juntar ao grupo</a>"

        subject = f"Convite para participar do grupo {group.name}"
        message = f"Você foi convidado a participar do grupo {group.name} no aplicativo Contas Compartilhadas.\n\n"
        message += f"Para se juntar ao grupo, clique no link abaixo:\n{invite_link}\n\n"
        message += "Se você não esperava este convite, por favor ignore este e-mail."
        message += f"<br><br>{button_text}"

        send_mail(
            subject,
            message,
            "your-email@example.com",
            [email],
            fail_silently=False,
        )

        return Response(
            {"detail": f"Convite enviado para {email}."}, status=status.HTTP_200_OK
        )

    @action(
        detail=True,
        methods=["get"],
        url_path="members",
        serializer_class=MembershipDetailsSerializer,
    )
    def members(self, request, *args, **kwargs):
        group = self.get_object()
        memberships = Membership.objects.filter(group=group)
        serializer = MembershipDetailsSerializer(memberships, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="add-member",
        serializer_class=MembershipSerializer,
    )
    def add_member(self, request, *args, **kwargs):
        group = self.get_object()
        serializer = MembershipSerializer(
            data={"user": request.data.get("user"), "group": group.id}
        )

        if serializer.is_valid():
            if Membership.objects.filter(
                group=group, user=serializer.validated_data["user"]
            ).exists():
                return Response(
                    {"detail": "Este membro já faz parte do grupo."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save(group=group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put"], url_path="remove-member")
    def remove_member(self, request, *args, **kwargs):
        group = self.get_object()
        user_id = request.data.get("user_id")

        if not user_id:
            return Response(
                {"detail": "O ID do usuário é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if group.owner.id == user_id:
            return Response(
                {"detail": "O dono do grupo não pode ser removido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        membership = Membership.objects.filter(group=group, user_id=user_id).first()
        if membership:
            membership.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"detail": "Membro não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    @action(
        detail=True,
        methods=["get"],
        url_path="expenses",
    )
    def expenses(self, request, *args, **kwargs):
        group = self.get_object()
        expenses = Expense.objects.filter(group=group)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        url_path="add-expense",
        serializer_class=ExpenseSerializer,
    )
    def add_expense(self, request, *args, **kwargs):
        group = self.get_object()
        user = request.user
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data.get("amount")
            if amount <= 0:
                return Response(
                    {"detail": "O valor da despesa deve ser maior que zero."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save(group=group, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["get"],
        url_path="financial-summary",
        serializer_class=FinancialSummarySerializer,
    )
    def financial_summary(self, request, *args, **kwargs):
        group = self.get_object()

        total_expense = (
            Expense.objects.filter(group=group).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        total_expense = round(total_expense, 2)
        balance = -total_expense
        balance = round(balance, 2)

        data = {
            "total_expense": total_expense,
            "balance": balance,
        }

        serializer = FinancialSummarySerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], url_path="join", name="join")
    def join(self, request, pk=None):
        user = request.user
        group = get_object_or_404(Group, id=pk)


        if Membership.objects.filter(user=user, group=group).exists():
            return Response(
                {"detail": "Você já é membro deste grupo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Membership.objects.create(user=user, group=group)

        return Response(
            {"detail": "Você entrou no grupo com sucesso."},
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["get"],
        url_path="expense-comparison",
    )
    def expense_comparison(self, request, *args, **kwargs):
        group = self.get_object()
        month = request.query_params.get("month", None)
        year = request.query_params.get("year", None)

        if not month or not year:
            return Response(
                {"detail": "Mês e ano são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Validar se o mês e o ano são números válidos
            month = int(month)
            year = int(year)
            # Obter o primeiro e o último dia do mês
            start_date = datetime(year, month, 1)
            end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
        except ValueError:
            return Response(
                {"detail": "Mês ou ano inválido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Filtrar as despesas do grupo no período especificado
        expenses = Expense.objects.filter(
            group=group,
            date_spent__gte=start_date,
            date_spent__lt=end_date,
        )

        # Calcular o total geral de despesas
        total_expense_all = expenses.aggregate(total=Sum('amount'))['total'] or 0

        if total_expense_all == 0:
            return Response([], status=status.HTTP_200_OK)

        # Agregar os gastos por membro e calcular o percentual
        expense_by_member = expenses.values("user__id", "user__email").annotate(
            total_expense=Sum("amount")
        ).order_by("-total_expense")

        for member in expense_by_member:
            member['percent'] = round((member['total_expense'] / total_expense_all) * 100, 2)

        return Response(expense_by_member, status=status.HTTP_200_OK)