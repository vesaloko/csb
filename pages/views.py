from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from .models import Todo
from django.contrib.auth.models import User


@login_required
def index(request):
    todos = Todo.objects.filter(owner=request.user)
    return render(request, 'index.html', {'todos': todos, "currentuser":request.user})


# FLAW 2: Sensitive data exposure
# FLAW 3: Broken acces control
@csrf_exempt # FLAW 4: FIX: change to @csrf_protect
@login_required
def addtodo(request):
    if request.method == "GET":  
        user = User.objects.get(username=request.GET.get("user"))
        text = request.GET.get("todo")
        done = request.GET.get("done") == 'on'

        if text:
            todo = Todo(owner=user, text=text, done=done)
            todo.save()

        return redirect("/")
    
# FLAW 2 & 3: FIX
# @login_required
## FLAW 4: @csrf_protect
# def addtodo(request):
#   if request.method == "POST":
#        user = request.user
#        text = request.POST.get("todo")
#        done = request.POST.get("done") == 'on'
#       
#        if text:
#            todo = Todo(owner=user, text=text, done=done)
#            todo.save()
#   return redirect("/")


# FLAW 3: FIX: @login_required
@csrf_exempt # FLAW 4: FIX: change to csrf_protect
def deletetodo(request):
        todo = Todo.objects.get(pk=request.POST.get('id'))
        if  todo and request.user == todo.owner: # FLAW 3: enhanced acces control
            todo.delete()
        else:
            return HttpResponse("You do not own this todo. Deleting the todo needs authorization of the correct user. ")
        return redirect("/")


# FLAW 3: FIX: @login_required
def viewall(request):
    text = request.GET.get("text") 
    todo = Todo.objects.raw("SELECT * FROM pages_todo WHERE owner_id = {} OR text LIKE '%{}%'".format(request.user.id, text)) # FLAW 1: SQL injection
    # FLAW 1: FIX: todo = Todo.objects.filter(owner=request.user)
    return render(request, 'viewall.html', {'todo': todo})


# FLAW 3: FIX: @login_required
def viewtodo(request, todo_id):
    todo = Todo.objects.get(id=todo_id) # FLAW 2: Sensitive data exposure
    # FLAW 2 & 3: FIX: todo = Todo.objects.get(id=todo_id, owner=request.user)
    return render(request, 'viewtodo.html', {'todo': todo})


