from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from markdown2 import Markdown
from . import util
from . import forms
import random

markdowner = Markdown()
entries = util.list_entries()


def index(request):
    """
    Render index.html showing sorted list of entry in the encyclopedia. 
    """
    return render(request, "encyclopedia/index.html", {
        "entries": sorted(entries)
    })

def entry(request, title):
    """
    Render a page that displays the contents of encyclopedia entry specified in wiki/TITLE.
    If TITLE does not exist in the entry list, render error page.
    """
    # convert Markdown content to HTML 
    content = markdowner.convert(str(util.get_entry(title)))
    
    if util.is_entry(entries, title):
        return render(request, "encyclopedia/entry.html", {
            "content": content,
            "title": title
        })
    return render(request, "encyclopedia/error.html" )

def search(request):
    """
    Redirect to entry page that user type in the search box. 
    If query does not exist, render Search Result page that list all encyclopedia
    entries that have the query as substring. 
    """
    if request.method == "GET":
        q = request.GET.get("q")
        if not util.is_entry(entries, q):
            results = [entry for entry in entries if q.lower() in entry.lower()]
            return render(request, "encyclopedia/search.html", {
                "results": results, 
                "len": len(results)
            })
        return redirect(reverse("entry", args=[q]))

def create(request):
    """
    Render a page displaying a form to create new entry. 
    On "POST": 
        If title already exists, show alerts and display the form back to user.
        Otherwise, save entry to disk and redirect user to the new entry's page. 
    """
    if request.method == "POST":
        form = forms.NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            if not util.is_entry(entries, title):
                util.save_entry(title, body)
                entries.append(title)
                return redirect(reverse("entry", args=[title]))
            return render(request, 'encyclopedia/create.html', {
                "duplicate": True, 
                "form": form,
                "title": title,
                "alert": "This title already exist "
            })
        else:
            return render(request, 'encyclopedia/create.html', {
                "invalid": True, 
                "form": form,
                "alert": "Please fill in all the fields."
            })
    else:
        return render(request, "encyclopedia/create.html", {
            "form": forms.NewEntryForm()
        })

def random_page(request):
    """
    Redirect user to a random encyclopedia entry. 
    """
    entry = random.choice(entries)
    return redirect(reverse("entry", args=[entry]))

def edit(request, title):
    """
    Render a page to edit entry, 
    displaying a form pre-populated with the existing Markdown content of the page.
    On "POST":
        Rename title and content of the file on disk. 
        Redirect user to that entry's page. 
    """
    if request.method == "POST":
        form = forms.NewEntryForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data["title"]
            new_body = form.cleaned_data["body"]
            if title != new_title:
                util.delete_entry(title)
                entries[entries.index(title)] = new_title
            util.save_entry(new_title, new_body)
            return redirect(reverse("entry", args=[new_title]))
    else:
        body = util.get_entry(title)
        data = {'title': title, 'body': body}

        return render(request, 'encyclopedia/edit.html', {
            "title": title,
            "form": forms.NewEntryForm(data)
        })
