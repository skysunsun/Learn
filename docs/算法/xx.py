class Solution:
    def exist(self, board, word):
        # def dfs(i,j,k):
        #     if not 0 <= i < len(board) or not 0 <= j < len(board[0]) or board[i][j] != word[k]: 
        #         return False
        #     if k==len(word)-1:
        #         return True
        #     tmp,board[i][j]=board[i][j],'/'
        #     res = dfs(i + 1, j, k + 1) or dfs(i - 1, j, k + 1) or dfs(i, j + 1, k + 1) or dfs(i, j - 1, k + 1)
        #     board[i][j] = tmp
        #     return res                    
        # for i in range(len(board)):
        #     for j in range(len(board[0])):
        #         if dfs(i,j,0):
        #             return True
        # return False
        visited = set()
        dirction = [[0,1],[0,-1],[1,0],[-1,0]]
        stack = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j]==word[0]:
                    stack.append((i,j))
                    break
        k=0
        while stack:
            if k==len(word)-1:
                return True
            x,y = stack.pop()
            if (x,y) not in visited and 0<=x<len(board) and 0<=y<len(board[0]) and board[x][y]==word[k]:
                k+=1
                visited.add((x,y))
            for di,dj in dirction:
                stack.append((x+di,x+dj))
        return False
y = Solution().exist([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]],"ABCCED")
