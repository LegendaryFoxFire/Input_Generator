# John Bukoski

# Notes:

# Cloud systems are mainly Linux based! 90% Observed Statistic. https://www.enterpriseappstoday.com/stats/linux-statistics.html
# Based off of common knowledge: 16 or 32 GB Ram average. (Thank goodness we don't have to worry about some of these other statistics!)
# https://www.spec.org/cloud_iaas2018/results/ was an interesting introspection into the industry
# https://www.researchgate.net/publication/232069216_Energy_Efficient_Scheduling_of_HPC_Jobs_on_Virtualized_Clusters_Using_Host_and_VM_Dynamic_Configuration || https://www.intel.com/content/dam/doc/white-paper/risc-migration-itanium-xeon-hp-mainframe-workloads-paper.pdf [1]
# https://learn.microsoft.com/en-us/archive/blogs/nickmac/hyper-v-maximum-supported-configurations
# https://serverfault.com/questions/196083/common-and-maximum-number-of-virtual-machines-per-server between 320 ~ 512? 

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
    Task_Class(0, 0, False)


# Machine Class

""" Define distributions for machine parameters."""
# Constants
# =========

# 1 for Ceiling Rounding.
ROUNDING        = 1                                
# List Definitions
CPU_LIST        = ["X86"]#["ARM", "POWER", "RISCV", "X86"]
CORE_LIST       = [1, 2, 4, 8, 16, 32, 64]
MEMORY_LIST     = [1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144]
BOOL_LIST       = ["yes", "no"]                     # I hate that I'm even typing this.

# Settings
Machine_Number  = 350                              # Number of machines in cluster
CPU_Dist        = [100]                    # [%ARM, %POWER, %RISCV, %X86]
Core_Dist       = [0, 0, 0, 100, 0, 0, 0]         # [%1Core, %2Core, %4Core, %8Core, %16Core, %32Core, %64Core]
Memory_Dist     = [0, 0, 0, 0, 100, 0, 0, 0, 0]  # [%1GB, %2GB, %4GB, %8GB, %16GB, %32GB, %64GB, %128GB, %256GB]
Bool_Dist       = [100, 0]                          # [%Yes, %No]
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
    if(len(CPU_Dist) != len(CPU_LIST)):
        error_list.append(f"CPU_Dist must have {len(CPU_LIST)} elements. It currently has {len(CPU_Dist)}")
    if(Check_Distribution(CPU_Dist) != 100):
        error_list.append(f"CPU_Dist must values add to 100. Currently it adds to {Check_Distribution(CPU_Dist)}")

    #Core_Dist errors:
    if(len(Core_Dist) != len(CORE_LIST)):
        error_list.append(f"Core_Dist must have {len(CORE_LIST)} elements. It currently has {len(Core_Dist)}")
    if(Check_Distribution(Core_Dist) != 100):
        error_list.append(f"Core_Dist must values add to 100. Currently it adds to {Check_Distribution(Core_Dist)}")

    #Memory_Dist errors:
    if(len(Memory_Dist) != len(MEMORY_LIST)):
        error_list.append(f"Memory_Dist must have {len(MEMORY_LIST)} elements. It currently has {len(Memory_Dist)}")
    if(Check_Distribution(Memory_Dist) != 100):
        error_list.append(f"Memory_Dist must values add to 100. Currently it adds to {Check_Distribution(Memory_Dist)}")

    #Bool_Dist errors:

    if(len(Bool_Dist) != len(BOOL_LIST)):
        error_list.append(f"Bool_Dist must have {len(BOOL_LIST)} elements. It currently has {len(Bool_Dist)}")
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
                                S_Adjust(core_type),
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
    coefficient = (((HIGHER_STATE_COEFF - LOWER_STATE_COEFF) / len(CORE_LIST)) * cores) + LOWER_STATE_COEFF
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

EPOCH           = 2400000000
MEM_BENCH_DUR   = 900000000
SLA_LIST        = ["SLA0", "SLA1", "SLA2", "SLA3"]
VM_LIST         = ["LINUX"] #, "LINUX_RT", "WIN", "AIX"]



NUM_CASES = 3

