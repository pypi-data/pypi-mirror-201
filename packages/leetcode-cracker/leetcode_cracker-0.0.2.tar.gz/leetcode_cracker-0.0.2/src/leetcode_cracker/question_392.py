def print_solution():

    print("""
   class Solution:
    
    def isSubsequence(self, s: str, t: str) -> bool:
        # Init Both Variables
        i = 0
        j = 0

        # Loop Through Both Variables
        while i<len(s) and j<len(t):
            # If both Pointers are the same, increment both by one
            if s[i] == t[j]:
                i += 1
                j += 1
            #Otherwise, only increment the second pointer
            else:
                j += 1
        #If the function has finnished running, return true.
        if i == len(s):
            return True
        else:
            return False
    """)

  
