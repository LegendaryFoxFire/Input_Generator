#Remember the file is split up into 2 different pieces >:3




# Cloud systems are mainly Linux based! 90% Observed Statistic. https://www.enterpriseappstoday.com/stats/linux-statistics.html
# Based off of common knowledge: 16 or 32 GB Ram average. (Thank goodness we don't have to worry about some of these other statistics!)
# https://www.spec.org/cloud_iaas2018/results/ was an interesting introspection into the industry
# https://www.researchgate.net/publication/232069216_Energy_Efficient_Scheduling_of_HPC_Jobs_on_Virtualized_Clusters_Using_Host_and_VM_Dynamic_Configuration || https://www.intel.com/content/dam/doc/white-paper/risc-migration-itanium-xeon-hp-mainframe-workloads-paper.pdf [1]
# https://learn.microsoft.com/en-us/archive/blogs/nickmac/hyper-v-maximum-supported-configurations
        
"""
machine class:
{
# comment
        Number of machines:               N                                                    TODO: find average cloud machine # https://serverfault.com/questions/196083/common-and-maximum-number-of-virtual-machines-per-server between 320 ~ 512? 
        CPU type:                         ARM, POWER, RISCV, X86                               checked!
        Number of cores:                  1, 2, 4, 8, 16, 32, 64                               checked!
        Memory:                           (2GB, 4GB, 8GB, 16GB, 32GB, 64GB, 128GB, 256GB)      checked!
        S-States:                         [120, 100, 100, 80, 40, 10, 0]                       Found: higher processors (180) lower (95)
        P-States:                         [12, 8, 6, 4]                                        TODO: Followup. [1] 
        C-States:                         [12, 3, 1, 0]                                        checked!                   
        MIPS:                             [1000, 800, 600, 400]                                checked!
        GPUs:                             BOOL                                                 (going off of a rough 20%) 
}
"""











"""


machine class:
{
# comment
        Number of machines: 16
        CPU type: X86
        Number of cores: 8
        Memory: 16384
        S-States: [120, 100, 100, 80, 40, 10, 0]
        P-States: [12, 8, 6, 4]
        C-States: [12, 3, 1, 0]
        MIPS: [1000, 800, 600, 400]
        GPUs: yes
}
machine class:
{
        Number of machines: 24
        Number of cores: 16
        CPU type: ARM
        Memory: 16384
        S-States: [120, 100, 100, 80, 40, 10, 0]
        P-States: [12, 8, 6, 4]
        C-States: [12, 3, 1, 0]
        MIPS: [1000, 800, 600, 400]
        GPUs: yes
}
task class:
{
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
}


"""



