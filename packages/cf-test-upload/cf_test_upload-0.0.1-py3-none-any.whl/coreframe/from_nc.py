import h5py
from coreframe import CoreFrame
import numpy as np

def num2date(times, units):
    # Parse the units string to get the base unit and the origin time
    units = units.decode()

    base_unit = units.split()[0]
    origin_str = units.split('since')[1].strip()

    base_unit_dict = {'seconds': 's',
                      'minutes': 'm',
                      'hours': 'h',
                      'days': 'D',
                      'weeks': 'W',
                      'months': 'M',
                      'years': 'Y'}

    origin_time = np.datetime64(origin_str)
  
    # Get the base unit duration from the dictionary
    base_unit_duration = np.timedelta64(1, base_unit_dict.get(base_unit, 's'))

    # Convert the times to datetime64 objects
    datetime_array = origin_time + times * base_unit_duration

    return datetime_array

def from_nc(path, data_key, dtime_key):
    data = h5py.File(path, 'r')

    # Access a dataset from the file
    dataset = data[data_key]

    time = num2date(data[dtime_key], units=data[dtime_key].attrs['units'])

    dataset = CoreFrame(dataset, dtimes=time)
    # Close the file
    data.close()
    return dataset


if __name__ == "__main__":
    cf = from_nc("GSWP3.BC.Tair.3hrMap.2014.nc", "Tair", "time")
    print(cf)