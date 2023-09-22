#import self as self
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from .forms import PostForm, DebateForm, MessageForm
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, request
from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordChangeView
from MainApp.models import Post, Category, Profile, Comment
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, CreateView
from .models import Post, Debate, Category, Comment, User, Note
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from .forms import NoteForm, CommentForm

class DraftListView(LoginRequiredMixin, ListView):
    template_name = 'MainApp/post/draft_list.html'
    context_object_name = 'draft_posts'

    def get_queryset(self):
        # Retrieve draft posts authored by the currently logged-in user
        return Post.objects.filter(author=self.request.user, status=Post.Status.DRAFT)

    def get_post_detail_url(self, post):
        return reverse('MainApp:post_detail', kwargs={'pk': post.pk})


class user_blogs(ListView):
    print("blog LIST")
    model = Post
    template_name = 'MainApp/post/user_blogs.html'

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        print("author_id =", author_id)
        if author_id:
            return Post.objects.filter(author_id=author_id)
        else:
            return Post.objects.all()


def philosophy_view(request):
    # Logic for the philosophy section
    posts = get_category_posts("Philosophy", request)
    return render(request, 'MainApp/post/philosophy_blog.html', {'posts': posts})

def economics_view(request):
    # Logic for the economics section
    posts = get_category_posts("Economics", request)
    return render(request, 'MainApp/post/economics.html', {'posts': posts})

def medicine_view(request):
    # Logic for the medicine section
    posts = get_category_posts("Medicine", request)
    return render(request, 'MainApp/post/medicine_blogs.html', {'posts': posts})

def polisci_view(request):
    # Logic for the political science section
    posts = get_category_posts("Political Science", request)
    return render(request, 'MainApp/post/polisci_blogs.html', {'posts': posts})

def about(request):
    return render(request, 'MainApp/post/about.html')

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'MainApp/post/list.html')

    form = NoteForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            note = form.save(commit=False)
            note.profile = request.user.profile
            note.user = request.user
            note.save()
            return redirect('MainApp:home')

    try:
        profile = request.user.profile
        followed_profiles = profile.follows.all()
        notes = Note.objects.filter(profile__in=followed_profiles).order_by("-created_at")
    except:
        return redirect("create_profile_page")

    return render(request, 'MainApp/post/list.html', {'notes': notes, "form": form})

# Helper function to get posts by category and paginate them
def get_category_posts(category_name, request):
    home = Post.published.all().filter(category__category=category_name)
    paginator = Paginator(home, 2)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts

class post_detail(DetailView, ):
    model = Post
    template_name = 'MainApp/post/detail.html'
    success_url = reverse_lazy('post_detail')

@require_POST
def debate_post(request, debate_id):
    print("DEBATE POST")
    post = get_object_or_404(Debate, id=debate_id)
    comment = None
    #???????????????????????????????
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'MainApp/debate/comment.html',
                  {'post':post, 'form':form, 'comment':comment})


class user_debate_list(ListView):
    print("DEBATE LIST")
    model = Debate
    template_name = 'MainApp/debate/user_debates.html'

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        print("author_id =", author_id)
        if author_id:
            return Debate.objects.filter(author_id=author_id)
        else:
            return Debate.objects.all()

class debate_list(ListView):
    print("DEBATE LIST")
    model = Debate
    template_name = 'MainApp/debate/debate_list.html'
    def get_queryset(self):
        author_id = self.request.GET.get('author')
        print("author_id =", author_id)
        if author_id:
            return Debate.objects.filter(author_id=author_id)
        else:
            return Debate.objects.all()

class economics_debate_list(ListView):
    print("ECON DEBATE LIST")
    model = Debate
    template_name = 'MainApp/debate/economics_debate_list.html'

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        print("author_id =", author_id)
        if author_id:
            return Debate.objects.filter(author_id=author_id)
        else:
            return Debate.objects.all()

class polisci_debate_list(ListView):
    print("POLISCI DEBATE LIST")
    model = Debate
    template_name = 'MainApp/debate/polisci_debate_list.html'

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        print("author_id =", author_id)
        if author_id:
            return Debate.objects.filter(author_id=author_id)
        else:
            return Debate.objects.all()

class medicine_debate_list(ListView):
    print("MEDICINE DEBATE LIST")
    model = Debate
    template_name = 'MainApp/debate/medicine_debate_list.html'

    def get_queryset(self):
        author_id = self.request.GET.get('author')
        print("author_id =", author_id)
        if author_id:
            return Debate.objects.filter(author_id=author_id)
        else:
            return Debate.objects.all()

class debate_detail(DetailView):
    model = Debate
    template_name = 'MainApp/debate/debate_detail.html'

class philosophy_blog(ListView):
    model = Post
    template_name = 'MainApp/post/philosophy_blog.html'


