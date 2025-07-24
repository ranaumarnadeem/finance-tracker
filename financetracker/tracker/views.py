from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from .models import DebtEntry
from .serial import DebtEntrySerializer
from django.core.mail import send_mail


# ========== API VIEWS ==========

class DebtEntryListCreateView(APIView):
    def get(self, request):
        debt_entries = DebtEntry.objects.all()
        serializer = DebtEntrySerializer(debt_entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DebtEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAllDebtEntriesView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request):
        DebtEntry.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToggleDebtCheckboxView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            debt_entry = DebtEntry.objects.get(pk=pk)
            debt_entry.checkbox = not debt_entry.checkbox
            debt_entry.save()
            serializer = DebtEntrySerializer(debt_entry)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DebtEntry.DoesNotExist:
            return Response({"detail": "Debt entry not found."}, status=status.HTTP_404_NOT_FOUND)


class SendDebtEmailsView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        entries = DebtEntry.objects.all()
        if not entries:
            return Response({"message": "No debts to email."}, status=status.HTTP_204_NO_CONTENT)

        emails_sent = 0
        skipped_entries = []

        for entry in entries:
            if not entry.email:
                skipped_entries.append(entry.name)
                continue

            subject = f"Payment Reminder: You owe {entry.amount} PKR"
            message = (
                f"Dear {entry.name},\n\n"
                f"You owe Rs. {entry.amount} for: {entry.description}\n"
                f"Date: {entry.date_incurred}\n\n"
                "Please return the amount to the lender.\nThank you!"
            )

            send_mail(
                subject,
                message,
                "ranaumarnadeem632@gmail.com",  # Must match SendGrid verified sender
                [entry.email],
                fail_silently=False
            )
            emails_sent += 1

        return Response({
            "message": f"{emails_sent} email(s) sent.",
            "skipped": skipped_entries
        }, status=status.HTTP_200_OK)


# ========== FRONTEND VIEWS ==========

@login_required
@login_required
def dashboard_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date_incurred')

        DebtEntry.objects.create(
            name=name,
            email=email,
            amount=amount,
            description=description,
            date_incurred=date
        )
        return redirect('dashboard')

    debts = DebtEntry.objects.all()
    return render(request, 'tracker/dashboard.html', {'debts': debts})


@csrf_exempt
@login_required
def toggle_checkbox_view(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboard')

    try:
        entry = DebtEntry.objects.get(pk=pk)
        entry.checkbox = not entry.checkbox
        entry.save()
    except DebtEntry.DoesNotExist:
        pass
    return redirect('dashboard')


@csrf_exempt
@login_required
def delete_all_view(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    DebtEntry.objects.all().delete()
    return redirect('dashboard')


@csrf_exempt
@login_required
def send_email_view(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    entries = DebtEntry.objects.all()
    for entry in entries:
        if not entry.email:
            continue
        subject = f"Payment Reminder: You owe {entry.amount} PKR"
        message = (
            f"Dear {entry.name},\n\n"
            f"You owe Rs. {entry.amount} for: {entry.description}\n"
            f"Date: {entry.date_incurred}\n\n"
            "Please return the amount to the lender.\nThank you!"
        )
        send_mail(
            subject,
            message,
            "ranaumarnadeem632@gmail.com",
            [entry.email],
            fail_silently=False
        )
    return redirect('dashboard')
