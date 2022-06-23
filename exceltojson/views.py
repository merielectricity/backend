#views.py (app)
from email import header
from http.client import HTTPResponse
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas

@api_view(['POST'])
def excelToJson(request):
    data = request.data
    File = data['file']
    excel_data_df = pandas.read_excel(File)
    headers = excel_data_df.columns
    json = {}
    for row in range(len(excel_data_df)):
        obj = {}
        for head in headers:
            obj[head] = excel_data_df[head][row]
        json[row] = obj
    excel_data_df = pandas.DataFrame.from_dict(json)
    json_str = excel_data_df.to_json()
    return JsonResponse(json_str, safe=False)
