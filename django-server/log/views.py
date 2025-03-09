from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserDeviceInfo


class DeviceInfoView(APIView):
    def post(self, request):
        data = request.data
        try:
            UserDeviceInfo.objects.create(
                ip_address=data.get("ip_address", ""),
                user_agent=data.get("user_agent", ""),
                device_type=data.get("device_type", ""),
                browser=data.get("browser", ""),
                os=data.get("os", ""),
                screen_resolution=data.get("screen_resolution", ""),
                timezone=data.get("timezone", ""),
            )
            return Response(
                {"message": "Device info saved."}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
