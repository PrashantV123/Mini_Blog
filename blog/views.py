from django.shortcuts import render, HttpResponseRedirect
from .forms import user_signup_form, user_login_form, add_post_form, EditUserProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import post, Contact
from django.contrib.auth.models import Group
from django.contrib.auth.forms import SetPasswordForm
from django.views.generic import ListView, DetailView
from django.http import Http404

# Create your views here.

# Home Page with Pagination with class based view.


class PostListView(ListView):
    model = post
    template_name = 'blog/home.html'
    ordering = ['-id']
    paginate_by = 3
    paginate_orphans = 1

    # when user enters invalid page number in address bar in browser
    def get_context_data(self, *args, **kwargs):
        try:
            return super(PostListView, self).get_context_data(*args, **kwargs)
        except Http404:
            self.kwargs['page'] = 1
            return super(PostListView, self).get_context_data(*args, **kwargs)


class PostDetailView(DetailView):
    model = post
    template_name = 'blog/post.html'


# About Page


def about(request):
    if request.user.is_authenticated:
        return render(request, 'blog/about.html', {'name': request.user.get_short_name()})
    else:
        return render(request, 'blog/about.html')


# Contact Page


def contact(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            contact = Contact()
            contact.name = request.POST.get('name')
            contact.email = request.POST.get('email')
            contact.address = request.POST.get('address')
            contact.message = request.POST.get('message')
            contact.save()
            messages.success(
                request, 'Success! Your message has been sent to Site Admin.')
            return render(request, 'blog/contact.html', {'name': request.user.get_short_name()})
        else:
            return render(request, 'blog/contact.html', {'name': request.user.get_short_name()})

    else:
        if request.method == "POST":
            contact = Contact()
            contact.name = request.POST.get('name')
            contact.email = request.POST.get('email')
            contact.address = request.POST.get('address')
            contact.message = request.POST.get('message')
            contact.save()
            messages.success(
                request, 'Success! Your message has been sent to Site Admin.')
            return render(request, 'blog/contact.html')
        else:
            return render(request, 'blog/contact.html')


# Dashboard Page


def dashboard(request):
    if request.user.is_authenticated:
        # posts = post.objects.all().order_by('-id')
        posts = post.objects.filter(user=request.user).order_by('-id')
        return render(request, 'blog/dashboard.html', {'posts': posts, 'name': request.user.get_short_name()})
    else:
        return HttpResponseRedirect('/login/')

# SignUp Page


def user_signup(request):
    if request.method == "POST":
        form = user_signup_form(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Account created successfully!! Now, make your impact!!')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = user_signup_form()
    return render(request, 'blog/signup.html', {'form': form})

# LogIn Page


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = user_login_form(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Welcome, You are logged in as')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = user_login_form()
        return render(request, 'blog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')


# Logout Page


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


# Update User Profile (username, First Name, Last Name, Email address)

def user_profile_update(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = EditUserProfileForm(request.POST, instance=request.user)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Profile Updated Successfully!!')
        else:
            fm = EditUserProfileForm(instance=request.user)
        return render(request, 'blog/profile.html', {
            'name': request.user.get_short_name(), 'form': fm})
    else:
        return HttpResponseRedirect('/login/')

# Update User Password


def user_password_update(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = SetPasswordForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                return HttpResponseRedirect('/login/')
                # update_session_auth_hash(request, fm.user)
                # return HttpResponseRedirect('/profile/')
                # if you want to maintain and leave session open then use this. It will not logout user after password change.

        else:
            fm = SetPasswordForm(user=request.user)
        return render(request, 'blog/updatepassword.html', {'name': request.user.get_short_name(), 'form': fm})
    else:
        return HttpResponseRedirect('/login/')

# Add New Post Page


def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            form = add_post_form(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = post(user=user, title=title, desc=desc)
                pst.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            form = add_post_form()
        return render(request, 'blog/addpost.html', {'form': form, 'name': request.user.get_short_name()})
    else:
        return HttpResponseRedirect('/login/')

# Edit Post Page


def edit_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = post.objects.get(pk=id)
            form = add_post_form(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = post.objects.get(pk=id)
            form = add_post_form(instance=pi)
        return render(request, 'blog/editpost.html', {'form': form, 'name': request.user.get_short_name()})
    else:
        return HttpResponseRedirect('/login/')

# Delete Post


def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
