from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import PasswordEntry
from .forms import PasswordEntryForm
from .crypto import encrypt_password, decrypt_password

def home(request):
    return render(request, 'home.html') 

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Store master password in session for encryption
            request.session['master_password'] = request.POST.get('password')
            return redirect('vault:password_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    # Clear session on logout
    if 'master_password' in request.session:
        del request.session['master_password']
    logout(request)
    return redirect('vault:login')

@login_required
def password_list(request):
    passwords = PasswordEntry.objects.filter(user=request.user)
    return render(request, 'list.html', {'passwords': passwords})

@login_required
def add_password(request):
    master_pass = request.session.get('master_password')
    if not master_pass:
        return redirect('vault:login')

    if request.method == 'POST':
        form = PasswordEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            
            # Encrypt the password using the master password
            salt = b'some_static_salt' # In a real app, store this in models/settings
            plain_pass = form.cleaned_data['plain_password']
            entry.encrypted_password = encrypt_password(plain_pass, master_pass, salt)
            entry.iv = b'0000000000000000' 
            entry.save()
            return redirect('vault:password_list')
    else:
        form = PasswordEntryForm()
    return render(request, 'form.html', {'form': form})
@login_required
def reveal_password(request, entry_id):
    master_pass = request.session.get('master_password')
    if not master_pass:
        return redirect('vault:login')
        
    entry = PasswordEntry.objects.get(id=entry_id, user=request.user)
    salt = b'some_static_salt' # MUST match the salt used in add_password
    
    # Decrypt the password
    plain_pass = decrypt_password(entry.encrypted_password, master_pass, salt)
    
    return render(request, 'reveal.html', {'password': plain_pass, 'entry': entry})