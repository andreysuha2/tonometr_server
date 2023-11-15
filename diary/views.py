from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from diary.models import Record as DiaryRecord
from diary.serializers import DiaryRecordSerializer
from datetime import datetime

# Create your views here.
class DiaryRecordList(APIView):    
    def get(self, request):
        now = datetime.now()
        year = request.query_params.get("year", now.year)
        month = request.query_params.get("month", now.month)
        records = DiaryRecord.objects.filter(timestamp__year=year, timestamp__month=month).order_by('timestamp')
        serializer = DiaryRecordSerializer(records, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = DiaryRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DiaryRecordDetails(APIView):
    def get_object(self, pk):
        try:
            return DiaryRecord.objects.get(pk=pk)
        except DiaryRecord.DoesNotExist:
            raise NotFound(detail="Record not found")
    
    def get(self, request, pk, format=None):
        record = self.get_object(pk)
        serializer = DiaryRecordSerializer(record)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        record = self.get_object(pk)
        serializer = DiaryRecordSerializer(instance=record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None, format=None):
        record = self.get_object(pk)
        record.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)