import sys
def main():
    num_suc = 0
    num_times = int(sys.argv[1])
    for i in range(num_times):
        inpt = input()
        if inpt == "Success":
            num_suc += 1
    if num_suc/num_times < 0.9:
        print("ERROR failed to many times")
    else:
        print("SUCCESS succeded " + str(num_suc) + " out of " + sys.argv[1] + " random instances")
if __name__ == "__main__":
    main()
