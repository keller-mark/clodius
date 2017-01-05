from __future__ import print_function

import clodius.hdf_tiles as cht
import h5py
import pybedtools as pbt

def test_get_tiles():
    f = h5py.File('test/sample_data/cnv.hibed')
    data = cht.get_discrete_data(f, 22, 48)

    assert(len(data) > 0)

    data = cht.get_discrete_data(f, 22, 50)
    assert(len(data) > 0)

    data = cht.get_discrete_data(f, 0, 0)
    assert(len(data) == 100)

def check_tile_for_duplicate_entries(discrete_data):
    '''
    Make sure that there are no entries with the same UID in any tile.
    '''
    seen = set()
    
    for i,d in enumerate(discrete_data):
        uid = d[-2]

        if uid in seen:
            #print("seen uid:", uid)
            #print("d:", d)
            return False

        #print("adding uid:", uid, d[:3])
        seen.add(uid)

    return True


def test_tile_ranges():
    f = h5py.File('test/sample_data/cnv.hibed')

    data11 = cht.get_discrete_data(f, 11, 6)
    assert(check_tile_for_duplicate_entries(data11) == True)

    max_length_11 = max([int(d[2]) - int(d[1]) for d in data11])
    #print("data11:", max_length_11)

    data10 = cht.get_discrete_data(f, 10, 3)
    max_length_10 = max([int(d[2]) - int(d[1]) for d in data10])
    #print("data10:", max_length_10)

    # more zoomed out tiles should have longer tiles than more
    # zoomed in tiles
    assert(max_length_10 >= max_length_11)

    d1 = cht.get_discrete_data(f, 11, 5)
    #print("d1:", len(d1))
    #print("dv:", [x for x in d1 if (int(x[1]) < 12000000 and int(x[2]) > 12000000)])

    d3 = cht.get_discrete_data(f, 12, 10)
    #print("d2:", len(d3))

    d4 = cht.get_discrete_data(f, 12, 11)
    #print("d3:", len(d4))