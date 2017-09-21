import sys
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cv2
import skimage
from skimage import io
import skimage.data
import selectivesearch
import gtcfeat as gtc
import numpy as np
from sklearn.svm import SVC


#code start 
# loading astronaut image
sk_img = None
cv_img = None

if len(sys.argv) > 1 :
    fname = sys.argv[1]
    sk_img = io.imread(fname)
    cv_img = cv2.imread(fname, cv2.IMREAD_COLOR)
else :
    print('Failed to load images')
    #exit(-1)
    images = os.listdir('/home/hyeon/gtc/data/true')
    """sk_img = []
    cv_img = []
    for itr in images:
        sk_img.append(io.imread('/home/hyeon/gtc/data/true/' + itr))
        cv_img.append(cv2.imread('/home/hyeon/gtc/data/true/' + itr, cv2.IMREAD_COLOR))"""
    sk_img = io.imread('/home/hyeon/gtc/data/false/12.jpg')
    cv_img = cv2.imread('/home/hyeon/gtc/data/false/12.jpg', cv2.IMREAD_COLOR)

def extractFeature(img):
    return gtc.getFeat(img, algorithm = 'histogram')

def loadDBFromPath(path, classnum):
    db = []
    for file in os.listdir(path):
        if not file.upper().endswith('.JPG') :
            continue
        data = {}
        data['class'] = classnum
        img = cv2.imread(path + '/' + file, cv2.IMREAD_COLOR)
        data['feat'] = extractFeature(img)
        db.append(data)
    return db
"""
def transformForSVM(data, labels):
    train = []
    cnt_row = 0
    for row in trainset:
        train.append([labels[cnt_row]])'/home/hye ...,on/gtc/data/true' + 
        for col in trainset[cnt_row]:
            train[cnt_row].append(col)
        cnt_row += 1true

    return train
"""

positivePath = os.getcwd() + '/data/true'  
negativePath = os.getcwd() + '/data/false'
negativeBGPath = negativePath + '/bg'

db = []
db += loadDBFromPath(positivePath, 1)
db += loadDBFromPath(negativePath, -1)
db += loadDBFromPath(negativeBGPath, -1)


# perform selective search (selective search from https://github.com/AlpacaDB/selectivesearch)
img_lbl, regions = selectivesearch.selective_search(sk_img, scale=500, sigma=0.9, min_size=20)

candidates = set()
for r in regions:
    # excluding same rectangle (with different segments)
    if r['rect'] in candidates:
        continue

    # distorted rects
    x, y, w, h = r['rect']

    if w < 10 or h < 10 or w > 100 or h > 100 or w / h > 2 or h / w > 2:
        continue
    
    candidates.add(r['rect'])

# draw rectangles on the original image
fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
ax.imshow(sk_img)

fileList = os.listdir(os.getcwd())
trainset = np.float32([data['feat'] for data in db])
classes = np.array([data['class'] for data in db])

print (trainset)
print (classes)

clf = SVC()

#svm in opencvcv_img = cv2.imread('/home/hyeon/gtc/data/false/0.jpg', cv2.IMREAD_COLOR)
"""svm = cv2.ml.SVM_create()
svm.setType(cv2.ml.SVM_C_SVC)
svm.setKernel(cv2.ml.SVM_LINEAR)
svm.setC(2.67)
svm.setGamma(5.383)
svm.setTermCriteria((cv2.TERM_CRITERIA_COUNT, 100, 1.e-06))"""
#Check that train data is in 'cwd'
dataChk = 0
for item in fileList:
    if item.find('svm_data.dat') is not -1:
        pass
        #dataChk = false
        #cv2.ml.SVM_load('svm_data.dat')

#No data in 'cwd'
if dataChk == 0:
    clf.fit(trainset, classes)
    #svm.train(trainset, cv2.ml.ROW_SAMPLE, classes)
    #svm.save('svm_data.dat')

#Blue for true barcod[ye, Red for false barcode

##cv_img = cv2.imread('/home/hyeon/gtc/data/false/0.jpg', cv2.IMREAD_COLOR)


for x, y, w, h in candidates:
    x1 = x 
    x2 = x + w - 1
    y1 = y 
    y2 = y + h - 1 
    cropped = cv_img[y1:y2, x1:x2]
    feat = extractFeature(cropped)
    feat = [feat]
    np.reshape(feat, (-1, 1))
    pred = clf.predict(feat)
    #pred = svm.predict(samples)
    
    if pred[0] == 1:
        ec = 'blue'
        lw = 3
    else:
        ec = 'red'
        lw = 1
    
    rect = mpatches.Rectangle(
        (x, y), w, h, fill=False, edgecolor=ec, linewidth=lw)
    
    ax.add_patch(rect)
plt.show()