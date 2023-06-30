from django.shortcuts import render, redirect, HttpResponse
from .forms import RegisterForm, PostingModelForm, UserUpdateForm, PostingUpdateForm, CommentForm, like_clicked, LoginForm
from django.contrib.auth import login, authenticate
from .models import User, PostModel, make_query, Friend, Messages
from django.contrib.auth.decorators import login_required
from django.db import connection
import os


def sign_up(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f'You are already authenticated as {user.email}.')
    context = {}
    if request.method == 'POST':
        print(request.POST)
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
        else:
            context['form'] = form
    else:
        form = RegisterForm()
        context['form'] = form

    return render(request, 'registration/sign_up.html', context)


def login_view(request):

    def get_recent_images(folder_path):
        num_files = 5

        files = os.listdir(folder_path)

        image_files = [f for f in files if f.lower().endswith(
            ('.jpg', '.jpeg', '.png', '.gif'))]

        image_files.sort(key=lambda x: os.path.getmtime(
            os.path.join(folder_path, x)), reverse=True)

        recent_files = image_files[:num_files]

        return ['media/profile/' + file for file in recent_files]

    path = r'{}\media\profile'.format(os.getcwd())
    print('path---->', path)

    recent_images = get_recent_images(path)

    context = {'images': recent_images}

    user = request.user
    if user.is_authenticated:
        return redirect("/home")

    if request.POST:
        print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("/home")
    else:
        form = LoginForm()

    context['login_form'] = form

    return render(request, "registration/login.html", context)


@login_required
def home(request):
    users = User.objects.raw('SELECT * FROM user')
    posts = PostModel.objects.raw(
        'SELECT * FROM post order by date_created desc;')
    if request.method == 'POST':
        form = PostingModelForm(request.POST)
        print(request.POST)
        if form.is_valid():
            current_user = request.user
            title = request.POST.get('title')
            content = request.POST.get('content')
            post = PostModel(created_by=current_user,
                             title=title, content=content)
            post.save()
            return redirect('/home')

    else:
        form = PostingModelForm()

    context = {
        'users': users,
        'posts': posts,
        'form': form,
    }

    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'main/home.html', context)


@login_required
def profile(request, user_id):
    user_profile = User.objects.raw(
        f'SELECT * FROM user WHERE id={user_id}')[0]
    posts = PostModel.objects.raw(
        f'SELECT * FROM post WHERE created_by={user_id}')
    print(posts)
    print(user_id)
    if request.method == 'POST':
        user_form = UserUpdateForm(
            request.POST, instance=request.user)
        if user_form.is_valid():
            instance = user_form.save()
            try:
                uploaded_file = request.FILES['image']
                if uploaded_file:
                    instance.image = uploaded_file
                    instance.save()
            except:
                pass

            redirect(f'/profile/{user_id}')
    else:
        user_form = UserUpdateForm(instance=request.user)
    context = {
        'user_profile': user_profile,
        'user_form': user_form,
        'posts': posts
    }

    return render(request, 'main/profile.html', context)


@login_required
def post_detail(request, pk):
    post = PostModel.objects.raw(f'SELECT * FROM post WHERE id={pk};')[0]
    like = like_clicked(request.GET)
    if 'button' in request.GET:
        post.likes_number += 1
        post.save()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            return redirect(f'/post_detail/{pk}')
    else:
        form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'like': like
    }
    return render(request, 'main/post_detail.html', context)


@login_required
def post_edit(request, pk):
    post = PostModel.objects.raw(f'SELECT * FROM post WHERE id={pk};')[0]
    if request.method == 'POST':
        form = PostingUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(f'/post_detail/{post.id}')
    else:
        form = PostingUpdateForm(instance=post)

    context = {
        'post': post,
        'form': form
    }
    return render(request, 'main/post_edit.html', context)


@login_required
def post_delete(request, pk):
    post = PostModel.objects.raw(f'SELECT * FROM post WHERE id={pk};')[0]
    if request.method == 'POST':
        post.delete()
        return redirect('/home')
    context = {
        'post': post
    }
    return render(request, 'main/post_delete.html', context)


@login_required
def account_search_view(request):
    context = {}
    if request.method == "GET":
        search_query = '%%' + request.GET.get("q") + '%%'

        if len(search_query) > 0:
            query = f"SELECT  * FROM user where first_name like '{search_query}' "
            search_results = make_query(User, query)
            accounts = []
            friend_query1 = f'select DISTINCT id_2, id from friend where id_1 = {request.user.id}'
            friend_query2 = f'select DISTINCT id_1, id from friend where id_2 = {request.user.id}'
            friend_result1 = make_query(Friend, friend_query1)
            friend_result2 = make_query(Friend, friend_query2)
            friends_ids1 = [friend.id_2.id for friend in friend_result1]
            friends_ids2 = [friend.id_1.id for friend in friend_result2]
            friends_ids = friends_ids1 + friends_ids2
            for account in search_results:

                if account.id in friends_ids:
                    accounts.append((account, True))
                else:
                    accounts.append((account, False))

            context['accounts'] = accounts
        print(context['accounts'])

    return render(request, "search/search_results.html", context)


@login_required
def chat_view(request):
    context = {}
    query = f'SELECT * FROM messages'
    results = make_query(Messages, query)
    for m in results:
        print(dir(m))
    context['messages'] = results
    return render(request, 'main/chat.html', context)
