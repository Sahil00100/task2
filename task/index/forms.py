from django import forms
from django.contrib.auth.models import User
from.models import *
import requests
class SignupForm(forms.Form):
    #form elements
    first_name=forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class':'form-control-xl col-12'}))  
    last_name=forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class':'form-control-xl col-12'}))  
    email=forms.EmailField(required=True,widget=forms.TextInput(attrs={'class':'form-control-xl col-12'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control-xl col-12'}),required=True)
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control-xl col-12'}),required=True)

    #clean email
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Using this email already an account created,use another email')       
        else:
            #email validation using real email api (https://isitarealemail.com/)
            email_address = email
            response = requests.get(
                "https://isitarealemail.com/api/email/validate",
                params = {'email': email_address})

            status = response.json()['status']
            if status == "valid":
                print("email is valid")
                return email
            elif status == "invalid":
                print("email is invalid")
                raise forms.ValidationError('email is invalid')
            else:
                print("email was unknown")
                raise forms.ValidationError('email in unknown')
                
        
    #clean passwords
    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        
        if password1 and password2 and password1!=password2:
           raise forms.ValidationError('Password incorrect! try again')
        else:
            return password2

    #create user
    def create_user(self):
        user=User.objects.create_user(
            username=self.clean_email(),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.clean_email(),
            password=self.clean_password2()
            )
        user.save()
        

        return user
    def create_result(self):
            user=User.objects.get(username=self.cleaned_data.get('email'))
            
            result=Result(
            user=user,
            result=0

            )
            result.save()

