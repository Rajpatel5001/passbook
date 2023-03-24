from rest_framework import serializers
from .models import passbookInfoModel
from django.core.exceptions import ValidationError
def remin(data):
        try:
            balance = passbookInfoModel.objects.values('balance').last()['balance']
        except:
            balance = 0
        try:
            credit = data["credit"]
        except:
            data["credit"] = 0
        try:
            debit = data["debit"]
        except:
            data["debit"] = 0
        balance = balance + data["credit"] - data["debit"]
        return balance

class passbookserilizer(serializers.ModelSerializer):
    # prize = serializers.DecimalField(max_digits=14,decimal_places=2)
    # Ch = [("DEBIT","DEBIT"),("CREDIT","CREDIT")]
    # credit_debit = serializers.ChoiceField(choices=Ch)
    balance = serializers.CharField(style={'input_type':'hidden'},allow_blank=True,label="")
    debit = serializers.DecimalField(max_digits=14,decimal_places=2,required=False)
    credit = serializers.DecimalField(max_digits=14,decimal_places=2,required=False)
    def to_internal_value(self, data):
        data =  super().to_internal_value(data)
        data['balance'] = remin(data)
        return data

    class Meta:
        model = passbookInfoModel
        fields = '__all__'

    def validate(self, data):
        data = super().validate(data)
        return data
    
class exportserilaizer(serializers.ModelSerializer):
    startdate = serializers.DateField(required=False)
    enddate = serializers.DateField(required=False)
    queryset = serializers.CharField(required=False)

    def validate(self,obj):
        if "startdate" not in obj:
            raise ValidationError("Enter Start Date")
        if "enddate" not in obj:
            raise ValidationError("Enter end date")
        if "startdate" in obj  and  "enddate" in obj:
            if obj["startdate"] > obj["enddate"]:
                raise ValidationError("Enter correct date range")
        return obj

    class Meta:
        model = passbookInfoModel
        fields = ['startdate','enddate','queryset']