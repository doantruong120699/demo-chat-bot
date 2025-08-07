from rest_framework.filters import SearchFilter


class CustomSearchFilter(SearchFilter):
    def get_search_terms(self, request):
        params = request.query_params.get(self.search_param, "")
        params = params.replace("\x00", "")  # strip null characters
        params = params.replace(",", " ")
        params = params.strip()
        return [params]
