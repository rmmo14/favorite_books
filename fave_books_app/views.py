from django.shortcuts import render, redirect
from .models import User, Book
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    context = {
        'allUsers': User.objects.all()
    }
    return render(request, "index.html", context)

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.my_validator(request.POST)
    c = User.objects.last()
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        c.delete()
        return redirect ('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print('hash', User.objects.all())
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash,
        )
        request.session['user_id'] = new_user.id
        return redirect('/books')

def login(request):
    if request.method == "GET":
        return redirect('/')
    user = User.objects.filter(email = request.POST['email'])
    print('email')
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['login_pw'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            print('id is', logged_user.id)
            return redirect('/books')
        else:
            messages.error(request, "Incorrect email or password")
        return redirect('/')
    messages.error(request, "No account with that information...please register")
    return redirect('/')   

def books(request):
    if 'user_id' not in request.session:
        print("not in session")
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    context = {
        'user': user,
        'books': Book.objects.all(),
    }
    request.session['email'] = user.email
    print(user.email)
    return render(request, "books.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def add_book(request):
    if 'user_id' not in request.session:
        print("not in session")
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    if len(request.POST['title']) > 0:
        print('desc is', request.POST['description'])
        if len(request.POST['description']) > 4:
            new_book = Book.objects.create(title = request.POST['title'], description=request.POST['description'], uploaded_by=user)
            user.liked_books.add(new_book)
    return redirect(f'/books/{new_book.id}')

def bookinfo(request, book_id):
    if 'user_id' not in request.session:
        print("not in session")
        return redirect('/')
    this_book = Book.objects.get(id=book_id)
    context = {
        'this_book': this_book,
        'this_user': User.objects.get(id=request.session['user_id'])
    }
    print('check this:',this_book.users_who_like.all())
    return render(request, 'bookinfo.html', context)

def update(request, book_id):
    book = Book.objects.get(id=book_id)
    book.title = request.POST['title']
    book.description = request.POST['description']
    book.save()
    return redirect(f"/books/{book_id}")

def delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('/books')

def favorite(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    user.liked_books.add(book)
    return redirect(f'/books/{book_id}')

def unfavorite(request, book_id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=book_id)
    user.liked_books.remove(book)
    return redirect(f'/books/{book_id}')
