from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Slip, SlipQuestion, ClassList, YEAR_CHOICES, SEM_CHOICES, ExploreTopic, CATEGORY_CHOICES, Profile, CommunityThread, CommunityReply, Bookmark
from .forms import UserRegistrationForm, CommunityThreadForm, CommunityReplyForm, ProfileEditForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
#curscor
# Create your views here.

def home(request):
    print("helloWorld")
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        print(name)
        user=authenticate(request, username = name, password = password)
        if user is not None:
            login(request,user)
            messages.success(request,f"{user.username} Login Sucessfully")
            return redirect('CampusMateApp:profile',request.user.username)
        else:
            messages.error(request,'Invalid Name and Password ')
            return redirect('CampusMateApp:login')
    return render(request, 'login.html')

def profile_view(request,username):
    user= get_object_or_404(User, username=username)

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    user_info = Profile.objects.get(user=user)
    bookmarks = Bookmark.objects.filter(user=user)[:10]  # Show latest 10 bookmarks
    
    context = {
        'user_info': user_info,
        'bookmarks': bookmarks,
        'user': user,
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    
    # Check if user is editing their own profile
    if request.user != user:
        messages.error(request, 'You can only edit your own profile.')
        return redirect('CampusMateApp:profile', username=username)
    
    try:
        user_info = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        user_info = Profile.objects.create(user=user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user_info)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('CampusMateApp:profile', username=username)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileEditForm(instance=user_info)
    
    return render(request, 'edit_profile.html', {'form': form, 'user': user, 'user_info': user_info})

def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Save the user first
            Profile.objects.create(user=user)  # Create an empty profile for the new user
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('CampusMateApp:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('CampusMateApp:login')



def settings_view(request):
    if request.method == 'POST':
        # Handle dark mode toggle
        dark_mode = request.POST.get('dark_mode') == 'on'
        request.session['dark_mode'] = dark_mode
        messages.success(request, 'Settings updated successfully!')
        return redirect('CampusMateApp:settings')
    
    # Get current dark mode status
    dark_mode = request.session.get('dark_mode', False)
    
    return render(request, 'settings.html', {'dark_mode': dark_mode})

def explore_topics_view(request):
    selected_category = request.GET.get('category')
    search_query = request.GET.get('q')

    topics = ExploreTopic.objects.all()

    if selected_category:
        topics = topics.filter(category=selected_category)

    if search_query:
        topics = topics.filter(title__icontains=search_query) | topics.filter(description__icontains=search_query)

    context = {
        'topics': topics,
        'categories': [choice[0] for choice in CATEGORY_CHOICES],
        'selected_category': selected_category,
        'search_query': search_query,
    }
    return render(request, 'explore.html', context)

def explore_topic_detail_view(request, pk):
    topic = get_object_or_404(ExploreTopic, pk=pk)
    return render(request, 'explore_topic_detail.html', {'topic': topic})

def community_view(request):
    search_query = request.GET.get('q')
    category_filter = request.GET.get('category')
    
    threads = CommunityThread.objects.all()
    
    if search_query:
        threads = threads.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )
    
    if category_filter:
        threads = threads.filter(category=category_filter)
    
    context = {
        'threads': threads,
        'categories': [choice[0] for choice in CATEGORY_CHOICES],
        'search_query': search_query,
        'selected_category': category_filter,
    }
    return render(request, 'community.html', context)


@login_required
def create_thread_view(request):
    if request.method == 'POST':
        form = CommunityThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            messages.success(request, 'Thread created successfully!')
            return redirect('CampusMateApp:thread_detail', pk=thread.pk)
    else:
        form = CommunityThreadForm()
    
    return render(request, 'create_thread.html', {'form': form})


def thread_detail_view(request, pk):
    thread = get_object_or_404(CommunityThread, pk=pk)
    
    # Increment view count
    thread.views += 1
    thread.save(update_fields=['views'])
    
    if request.method == 'POST' and request.user.is_authenticated:
        reply_form = CommunityReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.thread = thread
            reply.author = request.user
            reply.save()
            messages.success(request, 'Reply posted successfully!')
            return redirect('CampusMateApp:thread_detail', pk=thread.pk)
    else:
        reply_form = CommunityReplyForm()
    
    replies = thread.replies.all()
    
    context = {
        'thread': thread,
        'replies': replies,
        'reply_form': reply_form,
    }
    return render(request, 'thread_detail.html', context)

def slip_solutions(request):
    selected_class_name = request.GET.get('class')
    selected_year = request.GET.get('year')
    selected_sem = request.GET.get('sem')

    slips = Slip.objects.all()
    if selected_class_name:
        slips = slips.filter(class_name__class_name=selected_class_name)
    if selected_year:
        slips = slips.filter(year=selected_year)
    if selected_sem:
        slips = slips.filter(sem=selected_sem)

    classes = ClassList.objects.all().order_by('class_name')
    years = [choice[0] for choice in YEAR_CHOICES]
    semesters = [choice[0] for choice in SEM_CHOICES]

    context = {
        'slips': slips,
        'classes': classes,
        'years': years,
        'semesters': semesters,
        'selected_class': selected_class_name,
        'selected_year': selected_year,
        'selected_sem': selected_sem,
    }
    return render(request, 'slip_list.html', context)


def slip_question_detail(request, pk):
    question = get_object_or_404(SlipQuestion, pk=pk)
    return render(request, 'slip_question_detail.html', {'question': question})

def privacy_policy_view(request):
    return render(request, 'privacy_policy.html')

def terms_of_service_view(request):
    return render(request, 'terms_of_service.html')

def support_view(request):
    return render(request, 'support.html')