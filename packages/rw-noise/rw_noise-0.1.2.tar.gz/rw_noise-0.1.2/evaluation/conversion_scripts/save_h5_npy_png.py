import h5py
import matplotlib.pyplot as plt
import numpy as np
import sigpy.mri.app as smri
import os
from PIL import Image
import imageio

filenames = ['file1000000', 
            'file1000007', 
            'file1000017', 
            'file1000026', 
            'file1000031']

im_slice = 18
data_path = '/data/home/f_eile01/Projects/Random_Walker_Noise/data/'

for i, filename in enumerate(filenames):
    f = h5py.File(filename + '.h5', 'r')

    kspace = np.array(f['kspace'])
    shape_y = kspace.shape[2]

    recon_fft = np.fft.ifftshift(np.fft.ifft2(np.fft.fftshift(kspace)))
    save_path = os.path.join(data_path, filename)

    # np.save(save_path, recon_fft)  # to save npy 

    recon_abs = np.abs(recon_fft)
    im_abs = (recon_abs / np.max(recon_abs) * 255).astype(np.uint8)
    imageio.imwrite(save_path + '_{}.png'.format(im_slice), im_abs[im_slice, :, :])  # to save png

#     fig = plt.figure(i)
# 
#     fig.add_subplot(1, 2, 1)
#     plt.imshow(recon_abs[im_slice, :, :], cmap='gray')
# 
#     fig.add_subplot(1, 2, 2)
#     plt.imshow(recon_ang[im_slice, :, :], cmap='gray')
# 
# plt.show()

