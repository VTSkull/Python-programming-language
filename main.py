with open("main.ppl", "r") as file:
    data = file.read()
    file.close()
#print(data)

import time
memory={}
placeholder = ""
line = -1
splitData = data.split('\n')
errored = False
errormsg = ""
#print(splitData)

debug = False

dataArea = False

#initialize data from dat section
for x in splitData:
    if x == "dat":
        if dataArea:
            errored = True
            errormsg = "dat initialized twice"
            break
        dataArea = True
    
    if x == "edt":
        if dataArea:
            dataArea = False
        else:
            errored = True
            errormsg = "edt closing nonexistant data section"
            break
    
    if dataArea:
        #var instruction
        if x[:3] == "var":
            try:
                #memory[splitData[line][4:7]] = splitData[line][8:]
                #print(memory)
                if x[8] == "i":
                    try:
                        memory[x[4:7]] = int(x[10:])
                    except:
                        print(f"error in data section; could not convert value to integer")
                        break
                    
                elif x[8] == "s":
                    memory[x[4:7]] = str(x[10:])
                    
                elif x[8] == "b":
                    if x[9:] == "true" or x[10:] == "1" or x[9:] == "True":
                        memory[x[4:7]] = True
                    elif x[9:] == "false" or x[10:] == "0" or x[9:] == "False":
                        memory[x[4:7]] = False
                    else:
                        print(f"error in data section; invalid boolean type: {x[9:]}")
                        break
                
                elif x[8] == "f":
                    try:
                        memory[x[4:7]] = float(x[9:])
                    except:
                        print(f"error in data section; could not convert value to float")
                        break
                
            except:
                print(f"error in data section; could not update variable")
                break
        
        
