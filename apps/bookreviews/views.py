from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Book, Review
from django.http import HttpResponseRedirect

# Create your views here.
# login and registration page
def index(request):
	# # Use to clear the whole db 
	# User.objects.all().delete()
	# Book.objects.all().delete()
	# Review.objects.all().delete()
	return render(request, "bookreviews/index.html")

# home page
def home(request):
	reviews = Review.objects.all().order_by('-created_at')[:3]
	books_with_reviews = []
	books_with_reviews_titles = []
	reviewed = Review.objects.all()
	for review in reviewed:
		if review.book.title not in books_with_reviews_titles:
			books_with_reviews_titles.append(review.book.title)
			books_with_reviews.append(review.book)
	context = {
		"user": User.objects.get(id=request.session['user']),
		"reviews": reviews,
		"books": books_with_reviews
	}
	return render(request, "bookreviews/home.html", context)

# add a book and review page
def add_review_page(request):
	authors = []
	books = Book.objects.all()
	for book in books:
		if book.author not in authors:
			authors.append(book.author)
	print authors
	context  = {
		"authors": authors
	}
	return render(request, "bookreviews/add.html", context)

# book page
def books(request, id):
	user = User.objects.get(id=request.session['user'])
	book = Book.objects.get(id=id)
	context = {
		"user": user,
		"book": book,
		"reviews": Review.objects.filter(book=book)
	}
	return render(request, "bookreviews/book.html", context)

# user page
def user(request, id):
	user = User.objects.get(id=id)
	context = {
		"user": user,
		"books": user.reviewed.all(),
		"reviews": Review.objects.filter(user=user)
	}
	return render(request, "bookreviews/user.html", context)


# process log in and regstration
def process_logreg(request):
	if request.POST['action'] == 'register':
		postData = {
			'name': request.POST['name'],
			'alias': request.POST['alias'],
			'email': request.POST['email'],
			'password': request.POST['password'],
			'confirm_pw': request.POST['confirm_pw']
		}
		user = User.objects.register(postData)
		if 'error' in user:
			for message in user['error']:
				messages.error(request, message)
			return redirect('/')
		if 'theuser' in user:
			messages.success(request, 'Successfully registered, you may now log in.')
			return redirect('/')
	elif request.POST['action'] == 'login':
		postData = {
			'email': request.POST['email'],
			'password': request.POST['password']
		}
		user = User.objects.login(postData)
		if 'error' in user:
			for message in user['error']:
				messages.error(request, message)
			return redirect('/')
		if 'theuser' in user:
			request.session['user'] = user['theuser'].id
			return redirect('/books')

# creating review from add new book page
def post_review(request):
	user = User.objects.get(id=request.session['user'])
	authors = request.POST.getlist('author')
	for a in authors:
		if a:
			author = a
	print authors
	print author
	book, created = Book.objects.get_or_create(title=request.POST['title'], author=author)
	Review.objects.create(content=request.POST['content'], rating=request.POST['rating'], user=user, book=book)
	book.reviewed.add(user)
	return redirect('/books/' + str(book.id))

# creating review from book page
def post_review2(request, id):
	user = User.objects.get(id=request.session['user'])
	book = Book.objects.get(id=id)
	Review.objects.create(content=request.POST['content'], rating=request.POST['rating'], user=user, book=book)
	book.reviewed.add(user)
	return redirect('/books/' + str(id))

# deleting review
def delete_review(request, id):
	Review.objects.get(id=id).delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# logout, clear session, return to log in page
def logout(request):
	request.session.clear()
	return redirect('/')

