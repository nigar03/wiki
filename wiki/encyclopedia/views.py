
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .forms import EditPageForm
from .util import get_entry_content,  get_all_entries,save_entry,convert_markdown_to_html
from django.http import HttpResponse
from .forms import NewPageForm
from . import util
import random




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_view(request, title):
    entries = get_all_entries()
    if title not in entries:
        return HttpResponse("Page not found.", status=404)

    content = get_entry_content(title)
    html_content = convert_markdown_to_html(content)
    return render(request, 'entry.html', {'title': title, 'content': html_content})
# views.py

from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

def index_view(request):
    entries = get_all_entries()  # Retrieve all entries
    return render(request, 'index.html', {'entries': entries})


def search_view(request):
    query = request.GET.get('q', '').strip()
    entries = get_all_entries()

    if query:
        # Check for exact match
        if query in entries:
            return redirect('entry_view', title=query)

        # Find entries that contain the query as a substring
        search_results = [entry for entry in entries if query.lower() in entry.lower()]

        return render(request, 'search_results.html', {
            'query': query,
            'search_results': search_results,
        })

    return HttpResponse("No query provided.")


def create_page_view(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            entries = get_all_entries()
            if title in entries:
                # Title already exists
                return render(request, 'create_page.html', {
                    'form': form,
                    'error': 'An entry with this title already exists.',
                })
            else:
                # Save the new entry
                save_entry(title, content)
                return redirect('entry_view', title=title)
    else:
        form = NewPageForm()

    return render(request, 'create_page.html', {'form': form})


def edit_page_view(request, title):
    entries = get_all_entries()

    if title not in entries:
        return HttpResponse("Page not found.", status=404)

    if request.method == 'POST':
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            save_entry(title, content)  # Save the updated content
            return redirect('entry_view', title=title)
    else:
        content = get_entry_content(title)  # Get the current content of the page
        form = EditPageForm(initial={'content': content})

    return render(request, 'edit_page.html', {'form': form, 'title': title})


def random_page_view(request):
    entries = get_all_entries()
    if entries:
        random_entry = random.choice(entries)
        return redirect('entry_view', title=random_entry)
    else:
        return HttpResponse("No entries available.", status=404)