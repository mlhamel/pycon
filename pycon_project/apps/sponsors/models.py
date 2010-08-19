import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _


class SponsorLevel(models.Model):
    
    name = models.CharField(_("name"), max_length=100)
    order = models.IntegerField(_("order"), default=0)
    description = models.TextField(_("description"), blank=True, help_text=_("This is private."))
    
    class Meta:
        ordering = ["order"]
    
    def __unicode__(self):
        return self.name


class Sponsor(models.Model):
    
    name = models.CharField(_("name"), max_length=100)
    external_url = models.URLField(_("external URL"))
    annotation = models.TextField(_("annotation"), blank=True)
    contact_name = models.CharField(_("contact name"), max_length=100)
    contact_email = models.EmailField(_(u"Contact e\u2011mail"))
    level = models.ForeignKey(SponsorLevel, verbose_name=_("level"))
    added = models.DateTimeField(_("added"), default=datetime.datetime.now)
    active = models.BooleanField(_("active"), default=False)
    
    def __unicode__(self):
        return self.name
    
    @property
    def website_logo_url(self):
        try:
            logo = SponsorLogo.objects.get(sponsor=self, label="website")
        except SponsorLogo.DoesNotExist:
            return u""
        else:
            return logo.logo.url


class SponsorLogo(models.Model):
    
    sponsor = models.ForeignKey(Sponsor, verbose_name=_("sponsor"))
    label = models.CharField(
        max_length = 100,
        help_text = _("To display this logo on site use label 'website'")
    )
    logo = models.ImageField(_("logo"), upload_to="sponsor_logos/")
    
    class Meta:
        unique_together = [("sponsor", "label")]