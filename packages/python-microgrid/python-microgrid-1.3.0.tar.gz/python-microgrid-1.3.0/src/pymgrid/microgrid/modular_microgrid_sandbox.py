from pymgrid.microgrid.microgrid import Microgrid
from pymgrid.envs.discrete import DiscreteMicrogridEnv
import numpy as np
import yaml

np.random.seed(0)

genset = GensetModule(running_min_production=10, running_max_production=50, genset_cost=0.5)

battery = BatteryModule(min_capacity=0,
                        max_capacity=100,
                        max_charge=50,
                        max_discharge=50,
                        efficiency=1.0,
                        init_soc=0.5)

battery_2 = BatteryModule(min_capacity=10,
                          max_capacity=200,
                        max_charge=50,
                        max_discharge=50,
                        efficiency=1.0,
                        init_soc=0.8)

pv = RenewableModule(time_series= 50*np.ones(100))

load = LoadModule(time_series=60*np.ones(100),
                  loss_load_cost=10)

load_2 = LoadModule(time_series=60*np.ones(100),
                    loss_load_cost=10)


grid = GridModule(max_import=100, max_export=0, time_series=np.ones((100, 3)), raise_errors=True)

env = DiscreteMicrogridEnv([genset,
                              ('small_battery', battery),
                              ('big_battery',battery_2),
                              pv,
                              load,
                              load_2,
                              grid])

microgrid = Microgrid([genset,
                       # ('small_battery', battery),
                       ('big_battery',battery_2),
                       pv,
                       load,
                       # load_2,
                       grid
                       ])

nonmodular = microgrid.to_nonmodular().to_modular().to_nonmodular()


for j in range(2):
    action = microgrid.sample_action(strict_bound=True)
    microgrid.run(action)


# print("dump")
# print(yaml.dump(microgrid.small_battery.item()))
print('safe dump')
dump = yaml.safe_dump(microgrid.small_battery.item())
print(dump)

print("safe load")
loaded = yaml.safe_load(dump)
print(loaded)

out = microgrid.get_log(drop_singleton_key=True)


# pv_series = 50*np.ones(ts_len)
# load_series = 40*np.ones(ts_len)
# load_series[::2] = 60


load = LoadModule(time_series=60*np.ones(100),
                  loss_load_cost=10)

# load_series[::2] = 30


# microgrid = ModularMicrogrid([('small_battery', battery), ('big_battery',battery_2), pv, load, load_2, grid, genset])
microgrid = Microgrid([genset, ('small_battery', battery), ('big_battery', battery_2), pv, load, load_2, grid])
print(microgrid.fixed_modules)
print('init!')

action = microgrid.sample_action(strict_bound=True)
print('action')
print(action)
print('unnormalized')
print(microgrid.from_normalized(action, act=True))
out = microgrid.run(action)
print(microgrid.get_log(drop_singleton_key=True))
print('stepped!')

"""
TODO
1) Make a quick rundown of changes.
2) Write list of things yet to be done as github issues
3) push to a branch
"""

"""
TODO
1) DONE. Your pv/load log (state_dict) is pre-action, but your battery log (state_dict) is post-action. Fix
2) DONE. Your types in log are inconsistent. Also in observations/provided/absorbed energy I think.
3) DONE. Your get_log function needs to add another layer to column multiindex instead of setting the index
4) DONE. You should drop a layer from multiindex log if there is only one of each module (or allow this with kwarg)
5) DONE. Add loss load to load modules (with a cost)
6) DONE. Add pv curtailment to renewable modules
7) If loss load is in load modules, do you need unbalanced energy module? Wb overgeneration?
    I don't this these are needed. Overgeneration should be renewable curtailment and loss load should be in load modules.
8) DONE. Currently unbalanced energy module is not working
9) DONE. You need to figure out a way to allow for using renewable/load less than the min of the timeseries
10) DONE. Figure out issues in base_module._conform_output().
11) DONE. Add logger for provided/absorbed energy to Modular Microgrid
12) Test genset and grid
"""

# Testing conversion
# from pymgrid.MicrogridGenerator import MicrogridGenerator
#
# mgen = MicrogridGenerator(nb_microgrid=2)
# mgen.generate_microgrid()
# microgrid = mgen.microgrids[0]
# modular_version = ModularMicrogrid.from_nonmodular(microgrid)