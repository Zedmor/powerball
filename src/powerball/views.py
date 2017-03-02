import logging
import operator
from random import shuffle

import collections
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic
from functools import cmp_to_key
from django.shortcuts import render_to_response

from .forms import PowerballForm  # , DeleteForm

# Get an instance of a logger
logger = logging.getLogger(__name__)

from . import models
from .models import Drawentry


class HomePage(generic.TemplateView):
    template_name = "home.html"
    http_method_names = ['get', 'post']

    def compare_with_ties(x, y):

        if x < y:
            return(-1)
        elif x > y:
            return(1)
        else:
            return (random.randint(0, 1) * 2 - 1)

    def winningnumberhelper(self, allnumbers):
        """
        :param allnumbers: Drawentry collection
        :return: winnindnumberobject
        """

        def f7(seq):
            seen = set()
            seen_add = seen.add
            return [x for x in seq if not (x in seen or seen_add(x))]

        numberlist = []
        power_ball_list = []
        for numberset in allnumbers:
            for ball in numberset.balls:
                numberlist.append(ball)
            power_ball_list.append(numberset.powerball)

        shuffle(numberlist)
        shuffle(power_ball_list)
        counts = collections.Counter(numberlist)
        numberlist = f7(sorted(numberlist, key=lambda x: -counts[x]))

        counts = collections.Counter(power_ball_list)
        power_ball_list = f7(sorted(power_ball_list, key=lambda x: -counts[x]))


        top5nums = numberlist[:5]
        poweballnum = power_ball_list[:1]

        return {"numbers": " ".join(map(str, top5nums)),
                "powernumber": " ".join(map(str, poweballnum
                                            ))}

    def get(self, request, *args, **kwargs):
        # deletebutton = DeleteForm()
        # todo delete button
        if 'error' in request.GET and request.GET['error'] == \
                'NonUniqueNumbers':
            kwargs["formsubmiterror"] = True
        formdata = {}
        alldraws = Drawentry.objects.all()
        slug = self.kwargs.get('slug')
        if slug:
            profile = get_object_or_404(models.Profile, slug=slug)
            user = profile.user
        else:
            user = self.request.user

        if user == self.request.user:
            kwargs["editable"] = True
        if user.is_authenticated:
            userdraw = Drawentry.objects.filter(user=user)
            if userdraw:
                kwargs["userdraw"] = userdraw[0]
                formdata = userdraw[0]

        ballform = PowerballForm(userdraw=formdata)
        kwargs["show_user"] = user
        kwargs["alldraws"] = alldraws
        kwargs["ballform"] = ballform
        kwargs["winning"] = self.winningnumberhelper(alldraws)
        return super(HomePage, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        addnewform = PowerballForm(request.POST)
        slug = self.kwargs.get('slug')
        if slug:
            profile = get_object_or_404(models.Profile, slug=slug)
            user = profile.user
        else:
            user = self.request.user

        if addnewform.is_valid():
            balls = [addnewform.cleaned_data['ball1'],
                     addnewform.cleaned_data['ball2'],
                     addnewform.cleaned_data['ball3'],
                     addnewform.cleaned_data['ball4'],
                     addnewform.cleaned_data['ball5']]
            drawing = Drawentry(user=user,
                                balls=balls,
                                powerball=addnewform.cleaned_data['powerball']
                                )
            drawing.save()
            return HttpResponseRedirect('/')
        elif addnewform.errors:
            return HttpResponseRedirect('/?error=NonUniqueNumbers')
        else:
            return HttpResponseRedirect('/')
            # TODO Check form validity - validators? Inline?


class AboutPage(generic.TemplateView):
    template_name = "about.html"
