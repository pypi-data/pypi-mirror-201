import random


def bubble_sort(arr):
    ordered = False
    while not ordered:
        ordered = True
        for idx, value in enumerate(arr):
            if idx == 0:
                continue

            if value < arr[idx - 1]:
                ordered = False
                temp = value
                arr[idx] = arr[idx - 1]
                arr[idx - 1] = temp
    return arr


def merge_sort(arr: list):
    if len(arr) > 1:
        left_arr = arr[: len(arr) // 2]
        right_arr = arr[len(arr) // 2 :]

        # recursion
        merge_sort(left_arr)
        merge_sort(right_arr)

        # merge
        i = 0  # left_arr index
        j = 0  # right_arr index
        k = 0  # merged arr index

        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] < right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1

        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1

        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1
    return arr


def make_list(length, data_type: type):
    lis = []
    if data_type == int:
        for i in range(length):
            lis.append(random.randint(0, length))
    elif data_type == float:
        for i in range(length):
            lis.append(random.random())
    return lis


if __name__ == "__main__":
    import time
    from colorama import Fore

    arr = make_list(100, int)
    orr_arr = arr.copy()

    # * Original list
    print(Fore.GREEN + f"\nOriginal array:" + Fore.WHITE)
    print(f"{arr}\n")

    # * Bubble sort
    print(Fore.GREEN + f"\nBubble sort:" + Fore.WHITE)
    arr = orr_arr.copy()
    start = time.time()
    bubble_sort(arr)
    end = time.time()
    if len(arr) < 101:
        print(arr)
    speed = end - start
    print(Fore.RED + f"{speed} seconds, length: {len(arr)}\n" + Fore.WHITE)

    # * Merge sort
    print(Fore.GREEN + f"\nMerge sort:" + Fore.WHITE)
    arr = orr_arr.copy()
    start = time.time()
    merge_sort(arr)
    end = time.time()
    if len(arr) < 101:
        print(arr)
    speed = end - start
    print(Fore.RED + f"{speed} seconds, length: {len(arr)}\n" + Fore.WHITE)

    # * Built-in sort
    print(Fore.GREEN + f"\nBuilt-in sort:" + Fore.WHITE)
    arr = orr_arr.copy()
    start = time.time()
    arr.sort()
    end = time.time()
    if len(arr) < 101:
        print(arr)
    speed = end - start
    print(Fore.RED + f"{speed} seconds, length: {len(arr)}\n" + Fore.WHITE)
