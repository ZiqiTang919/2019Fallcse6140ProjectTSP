import re
import numpy as np

def cost_matrix(dtype, coor):
    v_num = coor.shape[0]
    if dtype == "EUC_2D":
        diff = np.tile(coor,v_num).reshape((-1,2)) - np.tile(coor.flatten(),v_num).reshape((-1,2))

        s = np.sum(np.power(diff,2),axis = 1)
        dist = np.rint(np.sqrt(s).reshape((v_num,v_num))).astype(int)
#         cost_mat = np.diag([float('inf')]*v_num) + cost_mat

    elif dtype == "GEO":
        deg = coor.astype(int)
        coors = ((coor- deg) * 5. /3. + deg) / 180. * np.pi
        q21 = np.cos(np.tile(coors,v_num).reshape((-1,2)) -         np.tile(coors.flatten(),v_num).reshape((-1,2)))
        q1,q2 = q21[:,[1]].flatten(),q21[:,[0]].flatten()
        lat = coors[:,[0]]
        q3 = np.cos(np.tile(lat,v_num).flatten() + np.tile(lat.flatten(),v_num).flatten())
        dist = (np.arccos(.5 * ((1+q1) * q2 - (1-q1) * q3)) * 6378.388 + 1).reshape((v_num,v_num))
        dist = dist.astype(int) - np.eye(v_num,dtype=int)
#         cost_mat = np.diag([float('inf')]*v_num) + dist.astype(int)
    return dist.astype(int)

def read_data(tsp_file):

    with open("./DATA/{}.tsp".format(tsp_file),"rb") as fi:
        content = fi.read().decode('utf-8')
        content = re.split('\n |\n',content)
        txt_ind = content.index('NODE_COORD_SECTION')
        end_ind = content.index('EOF')
        text = content[:txt_ind]
        data = content[txt_ind + 1:end_ind]

        # record the text information in a dictionary
        info_dict = dict(text[i].split(": ") for i in
                         range(0,len(text)))

        v_num = (int)(info_dict['DIMENSION'])

        d = np.array(' '.join(data).split(),
                     dtype=np.float).reshape([-1,3])
        cost_mat = cost_matrix(info_dict['EDGE_WEIGHT_TYPE'],
                               d[:,[1,2]])
    return cost_mat