class AddBlogView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'MainApp/post/add_post.html'
    success_url = reverse_lazy('MainApp:home')

    def form_valid(self, form):
        # Set the author of the post to the currently logged-in user
        form.instance.author = self.request.user

        # Capitalize the first letter of the academic_field and set it as the category name
        academic_field = self.request.user.profile.academic_field.capitalize()
        category, _ = Category.objects.get_or_create(category=academic_field)
        form.instance.category = category

        return super().form_valid(form)

class AddDebateView(LoginRequiredMixin, CreateView):
    model = Debate
    form_class = DebateForm
    template_name = 'MainApp/debate/add_debate.html'
    success_url = reverse_lazy('MainApp:debate_list')

def AddCommentView(request, pk):
    debate = get_object_or_404(Debate, id=pk)
    comment = get_object_or_404(Debate, id=pk)
    user = request.user
    opponent = debate.opponent
    comments = debate.comments.all()
    # Check if the user is the author or opponent
    if user != debate.author and user != opponent:
        return redirect('MainApp:home')

    if comments.exists():
        last_comment = comments.last()
        last_commenter_name = last_comment.commenter_name
        print("Opponent: ", last_commenter_name)
        if last_commenter_name == request.user:
            return redirect('MainApp:home')
        else:
            form = CommentForm(request.POST or None)
            if request.method == 'POST' and form.is_valid():
                comment = form.save(commit=False)
                comment.debate_id = pk
                comment.save()
                return redirect('MainApp:home')

    return render(request, 'MainApp/debate/add_comment.html', {'form': form, 'debate': debate})

class UpdateBlogView(UpdateView):
    model = Post
    template_name = 'MainApp/post/update_blog.html'
    fields = ['title', 'body', 'status']
    success_url = reverse_lazy('MainApp:home')

    def form_valid(self, form):
        # Set the author of the post to the currently logged-in user
        form.instance.author = self.request.user

        # Capitalize the first letter of the academic_field and set it as the category name
        academic_field = self.request.user.profile.academic_field.capitalize()
        category, _ = Category.objects.get_or_create(category=academic_field)
        form.instance.category = category

        return super().form_valid(form)

class DeleteBlogView(DeleteView):
    model = Post
    template_name = 'MainApp/post/delete_blog.html'
    success_url = reverse_lazy('MainApp:philosophy_blog_list')

def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'MainApp/post/profile_list.html', {'profiles':profiles})

def delete_note(request, pk):
    if request.user.is_authenticated:
        note = get_object_or_404(Note, id=pk)
        #check if user owns note
        if request.user.username == note.user.username:
            note.delete()
            #messages
            print("Note Deleted")
            return redirect('MainApp:home')
        else:
            #messages
            print("not your note")
            return redirect("MainApp:home")

def edit_note(request, pk):
    if request.user.is_authenticated:
        note = get_object_or_404(Note, id=pk)
        if request.user.username == note.user.username:
            form = NoteForm(request.POST or None, instance=note)
            if request.method == "POST":
                if form.is_valid():
                    note = form.save(commit=False)
                    note.profile = request.user.profile
                    note.user = request.user
                    note.save()
                    print("Note edited")
                    return redirect('MainApp:home')
                    print("error1")
            else:
                #messages
                print("error2")
                print("not your note")
                return render(request, 'MainApp/note/edit_note.html', {'form':form, 'note':note})
        else:
            print("error3")
            success_url = reverse_lazy('MainApp:philosophy_blog_list')

@login_required
def conversation_list(request):
    user = request.user
    conversations = User.objects.exclude(id=user.id)

    conversations_with_messages = []
    for conversation in conversations:
        has_sent_messages = Message.objects.filter(sender=user, receiver=conversation).exists()
        has_received_messages = Message.objects.filter(sender=conversation, receiver=user).exists()

        if has_sent_messages or has_received_messages:
            conversations_with_messages.append(conversation)

    return render(request, 'MainApp/conversations/conversation_list.html', {'conversations': conversations_with_messages})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message

@login_required
def conversation_detail(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    sender = request.user

    messages = Message.objects.filter(
        (Q(sender=sender) & Q(receiver=receiver)) |
        (Q(sender=receiver) & Q(receiver=sender))
    ).order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.receiver = receiver
            message.save()
            return redirect('MainApp:conversation_detail', receiver_id=receiver_id)
    else:
        form = MessageForm()

    return render(request, 'MainApp/conversations/conversation_detail.html', {'receiver': receiver, 'messages': messages, 'form': form})


@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()

            # Redirect to the conversation_detail view with the correct receiver_id
            return redirect('MainApp:conversation_detail', receiver_id=receiver_id)
    else:
        form = MessageForm()

    return render(request, 'MainApp:conversation_detail', {'receiver': receiver, 'form': form})