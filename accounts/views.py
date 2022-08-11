from django.shortcuts import redirect, render
from accounts.forms import Registration,Profile_update

# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Account
from django.urls import reverse_lazy

#activation email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .task import sending_activation_mail



# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('Amazon_crawler:best-selling'))


    if request.method=='POST':
        form=Registration(request.POST)
        context={
            'form':form     }
        if form.is_valid():
            current_site=get_current_site(request)
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            username=form.cleaned_data['username']
            word=form.cleaned_data['password']
            Repeat_password=form.cleaned_data['Repeat_password']
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=word.strip())
            user.save()
            user_id=user.id
            
            sending_activation_mail.delay("account_verification_email",str(current_site),user_id,email,"ParseJet Account Verification !") #Celery Job
            
    
            return redirect('/accounts/login/?command=verification&email='+email)       
    else:
        
        form=Registration()
        context={"form":form}
    return render(request,'accounts/register.html',context)




def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Congratulations! You are ready to go!. ")
        return redirect('accounts:login')
    else:
        messages.error(request,"Inavalid Activation Link ")
        return redirect('register')
    

def view_login(request):
    if request.user.is_authenticated ==True:
        return redirect(reverse_lazy('Amazon_crawler:best-selling'))

    elif request.method=="POST":
        mail=request.POST.get('email')
        word=request.POST.get('password')
        user=authenticate(request,email=mail,password=word)
        
        if user is not None:
            login(request,user)
            # messages.SUCCESS(request,"You are now Login.")
            return redirect(reverse_lazy('Amazon_crawler:best-selling'))
        else:
            messages.error(request,'Invalid Login details !')
            return redirect('accounts:login')
    
    return render(request,'accounts/login.html')


@login_required
def logouting(request):
    logout(request)
    messages.success(request,'You are logged out.')
    return redirect('accounts:login')


#Recovering password sending email
def forgotPassword(request):
    if request.method=="POST":
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email=email)
            #Reset password 
            current_site=get_current_site(request)
            user_id=user.id
            mail_subject="ParseJet Reset Your Password"
            
            sending_activation_mail.delay("reset_pass_email",str(current_site),user_id,email,mail_subject) #Celery Job

            messages.success(request,"password Reset email has been send to your email address !")
            return redirect('accounts:login')
        else:
            messages.error(request,"Account does not exists with this email!")
    return render(request,'accounts/forgotpassword.html')



#Validate the ssession and user
def resetpassword_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,"Please Reset your Password")
        return redirect('resetpassword')
    else:
        messages.error(request,"Inavalid Reset Link!")
        return redirect('register')
 


#Update the password
def resetpassword(request):
    if request.method=="POST":
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password==confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password changed succesfully !')
            return redirect('login')

        else:
            messages.error(request,'The Password did not match !')
            return redirect('resetpassword')
    else:
        return render(request,
        'accounts/resetpassword.html')


def ok(request):
    return HttpResponse(request,"ok")


