import csv
from django.http import HttpResponse
from django.db.models import Sum
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import passbookInfoModel
from .serilizer import passbookserilizer, exportserilaizer

class passbookVIEW(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'display_book.html'
    queryset = passbookInfoModel.objects.all().order_by('-entry_created_date', '-id')
    pagination_class = PageNumberPagination
    serializer_class = passbookserilizer

    def totalbalance(self):
        try:
            totalbalance_obj = passbookInfoModel.objects.only('balance').last()
            totalbalance = totalbalance_obj.balance
        except:
            totalbalance = 0
        return totalbalance

    def get(self, request, *args, **kwargs):
        try:
            if request.GET.get("date"):
                query = request.GET.get("date")
                self.queryset = self.queryset.filter(entry_created_date=query)
        except:
            return Response({"error": "Eenter valid date"})
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            total = self.totalbalance()
            return self.get_paginated_response(data={'entrys': serializer.data}, kwargs={'total': total})
        return Response({'entrys': serializer.data})

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data, kwargs):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data, kwargs)


class postentry(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'form.html'

    def get(self, request, *args, **kwargs):
        serailizer = passbookserilizer()
        return Response({'serializer': serailizer})

    def post(self, request, *args, **kwargs):
        serailizer = passbookserilizer(data=request.data)
        if serailizer.is_valid():
            serailizer.save()
            # return Response({'serializer': serailizer})
            return redirect('passbook:passbookurl')
        else:
            return Response({'serializer': serailizer})


class exportUSerApiView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'export.html'

    def export_users_csv(self, startdate=None, enddate=None, queryset=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'
        writer = csv.writer(response)
        # writer.writerow(['DATE', 'PARTICULARS', 'CREDIT', 'DEBIT', 'BALANCE'])

        if startdate and enddate and queryset:
            if queryset == 'ALL':
                users = passbookInfoModel.objects.filter(entry_created_date__range=(startdate, enddate)).values('particular').annotate(totalcredit=Sum('credit'), totaldebit=Sum(
                    'debit')).values_list('entry_created_date', 'particular', 'totalcredit', 'totaldebit')
                writer.writerow(['DATE', 'PARTICULARS', 'TOTAL_CREDIT', 'TOTAL_DEBIT'])
            else:
                users = passbookInfoModel.objects.filter(entry_created_date__range=(startdate, enddate),particular__icontains=queryset).values('particular').annotate(totalcredit=Sum('credit'), totaldebit=Sum(
                    'debit')).values_list('entry_created_date', 'particular', 'totalcredit', 'totaldebit')
                writer.writerow(['DATE', 'PARTICULARS', 'TOTAL_CREDIT', 'TOTAL_DEBIT'])
                
        elif queryset:
            users = passbookInfoModel.objects.filter(particular__icontains=queryset).values('particular').annotate(totalcredit=Sum(
                'credit'), totaldebit=Sum('debit')).values_list( 'particular', 'totalcredit', 'totaldebit')
            writer.writerow(['PARTICULARS', 'TOTAL_CREDIT', 'TOTAL_DEBIT'])

        elif startdate and enddate:
            users = passbookInfoModel.objects.filter(entry_created_date__range=(startdate, enddate)).values_list(
                'entry_created_date', 'particular', 'credit', 'debit', 'balance').order_by('-entry_created_date', '-id')
            writer.writerow(['DATE', 'PARTICULARS', 'TOTAL_CREDIT', 'TOTAL_DEBIT','BALANCE'])
        else:
            return False

        if users:
            for user in users:
                user_list = list(user)
                writer.writerow(user_list)
            return response
        else:
            return False

    def get(self, request, *args, **kwargs):
        seailizer = exportserilaizer()
        return Response({'serializer': seailizer})

    def post(self, request, *args, **kwargs):
        serailizer = exportserilaizer(data=request.data)
        if serailizer.is_valid():
            # date
            if "queryset" in serailizer.data and "startdate" in serailizer.data and "enddate" in serailizer.data:
                csvfile = self.export_users_csv(startdate=serailizer.data["startdate"],enddate = serailizer.data["enddate"],queryset= serailizer.data["queryset"])
            elif "queryset" in serailizer.data:
                csvfile = self.export_users_csv(queryset=serailizer.data["queryset"])
            elif "startdate" in serailizer.data:
                csvfile = self.export_users_csv(startdate =serailizer.data["startdate"],enddate = serailizer.data["enddate"])
            else:
                csvfile = False

            if csvfile is False:
                return Response({'serializer': serailizer, 'error': "DATE RANGE DONT HAVE DATA OR QUERYSET"})
            else:
                return csvfile
        else:
            return Response({'serializer': serailizer, 'error': "check Input dates and query"})
