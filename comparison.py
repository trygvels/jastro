import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt
# THIS DOES NOT WORK!
# DIFFERENT COLOR-BARS!

images = ["ame1_c0001_k00001.png",
          "ame1_nup_c0001_k00001.png",
          "ame2_c0001_k00001.png",
          "ame2_nup_c0001_k00001.png",
          "chisq_k00001.png",
          "cmb_c0001_k00001.png",
          "co10_c0001_k00001.png",
          "co21_c0001_k00001.png",
          "co32_c0001_k00001.png",
          "dust_Td_c0001_k00001.png",
          "dust_beta_c0001_k00001.png",
          "dust_c0001_k00001.png",
          "ff_EM_c0001_k00001.png",
          "ff_T_e_c0001_k00001.png",
          "hcn_c0001_k00001.png",
          "residual_030_c01_k00001.png",
          "residual_044_c01_k00001.png",
          "residual_070-18_23_c01_k00001.png",
          "residual_070-19_22_c01_k00001.png",
          "residual_070-20_21_c01_k00001.png",
          "residual_100-ds1_c01_k00001.png",
          "residual_100-ds2_c01_k00001.png",
          "residual_143-5_c01_k00001.png",
          "residual_143-6_c01_k00001.png",
          "residual_143-7_c01_k00001.png",
            "residual_143-ds1_c01_k00001.png",
            "residual_143-ds2_c01_k00001.png",
            "residual_217-1_c01_k00001.png",
            "residual_217-2_c01_k00001.png",
            "residual_217-3_c01_k00001.png",
            "residual_217-4_c01_k00001.png",
            "residual_353-1_c01_k00001.png",
            "residual_353-ds2_c01_k00001.png",
            "residual_545-2_c01_k00001.png",
            "residual_545-4_c01_k00001.png",
            "residual_857-2_c01_k00001.png",
            "residual_Haslam_c01_k00001.png",
            "residual_WMAP_K_c01_k00001.png",
            "residual_WMAP_Ka_c01_k00001.png",
            "residual_WMAP_Q1_c01_k00001.png",
            "residual_WMAP_Q2_c01_k00001.png",
            "residual_WMAP_V1_c01_k00001.png",
            "residual_WMAP_V2_c01_k00001.png",
            "residual_WMAP_W1_c01_k00001.png",
            "residual_WMAP_W2_c01_k00001.png",
            "residual_WMAP_W3_c01_k00001.png",
            "residual_WMAP_W4_c01_k00001.png",
            "synch_c0001_k00001.png",
            "synch_nup_c0001_k00001.png",
            "sz_c0001_k00001.png"]
images1 = ["chisq_k00001.png",
            "cmb_c0001_k00001.png",
            "residual_030_c01_k00001.png",
            "residual_044_c01_k00001.png",
            "residual_070_c01_k00001.png",
            "residual_100_c01_k00001.png",
            "residual_143_c01_k00001.png",
            "residual_217_c01_k00001.png",
            "residual_353_c01_k00001.png",
            "residual_545_c01_k00001.png",
            "residual_857_c01_k00001.png",
            "co_c0001_k00001.png",
            "dust_Td_c0001_k00001.png",
            "dust_beta_c0001_k00001.png",
            "dust_c0001_k00001.png",
            "synch_beta_c0001_k00001.png",
            "synch_c0001_k00001.png"]

images2 = ["chisq_k00050.png",
            "cmb_c0001_k00050.png",
            "cmb_cl_c0001_k00050.png",
            "residual_030_c01_k00050.png",
            "residual_044_c01_k00050.png",
            "residual_070_c01_k00050.png",
            "residual_100_c01_k00050.png",
            "residual_143_c01_k00050.png",
            "residual_217_c01_k00050.png",
            "residual_353_c01_k00050.png",
            "residual_545_c01_k00050.png",
            "residual_857_c01_k00050.png",
            "co_c0001_k00050.png",
            "dust_Td_c0001_k00050.png",
            "dust_beta_c0001_k00050.png",
            "dust_c0001_k00050.png",
            "synch_beta_c0001_k00050.png",
            "synch_c0001_k00050.png"]

