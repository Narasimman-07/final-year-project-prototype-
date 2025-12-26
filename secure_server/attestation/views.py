from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AppVerification, TamperLog
from .serializers import AppVerificationSerializer
from django.http import JsonResponse
import datetime

from django.http import JsonResponse
from .models import AppVerification, TamperLog
from attestation.models import AppVerification, TamperLog, RegisteredApp
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.utils import timezone
from datetime import timedelta

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def resolve_tamper(request, log_id):
    try:
        tamper = get_object_or_404(TamperLog, id=log_id)
        tamper.resolved = True
        tamper.save()
        return Response({'status': 'RESOLVED', 'message': 'Tamper log resolved successfully'})
    except Exception as e:
        return Response({'status': 'ERROR', 'message': str(e)}, status=400)


@api_view(['POST'])
def verify_integrity(request):
    app_name = request.data.get('app_name')
    current_hash = request.data.get('hash')
    device_id = request.data.get('device_id')
    os_info = request.data.get('os_info')

    try:
        record = AppVerification.objects.get(app_name=app_name, device_id=device_id)

        if record.reference_hash == current_hash:
            # ✅ App integrity verified successfully
            record.is_valid = True
            record.last_verified = timezone.now()
            record.save()
            return Response({'status': 'OK', 'message': 'Integrity Verified'})

        else:
            # ⚠️ Tampering detected
            record.is_valid = False
            record.last_verified = timezone.now()
            record.save()

            # ✅ Prevent duplicate tamper entries within 1 hour
            one_hour_ago = timezone.now() - timedelta(hours=1)
            recent_tamper = TamperLog.objects.filter(
                app_name=app_name,
                device_id=device_id,
                timestamp__gte=one_hour_ago
            ).exists()

            if not recent_tamper:
                TamperLog.objects.create(
                    app_name=app_name,
                    device_id=device_id,
                    issue=f"Hash mismatch detected at {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )

            return Response({'status': 'ALERT', 'message': 'Tampering Detected'})

    except AppVerification.DoesNotExist:
        # 🆕 First-time app verification
        AppVerification.objects.create(
            app_name=app_name,
            reference_hash=current_hash,
            device_id=device_id,
            os_info=os_info,
            last_verified=timezone.now()
        )
        return Response({'status': 'NEW', 'message': 'Reference hash saved for first time'})

    except AppVerification.DoesNotExist:
        # 🆕 First-time app verification
        AppVerification.objects.create(
            app_name=app_name,
            reference_hash=current_hash,
            device_id=device_id,
            os_info=os_info
        )
        return Response({'status': 'NEW', 'message': 'Reference hash saved for first time'})


def get_logs(request):
    logs = []

    # Verified logs
    app_logs = AppVerification.objects.all().order_by('-id')
    for log in app_logs:
        logs.append({
            "id": log.id,
            "app_name": log.app_name,
            "device_id": log.device_id,
            "os_info": log.os_info,
            "status": "OK" if log.is_valid else "ALERT",
            "timestamp": log.last_verified.strftime("%Y-%m-%d %H:%M:%S") if log.last_verified else "",
        })

    # Tamper logs
    tamper_logs = TamperLog.objects.all().order_by('-id')
    for log in tamper_logs:
        logs.append({
            "id": log.id,
            "app_name": log.app_name,
            "device_id": log.device_id,
            "os_info": "N/A",
            "status": "RESOLVED" if log.resolved else "ALERT",
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S") if log.timestamp else "",
        })

    logs = sorted(logs, key=lambda x: x['timestamp'], reverse=True)
    return JsonResponse(logs, safe=False)




@api_view(['POST'])
def verify_integrity(request):
    app_name = request.data.get('app_name')
    current_hash = request.data.get('hash')
    device_id = request.data.get('device_id')
    os_info = request.data.get('os_info')

    try:
        record = AppVerification.objects.get(app_name=app_name, device_id=device_id)
        if record.reference_hash == current_hash:
            record.is_valid = True
            record.save()
            return Response({'status': 'OK', 'message': 'Integrity Verified'})
        else:
            record.is_valid = False
            record.save()
            TamperLog.objects.create(
                app_name=app_name,
                device_id=device_id,
                issue=f"Hash mismatch. Expected {record.reference_hash}, got {current_hash}"
            )

            return Response({'status': 'ALERT', 'message': 'Tampering Detected'})
    except AppVerification.DoesNotExist:
        AppVerification.objects.create(
            app_name=app_name,
            reference_hash=current_hash,
            device_id=device_id,
            os_info=os_info
        )
        return Response({'status': 'NEW', 'message': 'Reference hash saved for first time'})
