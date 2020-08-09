from fuzzywuzzy import fuzz
c=fuzz.token_sort_ratio("fuzzy-wuzzy", "wuzzy-fuzzy")
print (c)