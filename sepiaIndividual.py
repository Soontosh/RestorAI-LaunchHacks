import numpy as np
import random
import cv2
import os

"""
################## FIX NOISISIOSIEI FIX NOISE MONKEY
##################
##################
################## ADD RANDOM POSITIONING AND ROTATION!
################## REMOVE THE THINGYGGYGYGYGYGG THE OCNVEOUTHRUAHGU THIEHFUE
################## REMOVE THE AOUTOMATIC LIGHT THING!!!!!!!!!!!!!!!!!!!!!!!!!!! 
##################THE THING THE LIGHT FLAR 
"""



#create random effect
#80% sepia 20% black and white

#vignette if grey range(2)

#add random noise with skimage with a 15% chance no
#add gausian filtering(only up to 10%)
#add film grain overlays files
#lower contrast
#vignette filter no
#automated files(before and after folders, bulk images)
#scractches and dust overlay no
#add grunge files
#light leak overlays files
def convert2Sepia(img):
    if(len(img.shape) > 2): 
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        return img
    normalized_gray = np.array(grey, np.float32)/255


    sepia = np.ones(img.shape)
    sepia[:,:,0] *= 153 #B
    sepia[:,:,1] *= 204 #G
    sepia[:,:,2] *= 255 #R
    
    sepia[:,:,0] *= normalized_gray
    sepia[:,:,1] *= normalized_gray
    sepia[:,:,2] *= normalized_gray
    return np.array(sepia, np.uint8)
    
def covert2BlackAndWhite(img):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return grey

def dust(image, isGrey, density=0.01, isPaper=False, alpha = 0.5):
    emptyArray = np.empty_like(image)

    if isGrey:
        noiseShape = (image.shape[0], image.shape[1]) 
    else:
        noiseShape = image.shape

    noise = np.empty(noiseShape, dtype=np.uint8)
    noise  = cv2.randn(noise, (0), (20))

    image = cv2.addWeighted(image, 1-alpha, noise, alpha, 30)

    return image

def deSaturate(image, saturatonAmount, isGrey):
    if not isGrey: image[:, :, 1] = np.clip(image[:, :, 1] * saturatonAmount, 0, 255)
    return image

def getRandomFile(folderPath):
    files = [file for file in os.listdir(folderPath)]
    finalFile = folderPath + "/" + random.choice(files)
    print(finalFile)
    return finalFile

