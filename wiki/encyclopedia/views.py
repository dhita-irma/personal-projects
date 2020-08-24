from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from markdown2 import Markdown
from . import util
from . import forms
import os
import random

markdowner = Markdown()
entries = util.list_entries()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": sorted(entries)
    })

def entry(request, title):
    if util.is_entry(entries, title):
        return render(request, "encyclopedia/entry.html", {
            "content": markdowner.convert(str(util.get_entry(title))),
            "title": title
        })
    return render(request, "encyclopedia/error.html" )

def search(request):
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
    if request.method == "POST":
        form = forms.NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            if not util.is_entry(entries, title):
                filepath = os.path.join("entries", f"{title}.md")
                f = open(filepath, "w")
                f.write(body)
                f.close()
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
    entry = random.choice(entries)
    return redirect(reverse("entry", args=[entry]))

def edit(request, title):
    if request.method == "POST":
        form = forms.NewEntryForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data["title"]
            new_body = form.cleaned_data["body"]
            filepath = os.path.join("entries", f"{title}.md")
            with open(filepath, 'w+') as file:
                body = file.read()
                if body != new_body:
                    file.write(new_body)
            file.close()
            if title != new_title:
                os.rename(filepath, os.path.join("entries", f"{new_title}.md"))
                entries[entries.index(title)] = new_title
            return redirect(reverse("entry", args=[new_title]))

    else:
        filepath = os.path.join("entries", f"{title}.md")
        with open(filepath, 'r') as file:
            body = file.read()

        data = {'title': title, 'body': body}
        return render(request, 'encyclopedia/edit.html', {
            "title": title,
            "form": forms.NewEntryForm(data)
        })
