import inflect
p = inflect.engine
with open('canonical_names_list_updated_lower.txt','r') as f:
    lines = f.readlines()

with open('canonical_names_list_updated_lower_singular.txt','r') as f:
    for line in lines:
        word = line.strip().lower()
        word = p.singular_noun(word) if p.singular_noun(word) else word
        f.write(word)
