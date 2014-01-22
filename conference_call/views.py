from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings 

from twilio import twiml
from twilio.rest import TwilioRestClient

from .models import ConferenceCall, CallParticipant


def selection(req):
    if req.method == 'GET':
        try:
            cc = ConferenceCall.objects.get(owner=req.user.get_profile())
        except ObjectDoesNotExist as e:
            # this person has never made a conference call before
            cc = ConferenceCall()
            cc.owner = req.user.get_profile()
            cc.save()
        cp = CallParticipant.objects.filter(conference_call=cc)
        p  = {'cc': cc, 'cp': cp}
        p.update(csrf(req))
        return render(req, 'conference_call/selection.html', p)


def add_participant(req):
    if req.method == 'POST':
        # TODO: integrate with real collab search
        last_name = req.POST.get('name_search', '')
        u = User.objects.get(last_name=last_name)
        cp = CallParticipant()
        cp.conference_call = ConferenceCall.objects.get( \
            owner=req.user.get_profile())
        cp.participant = u.get_profile()
        cp.save()
        return HttpResponseRedirect(reverse('conference_call:selections'))


def dial(req):
    cc = ConferenceCall.objects.get(owner=req.user.get_profile())
    call_participants = CallParticipant.objects.filter(conference_call=cc)
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, 
        settings.TWILIO_AUTH_TOKEN)
    for cp in call_participants:
        # the TWILIO_POSTBACK_URL would be the server hostname
        # plus the exposed /conference-call/postback/ URL
        client.calls.create(to=cp.participant.mobile_phone, 
            from_=settings.TWILIO_CONF_NUMBER, 
            url=settings.TWILIO_POSTBACK_URL)
    return render(req, 'conference_call/conference_started.html', {'cc': cc})


def conference_postback(req):
    response = twiml.Response()
    dial = response.dial()
    # the name of the conference needs to be made dynamic
    conference = dial.conference("collab conference call")
    return HttpResponse(str(response.toxml()), content_type="text/xml")


