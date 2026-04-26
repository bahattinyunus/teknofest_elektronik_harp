import torch
import torch.nn as nn
import torch.nn.functional as F

class ResidualBlock1D(nn.Module):
    """
    Standard residual block for 1D convolutions used in ResNet-1D.
    """
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock1D, self).__init__()
        self.conv1 = nn.Conv1d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm1d(out_channels)
        self.conv2 = nn.Conv1d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm1d(out_channels)
        
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv1d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm1d(out_channels)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out

class MultimodalAMC(nn.Module):
    """
    Multimodal Automatic Modulation Classification (AMC) Model.
    Combines I/Q data (1D-ResNet) and Spectral Magnitude (2D-CNN/Dense).
    """
    def __init__(self, num_classes=10):
        super(MultimodalAMC, self).__init__()
        
        # Branch 1: I/Q Raw Data (ResNet-1D)
        # Input shape: (Batch, 2, 1024) - I and Q channels
        self.iq_branch = nn.Sequential(
            nn.Conv1d(2, 64, kernel_size=7, stride=2, padding=3, bias=False),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            ResidualBlock1D(64, 64),
            ResidualBlock1D(64, 128, stride=2),
            ResidualBlock1D(128, 256, stride=2),
            nn.AdaptiveAvgPool1d(1)
        )
        
        # Branch 2: Spectral Magnitude (2D-CNN or Dense)
        # Input shape: (Batch, 1, 512) - Positive FFT magnitudes
        self.spec_branch = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU()
        )
        
        # Fusion Layer
        self.fusion = nn.Sequential(
            nn.Linear(256 + 128, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )

    def forward(self, iq, spec):
        # IQ feature extraction
        x1 = self.iq_branch(iq)
        x1 = x1.view(x1.size(0), -1) # Flatten: (Batch, 256)
        
        # Spectral feature extraction
        x2 = self.spec_branch(spec)
        x2 = x2.view(x2.size(0), -1) # Flatten: (Batch, 128)
        
        # Concatenate features
        merged = torch.cat((x1, x2), dim=1)
        
        # Final classification
        out = self.fusion(merged)
        return out

if __name__ == "__main__":
    # Test inference
    model = MultimodalAMC(num_classes=10)
    dummy_iq = torch.randn(1, 2, 1024)
    dummy_spec = torch.randn(1, 1, 512)
    output = model(dummy_iq, dummy_spec)
    print(f"Model output shape: {output.shape}")
    print("Multimodal AMC architecture initialized successfully.")
