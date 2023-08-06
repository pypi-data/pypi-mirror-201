from PyaiVS import model_bulid
# model_bulid.running('/data/jianping/bokey/OCAICM/dataset/a1/a1.csv',
#                     out_dir='/data/jianping/bokey/OCAICM/dataset/',
#                     split=['random'],
#                     model=['SVM','DNN'],
#                     FP=['ECFP4'],
#                     run_type='para',
#                     cpus=8)
from PyaiVS import virtual_screen
virtual_screen.model_screen(model='SVM',
                           split='random',
                           FP='ECFP4',
                           prop=0.8,
                           model_dir='/data/jianping/bokey/OCAICM/dataset/a1/model_save',
                           screen_file='/data/jianping/bokey/OCAICM/dataset/a1/base.csv',
                           sep=';',
                           smiles_col='smiles')


