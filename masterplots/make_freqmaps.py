from setup_matplotlib import *
import healpy as hp
import matplotlib.cm as cm
import numpy as N

cmbtest="/Users/trygveleithesvalheim/Datafiles/mdata/npipe/fits/"
dx12="/Users/trygveleithesvalheim/Datafiles/mdata/dx12/fits_v2/master64/"
dx11="/Users/trygveleithesvalheim/Datafiles/mdata/dx11/fits_v3.3/64diffs/"
dipole="/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/MDcorrections/"
npipe="/Users/trygveleithesvalheim/Datafiles/mdata/npipe/fits/"
masks="/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/masks/"
rms="/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/rms/"
polwmap="/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/polwmap/"
srollnpipe="/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/srollnpipe/"
raw="/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/raw/"
anom="/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/anom/"
cobe="/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/cobe/"
dame="/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/dame/"
npipe21K="/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/npipe/npipe21K/"
#npipe21="/Users/trygveleithesvalheim/Datafiles/mdata/npipe/fits/npipe21/"
resarticle="/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/dx11article/"
br="/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/BR/"
goal="/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/goal/"
pres="/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/pres/"
slide3="/Users/trygveleithesvalheim/Documents/jobb/jastro/masterplots/figs/slide3/"
#version="v14.2"
ver=["v7", "v14.2", "sbgv8", "shbv1", "shbv18"]
#ver=["v5.4","v7"]
#ver=["v5.6"]
#ver=["sbgv8"]
#ver=["shbv1", "shbv11"]
#ver=["shbv18"]
#ver=["wmap5"]
#ver=["shbv18", "shbv11"]
#figure_rows, figure_columns = 1, 1
#for width in [18., 12., 8.8]:
#freqs=["030", "044", "070", "100", "143", "217", "353"]
#ver=["v7","v14.2", "sbgv8", "shbv1", "shbv18","npipe21"]
#ver=["npipe21"]
#freqs=["030", "044", "070", "100-1a", "100-1b", "100-2a", "100-2b", "100-3a", "100-3b", "100-4a", "100-4b", "143", "217-2", "217-3", "217-5a", "217-5b", "217-6", "217-6", "217-7a", "217-7b", "217-8", "353-3", "353-4"]

#freqs=["857-3","857-4"]
#freqs=["353-2"]

#ver=["shbv18"]
#ver=["npipe21K"]

