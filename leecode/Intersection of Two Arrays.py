nums1 = [4, 9, 5]
nums2 = [9, 4, 9, 8, 4]

class Solution:
    def intersection(self, nums1, nums2):
        result = set()
        for i in nums1:
            if i in nums2:
                result.add(i)
        return list(result)
s = Solution()
s.intersection(nums1, nums2)
print(s.intersection(nums1, nums2))