dataArea = False        
#main program loop
while True:
    if debug == True:
        time.sleep(1)
    line += 1
    
    if debug == True:
        print(splitData[line])
        print(line)

    #check if program threw error
    if errored == True:
        print(f"\n{errormsg}")
        break
    
    
    
    #get the command
    try:
        command = splitData[line][:3]
    except:
        try:
            placeholder = splitData[line + 1]
        except:
            print("\nend of program")
            break
        continue
    
    
    #data section skip logic
    if command == "dat":
        dataArea = True
    elif command == "edt":
        dataArea = False
        continue
    #end of section skip logic
    
    #check if in data section
    if dataArea:
        continue
    
    #com instruction
    elif command == "com":
        continue
    
    #end instruction
    elif command == "end":
        print("\nend of program")
        break
    
    #lod instruction
    elif command == "lod":
        try:
            placeholder = int(memory[splitData[line][4:7]])
            line = placeholder - 2
        except:
            print(f"error on line {line+1}; could not load line number {splitData[line][4:]}")
            break
    
    #var instruction
    elif command == "var":
        try:
            #memory[splitData[line][4:7]] = splitData[line][8:]
            #print(memory)
            if splitData[line][8] == "i":
                try:
                    memory[splitData[line][4:7]] = int(splitData[line][10:])
                except:
                    print(f"error on line {line+1}; could not convert value to integer")
                    break
                
            elif splitData[line][8] == "s":
                memory[splitData[line][4:7]] = str(splitData[line][10:])
                
            elif splitData[line][8] == "b":
                if splitData[line][9:] == "true" or splitData[line][10:] == "1" or splitData[line][9:] == "True":
                    memory[splitData[line][4:7]] = True
                elif splitData[line][9:] == "false" or splitData[line][10:] == "0" or splitData[line][9:] == "False":
                    memory[splitData[line][4:7]] = False
                else:
                    print(f"error on line {line+1}; invalid boolean type: {splitData[line][9:]}")
                    break
            
            elif splitData[line][8] == "f":
                try:
                    memory[splitData[line][4:7]] = float(splitData[line][9:])
                except:
                    print(f"error on line {line+1}; could not convert value to float")
                    break
            
        except:
            print(f"error on line {line+1}; could not update variable")
            break
    
    #out insruction
    elif command == "out":
        try:
            print(memory[splitData[line][4:7]], end="")
        except:
            print(f"error on line {line+1}; could not print value for variable {splitData[line][4:7]}")
            break
       
    #if- instruction
    elif command == "if-":
        try:
            try:
                placeholder = int(memory[splitData[line][8:11]])
            except:
                print(f"error on line {line+1}; could not get integer for line number")
                break
            
            try:
                placeholder = memory[splitData[line][4:7]]
            except:
                print(f"error on line {line+1}; could not get variable")
                break
            if placeholder == True:
                line = int(memory[splitData[line][8:11]]) - 2
        except:
            print(f"error on line {line+1}; unexpected error")
            break
    
    #eif instruction
    elif command == "eif":
        try:
            try:
                placeholder = int(memory[splitData[line][8:11]])
                print(f"1:{splitData[line][8:11]}\n{placeholder}")
                placeholder = int(memory[splitData[line][12:15]])
                print(f"2:{splitData[line][12:15]}\n{placeholder}")
            except:
                print(f"error on line {line+1}; could not get integer for line number")
                break
            
            try:
                placeholder = memory[splitData[line][4:7]]
            except:
                print(f"error on line {line+1}; could not get variable")
                break
            if placeholder == True:
                line = int(memory[splitData[line][8:11]]) - 2
            else:
                line = int(memory[splitData[line][12:15]])
        except:
            print(f"error on line {line+1}; unexpected error")
            break
    
    #uin instruction        
    elif command == "uin":
        try:
            placeholder = splitData[line][4:7]
            try:
                memory[splitData[line][4:7]] = int(input())
            except:
                try:
                    memory[splitData[line][4:7]] = float(input())
                except:
                    try:
                        memory[splitData[line][4:7]] = bool(input())
                    except:
                        memory[splitData[line][4:7]] = str(input())
            
        except:
            print(f"error on line {line+1}; could not update variable")
            break
       
       
    #math instructions 
    elif command == "add":
        try:
            var1 = memory[splitData[line][4:7]]
            var2 = memory[splitData[line][8:11]]
            placeholder = splitData[line][12:15]
            try:
                memory[splitData[line][12:15]] = var1 + var2
            except:
                print(f"error on line {line+1}; could not add values")
                break
        except:
            print(f"error on line {line+1}; could not get or update variables")
            break
        
    elif command == "sub":
        try:
            var1 = memory[splitData[line][4:7]]
            var2 = memory[splitData[line][8:11]]
            placeholder = splitData[line][12:15]
            try:
                memory[splitData[line][12:15]] = var1 - var2
            except:
                print(f"error on line {line+1}; could not subtract values")
                break
        except:
            print(f"error on line {line+1}; could not get or update variables")
            break
        
    elif command == "mlt":
        try:
            var1 = memory[splitData[line][4:7]]
            var2 = memory[splitData[line][8:11]]
            placeholder = splitData[line][12:15]
            try:
                memory[splitData[line][12:15]] = var1 * var2
            except:
                print(f"error on line {line+1}; could not multiply values")
                break
        except:
            print(f"error on line {line+1}; could not get or update variables")
            break
        
    elif command == "div":
        try:
            var1 = memory[splitData[line][4:7]]
            var2 = memory[splitData[line][8:11]]
            placeholder = splitData[line][12:15]
            try:
                memory[splitData[line][12:15]] = var1 / var2
            except:
                print(f"error on line {line+1}; could not divide values")
                break
        except:
            print(f"error on line {line+1}; could not get or update variables")
            break
    #end of math instructions
    
    
    #bitwise instructions
    elif command == "bor":
        try:
            var1 = memory[splitData[line][4:7]]
            var2 = memory[splitData[line][8:11]]
            placeholder = splitData[line][12:15]
            try:
                memory[splitData[line][12:15]] = False
                if var1 == True:
                    memory[splitData[line][12:15]] = True
                elif var1 == False:
                    pass
                else:
                    print(f"error on line {line+1}; {var1} is not a boolean")
                    break
                if var2 == True:
                    memory[splitData[line][12:15]] = True
                elif var2 == False:
                    pass
                else:
                    print(f"error on line {line+1}; {var2} is not a boolean")
                    break
            except:
                print(f"error on line {line+1}; could not do bitwise operation with values")
                break
        except:
            print(f"error on line {line+1}; could not get or update variables")
            break
    
    elif command == "and":
        try:
            var1 = memory[splitData[line][4:7]]
            var2 = memory[splitData[line][8:11]]
            placeholder = splitData[line][12:15]
            if var1 == True and var2 == True:
                memory[splitData[line][12:15]] = True
            elif var1 == False or var2 == False:
                memory[splitData[line][12:15]] = False
            if var1 != True and var1 != False:
                print(f"error on line {line+1}; could not do bitwise operation with values")
                break
            if var2 != True and var2 != False:
                print(f"error on line {line+1}; could not do bitwise operation with values")
                break
        except:
            print(f"error on line {line+1}; could not get or update variables")
            break
    #end of bitwise instructions
    
    
    #math logic instructions
    elif command == "equ":
        #check for variables
        try:
            placeholder = splitData[line][4:7]
        except:
            print(f'\nerror on line {line+1}; no variables provided')
        
        try:
            placeholder = splitData[line][8:11]
        except:
            print(f'\nerror on line {line+1}; only one variable provided')
        
        try:
            placeholder = splitData[line][12:15]
        except:
            print(f'\nerror on line {line+1}; no output variable provided')
        
        #get variable 1
        try:
            num1 = int(memory[splitData[line][4:7]])
        except:
            try:
                num1 = float(memory[splitData[line][4:7]])
            except:
                print(f'\nerror on line {line+1}; could not convert variable "{splitData[line][4:7]}" to a number')
        
        #get variable 2    
        try:
            num2 = int(memory[splitData[line][8:11]])
        except:
            try:
                num2 = float(memory[splitData[line][8:11]])
            except:
                print(f'\nerror on line {line+1}; could not convert variable "{splitData[line][8:11]}" to a number')
                
        if num1 == num2:
            memory[splitData[line][12:15]] = True
        else:
            memory[splitData[line][12:15]] = False
    
    elif command == "neq":
        #check for variables
        try:
            placeholder = splitData[line][4:7]
        except:
            print(f'\nerror on line {line+1}; no variables provided')
        
        try:
            placeholder = splitData[line][8:11]
        except:
            print(f'\nerror on line {line+1}; only one variable provided')
        
        try:
            placeholder = splitData[line][12:15]
        except:
            print(f'\nerror on line {line+1}; no output variable provided')
        
        #get variable 1
        try:
            num1 = int(memory[splitData[line][4:7]])
        except:
            try:
                num1 = float(memory[splitData[line][4:7]])
            except:
                print(f'\nerror on line {line+1}; could not convert variable "{splitData[line][4:7]}" to a number')
        
        #get variable 2    
        try:
            num2 = int(memory[splitData[line][8:11]])
        except:
            try:
                num2 = float(memory[splitData[line][8:11]])
            except:
                print(f'\nerror on line {line+1}; could not convert variable "{splitData[line][8:11]}" to a number')
                
        if num1 == num2:
            memory[splitData[line][12:15]] = False
        else:
            memory[splitData[line][12:15]] = True
    
    elif command == "les":
        #check for variables
        try:
            placeholder = splitData[line][4:7]
        except:
            print(f'\nerror on line {line+1}; no variables provided')
        
        try:
            placeholder = splitData[line][8:11]
        except:
            print(f'\nerror on line {line+1}; only one variable provided')
        
        try:
            placeholder = splitData[line][12:15]
        except:
            print(f'\nerror on line {line+1}; no output variable provided')
        
        #get variable 1
        try:
            num1 = int(memory[splitData[line][4:7]])
        except:
            try:
                num1 = float(memory[splitData[line][4:7]])
            except:
                print(f'\nerror on line {line+1}; could not convert variable "{splitData[line][4:7]}" to a number')
        
        #get variable 2    
        try:
            num2 = int(memory[splitData[line][8:11]])
        except:
            try:
                num2 = float(memory[splitData[line][8:11]])
            except:
                print(f'\nerror on line {line+1}; could not convert variable "{splitData[line][8:11]}" to a number')
                
        if num1 < num2:
            memory[splitData[line][12:15]] = True
        else:
            memory[splitData[line][12:15]] = False

    elif command == "grt":
        #check for variables
        try:
            placeholder = splitData[line][4:7]
        except:
            print(f'\nerror on line {line+1}; no variables provided')
        
        try:
            placeholder = splitData[line][8:11]
        except:
            print(f'\nerror on line {line+1}; only one variable provided')
        
        try:
            placeholder = splitData[line][12:15]
        except:
            print(f'\nerror on line {line+1}; no output variable provided')
        
        #get variable 1
        try:
            num1 = int(memory[splitData[line][4:7]])
        except:
            try:
                num1 = float(memory[splitData[line][4:7]])
            except:
                print(f'\nerror on line {line+1}; could not convert variable "{splitData[line][4:7]}" to a number')
        
        #get variable 2    
        try:
            num2 = int(memory[splitData[line][8:11]])
        except:
            try:
                num2 = float(memory[splitData[line][8:11]])
            except:
                print(f'\nerror on line {line+1}; could not convert variable "{splitData[line][8:11]}" to a number')
                
        if num1 > num2:
            memory[splitData[line][12:15]] = True
        else:
            memory[splitData[line][12:15]] = False
    
    elif command == "leq":
        #check for variables
        try:
            placeholder = splitData[line][4:7]
        except:
            print(f'\nerror on line {line+1}; no variables provided')
        
        try:
            placeholder = splitData[line][8:11]
        except:
            print(f'\nerror on line {line+1}; only one variable provided')
        
        try:
            placeholder = splitData[line][12:15]
        except:
            print(f'\nerror on line {line+1}; no output variable provided')
        
        #get variable 1
        try:
            num1 = int(memory[splitData[line][4:7]])
        except:
            try:
                num1 = float(memory[splitData[line][4:7]])
            except:
                print(f'\nerror on line {line+1}; could not convert variable "{splitData[line][4:7]}" to a number')
        
        #get variable 2    
        try:
            num2 = int(memory[splitData[line][8:11]])
        except:
            try:
                num2 = float(memory[splitData[line][8:11]])
            except:
                print(f'\nerror on line {line+1}; could not convert variable "{splitData[line][8:11]}" to a number')
                
        if num1 <= num2:
            memory[splitData[line][12:15]] = True
        else:
            memory[splitData[line][12:15]] = False

    elif command == "geq":
        #check for variables
        try:
            placeholder = splitData[line][4:7]
        except:
            print(f'\nerror on line {line+1}; no variables provided')
        
        try:
            placeholder = splitData[line][8:11]
        except:
            print(f'\nerror on line {line+1}; only one variable provided')
        
        try:
            placeholder = splitData[line][12:15]
        except:
            print(f'\nerror on line {line+1}; no output variable provided')
        
        #get variable 1
        try:
            num1 = int(memory[splitData[line][4:7]])
        except:
            try:
                num1 = float(memory[splitData[line][4:7]])
            except:
                print(f'\nerror on line {line+1}; could not convert variable "{splitData[line][4:7]}" to a number')
        
        #get variable 2    
        try:
            num2 = int(memory[splitData[line][8:11]])
        except:
            try:
                num2 = float(memory[splitData[line][8:11]])
            except:
                print(f'\nerror on line {line+1}; could not convert variable "{splitData[line][8:11]}" to a number')
                
        if num1 >= num2:
            memory[splitData[line][12:15]] = True
        else:
            memory[splitData[line][12:15]] = False
    
    
    #end of instruction list
    else:
        if command != "":
            print(f'\nerror on line {line+1}; could not execute instruction "{command}"')
            break
    
    
    #keep at end
    try:
        placeholder = splitData[line + 1]
    except:
        print("\nend of program")
        break
