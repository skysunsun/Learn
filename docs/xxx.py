# class Solution:
#     def change(self , s ):
#         # write code here
#         if not s:
#             return ''
#         count = 0
#         res = []
#         for i in range(len(s)):
#             if s[i]=='a':
#                 s[i]==''
#                 count+=1
#             else:
#                 res.append(s[i])
#         return ''.join(res)+'a'*count



class Solution:
    def solve(self , n , m ):
        step= 0
        flag=[0]*10000000
        # write code here
        deque = []
        deque.append(n-1)
        deque.append(n+1)
        deque.append(n*n)
        while deque:
            length = len(deque)
            for i in range(n):
                val = deque[0]
                deque.pop(0)
                if flag[val]==1:
                    continue
                if val==m:
                    step+=1
                    return step
                deque.append(val-1)
                deque.append(val+1)
                deque.append(val*val)
                flag[val]=1
            step+=1

                

            
# class Solution:
#     def minCost(self , breadNum , beverageNum , packageSum ):
#         packageSum.sort(key = lambda x:x[2])
#         res = 0
#         for x in packageSum:
#             breadNum -= x[0]
#             beverageNum -= x[1]
#             if beverageNum<0 and breadNum<0:
#                 return res
#             elif beverageNum<0:
#                 res+=x[2]
#             elif breadNum<0:
#                 res+=x
print(str(3)*2)