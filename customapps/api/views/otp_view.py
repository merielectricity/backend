from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from customapps.utils.otp_helper import send_otp,create_device_token



class GenerateOTPView(APIView):
    def post(self, request):
        user=request.user
        device, token = create_device_token(user=user)
        if(not send_otp(token.token,user.email,user.phone_number)):
            return Response("Failed to Send OTP", status=status.HTTP_400_BAD_REQUEST)
        return Response("OTP Sent",status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    def post(self, request, format=None):
        otp = request.data.get("otp")
        user = request.user
        if not user or not otp:
            return Response("OTP expected from authenticated user", status=status.HTTP_400_BAD_REQUEST)
        device, token = create_device_token(user=user,otp=otp)
        if (device is None or token is None):
            return Response("OTP Not Found", status=status.HTTP_400_BAD_REQUEST)
        if device.verify_token(otp):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

