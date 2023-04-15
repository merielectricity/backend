from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import EnquirySerializer

class EnquiryView(APIView):
    serializer_class = EnquirySerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Save the validated data to the database
            enquiry = serializer.save()

            # Return a success message
            response_data = {
                'message': 'Enquiry submitted successfully.'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # Return a validation error response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
