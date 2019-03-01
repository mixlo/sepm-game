import socket, random, sys, re

def test_valid():
    #create instance
    #have thread access value of instance
    #check if only valid input has been recieved
def test_invalid():
def test_run_normally():
    #create instance
def main():
    
    
    #s = input("test").strip()
    #print(s)
    #print(sys.argv[1])
    if sys.argv[1] == "valid":
        test_valid()
    elif sys.argv[1] == "invalid":
        test_invalid()
    else:
        test_run_normally()
    
if __name__ == "__main__":
    main()
