from django.shortcuts import render,redirect,get_object_or_404
from .models import userDatas,task
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from datetime import date
from django.db.models import Q
from django.contrib.auth import authenticate,login


def login(request):
    # Check if user is already logged in
    user_id = request.session.get('user_id')
    if user_id:
        return redirect('home')

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('rememberMe')

        # Try to find user by username or email
        user = (
            userDatas.objects.filter(username=username_or_email).first()
            or userDatas.objects.filter(email=username_or_email).first()
        )

        if user is None:
            messages.error(request, 'User does not exist')
            return render(request, 'Login.html')

        if not user.isApproved:
            messages.error(request, 'Your account is pending approval')
            return render(request, 'Login.html')

        if check_password(password, user.password):
            # Store user in session
            request.session['user_id'] = user.id

            # Set session expiry based on rememberMe
            if remember_me == 'on':
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # Expires on browser close

            messages.success(request, 'Welcome back!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'Login.html')

    return render(request, 'Login.html')


def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            return render(request,'Register.html',{'error' : 'password not matching'})
        if userDatas.objects.filter(email = email).exists():
            return render(request,'Register.html',{'error' : 'email already exists'})
        if userDatas.objects.filter(username = username).exists():
            return render(request,'Register.html',{'error' : 'username already exists'})
        userDatas.objects.create(full_name=full_name,email=email,username=username,password=make_password(password))
        return redirect('home')
            
    
    
    
    return render(request,'Register.html')

def landing(request):
    return render(request,'LandingPage.html')

def home(request):
    
    user_id = request.session.get('user_id')
   
    if user_id:
        user = userDatas.objects.get(id = user_id )
        tasks = task.objects.filter(user_id = user_id).order_by('due_date')
        return render(request,'Home.html',{'user':user,'tasks':tasks})

       
    return redirect('login')

def demo(request):
    return render(request,'Demo.html')

def howItWorks(request):
    return render(request,'HowItWorks.html')

def features(request):
    return render(request,'Features.html')

def logout(request):
    request.session.flush()
    return redirect('login')

def addTask(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date') 
        category = request.POST.get('category')
        important = request.POST.get('important')
        important = True if important == "on" else False
        if not due_date:
            due_date = date.today()
        else:
            due_date = date.fromisoformat(due_date)

        user = userDatas.objects.get(id = user_id)
    
        task.objects.create(user = user,title=title,important=important,description=description,due_date=due_date,category=category)
        return redirect('home')
    return render(request,'AddTask.html')

def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    try:
        user = userDatas.objects.get(id=user_id)
    except userDatas.DoesNotExist:
        request.session.flush()
        return redirect('login')


    

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')

        if userDatas.objects.filter(email=email).exclude(id=user_id).exists():
            return render(request, 'Profile.html', {'user': user})

        if userDatas.objects.filter(username=username).exclude(id=user_id).exists():
            return render(request, 'Profile.html', {'user': user})

        user.full_name = full_name
        user.email = email
        user.username = username
        user.save()

        return render(request, 'Profile.html', {'user': user, 'success': 'Profile updated successfully'})

    return render(request, 'Profile.html', {'user': user})

def important(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = userDatas.objects.get(id=user_id)
            tasks = task.objects.filter(user_id = user_id,important = True).order_by('due_date')
        
            return render(request,'Important.html',{'user':user,'important':tasks})
            
            
        except userDatas.DoesNotExist:
            request.session.flush()
            return redirect('login')
    else:
        request.session.flush()
        redirect('login')
        
def today(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = userDatas.objects.get(id=user_id)
            todayDate = date.today()
            tasks = task.objects.filter(user_id = user_id,due_date = todayDate).order_by('due_date')
        
            return render(request,'Today.html',{'user':user,'today':tasks})
            
            
        except userDatas.DoesNotExist:
            request.session.flush()
            return redirect('login')
    else:
        request.session.flush()
        redirect('login')
        
def completed(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = userDatas.objects.get(id=user_id)
            tasks = task.objects.filter(user_id = user_id,completed = True).order_by('due_date')
        
            return render(request,'Completed.html',{'user':user,'completed':tasks})
            
            
        except userDatas.DoesNotExist:
            request.session.flush()
            return redirect('login')
    else:
        request.session.flush()
        redirect('login')
        
def adminLogin(request):
    return render(request,'AdminLogin.html')

def adminPanel(request):
    query = request.GET.get('q')
    if query:
        datas = userDatas.objects.filter(Q(full_name__icontains = query)|Q(email__icontains = query))
    else:
        
        datas = userDatas.objects.all()
    active_users = userDatas.objects.filter(isblocked = False).count()
    inactive_users = userDatas.objects.filter(isblocked = True).count()
    pending_users = userDatas.objects.filter(isApproved = False).count()
    if datas:
        
        return render(request,'AdminPanel.html',{"datas":datas,"activeCount":active_users,"inactive_users":inactive_users,"pending_users":pending_users})
    else:
        return render(request,'AdminPanel.html')
        

def adminTable(request):
    return render(request,'AdminTable.html')

def adminApproval(request):
    datas = userDatas.objects.all()
    if datas:
        return render(request,'AdminApproval.html',{'datas':datas})
    else:
        
     
        return render(request,'AdminApproval.html')
    
def approve_user(request,userId):
    user = get_object_or_404(userDatas,id=userId)
    user.isApproved = True
    user.save()
    return redirect('adminApproval')

def revoke_user(request, userId):
    user = get_object_or_404(userDatas, id=userId)
    user.isApproved = False
    user.save()
    return redirect('adminApproval')