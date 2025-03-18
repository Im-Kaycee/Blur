from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

# Create your views here.

@login_required
def home1(request):
    # Separate group chats and private chats
    group_chats = ChatGroup.objects.filter(members=request.user, is_private=False)
    private_chats = ChatGroup.objects.filter(members=request.user, is_private=True)
    
    # Attach the last group chat message to each group chat
    for chatroom in group_chats:
        chatroom.last_message = chatroom.chat_messages.order_by('-created').first()

    # Attach the last private chat message to each private chat
    for chatroom in private_chats:
        chatroom.last_message = chatroom.chat_messages.order_by('-created').first()

    context = {
        'group_chats': group_chats,
        'private_chats': private_chats,
    }

    return render(request, 'index.html', context)

@login_required
def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    
    # Delete expired messages (24 hours after being viewed)
    chat_group.chat_messages.filter(viewed_at__lte=timezone.now() - timedelta(hours=24)).delete()

    chat_messages = chat_group.chat_messages.all()[:30]

    # Mark messages as viewed if they haven't been marked yet
    for message in chat_messages:
        if not message.viewed_at and message.author != request.user:
            message.viewed_at = timezone.now()
            message.save()

    form = ChatMessageCreateForm()
    other_user = None

    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404("You are not a member of this chat")
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    if chat_group.groupchat_name:
        if request.user not in chat_group.members.all():
            chat_group.members.add(request.user)

    if request.htmx:
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = { 
                'message': message,
                'user': request.user
            }
            return render(request, 'chat/partials/chat_message_p.html', context)

    context = {
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom_name,
        'chat_group': chat_group,
    }

    return render(request, 'chat/chat.html', context)

@login_required
def get_or_create_chatroom(request, username):
    if username == request.user.username:
        return redirect('home')
    try:
        other_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404(f"User '{username}' does not exist.")
    other_user = User.objects.get(username=username)
    mychatrooms = request.user.chat_groups.filter(is_private=True)
    if mychatrooms.exists():
        for chatroom in mychatrooms:
            if other_user in chatroom.members.all():
               chatroom = chatroom
               break
            else:
                chatroom = ChatGroup.objects.create(is_private=True)
                chatroom.members.add(request.user, other_user)
    else:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(request.user, other_user)
    if not chatroom.group_name:
        chatroom.save()  # This will trigger the model's save() method to generate a group_name
    return redirect('chatroom', chatroom.group_name)
    
@login_required
def create_groupchat(request):
    form = NewGroupForm()

    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('chatroom', new_groupchat.group_name)

    context = {
        'form': form
    }
    return render(request, 'chat/create_groupchat.html', context)
def chatroom_edit_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup,group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    form = ChatRoomEditForm(instance=chat_group)
    if request.method == "POST":
        form= ChatRoomEditForm(request.POST, instance=chat_group)
        if form.is_valid():
            form.save()
            remove_members = request.POST.getlist('remove_members')
            for member_id in remove_members:
                member = User.objects.get(id=member_id)
                chat_group.members.remove(member)
                return redirect('chatroom' ,chatroom_name)
    context = {
        'form':form,
        'chat_group':chat_group,
    }
    return render(request, 'chat/chatroom_edit.html', context)

@login_required
def chatroom_delete_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    
    if request.method == "POST":
        chat_group.delete()
        messages.success(request, 'Chatroom deleted')
        return redirect('home')
    
    return render(request, 'chat/chatroom_delete.html', {'chat_group':chat_group})
@login_required
def chatroom_leave_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)

    if request.user not in chat_group.members.all():
        raise Http404()

    if request.method == "POST":
        chat_group.members.remove(request.user)
        messages.success(request, 'You left the chat.')

        # Handle HTMX request (prevent full page reload)
        if request.htmx:
            return HttpResponse("<script>window.location.href='/';</script>")

        return redirect('index')

    # If it's a GET request, show the leave confirmation modal
    return render(request, 'chat/partials/modal_chat_leave.html', {'chat_group': chat_group})
login_required
def delete_message(request, message_id):
    message = get_object_or_404(GroupMessage, id=message_id)
    if message.author != request.user:
        raise Http404("You do not have permission to delete this message.")
    
    if request.method == "POST":
        message.delete()  
        messages.success(request, "Message deleted successfully.")
        return redirect('chatroom', message.group.group_name)
    
    return render(request, 'chat/confirm_delete_message.html', {'message': message})
@login_required
def edit_message(request, message_id):
    message = get_object_or_404(GroupMessage, id=message_id)
    if message.author != request.user:
        raise Http404("You do not have permission to edit this message.")
    
    if request.method == "POST":
        form = EditMessageForm(request.POST, instance=message)
        if form.is_valid():
            edited_message = form.save(commit=False)
            edited_message.edited_at = timezone.now()
            edited_message.save()
            messages.success(request, "Message edited successfully.")
            return redirect('chatroom', message.group.group_name)
    else:
        form = EditMessageForm(instance=message)
    
    return render(request, 'chat/edit_message.html', {'form': form, 'message': message})