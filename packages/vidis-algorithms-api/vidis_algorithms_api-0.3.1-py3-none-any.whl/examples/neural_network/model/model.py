import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import pytorch_lightning as pl



class MySuperNetLittleInput(nn.Module):
    
    def __init__(self, in_f=237, out_f=16, *args):
        super().__init__()
        #self.bn_start = nn.BatchNorm3d(in_f)


        self.block1 = nn.Sequential(
            # (N, in_f, 128, 128)
            nn.Conv2d(in_f, in_f * 4, kernel_size=3, stride=2, padding=1, bias=False),
            # (N, in_f * 4, 64, 64)
            nn.BatchNorm2d(in_f * 4),
            nn.ReLU(),
        ) # concat with block 8
        self.block2 = nn.Sequential(
            nn.Conv2d(in_f * 4, in_f * 8, kernel_size=3, stride=2, padding=1, bias=False),
            # (N,  in_f * 8, 32, 32)
            nn.BatchNorm2d( in_f * 8),
            nn.ReLU(),
        )# concat with block 7
        self.block3 = nn.Sequential(
            nn.Conv2d( in_f * 8,  in_f * 8, kernel_size=3, stride=1, padding=1, bias=False),
            # (N,  in_f * 8, 32, 32)
            nn.BatchNorm2d( in_f * 8),
            nn.ReLU(),
        )# concat with block 6
        self.block4 = nn.Sequential(
            nn.Conv2d( in_f * 8,  in_f * 8 * 3, kernel_size=3, stride=1, padding=1, bias=False),
            # (N,  in_f * 8 * 3, 32, 32)
            nn.BatchNorm2d(in_f * 8 * 3),
            nn.ReLU(),
        )
        self.block5 = nn.Sequential(
            nn.Conv2d( in_f * 8 * 3,  in_f * 8, kernel_size=1, stride=1, padding=0, bias=False),
            # (N,  in_f * 8, 32, 32)
            nn.BatchNorm2d( in_f * 8),
            nn.ReLU(),
        )

        self.block6_up = nn.Sequential(
            nn.Conv2d( in_f * 8 + in_f * 8,  in_f * 8, kernel_size=3, stride=1, padding=1, bias=False),
            # (N,  in_f * 8, 32, 32)
            nn.BatchNorm2d( in_f * 8),
            nn.ReLU(),
        )
        self.block7_up = nn.Sequential(
            nn.ConvTranspose2d(in_f * 8 + in_f * 8,  in_f * 8, kernel_size=3, stride=2, padding=1, output_padding=1, bias=False),
            # (N,  in_f * 8, 64, 64)
            nn.BatchNorm2d( in_f * 8),
            nn.ReLU(),
        )
        self.block8_up = nn.Sequential(
            nn.ConvTranspose2d( in_f * 4 + in_f * 8,  in_f * 4, kernel_size=3, stride=2, padding=1, output_padding=1, bias=False),
            # (N, in_f * 4, 128, 128)
            nn.BatchNorm2d(in_f * 4),
            nn.ReLU(),
        )

        self.block9 = nn.Sequential(
            nn.Conv2d(in_f * 4, out_f, kernel_size=3, stride=1, padding=1, bias=False),
            # (N, out_f, 128, 128)
            nn.BatchNorm2d(out_f),
            nn.ReLU(),
        )
        self.final_conv = nn.Conv2d(out_f, out_f, kernel_size=1, stride=1, padding=0, bias=False)
    
    def forward(self, x):
        x1 = self.block1(x)
        x2 = self.block2(x1)
        x3 = self.block3(x2)

        x = self.block4(x3)
        x = self.block5(x)

        x = torch.cat([x, x3], dim=1)
        x = self.block6_up(x)
        x = torch.cat([x, x2], dim=1)
        x = self.block7_up(x)
        x = torch.cat([x, x1], dim=1)
        x = self.block8_up(x)

        x = self.block9(x)
        x = self.final_conv(x)
        return x


class NnModel(pl.LightningModule):
    def __init__(
            self, model, loss,
            T_0=10, T_mult=2, experiment=None, enable_image_logging=True,
            lr=1e-3, lr_list=None, epoch_list=None):
        super().__init__()
        self.model = model
        self.loss = loss
        self.lr = lr
        self.experiment = experiment
        self.enable_image_logging = enable_image_logging
        self.T_0 = T_0
        self.T_mult = T_mult
            
    def forward(self, x):
        out = self.model(x)
        return out
