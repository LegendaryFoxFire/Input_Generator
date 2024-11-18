# John Bukoski

import Text_Editing as io

""" Input File Generator! 

    The objective is to produce basic code to generate the txt needed to copy over to 
    the simulator to run off of as realistic stats as I can hope to parse through. 

    The code will have 2 parts. The Machines, and the Tasks. These will work to produce
    the final file. Hopefully I can document comments appropriately! 
"""
def Input_Generator():
    io.init()
    Machine_Class()
    #Task_Class()




# Machine Class

""" Define distributions for machine parameters."""
# Constants
# =========

# 1 for Ceiling Rounding.
ROUNDING        = 1                                
# List Definitions
CPU_LIST        = ["ARM", "POWER", "RISCV", "X86"]
CORE_LIST       = [1, 2, 4, 8, 16, 32, 64]
MEMORY_LIST     = [1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144]
BOOL_LIST       = ["yes", "no"]                     # I hate that I'm even typing this.
# List Lengths
CPU_DIST_LEN    = 4
CORE_DIST_LEN   = 7
MEMORY_DIST_LEN = 9 
BOOL_DIST_LEN   = 2

Machine_Number  = 350                               # Number of machines in cluster
CPU_Dist        = [20, 10, 10, 60]                    # [%ARM, %POWER, %RISCV, %X86]
Core_Dist       = [5, 1, 4, 10, 60, 10, 10]         # [%1Core, %2Core, %4Core, %8Core, %16Core, %32Core, %64Core]
Memory_Dist     = [5, 5, 1, 4, 25, 30, 10, 10, 10]  # [%1GB, %2GB, %4GB, %8GB, %16GB, %32GB, %64GB, %128GB, %256GB]
Bool_Dist       = [10, 90]                          # [%Yes]
S_States        = [120, 100, 100, 80, 40, 10, 0]    # To be multiplied by core-based coefficient: {higher: (1.5) || (180)} {lower: (0.8) || (95)}
P_States        = [12, 8, 6, 4]                   
C_States        = [12, 3, 1, 0]                                             
MIPS            = [1000, 800, 600, 400]           

# Coefficients
HIGHER_STATE_COEFF = 1.5
LOWER_STATE_COEFF  = 0.8


"Ensures probabilities in dists are computable"
def Machine_Error_Checks():
    #This way I can capture all errors for the user at once.
    error_list = []

    #Machine Number errors: 
    if(Machine_Number < 1):
        error_list.append("Machine Number must be greater than 0.")
    if(type(Machine_Number) != int): 
        error_list.append("Machine Number must be an integer!") 
    
    #CPU_Dist errors:
    if(len(CPU_Dist) != CPU_DIST_LEN):
        error_list.append(f"CPU_Dist must have {CPU_DIST_LEN} elements. It currently has {len(CPU_Dist)}")
    if(Check_Distribution(CPU_Dist) != 100):
        error_list.append(f"CPU_Dist must values add to 100. Currently it adds to {Check_Distribution(CPU_Dist)}")

    #Core_Dist errors:
    if(len(Core_Dist) != CORE_DIST_LEN):
        error_list.append(f"Core_Dist must have {CORE_DIST_LEN} elements. It currently has {len(Core_Dist)}")
    if(Check_Distribution(Core_Dist) != 100):
        error_list.append(f"Core_Dist must values add to 100. Currently it adds to {Check_Distribution(Core_Dist)}")

    #Memory_Dist errors:
    if(len(Memory_Dist) != MEMORY_DIST_LEN):
        error_list.append(f"Memory_Dist must have {MEMORY_DIST_LEN} elements. It currently has {len(Memory_Dist)}")
    if(Check_Distribution(Memory_Dist) != 100):
        error_list.append(f"Memory_Dist must values add to 100. Currently it adds to {Check_Distribution(Memory_Dist)}")

    #Bool_Dist errors:

    if(len(Bool_Dist) != BOOL_DIST_LEN):
        error_list.append(f"Bool_Dist must have {BOOL_DIST_LEN} elements. It currently has {len(Bool_Dist)}")
    if(Check_Distribution(Bool_Dist) != 100):
        error_list.append(f"Bool_Dist must values add to 100. Currently it adds to {Check_Distribution(Bool_Dist)}")
    
    return error_list
    
""" Iterates through lists to check if it adds to 100% """
def Check_Distribution(items):
    result = 0
    for num in items:
        if(isinstance(num, str)):
            print(f"One of your values is a String: >{num}<!")
        result += num
    return result 

""" Executes the machine class input writing """
def Machine_Class():
    error_list = Machine_Error_Checks()
    if(len(error_list) > 0):
        for item in error_list:
            print(item)
    else:
        del error_list
        print("No Errors found! Nice!")
        Create_Machine_Input()

