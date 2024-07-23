from django import forms
from tourbuddy.models import *

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = "__all__"
        labels = {
            'location': 'ลิ้ง location',
            'latitude': 'ละติจูด',
            'longitude': 'ลองติจูด',
            'name': 'ชื่อสถานที่',
            'rating': 'คะแนน',
            'review': 'รีวิว',
            'trip_type': 'ประเภท',
            'g_type': 'กลุ่มประเภท',
            'image': 'ลิ้งรูปภาพ',
        }
        widgets = {
            'latitude': forms.NumberInput(attrs={'step': '0.0000001'}),
            'longitude': forms.NumberInput(attrs={'step': '0.0000001'}),
            'rating': forms.NumberInput(attrs={'step': '0.01'}),
        }
