from django import forms

from index.models import *

class LoginForm(forms.ModelForm):
    class Meta:
        # 1.指定关联的实体类
        model = Users
        #2.指定生成控件的属性们
        fields = ["uphone","upwd"]
        #3.指定每个控件对应的label
        labels = {
            'uphone':'手机号',
            "upwd":'密码',
        }
        #4.指定每个控件对应的小部件
        widgets = {
            "uphone":forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'请输入手机号',
                }
            ),
            'upwd':forms.PasswordInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'请输入6-20位字符',
                }
            ),
        }