""" Processes the distributions to various writes """
def Create_Machine_Input():
    count = 0
    for cpu_type, cpu_dist in enumerate(CPU_Dist):
        num_cpu_type = int(Machine_Number * (cpu_dist / 100) + ROUNDING)
        for core_type, core_dist in enumerate(Core_Dist):
            num_core_type = int(num_cpu_type * (core_dist / 100) + ROUNDING)
            for memory_type, memory_dist in enumerate(Memory_Dist):
                num_memory_type = int(num_core_type * (memory_dist / 100) + ROUNDING)
                for bool_type, bool_dist in enumerate(Bool_Dist):
                    num_bool_type = int(num_memory_type * (bool_dist / 100))


                    # just for debugging
                    count += num_bool_type
                    if(num_bool_type > 1):
                        args = [num_bool_type, 
                                CPU_LIST[cpu_type], 
                                CORE_LIST[core_type],
                                MEMORY_LIST[memory_type],
                                S_States,
                                P_States,
                                C_States,
                                MIPS,
                                BOOL_LIST[bool_type]]
                        Machine_Class_Writer(args)
    print(f"Our final count was {count}")        

""" S-States can seemingly flutuate roughly depending on the cores: 
    it's a loose connection: sure. But more cores typically are indicative
    of higher performance specs."""
def S_Adjust(cores):
    coefficient = (((HIGHER_STATE_COEFF - LOWER_STATE_COEFF) / CORE_DIST_LEN) * cores) + LOWER_STATE_COEFF
    result = []
    for state in S_States:
        result.append(int(coefficient * state))
    return result

""" Machine Class Writer:
    Takes in args and writes them to the file
    args:
        (example) 
        Number of machines: 16
        CPU type: X86
        Number of cores: 8
        Memory: 16384
        S-States: [120, 100, 100, 80, 40, 10, 0]
        P-States: [12, 8, 6, 4]
        C-States: [12, 3, 1, 0]
        MIPS: [1000, 800, 600, 400]
        GPUs: yes
"""
def Machine_Class_Writer(args):
    io.write("machine class:")
    io.write("{")
    io.write(f"        Number of machines: {args[0]}")
    io.write(f"        CPU type: {args[1]}")
    io.write(f"        Number of cores: {args[2]}")
    io.write(f"        Memory: {args[3]}")
    io.write(f"        S-States: {args[4]}")
    io.write(f"        P-States: {args[5]}")
    io.write(f"        C-States: {args[6]}")
    io.write(f"        MIPS: {args[7]}")
    io.write(f"        GPUs: {args[8]}")
    io.write("}")

# Task Class

""" Define distributions for task parameters."""
# Constants
# =========
SLA_LIST        = ["SLA0", "SLA1", "SLA2", "SLA3"]
VM_LIST         = ["LINUX", "LINUX_RT", "WIN", "AIX"]

# Consistent Task
C_Duration      = 2400000000
C_Inter         = 6000
C_Runtime       = 100000
C_Memory        = 8

# Memory Test 
M_Duration      = 300000000
M_Inter         = 6000
M_Runtime       = 100000    # Long version will be duration time.
M_Memory        = 8192

# Stress Test
S_Duration      = 300000000
S_Inter         = 1
S_Runtime       = 100000
S_Memory        = 8





def Task_Class():
    for sla, time in enumerate(SLA_LIST):
        Task_Pattern(sla, time)
        

def Task_Pattern(sla, time):
    Task(sla, time, )
    #memory
    #stress
    #both

def Task(sla, time, code):









# for 40 minutes are normal load, constant popping in and out 10% load tasks. etc.
# 5 minutes in we want to do a 5 minute, 5 minute, 5 minute mem load.
# 20 minutes in we want a load test.
# then 25 minutes we run both at the same time. 







""" Task Class Writer:
    Takes in args and writes them to the file
    args:
        (example)
        Start time: 60000
        End time : 8000000
        Inter arrival: 6000
        Expected runtime: 20000000
        Memory: 8
        VM type: LINUX
        GPU enabled: no
        SLA type: SLA0
        CPU type: X86
        Task type: WEB
        Seed: 520230

"""
def Task_Class_Writer(args):
    io.write("task class:")
    io.write("{")
    io.write(f"        Start time: {args[0]}")
    io.write(f"        End time: {args[1]}")
    io.write(f"        Inter arrival: {args[2]}")
    io.write(f"        Expected runtime: {args[3]}")
    io.write(f"        Memory: {args[4]}")
    io.write(f"        VM type: {args[5]}")
    io.write(f"        GPU enabled: {args[6]}")
    io.write(f"        SLA type: {args[7]}")
    io.write(f"        CPU type: {args[8]}")
    io.write(f"        Task type: {args[9]}")
    io.write(f"        Seed: 520230")
    io.write("}")























#Execute
Input_Generator()


