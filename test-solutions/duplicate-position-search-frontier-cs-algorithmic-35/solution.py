from __future__ import annotations
import sys

def read_ints():
    return list(map(int, sys.stdin.readline().split()))

def main():
    t=int(sys.stdin.readline())
    for _ in range(t):
        n=int(sys.stdin.readline())
        counts=[0]*(n+1)
        for x in range(1,n+1):
            for idx in range(1,2*n):
                print(f"? {x} 1 {idx}", flush=True)
                counts[x]+=int(sys.stdin.readline())
        ans=min(range(1,n+1), key=lambda i: counts[i])
        print(f"! {ans}", flush=True)
if __name__ == "__main__": main()
