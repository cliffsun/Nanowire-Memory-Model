import numpy as np

n = 4

nums = np.random.rand(n)
nums[0] = 0
nums[-1] = 1

print(np.average(nums))
print(nums)