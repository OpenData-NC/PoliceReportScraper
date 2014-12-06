URLs.py is very straightforward. Only 3 views are presented to the user in the ODNC Web App, and each is tied to a view defined in views.py
The first view, search, requires no user input to function, therefore the page can simply be rendered by the template for that view. For more information about the search template and any
other template, see Part 4 of the documentation.

The second view, result, first parses the URL received in order to interpret the user query.

    entry=request.META["QUERY_STRING"]
    entry_list=entry.split("&")
    entry_dict={}
    for item in entry_list:
        item_split=item.split("=")
        entry_dict[item_split[0]]=item_split[1]

The first line of the above code sets entry equal to the query part of the URL, which is received as a result of the user's selection of filters on the previous view. So if the user entered
Jeff into the searchbar and then entered 27 on the Age filter, entry would be equal to searchbar=Jeff&age=27. Then the string is split at each occurrance of the & symbol because
this character is used to separate each filter from the next filter. For each entry in the new list, each filter is then split from its value using the = symbol.
This serves to create a dictionary which will be used to query the database on the backend.


Then, a series of helper functions are defined. Below is an example.

    def filterByName(QuerySet, stringFilter):
        return QuerySet.filter(Name__icontains=stringFilter)

Each of these functions takes in a QuerySet as well as a value to query the database with. Then the function queries the database and outputs a QuerySet. In the function above, the database
applies a filter to the QuerySet which removes all entries where the Name field doesn't contain stringFilter (icontains is caps insensitive). The filterBySearchbar method is unique among
these methods, because the Searchbar is designed to return all results where the value entered is contained in ANY of the fields. This is done using Django "Q Objects" and a series of ORs.


