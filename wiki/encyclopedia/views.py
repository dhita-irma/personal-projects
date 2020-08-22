from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from markdown2 import Markdown
from . import util
import random

markdowner = Markdown()

entries = util.list_entries()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, title):
    entries = [x.lower() for x in util.list_entries()]
    if title.lower() in entries:
        return render(request, "encyclopedia/entry.html", {
            "content": markdowner.convert(str(util.get_entry(title))),
            "title": title
        })
    return render(request, "encyclopedia/error.html" )

def search(request):
    if request.method == "GET":
        q = request.GET.get("q")
        if q not in entries:
            results = [entry for entry in entries if q in entry]
            return render(request, "encyclopedia/search.html", {
                "results": results, 
                "len": len(results)
            })
        return HttpResponseRedirect(f"/{q}")

def create(request):
    if request.method == "POST":
        pass
    return render(request, "encyclopedia/create.html")

def random_page(request):
    entry = random.choice(entries)
    return HttpResponseRedirect(f"/{entry}")
