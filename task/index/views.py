from pickle import TRUE
from unittest import result
from django.shortcuts import render,redirect
from django.contrib import messages
from.forms import SignupForm
from.models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import time
# Create your views here.

#signup
def signup(request):
    form=SignupForm
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            user=form.create_user()
            user.save()
            result=form.create_result()
            
            return redirect('login')
    return render(request,'signup.html',{'form':form})
#login
def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(
            request,
            username=email,
            password=password
            )

        if user is not None:
            auth_login(request,user)
            print(user)
            if user.is_superuser:
                #return render(request,'admin-dashboard.html',{})
                return redirect(reverse('admin:index'))
            else:
                user_details=User.objects.get(username=request.user)
                return redirect('quiz')

        else:
            messages.add_message(
                request,
                messages.INFO,
                'Invalid Username or password'
                )
    else:
        return render(request,'login.html',{})
    return render(request,'login.html',{})
@login_required(login_url='login')
def quiz(request):

    if request.method=='POST':


        id=int(request.POST['id'])+1
        print(id)
        option=request.POST['op1']
        option=str(option)
        ans_obj=Question.objects.get(id=id-1)
        ans=str(ans_obj.ans)
        result_obj=Result.objects.get(user=request.user)
        print(ans)
        print(option)

        if ans==option:
            print('success')
            #data=Result.objects.get(result=int(result_obj)+1)
            result_obj.result=int(result_obj.result)+1
        
            result_obj.save()
        #print(id)
        bool=False
        print(id)
        if (Question.objects.all().last().id)+1==id:
            print(id)
            return redirect('result')
        else:
            while bool==False:
                if Question.objects.filter(id=id).exists()==False:
                    print('false')
                    id=id+1
                    print(id)
                else:
                   
                    bool=True
            
            total_q=Question.objects.all().count()
            ques=Question.objects.filter(id=id)
            return render(request,'quiz.html',{'q':ques,'total':total_q})
        
            
    else:

        total_q=Question.objects.all().count()
        obj=list(Question.objects.all().order_by('id'))
       # obj=obj1.sort(reverse=True)
        for x in obj:
            id=x.id
            print(id)
            break

        ques=Question.objects.filter(id=id)
        return render(request,'quiz.html',{'q':ques,'total':total_q})
@login_required(login_url='login')
def result(request):
    obj=Result.objects.get(user=request.user)
    result=int(obj.result)
    total_q=Question.objects.all().count()
    total_q=int(total_q)
    percentage=result/total_q
    return render(request,'result.html',{'result':result,'q':total_q,'p':percentage})