from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from markdown2 import Markdown
from . import util
import random

markdowner = Markdown()

entries = util.list_entries()
entries_lowercaps = [entry.lower() for entry in entries]

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, title):
    if title.lower() in entries_lowercaps:
        return render(request, "encyclopedia/entry.html", {
            "content": markdowner.convert(str(util.get_entry(title))),
            "title": title
        })
    return render(request, "encyclopedia/error.html" )

def search(request):
    if request.method == "GET":
        q = request.GET.get("q")
        if q.lower() not in entries_lowercaps:
            results = [entry for entry in entries if q.lower() in entry.lower()]
            return render(request, "encyclopedia/search.html", {
                "results": results, 
                "len": len(results)
            })
        return redirect(reverse("entry", args=[q]))

def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title in entries:
            return render(request, "encyclopedia/error.html")
        return HttpResponse("Ready to Create New Page")
    return render(request, "encyclopedia/create.html")

def random_page(request):
    entry = random.choice(entries)
    return redirect(reverse("entry", args=[entry]))