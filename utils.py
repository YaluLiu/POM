import torchvision
from torchvision import transforms
import PIL
import numpy as np

'''
import png

def read_png_3(png_name):
    flow_direct = png.Reader(filename=png_name).asDirect()
    #print(flow_direct)
    flow_data = list(flow_direct[2])
    (w, h) = flow_direct[3]['size']
    flow = np.zeros((w, h, 3), dtype=np.float64)
    #print("images_w:",w,":image_h:",h,"len_flow_data:",len(flow_data))
    for i in range(len(flow_data)):
        flow[:, i, 0] = flow_data[i][0::3]
        flow[:, i, 1] = flow_data[i][1::3]
        flow[:, i, 2] = flow_data[i][2::3]

    return flow 
    
def read_png_1(png_name):
    flow_direct = png.Reader(filename=png_name).asDirect()
    #print(flow_direct)
    flow_data = list(flow_direct[2])
    (w, h) = flow_direct[3]['size']
    flow = np.zeros((w, h, 3), dtype=np.float64)
    #print("images_w:",w,":image_h:",h,"len_flow_data:",len(flow_data))
    for i in range(len(flow_data)):
        flow[:, i, 0] = flow_data[i]
        flow[:, i, 1] = flow_data[i]
        flow[:, i, 2] = flow_data[i]

    return flow
'''

def tensor_to_PIL(tensor):
    image = tensor.cpu().clone()
    image = image.squeeze(0)
    unloader = transforms.ToPILImage(mode='L')
    image = unloader(image)
    return image
    
def genBackground_one(seg_model, img_path, score_thresh = 0.9, binary_thresh = 0.5, cuda=True, use_student = False):
    
    img_PIL = PIL.Image.open(img_path).convert("RGB")
    if cuda:
        img_tensor = [torchvision.transforms.functional.to_tensor(img_PIL).cuda()]
    else:
        img_tensor = [torchvision.transforms.functional.to_tensor(img_PIL).cuda()]
    
    if(use_student):
        img_tensor = img_tensor[0].reshape(1,3,720,1280)
        image = seg_model.forward(img_tensor)
        image_PIL = image[0].cpu().detach().numpy()[0]
    else:
        output = seg_model(img_tensor)[0]
        cond_person = output["labels"].cpu().detach().numpy() == 1
        cond_conf = output["scores"].cpu().detach().numpy() > score_thresh
        idx = cond_person & cond_conf
        B = output["masks"][idx]
        image = None
        for img in B:
            image = img if image is None else img+image
        
        for i in range(image.size()[1]):
            for j in range(image.size()[2]):
                if(image[0][i][j] > 1):
                    image[0][i][j] = 1

        image_PIL = tensor_to_PIL(image)

    np_data = np.transpose(np.asarray(image_PIL))
    ret_data = np.zeros((np_data.shape[0], np_data.shape[1], 3), dtype=np.uint8)
    ret_data[:,:,0] = np_data
    ret_data[:,:,1] = np_data
    ret_data[:,:,2] = np_data
                    

    #print("IMAGE_NDARRAY:",np_data.shape,np_data.dtype)
    #image_PIL.save("1.jpg")
    return ret_data
