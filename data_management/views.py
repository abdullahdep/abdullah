from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserData, SharedData
from .forms import UserDataForm
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
z
@login_required
def data_list(request):
    user_data = UserData.objects.filter(user=request.user)
    shared_data = SharedData.objects.filter(child_account=request.user)
    return render(request, 'data_management/data_list.html', {'user_data': user_data, 'shared_data': shared_data})

@login_required
def add_data(request):
    if request.method == 'POST':
        form = UserDataForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            messages.success(request, 'Data added successfully!')
            return redirect('data_list')
    else:
        form = UserDataForm()
    return render(request, 'data_management/add_data.html', {'form': form})

@login_required
def edit_data(request, pk):
    data = get_object_or_404(UserData, pk=pk, user=request.user)
    if request.method == 'POST':
        form = UserDataForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data updated successfully!')
            return redirect('data_list')
    else:
        form = UserDataForm(instance=data)
    return render(request, 'data_management/edit_data.html', {'form': form})

@login_required
def delete_data(request, pk):
    data = get_object_or_404(UserData, pk=pk, user=request.user)
    if request.method == 'POST':
        data.delete()
        messages.success(request, 'Data deleted successfully!')
        return redirect('data_list')
    return render(request, 'data_management/delete_data.html', {'data': data})

@login_required
def download_data(request, pk):
    data = get_object_or_404(UserData, pk=pk)
    if data.user == request.user or SharedData.objects.filter(parent_data=data, child_account=request.user).exists():
        if data.file:
            response = HttpResponse(data.file, content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename="{data.file.name}"'
            return response
        else:
            messages.error(request, 'No file associated with this data.')
            return redirect('data_list')
    else:
        raise PermissionDenied

@login_required
def share_data(request, pk):
    data = get_object_or_404(UserData, pk=pk, user=request.user)
    child_accounts = request.user.child_accounts.all()
    if request.method == 'POST':
        selected_accounts = request.POST.getlist('child_accounts')
        for account_id in selected_accounts:
            SharedData.objects.get_or_create(parent_data=data, child_account_id=account_id)
        messages.success(request, 'Data shared successfully!')
        return redirect('data_list')
    return render(request, 'data_management/share_data.html', {'data': data, 'child_accounts': child_accounts})

