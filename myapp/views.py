# Create your views here.
from django.shortcuts import render,redirect
from .models import *
from .serializers import userSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages
from django.utils import timezone

class taskViewSet(viewsets.ModelViewSet):
    queryset = user.objects.all()
    serializer_class = userSerializer


def index(request):
    search_query = request.GET.get('search', '')  # Fetch search query from request
    filter_option = request.GET.get('filter', '')  # Fetch filter option if any

    # Handle records_per_page parameter safely
    try:
        records_per_page = int(request.GET.get('records_per_page', 5))  # Default to 5 if not set or invalid
    except ValueError:
        records_per_page = 5  # Fallback to default if conversion fails

    # Start with all users in the database
    users = user.objects.all().order_by('-updated_at', '-id')

    # Apply search filter if search query is provided
    if search_query:
        users = users.filter(
            Q(author__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(book_type__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Apply additional filters (if any)
    if filter_option == 'published_before_2024':
        users = users.filter(date__lt='2024-01-01')  # Filter users with date before 2024
    elif filter_option == 'published_after_2024':
        users = users.filter(date__gte='2024-01-01')  # Filter users with date after 2024
    elif filter_option == 'Religious':
        users = users.filter(book_type__icontains='Religious')
    elif filter_option == 'Adventure':
        users = users.filter(book_type__icontains='Adventure')
    elif filter_option == 'Science Fiction':
        users = users.filter(book_type__icontains='Science Fiction')

    # Pagination logic
    paginator = Paginator(users, records_per_page)
    page_number = request.GET.get('page', 1)  # Get current page number (default to 1)
    page_obj = paginator.get_page(page_number)

    # Add sequential ID logic for user entries (for display purposes)
    for idx, user_obj in enumerate(page_obj.object_list, start=1):
        user_obj.display_id = idx

    start_index = (page_obj.number - 1) * records_per_page
    # Return the response with paginated data, search query, and filter option
    return render(request, 'index.html', {
        'users': page_obj,  # Paginated user data
        'search': search_query,  # Include the search query
        'filter': filter_option,  # Include the filter option
        'records_per_page': records_per_page,  # Include records per page selected
        'start_index': start_index  # Records per page
    })

def display_all(request):
    search_query = request.GET.get('search', '')  # Fetch search query from request
    filter_option = request.GET.get('filter', '')  # Fetch filter option if any

    # Default records per page from GET parameter
    try:
        records_per_page = int(request.GET.get('records_per_page', 5))  # Default to 5 if not set or invalid
    except ValueError:
        records_per_page = 5  # Fallback to default if conversion fails

    # Start with all users in the database
    users = user.objects.all().order_by('-id')

    # Apply search filter if search query is provided
    if search_query:
        users = users.filter(
            Q(author__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(book_type__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Apply additional filters (if any)
    if filter_option == 'published_before_2024':
        users = users.filter(date__lt='2024-01-01')  # Filter users with date before 2024
    elif filter_option == 'published_after_2024':
        users = users.filter(date__gte='2024-01-01')  # Filter users with date after 2024
    elif filter_option == 'Religious':
        users = users.filter(book_type__icontains='Religious')
    elif filter_option == 'Adventure':
        users = users.filter(book_type__icontains='Adventure')
    elif filter_option == 'Science Fiction':
        users = users.filter(book_type__icontains='Science Fiction')

    # Pagination logic
    paginator = Paginator(users, records_per_page)
    page_number = request.GET.get('page', 1)  # Get current page number (default to 1)
    page_obj = paginator.get_page(page_number)

    # Add sequential ID logic for user entries (for display purposes)
    for idx, user_obj in enumerate(page_obj.object_list, start=1):
        user_obj.display_id = idx

    start_index = (page_obj.number - 1) * records_per_page
    # Return the response with paginated data, search query, and filter option
    return render(request,'display_all.html', {
        'users': page_obj,  # Paginated user data
        'search': search_query,  # Include the search query
        'filter': filter_option,  # Include the filter option
        'records_per_page': records_per_page,  # Include records per page selected
        'start_index': start_index  # Records per page
    })


from datetime import datetime

def add_records(request):
    if request.POST:
        title = request.POST['title'].strip()
        author = request.POST['author'].strip()
        book_type = request.POST['book_type'].strip()
        date = request.POST['date'].strip()
        description = request.POST['description'].strip()

        # Convert date to a datetime object
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'add_records.html', {'error': 'Invalid Date Format! Please use YYYY-MM-DD.'})

        # Check for invalid date: 500 years ago or future date
        current_date = datetime.now().date()
        min_date = current_date.replace(year=current_date.year - 500)

        if date_obj > current_date:
            return render(request, 'add_records.html', {'error': 'Published Date cannot be in the future!'})
        elif date_obj < min_date:
            return render(request, 'add_records.html', {'error': 'Published Date cannot be older than 500 years!'})
            
        # Proceed with the save if all validations pass
        iid = user.objects.create(
            title=title,
            author=author,
            book_type=book_type,
            date=date_obj,
            description=description
        )

        messages.success(request, 'Book added successfully!')
        return redirect('index')
    else:
        return render(request, 'add_records.html')

def delete(request,id):

    did = user.objects.get(id=id).delete()

    messages.success(request, 'Book deleted successfully!')
    return redirect('index')

def update(request, id):
    uid = user.objects.get(id=id)

    if request.method == 'POST':
        title = request.POST['title'].strip()
        author = request.POST['author'].strip()
        book_type = request.POST['book_type'].strip()
        date = request.POST['date'].strip()
        description = request.POST['description'].strip()

        # Convert date to a datetime object
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'update.html', {'error': 'Invalid Date Format! Please use YYYY-MM-DD.', 'users': [uid]})

        # Check for invalid date: 500 years ago or future date
        current_date = datetime.now().date()
        min_date = current_date.replace(year=current_date.year - 500)

        if date_obj > current_date:
            return render(request, 'update.html', {'error': 'Date cannot be in the future!', 'users': [uid]})
        elif date_obj < min_date:
            return render(request, 'update.html', {'error': 'Date cannot be older than 500 years!', 'users': [uid]})

        # Update the record
        uid.title = title
        uid.author = author
        uid.date = date_obj
        uid.book_type = book_type
        uid.description = description
        uid.updated_at = timezone.now()
        uid.save()

        messages.success(request, 'Book updated successfully!')
        return redirect('index')
    else:
        return render(request, 'update.html', {'users': [uid]})


# def records_per_page_view(request):
#     # Step 1: Get the records_per_page from the session or GET parameter (default to 5)
#     if 'records_per_page' in request.GET:
#         records_per_page = int(request.GET.get('records_per_page'))
#         request.session['records_per_page'] = records_per_page  # Save to session
#     else:
#         records_per_page = request.session.get('records_per_page', 5)  # Default to 5

#     # Step 2: Fetch all records and order by '-id'
#     allrecords = user.objects.all().order_by('-id')

#     # Step 3: Apply pagination based on records_per_page
#     paginator = Paginator(allrecords, records_per_page)
#     page_number = request.GET.get('page', 1)  # Get the current page number (default to 1)
#     page_obj = paginator.get_page(page_number)  # Get paginated data

#     # Step 4: Render the template with paginated data
#     return render(request, 'index.html', {
#         'users': page_obj,  # Paginated records for the current page
#         'records_per_page': records_per_page,  # Pass selected records per page
#     })



def records_per_page_view_2(request):
    # Step 1: Check if the default parameter is sent to reset records_per_page
    if 'default' in request.GET:
        records_per_page = 5  # Reset to default value
        request.session['records_per_page'] = records_per_page  # Update session
    elif 'records_per_page' in request.GET:
        records_per_page = int(request.GET.get('records_per_page'))
        request.session['records_per_page'] = records_per_page  # Save to session
    else:
        records_per_page = request.session.get('records_per_page', 5)  # Default to 5

    # Step 2: Fetch all records and order by '-id'
    allrecords = user.objects.all().order_by('-id')

    # Step 3: Apply pagination based on records_per_page
    paginator = Paginator(allrecords, records_per_page)
    page_number = request.GET.get('page', 1)  # Get the current page number (default to 1)
    page_obj = paginator.get_page(page_number)  # Get paginated data

    # Step 4: Render the template with paginated data
    return render(request, 'display_all.html', {
        'users': page_obj,  # Paginated records for the current page
        'records_per_page': records_per_page,  # Pass selected records per page
    })

def search_all(request):
    search_query = request.GET.get('search', '')
    rid = user.objects.all()

    if search_query:
        rid = rid.filter(
            Q(author__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(book_type__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    records_per_page = int(request.GET.get('per_page', 5))  # Default per page is 5
    paginator = Paginator(rid, records_per_page)
    page_number = request.GET.get('page') # Get current page number
    page_obj = paginator.get_page(page_number)

    # Add sequential ID logic for user entries (for display purposes)
    for idx, user_obj in enumerate(page_obj.object_list, start=1):
        user_obj.display_id = idx

    start_index = (page_obj.number - 1) * records_per_page

    return render(request, 'display_all.html',{
        'rid': page_obj,  # Paginated user data
        'search': search_query,  # Include the search query
        'records_per_page': records_per_page,
        'start_index': start_index  })





      

            





























    


