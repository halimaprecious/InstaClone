from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *



# Create your views here.
@login_required(login_url='/accounts/login/')
def home(request):
    images = Post.get_images()
    comments = Comment.get_comment()
    profile = Profile.get_profile()

    current_user = request.user
    if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = current_user
                comment.save()
            return redirect('home')

    else:
            form = CommentForm()
    
    context={
     "images":images [::-1], 
     "comments":comments,
     "form": form,
     "profile":profile
    }

    return render(request,'main.html',context=context)

@login_required
def profile(request,id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user_id= user)
    images = Post.objects.filter(user=id)

    context ={
        "user":user,
        "profile":profile,
        "images":images   
    } 
    return render(request,"profile.html",context=context)

# update profile
def add_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return redirect('home')

    else:
        form = NewProfileForm()
    return render(request, 'edit_profile.html', {"form": form})


def search_results(request):
    current_user = request.user
    profile = Profile.get_profile()
    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_name = Profile.find_profile(search_term)
        message = search_term

        return render(request,'search.html',{"message":message,
                                             "profiles":profile,
                                             "user":current_user,
                                             "username":searched_name})
    else:
        message = "You haven't searched for any user"
        return render(request,'search.html',{"message":message})

# single image
def get_image_by_id(request,image_id):

    image = Post.objects.get(id = image_id)
    comment = Post.objects.filter(id = image_id).all()

    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
        return redirect('home')

    else:
        form = CommentForm()

    return render(request,"detail.html", {"image":image,"comment":comment,"form": form})


@login_required(login_url='/accounts/login/')
def update_image(request):
    current_user = request.user
    profiles = Profile.get_profile()
    for profile in profiles:
        if profile.user.id == current_user.id:
            if request.method == 'POST':
                form = UploadForm(request.POST,request.FILES)
                if form.is_valid():
                    upload = form.save(commit=False)
                    upload.user = current_user
                    upload.profile = profile
                    upload.save()
                    return redirect('home')
            else:
                form = UploadForm()
            return render(request,'upload.html',{"user":current_user,"form":form})

@login_required(login_url='/accounts/login/')
def add_comment(request,pk):
    image = get_object_or_404(Post, pk=pk)
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.poster = current_user
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
        return render(request,'comment.html',{"user":current_user,"comment_form":form})

@login_required(login_url="/accounts/login/")
def like(request,operation,pk):
    image = get_object_or_404(Post,pk=pk)
    
    if operation == 'like':
        image.likes += 1
        image.save()
    elif operation =='unlike':
        image.likes -= 1
        image.save()
    return redirect('home')

# individual profile
@login_required(login_url='/accounts/login/')
def all(request, pk):
    profile = Profile.objects.get(pk=pk)
    images = Post.objects.all().filter(user=pk)
    content = {
        "profile": profile,
        'images': images,
    }
    return render(request, 'display.html', content)

@login_required(login_url='/accounts/login/')
def follow(request,operation,id):
    current_user=User.objects.get(id=id)
    if operation=='follow':
        Follow.follow(request.user,current_user)
        return redirect('home')
    elif operation=='unfollow':
        Follow.unfollow(request.user,current_user)
        return redirect('home')