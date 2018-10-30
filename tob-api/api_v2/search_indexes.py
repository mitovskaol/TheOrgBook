# TODO: Figure out how to configure haystack to register indices in
#       ./indices/<IndexName> instead of this default file...

from itertools import chain
import logging

from haystack import indexes
from django.db.models import Prefetch
from django.utils import timezone

from api_v2.models.Credential import Credential as CredentialModel
from api_v2.models.Name import Name as NameModel
from api_v2.search.index import TxnAwareSearchIndex

LOGGER = logging.getLogger(__name__)


class CredentialIndex(TxnAwareSearchIndex, indexes.Indexable):
    document = indexes.CharField(document=True, use_template=True)

    name = indexes.MultiValueField()
    location = indexes.MultiValueField()
    category = indexes.MultiValueField()
    topic_id = indexes.IntegerField(model_attr="topic_id")
    topic_type = indexes.CharField(faceted=True, model_attr="topic__type")
    source_id = indexes.CharField(model_attr="topic__source_id")
    inactive = indexes.BooleanField(model_attr="inactive")
    revoked = indexes.BooleanField(model_attr="revoked")
    effective_date = indexes.DateTimeField(faceted=True, model_attr="effective_date")
    credential_type_id = indexes.IntegerField(faceted=True, model_attr="credential_type_id")
    issuer_id = indexes.IntegerField(model_attr="credential_type__issuer_id")

    @staticmethod
    def prepare_name(obj):
        return [name.text for name in obj.names.all()]

    @staticmethod
    def prepare_category(obj):
        return [
            "{}::{}".format(cat.type, cat.value)
            for cat in obj.attributes.all()
            if cat.format == "category"]

    @staticmethod
    def prepare_location(obj):
        locations = []
        for address in obj.addresses.all():
            loc = " ".join(filter(None, (
              address.addressee,
              address.civic_address,
              address.city,
              address.province,
              address.postal_code,
              address.country,
            )))
            if loc:
              locations.append(loc)
        return locations

    def get_model(self):
        return CredentialModel

    def index_queryset(self, using=None):
        prefetch = (
            "addresses",
            "attributes",
            "names",
        )
        select = (
          "credential_type",
          "topic",
        )
        queryset = super(CredentialIndex, self).index_queryset(using)\
            .prefetch_related(*prefetch)\
            .select_related(*select)
        return queryset

    def read_queryset(self, using=None):
        select = (
            "credential_type__issuer",
            "credential_type__schema",
        )
        queryset = self.index_queryset(using) \
            .select_related(*select)
        return queryset

    def get_updated_field(self):
      return "update_timestamp"
