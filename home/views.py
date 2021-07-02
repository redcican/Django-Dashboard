from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from django import template


@login_required(login_url="authentication/login/")
def home(request):
    context = {}
    context['segment'] = 'index'
    return render(request, 'index.html', context)


@login_required(login_url="authentication/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        # import pdb
        # pdb.set_trace()
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        return render(request, '404.html', context)
    except:
        return render(request, '500.html', context)
