from django.db import models
from django.template.defaultfilters import slugify


class ConferenceCall(models.Model):
    owner = models.ForeignKey('core.Person', related_name='conf_call_owner')
    slug = models.CharField(max_length=128, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = create_slug(ConferenceCall, unicode(self))
        super(ConferenceCall, self).save(*args, **kwargs)

    def __unicode__(self):
        return "Conf call by %s" % str(self.owner)
   

class CallParticipant(models.Model):
    participant = models.ForeignKey('core.Person', 
        related_name='conf_call_participant')
    conference_call = models.ForeignKey(ConferenceCall)
    
    def __unicode__(self):
        return "%s call participant in %s" % (str(self.participant), 
            str(self.conference_call))



def create_slug(cls, unslugged):
    trial_slug = slugify(unslugged)
    if trial_slug == '':
        # set a default value in case of empty string
        trial_slug = slugify(cls.__name__) 
    slug = trial_slug
    count = 0
    while(cls.objects.filter(slug=slug).count() > 0):
        count += 1
        slug = trial_slug + str(count)
    return slug

