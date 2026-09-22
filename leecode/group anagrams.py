strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
def group_anagrams(strs):
    group={}
    for word in strs:
        key="".join(sorted(word))
        if key not in group:
            group[key]=[]
        group[key].append(word)
    return list(group.values())
print(group_anagrams(strs))