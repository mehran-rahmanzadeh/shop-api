from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from rest_framework.filters import SearchFilter


class CustomSearchBackend(SearchFilter):
    """Custom search backend
    use advanced search methods in PostgreSQL
    """
    @staticmethod
    def __get_search_type(view):
        """Get search type"""
        return getattr(view, 'search_type', 'trigram')

    @staticmethod
    def __get_search_vector(search_fields):
        """Get search vector"""
        return SearchVector(*search_fields)

    @staticmethod
    def __get_search_query(search_terms):
        """Get search query"""
        return SearchQuery(' '.join(search_terms))

    @staticmethod
    def __get_search_rank(search_vector, search_query):
        """Get search rank"""
        return SearchRank(search_vector, search_query)

    @staticmethod
    def __get_trigram_similarity(value, field):
        """Get trigram similarity"""
        return TrigramSimilarity(field, value)

    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset
        print(search_terms)
        search_type = self.__get_search_type(view)
        if search_type == 'vector':
            search_vector = self.__get_search_vector(search_fields)
            search_query = self.__get_search_query(search_terms)
            qs = queryset.annotate(search=search_vector).filter(search=search_query)
        elif search_type == 'rank':
            search_vector = self.__get_search_vector(search_fields)
            search_query = self.__get_search_query(search_terms)
            search_rank = self.__get_search_rank(search_vector, search_query)
            qs = queryset.annotate(rank=search_rank).order_by('-rank')
        elif search_type == 'trigram':
            search_trigram = self.__get_trigram_similarity(' '.join(search_terms), search_fields[0])
            qs = queryset.annotate(similarity=search_trigram).filter(similarity__gt=0.1).order_by('-similarity')
        else:
            qs = queryset

        return qs
