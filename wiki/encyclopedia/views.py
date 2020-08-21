from django.shortcuts import render
from markdown2 import Markdown
from . import util

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
    else:
        return render(request, "encyclopedia/error.html" )
