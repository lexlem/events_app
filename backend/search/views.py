# -*- coding: utf-8 -*-
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
from rest_framework import generics

from backend.events.models import Event
from backend.search.serializer import EventSearchSerializer


class EventSearchList(generics.ListAPIView):
    serializer_class = EventSearchSerializer
    pagination_class = None

    def get_queryset(self):
        query = self.request.query_params.get("q", None)
        if query:
            pg_query = SearchQuery(query)
            title_vector = SearchVector("title", weight="A")
            description_vector = SearchVector("description", weight="B")
            events_vectors = title_vector + description_vector
            events = (
                Event.objects.all()
                .annotate(search=events_vectors)
                .filter(status=Event.PUBLISHED, search=pg_query)
                .annotate(rank=SearchRank(events_vectors, pg_query))
                .order_by("-rank")
            )

            if not events:
                events = Event.objects.filter(
                    Q(status=Event.PUBLISHED),
                    Q(title__icontains=query) | Q(description__icontains=query),
                )
            all_results = list(events)
            all_results.sort(key=lambda x: x.created)
            return all_results
        else:
            return
