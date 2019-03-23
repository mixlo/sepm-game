import random
def genMatrix(l1, l2):
    j = 0
    l3 = list(zip(l1, l2))
    l4 = [[None for i in range(4)] for i in range(4)]
    for (i, ix) in l3:
        j = int((i-1) % 4)
        a = int(((i-1) / 4))
        
        #if i<5:
        #    j = i
        #elif i<9:
        #    j = i - 4 
        #elif i<13:
        #    j = i - 8
        #else:
        #    j = i - 12
        #print("a==")
        #print(a)
        l4[j][a] = ix -1
        
    print(l4)
    #print("[[1, 2, 3, 4], ")
    #print("[None, None, None, None], ")
    #print("[None, None, None, None], ")
    #print("[None, None, None, None]]")
    
def genCommands(l1, l2):
    j = 0
    l3 = list(zip(l1, l2))
    
    for (i, ix) in l3:
        j = int((i-1) % 4) + 1
        a = int(((i-1) / 4) + 1)
        
        #if i<5:
        #    j = i
        #elif i<9:
        #    j = i - 4 
        #elif i<13:
        #    j = i - 8
        #else:
        #    j = i - 12
        #print("a==")
        #print(a)
        print(ix)
        if a == 1:
            print(str(j) + "A")
        elif a == 2:
            print(str(j) + "B")
        elif a == 3:
            print(str(j) + "C")
        elif a == 4:
            print(str(j) + "D")

            
            

    #print("Alfred")
    #print("Martha")
    #print("1")
    #print("1A")
    #print("2")
    #print("1B")
    #print("3")
   # print("1C")
   # print("4")
    #print("1D")
    
def piece_give_order():
    l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    random.shuffle(l)
    return l

def prompt_square_order():
    l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    random.shuffle(l)
    return l

def main():
    p_g_o = piece_give_order()
    p_s_o = prompt_square_order()
    #print(p_g_o)
    #print(p_s_o)
    genMatrix(p_g_o, p_s_o)

    print("Alfred")
    print("Martha")
    genCommands(p_g_o, p_s_o)
    
if __name__ == "__main__":
    main()
