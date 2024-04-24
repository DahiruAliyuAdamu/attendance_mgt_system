from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from attendance_app.models import Employee
from .forms import UserForm, LoginForm

# Create your views here.
class SignUp(View):
    template_name = 'registration/signup.html'
    
    def get(self, request):
        form = UserForm()
        staffs = Employee.objects.all()

        return render(request, self.template_name, {'form':form, 'staffs': staffs})
	
    def post(self, request):
        form = UserForm(request.POST)
        admin_user = request.POST.get('admin-user', None)
        user = request.POST.get('user', None)

        user_id = user.split(' - ')[1]
        print(user_id)
        if form.is_valid():
            if user:
                staff = Employee.objects.filter(Q(employee_id=user_id)).first()
                data = form.save(commit=False)
                data.set_password(data.password)
                data.staff = staff

                if admin_user:
                    data.is_superuser = True
                    data.is_staff = True
                data.save()

                messages.info(request, 'user created successful')
                return redirect('accounts:register')
            return render(request, self.template_name, {'form':form, 'user_error': 'Please select a user'})
        return render(request, self.template_name, {'form':form})
    
class Login(View):
    template_name = 'registration/login.html'
    
    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return JsonResponse({'message': "login"})
        return JsonResponse({'message': "not login"})
    
def user_logout(request):
    logout(request)
    # template_name = 'registration/logout.html'
    messages.success(request, f'You have successfully logout')
    return redirect('accounts:user_login')