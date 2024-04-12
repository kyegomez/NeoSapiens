import torch.nn as nn
import torch.nn.functional as F


class FaceNet(nn.Module):
    """
    Convolutional neural network architecture for facial recognition,
    trained to generate 128-d embeddings of face images.

    Architecture details:
        - Takes 160x160 RGB face images as input
        - Several convolutional layers, BatchNorm, MaxPooling
        -culminating in a linear layer outputting 128-d embedding vector
    """

    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv2d(3, 32, 5)
        self.bn1 = nn.BatchNorm2d(32)
        self.pool1 = nn.MaxPool2d(2, 2)

        self.conv2 = nn.Conv2d(32, 64, 5)
        self.bn2 = nn.BatchNorm2d(64)
        self.pool2 = nn.MaxPool2d(2, 2)

        self.conv3 = nn.Conv2d(64, 96, 3)
        self.bn3 = nn.BatchNorm2d(96)

        self.conv4 = nn.Conv2d(96, 128, 3)
        self.bn4 = nn.BatchNorm2d(128)

        self.fc1 = nn.Linear(128 * 8 * 8, 256)
        self.fc2 = nn.Linear(256, 128)  # 128-d embedding

    def forward(self, x):
        x = self.pool1(F.relu(self.bn1(self.conv1(x))))
        x = self.pool2(F.relu(self.bn2(self.conv2(x))))
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.relu(self.bn4(self.conv4(x)))

        x = x.view(-1, 128 * 8 * 8)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
