import os

class teacherDataset(object):
    def __init__(self, root, time_step, transforms=None):
        self.root = root
        self.transforms = transforms
        self.time_slice = sorted(os.listdir(root))[:-1]
        assert (len(self.time_slice) > time_step) & (time_step > 0)
        
        img_root = os.path.join(self.root, self.time_slice[time_step])
        img_names = sorted(os.listdir(img_root))
        self.imgs = [os.path.join(img_root, img_name) for img_name in img_names]
        
    def __getitem__(self, idx):
        img_path = self.imgs[idx]
        img = np.array(Image.open(img_path).convert("RGB"))
        target = {}
        
        if self.transforms is not None:
            img, _ = self.transforms(img, target)
            
        return img, target
    
    def __len__(self):
        return len(self.imgs)