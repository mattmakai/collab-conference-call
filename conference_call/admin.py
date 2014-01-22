from django.contrib import admin

from .models import ConferenceCall, CallParticipant

admin.site.register(ConferenceCall)
admin.site.register(CallParticipant)
