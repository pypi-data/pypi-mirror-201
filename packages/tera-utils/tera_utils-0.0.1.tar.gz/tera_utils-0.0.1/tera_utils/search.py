def linear(arr: list, item, length: int = -1):
    """Returns the index the item if the item is in the array and if not returns -1"""
    for idx, value in enumerate(arr):
        if value == item:
            return idx
    return -1

  
def binary(arr:list, item):
    """
    Deprecated!!! --- import bisect\n
    Returns the index the item if the item is in the array and if not returns -1
    """
    lo = 0
    hi = len(arr)
    while lo < hi:
        mid = (hi + lo)//2
        if arr[mid] < item:
            lo = mid + 1
        else:
            hi = mid
    return lo


if __name__ == "__main__":
    from sort import make_list, merge_sort
    import time, random
    from colorama import Fore

    arr = merge_sort(make_list(10000, int))

    # * Original list
    print(Fore.GREEN + f"\nOriginal array:" + Fore.WHITE)
    item = random.choice(arr)
    idx = arr.index(item)
    if len(arr) < 101:
        print(arr)
    print(Fore.BLUE + f"{idx}" + Fore.WHITE + "\n")


    # * Linear Search
    print(Fore.GREEN + f"\nLinear Search:" + Fore.WHITE)
    start = time.time()
    idx = linear(arr, item)
    end = time.time()
    print(Fore.BLUE + f"{idx}" + Fore.WHITE)
    speed = end - start
    print(Fore.RED + f"{speed} seconds, length: {len(arr)}\n" + Fore.WHITE)

    # * Binary Search
    print(Fore.GREEN + f"\nBinary Search:" + Fore.WHITE)
    start = time.time()
    idx = linear(arr, item)
    end = time.time()
    print(Fore.BLUE + f"{idx}" + Fore.WHITE)
    speed = end - start
    print(Fore.RED + f"{speed} seconds, length: {len(arr)}\n" + Fore.WHITE)
