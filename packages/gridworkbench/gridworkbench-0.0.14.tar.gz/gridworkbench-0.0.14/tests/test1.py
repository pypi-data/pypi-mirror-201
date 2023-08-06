import sys
sys.path.insert(0, r"G:\My Drive\AB\Re\Projects\Thrust_I_Extreme_Events\6017_Synthetic_Blackstart_Data\GridWorkbench_Project\gridworkbench\src")
from gridworkbench import GridWorkbench
from esa import saw

s = saw.SAW(r"G:\My Drive\AB\Re\Projects\Thrust_I_Extreme_Events\6017_Synthetic_Blackstart_Data\GridWorkbench_Project\gridworkbench\tests\Texas7k_20210309.pwb")

wb = GridWorkbench()
wb.saw_read_all(s)

for g in wb.gens():
    print(g.bus.name, "->", g.fuel_type)