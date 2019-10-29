import torch.nn as nn
import torch
import torch.nn.functional as F

class TinyNet(nn.Module):
    
    def __init__(self, device, num_classes):
        super(TinyNet,self).__init__()
        
        self.device = device

        self.num_classes = num_classes


        # Definition of subNet1 parameters
        self.conv1_1 = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=(3,3),stride=(2,2), padding=(1,1))
        self.batch1_1 = nn.BatchNorm2d(num_features=64, track_running_stats=False)

        self.conv1_2 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3,3),stride=(1,1), padding=(1,1))
        self.batch1_2 = nn.BatchNorm2d(num_features=64, track_running_stats=False)
        self.MaxPool1_2 = nn.MaxPool2d(kernel_size=(2,2), stride=(2,2))

        self.conv1_3 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3,3),stride=(1,1), padding=(1,1))
        self.batch1_3 = nn.BatchNorm2d(num_features=64, track_running_stats=False)
        self.MaxPool1_3 = nn.MaxPool2d(kernel_size=(2,2), stride=(2,2))


        # Definition of subNet2 parameters
        self.conv2_1 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3,3),stride=(1,1), padding=(1,1))
        self.batch2_1 = nn.BatchNorm2d(num_features=64, track_running_stats=False)

        self.conv2_2 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(9,9),stride=(1,1), padding=(4,4))
        self.batch2_2 = nn.BatchNorm2d(num_features=64, track_running_stats=False)

        self.conv2_3 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3,3),stride=(1,1), padding=(1,1))
        self.batch2_3 = nn.BatchNorm2d(num_features=64, track_running_stats=False)


        # Definition of subNet3 parameters
        self.conv3_1 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3,3),stride=(1,1), padding=(1,1))
        self.batch3_1 = nn.BatchNorm2d(num_features=64, track_running_stats=False)


        # # Definition of the pyramid parameters
        # self.pyr_AveragePool1 = nn.AvgPool2d(kernel_size=(135,240), stride=(135,240))
        # self.pyr_upsample1 = nn.Upsample(scale_factor=(135.0,240.0))

        # self.pyr_AveragePool2 = nn.AvgPool2d(kernel_size=(45,120), stride=(45,120))
        # self.pyr_conv2 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3,3),stride=(1,1), padding=(1,1))
        # self.pyr_upsample2 = nn.Upsample(scale_factor=(45.0,120.0))

        # self.pyr_AveragePool3 = nn.AvgPool2d(kernel_size=(27,80), stride=(27,80))
        # self.pyr_conv3 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3,3),stride=(1,1), padding=(1,1)) 
        # self.pyr_upsample3 = nn.Upsample(scale_factor=(27.0,80.0))

        # self.pyr_AveragePool4 = nn.AvgPool2d(kernel_size=(15,30), stride=(15,30))
        # self.pyr_conv4 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3,3),stride=(1,1), padding=(1,1))  
        # self.pyr_upsample4 = nn.Upsample(scale_factor=(15.0,30.0))

        self.pyr_AveragePool1 = nn.AvgPool2d(kernel_size=(90,160), stride=(90,160))
        self.pyr_upsample1 = nn.Upsample(scale_factor=(90.0,160.0))

        self.pyr_AveragePool2 = nn.AvgPool2d(kernel_size=(45,80), stride=(45,80))
        self.pyr_conv2 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3,3),stride=(1,1), padding=(1,1))
        self.pyr_upsample2 = nn.Upsample(scale_factor=(45.0,80.0))

        self.pyr_AveragePool3 = nn.AvgPool2d(kernel_size=(18,40), stride=(18,40))
        self.pyr_conv3 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3,3),stride=(1,1), padding=(1,1)) 
        self.pyr_upsample3 = nn.Upsample(scale_factor=(18.0,40.0))

        self.pyr_AveragePool4 = nn.AvgPool2d(kernel_size=(10,10), stride=(10,10))
        self.pyr_conv4 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3,3),stride=(1,1), padding=(1,1))  
        self.pyr_upsample4 = nn.Upsample(scale_factor=(10.0,10.0))

        # self.pyr_AveragePool2 = nn.AvgPool2d(kernel_size=(30,80), stride=(30,80))
        # self.pyr_conv2 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3,3),stride=(1,1), padding=(1,1))
        # self.pyr_upsample2 = nn.Upsample(scale_factor=(30.0,80.0))

        # self.pyr_AveragePool3 = nn.AvgPool2d(kernel_size=(18,54), stride=(18,54))
        # self.pyr_conv3 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3,3),stride=(1,1), padding=(1,1)) 
        # self.pyr_upsample3 = nn.Upsample(scale_factor=(18.0,54.0))

        # self.pyr_AveragePool4 = nn.AvgPool2d(kernel_size=(10,20), stride=(10,20))
        # self.pyr_conv4 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3,3),stride=(1,1), padding=(1,1))  
        # self.pyr_upsample4 = nn.Upsample(scale_factor=(10.0,20.0))

        self.batch4 = nn.BatchNorm2d(num_features=320, track_running_stats=False)


        # Definition of subNet5 parameters
        self.conv5_1 = nn.Conv2d(in_channels=320, out_channels=64, kernel_size=(3,3),stride=(1,1), padding=(1,1))
        #self.batch5_1 = nn.BatchNorm2d(num_features=64, track_running_stats=False)
        self.dropout5_1 = torch.nn.Dropout2d(p=0.25, inplace=False)
        self.upsample5_1 = nn.Upsample(scale_factor=(4.0,4.0))

        self.conv5_2 = nn.Conv2d(in_channels=64, out_channels=self.num_classes, kernel_size=(3,3),stride=(1,1), padding=(1,1))
        self.upsample5_2 = nn.Upsample(scale_factor=(2.0,2.0))

        self.conv5_3 = nn.Conv2d(in_channels=self.num_classes, out_channels=self.num_classes, kernel_size=(3,3),stride=(1,1), padding=(1,1))
        self.softmax = nn.Softmax2d()


    def forward(self, inputs):

        
        # print("Input : ", inputs.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)


        # # Forward through subNet1
        # subNet1_1 = F.relu(self.batch1_1(self.conv1_1(inputs)))
        # print("subNet 1_1 : ", subNet1_1.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)

        # subNet1_2 = self.MaxPool1_2(F.relu(self.batch1_2(self.conv1_2(subNet1_1))))
        # print("subNet 1_2 : ", subNet1_2.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)

        # subNet1 = self.MaxPool1_3(F.relu(self.batch1_3(self.conv1_3(subNet1_2))))
        # print("subNet 1 : ", subNet1.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)


        # # Forward through subNet2 
        # subNet2_1 = F.relu(self.batch2_1(self.conv2_1(subNet1)))
        # print("subNet 2_1 : ", subNet2_1.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)

        # subNet2_2 = F.relu(self.batch2_2(self.conv2_2(subNet2_1)))
        # print("subNet 2_2 : ", subNet2_2.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)

        # subNet2_3 = F.relu(self.batch2_3(self.conv2_3(subNet2_2)))
        # print("subNet 2_3 : ", subNet2_3.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)

        # subNet2 = torch.add(subNet2_3, subNet1)
        # print("subNet 2 : ", subNet2.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)


        # # Forward through subNet3
        # subNet3 = F.relu(self.batch3_1(self.conv3_1(subNet2)))
        # print("subNet 3 : ", subNet3.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)



        # # Forward through the pyramid
        # pyrBranch1 = self.pyr_upsample1(F.relu(self.pyr_AveragePool1(subNet3)))
        # print("pyrBranch 1 : ", pyrBranch1.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)

        # pyrBranch2 = self.pyr_upsample2(F.relu(self.pyr_conv2(self.pyr_AveragePool2(subNet3))))
        # print("pyrBranch 2 : ", pyrBranch2.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)

        # pyrBranch3 = self.pyr_upsample3(F.relu(self.pyr_conv3(self.pyr_AveragePool3(subNet3))))
        # print("pyrBranch 3 : ", pyrBranch3.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)

        # pyrBranch4 = self.pyr_upsample4(F.relu(self.pyr_conv4(self.pyr_AveragePool4(subNet3))))
        # print("pyrBranch 4 : ", pyrBranch4.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)

        # subNet4 = self.batch4(torch.cat((subNet3, pyrBranch1, pyrBranch2, pyrBranch3, pyrBranch4),1))
        # print("subNet 4 : ", subNet4.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)


        # #Forward through subNet5
        # subNet5_1 = self.upsample5_1(self.dropout5_1(F.relu(self.conv5_1(subNet4))))
        # print("subNet 5_1 : ", subNet5_1.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)

        # subNet5_2 = self.upsample5_2(F.relu(self.conv5_2(subNet5_1)))
        # print("subNet 5_2 : ", subNet5_2.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)

        # subNet5 = self.conv5_3(subNet5_2)
        # print("subNet 5 : ", subNet5.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)

        # prediction = self.softmax(subNet5)
        # print("prediction : ", prediction.size())
        # print("Memory used: ", torch.cuda.memory_allocated(self.device)/10**9)


        # Forward through subNet1
        subNet1_1 = F.relu(self.batch1_1(self.conv1_1(inputs)))
        subNet1_2 = self.MaxPool1_2(F.relu(self.batch1_2(self.conv1_2(subNet1_1))))
        subNet1 = self.MaxPool1_3(F.relu(self.batch1_3(self.conv1_3(subNet1_2))))


        # Forward through subNet2 
        subNet2_1 = F.relu(self.batch2_1(self.conv2_1(subNet1)))
        subNet2_2 = F.relu(self.batch2_2(self.conv2_2(subNet2_1)))
        subNet2_3 = F.relu(self.batch2_3(self.conv2_3(subNet2_2)))
        subNet2 = torch.add(subNet2_3, subNet1)


        # Forward through subNet3
        subNet3 = F.relu(self.batch3_1(self.conv3_1(subNet2)))



        # Forward through the pyramid
        pyrBranch1 = self.pyr_upsample1(F.relu(self.pyr_AveragePool1(subNet3)))
        pyrBranch2 = self.pyr_upsample2(F.relu(self.pyr_conv2(self.pyr_AveragePool2(subNet3))))
        pyrBranch3 = self.pyr_upsample3(F.relu(self.pyr_conv3(self.pyr_AveragePool3(subNet3))))
        pyrBranch4 = self.pyr_upsample4(F.relu(self.pyr_conv4(self.pyr_AveragePool4(subNet3))))
        subNet4 = self.batch4(torch.cat((subNet3, pyrBranch1, pyrBranch2, pyrBranch3, pyrBranch4),1))


        #Forward through subNet5
        subNet5_1 = self.upsample5_1(self.dropout5_1(F.relu(self.conv5_1(subNet4))))
        subNet5_2 = self.upsample5_2(F.relu(self.conv5_2(subNet5_1)))
        subNet5 = self.conv5_3(subNet5_2)
        prediction = self.softmax(subNet5)

        return subNet5

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features
