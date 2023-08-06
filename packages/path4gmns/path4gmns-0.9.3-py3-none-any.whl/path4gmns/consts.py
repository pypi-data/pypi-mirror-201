""" global constants """
# for shortest path calculation
MAX_LABEL_COST = 2147483647
# in case where the divisor/denominator is ZERO
# to do: combine SMALL_DIVISOR and MIN_OD_VOL
SMALL_DIVISOR = 0.00001
# for column generation
MIN_OD_VOL = 0.000001
# for accessibility evaluation
MIN_TIME_BUDGET = 10
MAX_TIME_BUDGET = 240
BUDGET_TIME_INTVL = 5
# unit
MILE_TO_METER = 1609
MPH_TO_KPH = 1.609
# reserved for simulation
NUM_OF_SECS_PER_SIMU_INTERVAL = 6