#freqs=["030", "044", "070", "100-1a", "100-1b", "100-2a", "100-2b", "100-3a", "100-3b", "100-4a", "100-4b", "143", "217-2", "217-3", "217-5a", "217-5b", "217-6",  "217-7a", "217-7b", "217-8","353-1","353-2","353-3", "353-4", "353-5","353-6",]
#freqs=["545-1", "545-2", "545-4", "857-1", "857-2", "857-3", "857-4"]
freqs=["353-3b"]
ver=["sbgv8"]
#for version in ver:
#freqs=["30", "70", "353"]
for f in freqs:
    version="sbgv8"
    nu = f
    min = -10
    max = 10
    if nu=="353" or nu=="30":
        min=-50
        max=50


    if version=="sbgv8":
        chimax=76
    elif version=="v7":
        chimax=18
    elif version=="v14.2":
        chimax=18
    elif version=="shbv1":
        chimax=60
    elif version=="shbv11":
        chimax=58
    elif version=="shbv18":
        chimax=66
    elif version=="npipe21":
        chimax=48
    elif version=="npipe21J":
        chimax=66


    for width in [8.8,12.0,18.0]:
        lol = 1
        #fig = plt.figure(figsize=(cm2inch(width), cm2inch(width)*0.5))
        for filename, outfile, vmin, vmax, unit, freq, scale, ticks, ticklabels, colorbar, title, titletext in [
            #(dx12+"chisq_64.fits", "chidx12", 0, 18, "", r"$\chi^2$", 1, [0,18], [r"$0$", r"$18$"], 1, 0,""),
            #(dx12+"cmb_64.fits", "cmbdx12", -300, 300, r"$\mu\mathrm{K}$", "CMB", 1, [-300,300], [r"$-300$", r"$300$"], 1, 0,""),
            #(dx12+"synch_64.fits", "synchdx12", 0, 1e3, r"$\mu\mathrm{K}_{RJ}$", r"$A_s$", 1, [0,1000], [r"$0$", r"$1000$"], 1, 0,""), #'uK_ant'???
            #(dx12+"synch_beta_64.fits", "synch_betadx12", -4, -1.5, "",r"$\beta_s$", 1, [-4,-1.5], [r"$-4$", r"$-1.5$"], 1, 0,""),
            #(dx12+"co_64.fits", "COdx12", 0, 2., r"$\mathrm{K}_{RJ}\, \mathrm{km}/\mathrm{s}$", "CO", 1, [0,2], [r"$0$", r"$2$"], 1, 0,""),
            #(dx12+"dust_64.fits", "dustdx12", 0, 1e3, r"$\mu\mathrm{K}_{RJ}$", r"$A_d$", 1, [0,1e3], [r"$0$", r"$1000$"], 1, 0,""),
            #(dx12+"dust_beta_64.fits", "dust_betadx12", 1.3, 2., "", r"$\beta_d$", 1, [1.3,2.], [r"$1.3$", r"$2.0$"], 1, 0,""),
            #(dx12+"dust_Td_64.fits", "dust_Tdx12", 14., 30., "K", r"$T_d$", 1, [14.,30.], [r"$14$", r"$30$"], 1, 0,""),


            #(dx12+"residual_030_64.fits", "dx12_residual_030", -10, 10, r"$\mu\mathrm{K}$", "30", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(dx12+"residual_044_64.fits", "dx12_residual_044", -10, 10, r"$\mu\mathrm{K}$", "44", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(dx12+"residual_070_64.fits", "dx12_residual_070", -10, 10, r"$\mu\mathrm{K}$", "70", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(dx12+"residual_100_64.fits", "dx12_residual_100", -10, 10, r"$\mu\mathrm{K}$", "100", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(dx12+"residual_143_64.fits", "dx12_residual_143", -10, 10, r"$\mu\mathrm{K}$", "143", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(dx12+"residual_217_64.fits", "dx12_residual_217", -10, 10, r"$\mu\mathrm{K}$", "217", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(dx12+"residual_353_64.fits", "dx12_residual_353", -10, 10, r"$\mu\mathrm{K}$", "353", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(dx12+"residual_545_64.fits", "dx12_residual_545", -5e-2, 5e-2, r"$\mathrm{MJy/sr}$", "545", 1, [-5e-2,5e-2], [r"$-10^{-2}$", r"$10^{-2}$"], 1, 0,""),
            #(dx12+"residual_857_64.fits", "dx12_residual_857", -5e-2, 5e-2, r"$\mathrm{MJy/sr}$", "857", 1, [-5e-2,5e-2], [r"$-10^{-2}$", r"$10^{-2}$"], 1, 0,""),

            #(dx11+"chisq_dx11_64.fits", "chidx11", 0, 18, "", r"$\chi^2$", 1, [0,18], [r"$0$", r"$18$"], 1, 0,""),
            #(dx11+"cmb_dx11_64.fits", "cmbdx11", -300, 300, r"$\mu\mathrm{K}$", "CMB", 1, [-300,300], [r"$-300$", r"$300$"], 1, 0,""),
            #(dx11+"diff-CMB_dx12-dx11_64.fits", "diff_cmb_dx12dx11", -10, 10, r"$\mu\mathrm{K}$", "CMB diff", 1, [-10,10], [r"$-10$", r"$10$"], 1, 0,""),
            #(dx11+"diff-synch_dx12-dx11_64.fits", "diff_synch_dx12dx11", -10, 10, r"$\mu\mathrm{K}_{RJ}$", r"$A_s$ diff", 1, [-10,10], [r"$-10$", r"$10$"], 1, 0,""), #'uK_ant'???
            #(dx11+"diff-synchbeta_dx12-dx11_64.fits", "diff_synch_beta_dx12dx11", -0.1, 0.1, "",r"$\beta_s$ diff", 1, [-0.1,0.1], [r"$-0.1$", r"$0.1$"], 1, 0,""),
            #(dx11+"diff-CO_dx12-dx11_64.fits", "diff_CO_dx12dx11", -1, 1., r"$\mathrm{K}_{RJ}\, \mathrm{km}/\mathrm{s}$", "CO diff", 1, [-1,1], [r"$-1$", r"$1$"], 1, 0,""),
            #(dx11+"diff-dust_dx12-dx11_64.fits", "diff_dust_dx12dx11", -10, 10, r"$\mu\mathrm{K}_{RJ}$", r"$A_d$ diff", 1, [-10,10], [r"$-10$", r"$10$"], 1, 0,""),
            #(dx11+"diff-dustbeta_dx12-dx11_64.fits", "diff_dust_beta_dx12", -1e-1,1e-1, "", r"$\beta_d$ diff", 1, [-1e-1,1e-1], [r"$0.1$", r"$0.1$"], 1, 0,""),

            #(dx11+"residual_030_64.fits", "dx11_residual_030", -10, 10, r"$\mu\mathrm{K}$", "30", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(dx11+"residual_044_64.fits", "dx11_residual_044", -10, 10, r"$\mu\mathrm{K}$", "44", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(dx11+"residual_070_64.fits", "dx11_residual_070", -10, 10, r"$\mu\mathrm{K}$", "70", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(dx11+"residual_100_64.fits", "dx11_residual_100", -10, 10, r"$\mu\mathrm{K}$", "100", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(dx11+"residual_143_64.fits", "dx11_residual_143", -10, 10, r"$\mu\mathrm{K}$", "143", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(dx11+"residual_217_64.fits", "dx11_residual_217", -10, 10, r"$\mu\mathrm{K}$", "217", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(dx11+"residual_353_64.fits", "dx11_residual_353", -10, 10, r"$\mu\mathrm{K}$", "353", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(dx11+"residual_545_64.fits", "dx11_residual_545", -5e-2, 5e-2, r"$\mathrm{MJy/sr}$", "545", 1, [-5e-2,5e-2], [r"$-10^{-2}$", r"$10^{-2}$"], 1, 0,""),
            #(dx11+"residual_857_64.fits", "dx11_residual_857", -5e-2, 5e-2, r"$\mathrm{MJy/sr}$", "857", 1, [-5e-2,5e-2], [r"$-10^{-2}$", r"$10^{-2}$"], 1, 0,""),

            #(dx11+"residual_100_c01_k00290.fits", "dx12_residual_100", -10, 10, r"$\mu\mathrm{K}$", "100", 1, [-10,0,10], ["-10", r"$0$", r"$10$"], 1, 0,""),

            #(dx12+"dust_beta_c0001_k00800.fits", "dx12_residual_100", 1.3, 2, r"$\mu\mathrm{K}$", "100", 1, [1.3,1.7,2], ["1.3", r"$1.7$", r"$2$"], 1, 0,""),
            #(dx11+"dust_beta_c0001_k00290.fits", "dx12_residual_100", 1.3, 2, r"$\mu\mathrm{K}$", "100", 1, [1.3,1.7,2], ["1.3", r"$1.7$", r"$2$"], 1, 0,""),

            #(dipole+"map_npipe4v205_v1_100_0256_40arcmin_full.fits", "uncorrected_100GHz", -3400, 3400, r"$\mu\mathrm{K}$", "100 GHz", 1, [-3.4e3,3.4e3], [r"$-3400$", r"$3400$"], 1, 0,"100 GHz"),
            #(dipole+"dipole_CMB_n0256_100GHz.fits", "dipole_100GHz", -3.4e-3, 3.4e-3, r"$\mu\mathrm{K}$", "Dipole", 1, [-3.4e-3,3.4e-3], [r"$-3400$", r"$3400$"], 1, 0,"Dipole"),
            #(dipole+"diff_dx12_npipe.fits", "diff_dx12_npipe", -10, 10, r"$\mu\mathrm{K}$", "dx12 - dx11", 1, [-10,10], [r"$-10$", r"$10$"], 1, 0,"CMB dx12-npipe"),
            #(dipole+"quadrupole.fits", "quadrupole", 1.7e-11, 1.3e-5, r"$\mu\mathrm{K}$", "Quadrupole", 1, [1.7e-11,1.3e-5], [r"$-1.7\cdot 10^{-5}$", r"$13$"], 1, 0,"Quadrupole"),
            #!!(dipole+"map_npipe4v205_v1_100_0256_40arcmin_full_MDCORm1v2.fits", "npipe_100_MDCOR", -300, 300, r"$\mu\mathrm{K}$", "100 GHz Corrected", 1, [-300,300], [r"$-300$", r"$300$"], 1, 0,"100 GHz Corrected"),

            # npipe!

            #(npipe+version+"/chisq_c0001_n064.fits", "chisq_"+version, 0, chimax, "", r"$\chi^2$", 1, [0,chimax], [r"$0$", str(chimax)], 1, 0,""),
            #(npipe+version+"/cmb_c0001_n064.fits", "cmb_"+version, -300, 300, r"$\mu\mathrm{K}$", "CMB", 1, [-300,300], [r"$-300$", r"$300$"], 1, 0,""),
            #(npipe+version+"/diff-CMB_dx12-"+version+".fits", "diff_CMB_dx12-"+version, -10, 10, r"$\mu\mathrm{K}$", "CMB DX12-M"+str(lal), 1, [-10,10], [r"$-10$", r"$10$"], 1, 0,""),
            #(npipe+version+"/diff-CMB_npipe-"+version+".fits", "diff_CMB_npipe-"+version, -10, 10, r"$\mu\mathrm{K}$", "CMB M6-M"+str(lal), 1, [-10,10], [r"$-10$", r"$10$"], 1, 0,""),
            #("figs/npipe/"+version+"/diff-CMB_npipe-"+version+".fits", "diff_CMB_npipe-"+version, -10, 10, r"$\mu\mathrm{K}$", "CMB M6-M"+str(lal), 1, [-10,10], [r"$-10$", r"$10$"], 1, 0,""),

            # Npipe best
            #(npipe+version+"/synch_c0001_n064.fits", "synch_"+version, 0, 1e3, r"$\mu\mathrm{K}_{RJ}$", r"$A_s$", 1, [0,1000], [r"$0$", r"$1000$"], 1, 0,""), #'uK_ant'???
            #(npipe+version+"/synch_beta_c0001_n064.fits", "synch_beta_"+version, -4, -1.5, "",r"$\beta_s$", 1, [-4,-1.5], [r"$-4$", r"$-1.5$"], 1, 0,""),
            #(npipe+version+"/co-100_c0001_n064.fits", "CO-100_nobar_"+version, 0, 2., r"$\mathrm{K}_{RJ}\, \mathrm{km}/\mathrm{s}$", "CO 1-0", 1, [0,2], [r"$0$", r"$2$"], 0, 0,""),
            #(npipe+version+"/co-217_c0001_n064.fits", "CO-217_nobar_"+version, 0, 2., r"$\mathrm{K}_{RJ}\, \mathrm{km}/\mathrm{s}$", "CO 2-1", 1, [0,2], [r"$0$", r"$2$"], 0, 0,""),
            #(npipe+version+"/co-353_c0001_n064.fits", "CO-353_nobar_"+version, 0, 2., r"$\mathrm{K}_{RJ}\, \mathrm{km}/\mathrm{s}$", "CO 3-2", 1, [0,2], [r"$0$", r"$2$"], 0, 0,""),
            #(npipe+version+"/dust_c0001_n064.fits", "dust_"+version, 0, 1e3, r"$\mu\mathrm{K}_{RJ}$", r"$A_d$", 1, [0,1e3], [r"$0$", r"$1000$"], 1, 0,""),
            #(npipe+version+"/dust_beta_c0001_n064.fits", "dust_beta_"+version, 1.3, 2., "", r"$\beta_d$", 1, [1.3,2.], [r"$1.3$", r"$2.0$"], 1, 0,""),
            #(npipe+version+"/dust_Td_c0001_n064.fits", "dust_Td_"+version, 14., 30., "K", r"$T_d$", 1, [14.,30.], [r"$14$", r"$30$"], 1, 0,""),


            #(npipe+version+"/residual_"+f+"_c01_n064.fits", "npipe_residual_20_"+f, -20, 20, r"$\mu\mathrm{K}$", f, 1, [-20,20], ["-20", r"$20$"], 1, 0,""),
            #(npipe21K+"residual_"+f+"_c01_n064.fits", "npipe_residual_"+f, -5e-2, 5e-2, r"$\mathrm{MJy/sr}$", f, 1, [-5e-2,5e-2], [r"$-0.05$", r"$0.05$"], 1, 0,""),

            # SBGv8 3xCO
            #(npipe+version+"/co-100_c0001_n064.fits", "CO100", 0, 2., r"$K_{RJ} km s^{-1}$", "CO 1-0", 1, [0,2], [r"$0$", r"$2$"], 1, 0,""),
            #(npipe+version+"/co-217_c0001_n064.fits", "CO217", 0, 2., r"$K_{RJ} km s^{-1}$", "CO 2-1", 1, [0,2], [r"$0$", r"$2$"], 1, 0,""),
            #(npipe+version+"/co-353_c0001_n064.fits", "CO353", 0, 2., r"$K_{RJ} km s^{-1}$", "CO 3-2", 1, [0,2], [r"$0$", r"$2$"], 1, 0,""),

            # masks
            #(masks+"commander_dx12_mask_n0064_likelihood_v2.fits", "mask_commander", 0, 1., r"$K_{RJ} km s^{-1}$", "dx12 Likelihood mask", 1, [0,2], [r"$0$", r"$2$"], 0, 0,""),
            #(masks+"mask_chisq_15band_n064_v2_ptsrc.fits", "mask_chisq", 0, 1., r"$K_{RJ} km s^{-1}$", "Chisq mask", 1, [0,2], [r"$0$", r"$2$"], 0, 0,""),
            #(masks+"857mask.fits", "mask_dust", 0, 1., r"$K_{RJ} km s^{-1}$", "Dust mask", 1, [0,2], [r"$0$", r"$2$"], 0, 0,""),

            # Interesting residuals
            #(npipe+version+"/residual_217-7a_c01_n064.fits", "npipe_residual_217-7a_k01", -10, 10, r"$\mu\mathrm{K}$", "217-7a", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(npipe+version+"/residual_353-2_c01_n064.fits", "npipe_residual_353-2", -10, 10, r"$\mu\mathrm{K}$", "353-2", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(npipe+version+"/residual_353-8_c01_n064.fits", "npipe_residual_353-8", -10, 10, r"$\mu\mathrm{K}$", "353-8", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(npipe+version+"/residual_353-3b_c01_n064.fits", "npipe_residual_353-3b", -10, 10, r"$\mu\mathrm{K}$", "353-3b", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),

            #(npipe+version+"/residual_030_c01_n064.fits", "npipe_residual_30", -10, 10, r"$\mu\mathrm{K}$", "30", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(npipe+version+"/residual_044_c01_n064.fits", "npipe_residual_44", -10, 10, r"$\mu\mathrm{K}$", "44", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),
            #(npipe+version+"/residual_070_c01_n064.fits", "npipe_residual_70", -10, 10, r"$\mu\mathrm{K}$", "70", 1, [-10,10], ["-10", r"$10$"], 1, 0,""),

            #(npipe+version+"/dust_beta_c0001_n064.fits", "dust_beta_npipe", 1.4, 1.7, "", r"$\beta_d$", 1, [1.4,1.5,1.6,1.7], [r"$1.4$",r"$1.5$", r"$1.6$", r"$1.7$"], 1, 0,""),

            #(npipe+version+"/ff_EM_c0001_n064.fits", "ff_EM", 0, 100,r"cm$^{-6}$ pc", r"$A_{ff}$", 1, [0,100], ["0", r"$100$"], 1, 0,""),

            # Zodi
            #(npipe+version+"/zodi_map_dx11c_100_0064_40arcmin_full.fits", "zodi_template", 1, 5,r"$\mu\mathrm{K}$", r"$zodi$", 1, [1,5], ["1", r"$5$"], 1, 0,""),

            #(npipe+version+"/residual_857-1_c01_n064.fits", "npipe_residual_857-1_k01",  -5e-2, 5e-2, r"$\mathrm{MJy\,sr}^{-1}$", "857-1", 1, [-5e-2,5e-2], [r"$-10^{-2}$", r"$10^{-2}$"], 1, 0,""),

            #(rms+"rms_ii_dx12_v2_100_0064_40arcmin_full.fits", "rms",  0, 2, "", "100 GHz RMS", 1, [0,2], [r"$0$", r"$2$"], 1, 0,""),

            #(srollnpipe+"srollcmb_diff_"+nu+".fits", "srollcmb_diff_"+nu, 0, 4, r"$\mu\mathrm{K}$", nu +" GHz - CMB", 1, [0,1,3,4], [r"$0$", r"$10$", r"$10^{3}$", r"$10^{4}$"], 1, 0,""),
            #(srollnpipe+"srollnpipe_diff_"+nu+".fits", "srollnpipe_diff_"+nu, min, max, r"$\mu\mathrm{K}$", nu +" GHz DX12", 1, [min,max], [str(min), str(max)], 1, 0,""),
            #(srollnpipe+"dx11npipe_diff_"+nu+".fits", "dx11npipe_diff_"+nu, min, max, r"$\mu\mathrm{K}$", nu +" GHz DX11", 1, [min,max], [str(min), str(max)], 0, 0,""),

            #(raw+"map_npipe4v205_v1_217_0256_40arcmin_full.fits", "217GHz", -3400, 3400, r"$\mu\mathrm{K}$", "217 GHz", 1, [-3400,3400], [r"$-3400$", r"$3400$"], 1, 0,""),

            #(anom+"chisq_dx11.fits", "chidx11", 0, 18, "", r"$\chi^2$", 1, [0,18], [r"$0$", r"$18$"], 1, 0,""),
            #(anom+"dust_Td_c0001_n064.fits", "dust_Tv18", 14., 30., "K", r"$T_d$", 1, [14.,30.], [r"$14$", r"$30$"], 1, 0,""),

            #COBE
            #(cobe+"cobe_54GHz_256.fits", "cobe53GHz_256", -300, 300, r"$\mu\mathrm{K}$", "53 GHz", 1, [-250,250], [r"$-250$", r"$250$"], 1, 0,""),

            #Dame
            #(dame+"co-100_c0001_n064.fits", "CO100", 0, 2., r"$K_{RJ} km s^{-1}$", "CO 1-0", 1, [0,2], [r"$0$", r"$2$"], 1, 0,""),

            #NpipeK Residuals
            #(npipe21K+"co-100_c0001_k00500.fits", "CO100", 0, 2., r"$K_{RJ} km s^{-1}$", "CO 1-0", 1, [0,2], [r"$0$", r"$2$"], 1, 0,""),
            #(npipe21K+"co-217_c0001_k00500.fits", "CO217", 0, 2., r"$K_{RJ} km s^{-1}$", "CO 2-1", 1, [0,2], [r"$0$", r"$2$"], 1, 0,""),
            #(npipe21K+"co-353_c0001_k00500.fits", "CO353", 0, 2., r"$K_{RJ} km s^{-1}$", "CO 3-2", 1, [0,2], [r"$0$", r"$2$"], 1, 0,""),
            #(npipe21K+"residual_353-2_c01_k00500.fits", "npipe_residual_353-2", -20, 20, r"$\mu\mathrm{K}$", "353-2", 1, [-20,20], ["-20", r"$20$"], 1, 0,""),
            #(npipe21K+"residual_857-3_c01_k00500.fits", "npipe_residual_857-3",  -5e-2, 5e-2, r"$\mathrm{MJy/sr}$", "857-3", 1, [-5e-2,5e-2], [r"$-0.05$", r"$0.05$"], 1, 0,""),
            #(npipe21K+"residual_857-4_c01_k00500.fits", "npipe_residual_857-4",  -5e-2, 5e-2, r"$\mathrm{MJy/sr}$", "857-4", 1, [-5e-2,5e-2], [r"$-0.05$", r"$0.05$"], 1, 0,""),

            #(resarticle+"residual_353-2_64.fits", "dx11_residual_353-2", -20, 20, r"$\mu\mathrm{K}$", "353-2", 1, [-20,20], ["-20", r"$20$"], 1, 0,""),
            #(resarticle+"residual_857-3_64.fits", "dx11_residual_857-3",  -5e-2, 5e-2, r"$\mathrm{MJy/sr}$", "857-3", 1, [-5e-2,5e-2], [r"$-0.05$", r"$0.05$"], 1, 0,""),
            #(resarticle+"residual_857-4_64.fits", "dx11_residual_857-4",  -5e-2, 5e-2, r"$\mathrm{MJy/sr}$", "857-4", 1, [-5e-2,5e-2], [r"$-0.05$", r"$0.05$"], 1, 0,""),

            #BR
            #(br+"cmb_cl_masked.fits", "cmb_masked", -300, 300, r"$\mu\mathrm{K}$", "CMB masked", 1, [-300,300], [r"$-300$", r"$300$"], 1, 0,""),
            #(br+"cmb_Cl_c0001_k00800.fits", "cmb_cl", -300, 300, r"$\mu\mathrm{K}$", "CMB Cl", 1, [-300,300], [r"$-300$", r"$300$"], 1, 0,""),

            #Best npipe21K
            #("figs/npipe/"+version+"/chisq_c0001_k00500.fits", "chisq_"+version, 0, chimax, "", r"$\chi^2$", 1, [0,chimax], [r"$0$", str(chimax)], 1, 0,""),
            #("figs/npipe/"+version+"/cmb_c0001_k00500.fits", "cmb_"+version, -300, 300, r"$\mu\mathrm{K}$", "CMB", 1, [-300,300], [r"$-300$", r"$300$"], 1, 0,""),
            #("figs/npipe/"+version+"/diff-CMB_dx12-"+version+".fits", "diff_CMB_dx12-"+version, -10, 10, r"$\mu\mathrm{K}$", "CMB DX12-M6", 1, [-10,10], [r"$-10$", r"$10$"], 1, 0,""),

            #("figs/npipe/"+version+"/synch_c0001_k00500.fits", "synch_"+version, 0, 1e3, r"$\mu\mathrm{K}_{RJ}$", r"$A_s$", 1, [0,1000], [r"$0$", r"$1000$"], 1, 0,""), #'uK_ant'???
            #("figs/npipe/"+version+"/synch_beta_c0001_k00500.fits", "synch_beta_"+version, -4, -1.5, "",r"$\beta_s$", 1, [-4,-1.5], [r"$-4$", r"$-1.5$"], 1, 0,""),
            #("figs/npipe/"+version+"/co-100_c0001_k00500.fits", "CO-100_"+version, 0, 2., r"$\mathrm{K}_{RJ}\, \mathrm{km}/\mathrm{s}$", "CO 1-0", 1, [0,2], [r"$0$", r"$2$"], 0, 0,""),
            #("figs/npipe/"+version+"/co-217_c0001_k00500.fits", "CO-217_"+version, 0, 2., r"$\mathrm{K}_{RJ}\, \mathrm{km}/\mathrm{s}$", "CO 2-1", 1, [0,2], [r"$0$", r"$2$"], 0, 0,""),
            #("figs/npipe/"+version+"/co-353_c0001_k00500.fits", "CO-353_"+version, 0, 2., r"$\mathrm{K}_{RJ}\, \mathrm{km}/\mathrm{s}$", "CO 3-2", 1, [0,2], [r"$0$", r"$2$"], 1, 0,""),
            #("figs/npipe/"+version+"/dust_c0001_k00500.fits", "dust_"+version, 0, 1e3, r"$\mu\mathrm{K}_{RJ}$", r"$A_d$", 1, [0,1e3], [r"$0$", r"$1000$"], 1, 0,""),
            #("figs/npipe/"+version+"/dust_beta_c0001_k00500.fits", "dust_beta_"+version, 1.3, 2., "", r"$\beta_d$", 1, [1.3,2.], [r"$1.3$", r"$2.0$"], 1, 0,""),
            #("figs/npipe/"+version+"/dust_Td_c0001_k00500.fits", "dust_Td_"+version, 14., 30., "K", r"$T_d$", 1, [14.,30.], [r"$14$", r"$30$"], 1, 0,""),

            #("figs/npipe/"+version+"/residual_"+f+"_c01_k00500.fits", "npipe_residual_"+f, -10, 10, r"$\mu\mathrm{K}$", f, 1, [-10,10], [r"$-10$", r"$10$"], 1, 0,""),
            #("figs/npipe/"+version+"/residual_"+f+"_c01_k00500.fits", "npipe_residual_"+f, -5e-2, 5e-2, r"$\mathrm{MJy/sr}$", f, 1, [-5e-2,5e-2], [r"$-0.05$", r"$0.05$"], 1, 0,""),

            #GOAL
            #(dx12+"synch_64.fits", "synchdx12", 0, 1e3, r"$\mu\mathrm{K}_{RJ}$", "", 1, [0,1000], [r"$0$", r"$1000$"], 0, 0,""),
            #(dx12+"dust_64.fits", "dustdx12", 0, 1e3, r"$\mu\mathrm{K}_{RJ}$", "", 1, [0,1e3], [r"$0$", r"$1000$"], 0, 0,""),
            #("figs/npipe/npipe21J/co-100_c0001_k00500.fits", "CO", 0, 2., r"$\mathrm{K}_{RJ}\, \mathrm{km}/\mathrm{s}$", "", 1, [0,2], [r"$0$", r"$2$"], 0, 0,""),
            #(dx12+"cmb_Cl_64.fits", "cmb_cl", -300, 300, r"$\mu\mathrm{K}$", "", 1, [-300,300], [r"$-300$", r"$300$"], 0, 0,""),
            #(goal+"map_143.fits", "uncorrected_100GHz", -3000, 3000, r"$\mu\mathrm{K}$", "", 1, [-3e3,3e3], [r"$-3000$", r"$3000$"], 0, 0,""),
            #(goal+"map_143_MDCOR.fits", "npipe_100_MDCOR", -300, 300, r"$\mu\mathrm{K}$", "", 1, [-300,300], [r"$-300$", r"$300$"], 0, 0,""),

            #("figs/npipe/v7/diff-CMB_dx12-v7s_64.fits", "diff_CMB_s_dx12-"+version, -10, 10, r"$\mu\mathrm{K}$", "CMB DX12-M1", 1, [-10,10], [r"$-10$", r"$10$"], 1, 0,""),
            #("/Users/trygveleithesvalheim/Datafiles/mdata/npipe/fits/sbgv8/residual_353-3b_c01_n064.fits", "npipe_residual_353-3b", -10, 10, r"$\mu\mathrm{K}$", f, 1, [-10,10], [r"$-10$", r"$10$"], 1, 0,""),

            #pres
            #(pres+"uniform.fits", "cmb_uniform", -0, 4, r"$\mu\mathrm{K}$", "", 1, [-0,4], [r"$-0$", r"$4$"], 0, 0,""),
            #(pres+"cmb_7deg.fits", "cmb_7deg", -250, 250, r"$\mu\mathrm{K}$", "", 1, [-250,250], [r"$-250$", r"$250$"], 0, 0,""),
            #(pres+"cmb_1deg.fits", "cmb_1deg", -250, 250, r"$\mu\mathrm{K}$", "", 1, [-250,250], [r"$-250$", r"$250$"], 0, 0,""),
            #(pres+"cmb_hires.fits", "cmb_hires", -250, 250, r"$\mu\mathrm{K}$", "", 1, [-250,250], [r"$-250$", r"$250$"], 0, 0,""),

            #(pres+"map_143.fits", "map_143", -300, 300, r"$\mu\mathrm{K}$", "", 1, [-300,300], [r"$-300$", r"$300$"], 0, 0,""),
            #(goal+"map_143.fits", "uncorrected_143GHz", -3000, 3000, r"$\mu\mathrm{K}$", "", 1, [-3e3,3e3], [r"$-3000$", r"$3000$"], 0, 0,""),
            #(pres+"map_8.fits", "map_8", -300, 300, r"$\mu\mathrm{K}$", "", 1, [-300,300], [r"$-300$", r"$300$"], 0, 0,""),
            #(dx12+"chisq_64.fits", "chidx12", 0, 18, "", r"$\chi^2$", 1, [0,18], [r"$0$", r"$18$"], 1, 0,""),

            (slide3+"residual_857-3_c01_k00400_MJy.fits", "npipe_residual_857-3",  -5e-2, 5e-2, r"$\mathrm{MJy/sr}$", "857-3", 1, [-5e-2,5e-2], [r"$-0.05$", r"$0.05$"], 1, 0,""),
            (slide3+"residual_353-2_c01_k00400.fits", "npipe_residual_353-2", -20, 20, r"$\mu\mathrm{K}$", "353-2", 1, [-20,20], ["-20", r"$20$"], 1, 0,""),
            ]:

            m = hp.ma(hp.read_map(filename))*scale
            #m = N.log10(0.5*(m+N.sqrt(4.+m*m))) # Allows for linear scale around the galactic band, but logarithmic at high latitudes
            #m = N.maximum(N.minimum(m,vmax),vmin)
            nside = hp.npix2nside(len(m))

            # setup colormap
            from matplotlib.colors import ListedColormap
            colombi1_cmap = ListedColormap(np.loadtxt("parchment1.dat")/255.)

            # for mask
            #colombi1_cmap = plt.get_cmap("bone")
            #colombi1_cmap.set_bad("gray") # color of missing pixels
            #colombi1_cmap.set_under("white") # color of background, necessary if you want to use
            # this colormap directly with hp.mollview(m, cmap=colombi1_cmap)
            #colombi1_cmap="jet"

            #colombi1_cmap="jet"
            use_mask = False

            # using directly matplotlib instead of mollview has higher
            # quality output, I plan to merge this into healpy

            # ratio is always 1/2
            xsize = 2000
            ysize = int(xsize/2.)

            #unit = r"$\mathrm{\mu K}$"

            # this is the mollview min and max
            #vmin = 0; vmax = 10

            theta = np.linspace(np.pi, 0, ysize)
            phi = np.linspace(-np.pi, np.pi, xsize)
            longitude = np.radians(np.linspace(-180, 180, xsize))
            latitude = np.radians(np.linspace(-90, 90, ysize))

            # project the map to a rectangular matrix xsize x ysize
            PHI, THETA = np.meshgrid(phi, theta)
            grid_pix = hp.ang2pix(nside, THETA, PHI)

            if use_mask:
                # mask
                m.mask = np.logical_not(hp.read_map("mask_T0.941_P10uK_v3_survey.fits",1))
                grid_mask = m.mask[grid_pix]
                grid_map = np.ma.MaskedArray(m[grid_pix], grid_mask)
            else:
                grid_map = m[grid_pix]

            from matplotlib.projections.geo import GeoAxes

            class ThetaFormatterShiftPi(GeoAxes.ThetaFormatter):
                """Shifts labelling by pi

                Shifts labelling from -180,180 to 0-360"""
                def __call__(self, x, pos=None):
                    if x != 0:
                        x *= -1
                    if x < 0:
                        x += 2*np.pi
                    return GeoAxes.ThetaFormatter.__call__(self, x, pos)

            #for cmap, colormaptag in [(None, ''), (colombi1_cmap, "colombi1_")]:
            cmap = colombi1_cmap
            colormaptag = "colombi1_"

            fig = plt.figure(figsize=(cm2inch(width), cm2inch(width/2.)))
            # matplotlib is doing the mollveide projection


            #ax = fig.add_subplot(figure_rows, figure_columns, lol, projection='mollweide')
            lol+=1
            ax = fig.add_subplot(111,projection='mollweide')

            # remove white space around the image
            #plt.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.01)

            # rasterized makes the map bitmap while the labels remain vectorial
            # flip longitude to the astro convention
            image = plt.pcolormesh(longitude[::-1], latitude, grid_map, vmin=vmin, vmax=vmax, rasterized=True, cmap=cmap)

            # graticule
            ax.set_longitude_grid(60)
            ax.xaxis.set_major_formatter(ThetaFormatterShiftPi(60))
            if width < 10:
                ax.set_latitude_grid(45)
                ax.set_longitude_grid_ends(90)


            if colorbar == 1:
                 # colorbar
                #cb = fig.colorbar(image, orientation='horizontal', shrink=.4, pad=0.08, ticks=ticks)
                cb = fig.colorbar(image, orientation='horizontal', shrink=.3, pad=0.08, ticks=ticks)
                cb.ax.set_xticklabels(ticklabels)
                cb.ax.xaxis.set_label_text(unit)
                cb.ax.tick_params(axis='x', direction='in')
                cb.ax.xaxis.labelpad = -11 #4
                # workaround for issue with viewers, see colorbar docstring
                cb.solids.set_edgecolor("face")

            #ax.tick_params(axis='x', labelsize=10)
            #ax.tick_params(axis='y', labelsize=10)

            # remove longitude tick labels
            ax.xaxis.set_ticklabels([])
            # remove horizontal grid
            ax.xaxis.set_ticks([])
            ax.yaxis.set_ticklabels([])
            ax.yaxis.set_ticks([])

            if title:
                plt.title(titletext)

            plt.grid(True)
            if width > 12.:
                plt.text(6.,  1.3, r"%s" % freq, ha='center', va='center', fontsize=8)
            elif width == 12.:
                plt.text(6.,  1.3, r"%s" % freq, ha='center', va='center', fontsize=7)
            else:
                plt.text(6.,  1.3, r"%s" % freq, ha='center', va='center', fontsize=6)
            #plt.text(5., -1.2, r"%s" % yr, ha='center', va='center')

            plt.tight_layout()
            plt.savefig("figs/slide3/"+outfile+"_w"+str(width)+".png", bbox_inches='tight',  pad_inches=0.02)

        #plt.draw()
        #plt.show()
