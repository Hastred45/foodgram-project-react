from rest_framework import filters


class CustomSearchFilter(filters.SearchFilter):
    search_param = 'name'