def splitImg(image):
    splitDirection = random.randint(0, 1) #0 means rigt, 1 means left

    height, width = image.shape[:2]

    if splitDirection == 0:
        print("splitDirecton: " + str(width // 2) + " : " + str(width - width // 2))
        try:
            pointOfSplit = random.randint(width // 2, width - width // 2)
        except:
            pointOfSplit = 60
        image = image[:, :pointOfSplit]
    else:
        print("splitDirecton: " + str(width - width) + " : " + str(width // 2))
        try:
            pointOfSplit = random.randint(width - width // 2, width // 2)
        except:
            pointOfSplit = 60
        image = image[:, :pointOfSplit]
    
    return image

def convertVignette(image, isGrey):
    rows, cols = image.shape[:2]
    xKernel = cv2.getGaussianKernel(cols, 200)
    yKernel = cv2.getGaussianKernel(rows, 200)

    finalKernel = yKernel * xKernel.T
    vigMask = 255 * finalKernel / np.linalg.norm(finalKernel)
    output = np.copy(image)
    if not isGrey:
        for i in range(3):
            output[:,:,i] = output[:,:,i] * vigMask
    else:
        for i in range(2):
            output[:,:,i] = output[:,:,i] * vigMask
    
    return output

def rotateImage(image, angleDiff):
    height, width = image.shape[:2]
    center = (width/2, height/2)

    lowerAngle = random.randint(-45, 45)
    
    upperAngle = lowerAngle + angleDiff

    rMatrix = cv2.getRotationMatrix2D(center=center, angle=random.randint(lowerAngle, upperAngle), scale=2)
    image = cv2.warpAffine(src=image, M=rMatrix, dsize=(width, height))

    return image

def translateImage(image, percentLower, percentUpper, imgParent):
    height, width = imgParent.shape[:2]

    tPercent = random.randint(percentLower, percentUpper) * 0.01
    tx, ty = width * tPercent, height * tPercent

    transMatrix = np.array([
        [1, 0, tx],
        [0, 1, ty]
    ], dtype=np.float32)

    image = cv2.warpAffine(src = image, M=transMatrix, dsize=(image.shape[0], image.shape[1]))

    return image

def greenTintCheck(img):
    hsvImg = cv2.cvtColor(img, cv2.Color_BGR2HSV)

    channel1, channel2, channel3 = cv2.split(hsvImg)
    averageHue = np.mean(channel1)
    averageSaturation = np.mean(channel2)
    averageValue = np.mean(channel3)

    minTint = 100

    if averageHue > averageValue + minTint and averageHue > averageSaturation + minTint:
        return False
    else:
        return True





def convertImg(filePath, outputName):
    print("File Path: " + filePath)
    sepiaProbability = random.randint(1, 10)
    noiseProbability = random.randint(1, 10)
    desaturationProbability = random.randint(1, 10)
    gaussianProbability = random.randint(1, 100)
    vignetteProbability = random.randint(1, 100)
    lightFlareProbability = random.randint(1, 100)

    noise = True
    desaturateBool = False
    paper = False
    gaussian = False
    vignette = False
    filmGrain = False
    grungeBool = False
    lightFlareBool = False

    if random.randint(1, 100) > 20: #20
        paper = True

    if random.randint(1, 100) > 0: #50
        filmGrain = True

    if random.randint(1, 100) > 0: #50
        grungeBool = True

    if noiseProbability > 9: noise = True
    if desaturationProbability > 6: desaturateBool = True
    if gaussianProbability > 65: gaussian = True
    if vignetteProbability > 50: vignette = True
    if lightFlareProbability > 75: lightFlareBool = True #80

    #START PROCESSING
    #START PROCESSING
    #START PROCESSING
    #START PROCESSING
    #START PROCESSING
    #START PROCESSING
    #START PROCESSING
    image = cv2.imread(filePath)


    '''
    if True:
        print("Converting To Vignette")
        image4 = convertVignette(image, False)
    '''



    if gaussian:
        kernel = random.randint(1, 2)
        if kernel % 2 == 0: kernel += 1
        print("Gaussian, kernal: " + str(kernel))
        image = cv2.GaussianBlur(image, (kernel, kernel), 0)

    print(image.shape)

    if sepiaProbability > 8:
        image2 = covert2BlackAndWhite(image)
        isGrey = True
    else:
        image2 = convert2Sepia(image)
        isGrey = False
    print("Is Grey: " + str(isGrey))
        
    image3 = image2 
    if noise:
        density = random.randint(1, 10) * 0.01
        print("Density: " + str(density))
        image3 = dust(image3, isGrey)

    image4 = image3
    if desaturateBool:
        desaturateAmount = random.randint(85, 95) * 0.01
        print("desaturateAmount: " + str(desaturateAmount))
        image4 = deSaturate(image4, desaturateAmount, isGrey)

    #FROM HERE START RANDOMIZATION
    #ROTATION IS A 40% CHANCE
    #20% TRANSLATION MAX 60% CHANCE
    for i in range(2):
        if paper:
            randomFile = getRandomFile("paper")
            paperOverlay = cv2.imread(randomFile)
            if random.randint(1, 10) > 5: paperOverlay = splitImg(paperOverlay)
            paperOverlay = cv2.resize(paperOverlay, (image.shape[1], image.shape[0])) #40% chance, Add noise after overlay is done, also add desaturation and test where you should blend
            blendAmount = random.randint(30, 35) * 0.01
            print("Blend Amount: " + str(blendAmount))
            #additionalLayers = [(image, folder)]
            if paperOverlay.shape[0] == 0 or paperOverlay.shape[1] == 0:
                print("paper overlay has lost")

        if isGrey and paper: paperOverlay = cv2.cvtColor(paperOverlay, cv2.COLOR_BGR2GRAY)

        if paper and random.randint(1, 10) > 7:
            pass
            #paperOverlay = dust(paperOverlay, isGrey, isPaper=True)

        if paper and random.randint(1, 10) > 5:
            desaturateAmount = random.randint(85, 95) * 0.01
            paperOverlay = deSaturate(paperOverlay, desaturateAmount, isGrey)

        if paper and random.randint(1, 10) > 3: paperOverlay = convert2Sepia(paperOverlay)

        if paper: 
            print("Shape: " + str(paperOverlay.shape))
            paperOverlay = cv2.resize(paperOverlay, (image4.shape[1], image4.shape[0]))
            try:
                if isGrey: paperOverlay = cv2.cvtColor(paperOverlay, cv2.COLOR_BGR2GRAY)
            except:
                pass
            print("Paper Overlay Size: " + str(paperOverlay.shape))
            print("Image Size: " + str(image4.shape))

            if isGrey: image4 = cv2.cvtColor(image4, cv2.COLOR_GRAY2BGR)

            paperOverlay = paperOverlay.astype(image4.dtype)
            
            image4 = cv2.addWeighted(image4, 1 - (blendAmount), paperOverlay, blendAmount, 0)

    if filmGrain: 
        randomFile = getRandomFile("filmgrain")
        grainOverlay = cv2.imread(randomFile)
        #if random.randint(1, 10) > 5: grainOverlay = splitImg(grainOverlay)
        print("Shape: " + str(grainOverlay.shape))
        grainOverlay = cv2.resize(grainOverlay, (image.shape[1], image.shape[0])) #40% chance, Add noise after overlay is done, also add desaturation and test where you should blend
        blendAmount = random.randint(20, 25) * 0.01
        print("Film Grain Blend Amount: " + str(blendAmount))
        #additionalLayers = [(image, folder)]
        if grainOverlay.shape[0] == 0 or grainOverlay.shape[1] == 0:
            print("grainOverlay overlay has lost")

    if filmGrain and random.randint(1, 10) > 7:
        pass
        #filmgrain = dust(filmgrain, isGrey, isPaper=True)

    if filmGrain and random.randint(1, 10) > 5:
        desaturateAmount = random.randint(85, 95) * 0.01
        filmgrain = deSaturate(grainOverlay, desaturateAmount, isGrey)

    if filmGrain and random.randint(1, 10) > 3: 
        grainOverlay = convert2Sepia(grainOverlay)

    if filmGrain: 
        print("Shape: " + str(grainOverlay.shape))
        grainOverlay = cv2.resize(grainOverlay, (image4.shape[1], image4.shape[0]))
        grainOverlay = rotateImage(grainOverlay, 50)
        #grainOverlay = translateImage(grainOverlay, 5, 25, image4)
        #grainOverlay = cv2.resize(grainOverlay, (image4.shape[1], image4.shape[0]))
        print("filmGrain Overlay Size: " + str(grainOverlay.shape))
        print("Image Size: " + str(image4.shape))

        if isGrey: image4 = cv2.cvtColor(image4, cv2.COLOR_GRAY2BGR)

        image4 = cv2.addWeighted(image4, 1 - (blendAmount), grainOverlay, blendAmount, 0)

    if grungeBool: 
        randomFile = getRandomFile("grunges")
        grungeOverlay = cv2.imread(randomFile)
        #if random.randint(1, 10) > 5: grungeOverlay = splitImg(grungeOverlay)
        print("Shape: " + str(grungeOverlay.shape))
        grungeOverlay = cv2.resize(grungeOverlay, (image4.shape[1], image4.shape[0])) #40% chance, Add noise after overlay is done, also add desaturation and test where you should blend
        blendAmount = random.randint(1, 10) * 0.01
        print("grunge Blend Amount: " + str(blendAmount))
        #additionalLayers = [(image, folder)]
        if grungeOverlay.shape[0] == 0 or grungeOverlay.shape[1] == 0:
            print("grungeOverlay overlay has lost")

    if grungeBool and random.randint(1, 10) > 7:
        pass
        #grunge = dust(grunge, isGrey, isPaper=True)

    if grungeBool: 
        print("Shape: " + str(grungeOverlay.shape))
        grungeOverlay = cv2.resize(grungeOverlay, (image4.shape[1], image4.shape[0]))
        grungeOverlay = rotateImage(grungeOverlay, 50)
        #grungeOverlay = translateImage(grungeOverlay, 5, 25, image4)
        #grungeOverlay = cv2.resize(grungeOverlay, (image4.shape[1], image4.shape[0]))
        print("grunge Overlay Size: " + str(grungeOverlay.shape))
        print("Grunge Image Size: " + str(image4.shape))
        try:
            if isGrey: image4 = cv2.cvtColor(image4, cv2.COLOR_GRAY2BGR)
        except:
            pass

        image4 = cv2.addWeighted(image4, 1 - (blendAmount), grungeOverlay, blendAmount, 0)     
    #start lightFlare
    if lightFlareBool:
        print(" LIGHT FLARE BOOL LIGHT FLARE BOOL")
        if True:
            if lightFlareBool: 
                randomFile = getRandomFile("lightFlare")
                flareOverlay = cv2.imread(randomFile)
                #if random.randint(1, 10) > 5: flareOverlay = splitImg(flareOverlay)
                print("Shape: " + str(flareOverlay.shape))
                flareOverlay = cv2.resize(flareOverlay, (image4.shape[1], image4.shape[0])) #40% chance, Add noise after overlay is done, also add desaturation and test where you should blend
                blendAmount = random.randint(20, 25) * 0.01
                print("grunge Blend Amount: " + str(blendAmount))
                #additionalLayers = [(image, folder)]
                if flareOverlay.shape[0] == 0 or flareOverlay.shape[1] == 0:
                    print("flareOverlay overlay has lost")

            if lightFlareBool and random.randint(1, 10) > 7:
                pass
                #grunge = dust(grunge, isGrey, isPaper=True)

            if lightFlareBool: 
                print("Shape: " + str(flareOverlay.shape))
                flareOverlay = cv2.resize(flareOverlay, (image4.shape[1], image4.shape[0]))
                flareOverlay = rotateImage(flareOverlay, 50)
                #flareOverlay = translateImage(flareOverlay, 5, 25, image4)
                flareOverlay = cv2.resize(flareOverlay, (image4.shape[1], image4.shape[0]))
                print("grunge Overlay Size: " + str(flareOverlay.shape))
                print("Image Size: " + str(image4.shape))
                try:
                    if isGrey: image4 = cv2.cvtColor(image4, cv2.COLOR_GRAY2BGR)
                except:
                    pass

                image4 = cv2.addWeighted(image4, 1 - (blendAmount), flareOverlay, blendAmount, 0)
    
    print("Output Name: " + outputName + ".jpg")
    cv2.imwrite(outputName, image4)

