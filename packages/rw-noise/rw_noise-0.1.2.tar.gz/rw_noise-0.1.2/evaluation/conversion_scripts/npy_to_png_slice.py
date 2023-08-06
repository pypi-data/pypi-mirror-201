import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import imageio

filenames = [#'file1000000', 
            'file1000007', ]
            #'file1000017', 
            #'file1000026', 
            #'file1000031']

im_slice = 19
data_path = os.path.expanduser('~/sciebo/pria-daten/FastMRI_reconstructed/')

for i, filename in enumerate(filenames):
    f = np.load(os.path.join(data_path, filename + '.npy'))

    save_path = os.path.join(data_path, filename)

    recon_abs = np.abs(f)
    im_abs = (recon_abs / np.max(recon_abs) * 255).astype(np.uint8)
    imageio.imwrite(save_path + '_{}.png'.format(im_slice), im_abs[im_slice, :, :])  # to save png

#    for i in range(0,f.shape[0]):
#        print(i)
#        plt.imshow(im_abs[i, :, :], cmap='gray')
#        plt.show()
 
#     fig.add_subplot(1, 2, 1)
#     plt.imshow(recon_abs[im_slice, :, :], cmap='gray')
# 
#     fig.add_subplot(1, 2, 2)
#     plt.imshow(recon_ang[im_slice, :, :], cmap='gray')
# 
# plt.show()