# Tasks: [Consistent, Memory, Stress]
# Consistent Task
Duration        = [  EPOCH, 300000000, 300000000]
Num_Tasks       = [   4000,      4000, 75000    ] #[  16000,     16000, 300000   ]
Runtime         = [ 100000,    100000, 100000   ] 
Memory          = [      8,      8192, 8        ]


""" It's important to make the selections compatible """
def Task_Errors(VM, CPU):
    if(VM >= len(VM_LIST)):
        print(f"{VM} is not a choice within the range of VM_List: \n{VM_LIST}")
        if(CPU >= len(CPU_LIST)):
            print(f"{CPU} is not a choice within the range of CPU_List: \n{CPU_LIST}")
    else: 
        if(VM_LIST[VM] == "AIX"):
            return CPU_LIST[CPU] == "POWER"
        if(VM_LIST[VM] == "WIN"):
            return (CPU_LIST[CPU] == "X86" or CPU_LIST[CPU] == "ARM")
        else:
            return True

""" Gathers the inputs for pattern call"""
def Task_Class(VM_Selection, CPU_Selection, GPU_Setting):
    if(not Task_Errors(VM_Selection, CPU_Selection)):
        print("There's a conflict in the selections! Make sure the VM and CPU selections are compatible")
    else:
        vm = VM_LIST[VM_Selection]
        cpu = CPU_LIST[CPU_Selection]
        gpu = "no"
        if(GPU_Setting):
            gpu = "yes"
        for time, sla in enumerate(SLA_LIST):
            Task_Pattern(time, sla, vm, cpu, gpu)
        
""" Defines a testing pattern with patterns
        for 40 minutes are normal load, constant popping in and out 10% load tasks. etc.
        5 minutes in we want to do a 5 minute, 5 minute, 5 minute mem load.
        20 minutes in we want a load test.
        then 25 minutes we run both at the same time. 
"""
def Task_Pattern(time, sla, vm, cpu, gpu):
    time *= EPOCH          # @+0 minutes.
    
    Consistent_Task(time, sla, vm, cpu, gpu, True)
    time += Duration[1]    # @+5 minutes.
    
    Memory_Benchmark(time, sla, vm, cpu, gpu)
    time += MEM_BENCH_DUR  # @+20 minutes.
    
    Load_Benchmark(time, sla, vm, cpu, gpu)
    time += Duration[1]    # @+25 minutes.

    Memory_Benchmark(time, sla, vm, cpu, gpu)
    Load_Benchmark(time, sla, vm, cpu, gpu)


""" A task pattern that represents normal load """
def Consistent_Task(time, sla, vm, cpu, gpu, isRandom):
    args = [time,
            time + Duration[0],
            Frequency(Num_Tasks[0], Duration[0]),
            Runtime[0],
            Memory[0],
            vm,
            gpu,
            sla,
            cpu,
            "STREAM"]
    if(isRandom):
        for item in VM_LIST:
            args[5] = item
            Task_Class_Writer(args)
    else:
        Task_Class_Writer(args)
        
def Memory_Benchmark(time, sla, vm, cpu, gpu):
    #15 Minute time duration (5 minute intervals)
    for i in range(0, MEM_BENCH_DUR, Duration[1]):
        time_incr = time + i
        runtime = Runtime[1]

        # Higher stress in middle section
        if(i%2 == 1):
            runtime = Duration[1]

        args = [time_incr,
                time_incr + Duration[1],
                Frequency(Num_Tasks[1], Duration[1]),
                runtime,
                Memory[1],
                vm,
                gpu,
                sla,
                cpu,
                "HPC"]
        Task_Class_Writer(args)

def Load_Benchmark(time, sla, vm, cpu, gpu):
    args = [time,
            time + Duration[2],
            Frequency(Num_Tasks[2], Duration[2]),
            Runtime[2],
            Memory[2],
            vm,
            gpu,
            sla,
            cpu,
            "WEB"]
    Task_Class_Writer(args)

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

""" Helper: 
        Intuitive rephrasing of the inter parameter
"""
def Frequency(num_tasks, time_frame):
    return time_frame // num_tasks 
#Execute
Input_Generator()
