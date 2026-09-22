def contains_duplicae(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
nums = [4, 7, 2, 9, 5,7]
print(contains_duplicae(nums))