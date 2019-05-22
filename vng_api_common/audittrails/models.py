import uuid

from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..constants import ComponentTypes
from ..descriptors import GegevensGroepType


class AuditTrail(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4,
        help_text=_("Unieke identificatie van de audit regel")
    )
    bron = models.CharField(
        max_length=50,
        help_text=_("De naam van het component waar de wijziging in is gedaan"),
        choices=ComponentTypes
    )
    actie = models.CharField(
        max_length=50,
        help_text=_("De uitgevoerde handeling")
    )
    actie_weergave = models.CharField(
        max_length=200,
        blank=True,
        help_text=_("Vriendelijke naam van de actie")
    )
    resultaat = models.IntegerField(
        help_text=_("HTTP status code van de API response van de uitgevoerde handeling"),
        validators=[MinValueValidator(100), MaxValueValidator(599)]
    )
    hoofd_object = models.URLField(
        max_length=1000,
        help_text=_("De URL naar het hoofdobject van een component")
    )
    resource = models.CharField(
        max_length=50,
        help_text=_("Het type resource waarop de actie gebeurde")
    )
    resource_url = models.URLField(
        max_length=1000,
        help_text=_("De URL naar het object")
    )
    aanmaakdatum = models.DateTimeField(
        auto_now=True,
        help_text=_("De datum waarop de handeling is gedaan")
    )
    applicatie_id = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("Unieke identificatie van de applicatie, binnen de organisatie")
    )
    applicatie_weergave = models.CharField(
        max_length=200,
        blank=True,
        help_text=_("Vriendelijke naam van de applicatie")
    )
    oud = JSONField(
        null=True,
        encoder=DjangoJSONEncoder,
        help_text=_("Volledige JSON body van het object zoals dat bestond voordat de actie heeft plaatsgevonden")
    )
    nieuw = JSONField(
        null=True,
        encoder=DjangoJSONEncoder,
        help_text=_("Volledige JSON body van het object na de actie")
    )

    gebruikers_id = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Unieke identificatie van de gebruiker die binnen de "
                    "organisatie herleid kan worden naar een persoon")
    )
    gebruikers_weergave = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Vriendelijke naam van de gebruiker")
    )
    toelichting = models.TextField(
        _("toelichting"),
        blank=True,
        help_text=_("Toelichting waarom de handeling is uitgevoerd")
    )
    wijzigingen = GegevensGroepType({
        'oud': oud,
        'nieuw': nieuw,
    }, optional=['oud', 'nieuw'], none_for_empty=True)