diffs = ["diff_chisq.png",
        "diff_cmb.png",
        "diff_cmb_cl.png",
        "diff_res_030.png",
        "diff_res_044.png",
        "diff_res_070.png",
        "diff_res_100.png",
        "diff_res_143.png",
        "diff_res_217.png",
        "diff_res_353.png",
        "diff_res_545.png",
        "diff_res_857.png",
        "diff_co.png",
        "diff_dust_Td.png",
        "diff_dust_beta.png",
        "diff_dust.png",
        "diff_synch_beta.png",
        "diff_synch.png"]

path1 = "/Users/trygveleithesvalheim/Documents/skole/master/data/dx12_cl_v2/"
path2 = "/Users/trygveleithesvalheim/Documents/skole/master/data/dx11_cl_v2/"

path3 = "/Users/trygveleithesvalheim/Documents/skole/master/data/diff_dx11-12_50_v2/"

i = 0

lol = raw_input("<For gibbs iteration 1 press x, else 50>")
if lol=="x":
    cl12=np.loadtxt(path1+'cl_c0001_k00001.dat')
    cl11=np.loadtxt(path2+'cl_c0001_k00001.dat')
    plt.title("Power spectrum, ITER 1")
else:
    cl12=np.loadtxt(path1+'cl_c0001_k00050.dat')
    cl11=np.loadtxt(path2+'cl_c0001_k00050.dat')
    plt.title("Power spectrum, ITER 30")

l = cl11[:1022,0]
dx11 = cl11[:1022,1]
dx12 = cl11[:1022,1]
plt.plot(l,dx11,label="dx11")                      #l*(l+1)
plt.plot(l,dx12, ":", label="dx12")                #l*(l+1)
plt.plot(l,(dx11-dx12),label="diff")      #l*(l+1)
plt.xlabel("l")
plt.ylabel("Cl")
plt.legend()
plt.draw()
plt.pause(1) # <-------
a = raw_input("<Enter to continue>")
plt.close()

while i<len(images1)+1:

    image = str(images2[i])
    image2 = str(images2[i])

    # If we want to look at GIBBSITER 1
    if lol == "x":
        path3 = "/Users/trygveleithesvalheim/Documents/skole/master/data/diff_dx11-12_01_v2/"
        image = str(images1[i])
        image2 = str(images1[i])


    img1 = img.imread(path1+image)
    img2 = img.imread(path2+image2)
    arr1 = np.array(img1)
    arr2 = np.array(img2)

    diff = abs(arr1[:505][:]-arr2[:505][:])

    print image
    print "Mean difference", np.mean(diff)

    fig = plt.figure(figsize=(5, 8), dpi=100)

    plt.subplot(311)
    if lol=="x":
        plt.title(image+" ITER 1")
    else:
        plt.title(image+" ITER 50")

    plt.imshow(arr1)
    plt.xlabel("dx12")
    plt.xticks([])
    plt.yticks([])

    plt.subplot(312)
    plt.imshow(arr2)
    plt.xlabel("dx11")
    plt.xticks([])
    plt.yticks([])

    image = str(diffs[i])
    diff = img.imread(path3+image)
    diff = np.array(diff)

    plt.subplot(313)
    plt.imshow(diff)
    plt.xlabel("Diff, mean:" + str(np.mean(diff)))
    plt.xticks([])
    plt.yticks([])

    plt.tight_layout()

    plt.draw()
    plt.pause(1) # <-------
    a = raw_input("<Enter to Continue - p for Previous or q to Quit>")
    plt.close()

    if a == "p":
        i -= 1
    elif a == "q":
        break
    elif a=="-":
        i+= 5
    elif a==".":
        i-=5
    else:
        i+=1
