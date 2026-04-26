import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import numpy as np
import logging
import os

from ai_engine.models import MultimodalAMC
from simulation.data_generator import IQDataGenerator

class EWDataset(Dataset):
    """
    Custom Dataset for Electronic Warfare signals.
    Generates data on-the-fly or from a pre-generated batch.
    """
    def __init__(self, num_samples_per_class=500, snr_db=15):
        self.generator = IQDataGenerator()
        self.classes = ["Noise", "BPSK", "QPSK", "16QAM"]
        self.data = []
        self.labels = []
        
        logging.info(f"Generating training dataset ({num_samples_per_class} per class)...")
        for idx, cls in enumerate(self.classes):
            for _ in range(num_samples_per_class):
                # Generate raw IQ (Complex)
                iq_signal = self.generator.get_labeled_batch(cls, snr_db=snr_db, num_samples=1024)
                
                # Pre-process for the model
                # 1. IQ Branch: Split into Real and Imag (Batch, 2, 1024)
                iq_dual = np.stack([iq_signal.real, iq_signal.imag])
                
                # 2. Spec Branch: Compute FFT Magnitudes (Batch, 1, 512)
                spec = np.abs(np.fft.fft(iq_signal))[:512]
                spec = spec / (np.max(spec) + 1e-9) # Normalize
                
                self.data.append((iq_dual, spec))
                self.labels.append(idx)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        iq, spec = self.data[idx]
        label = self.labels[idx]
        return (torch.tensor(iq, dtype=torch.float32), 
                torch.tensor(spec, dtype=torch.float32).unsqueeze(0), 
                torch.tensor(label, dtype=torch.long))

def train_model(epochs=10, batch_size=32, lr=0.001):
    """
    Main training loop for Multimodal AMC.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logging.info(f"Training on device: {device}")
    
    # 1. Prepare Data
    dataset = EWDataset(num_samples_per_class=250)
    train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    # 2. Initialize Model
    model = MultimodalAMC(num_classes=len(dataset.classes)).to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    
    # 3. Training Loop
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        correct = 0
        total = 0
        
        for iq, spec, labels in train_loader:
            iq, spec, labels = iq.to(device), spec.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(iq, spec)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
        acc = 100 * correct / total
        print(f"Epoch [{epoch+1}/{epochs}] - Loss: {total_loss/len(train_loader):.4f} - Acc: {acc:.2f}%")

    # 4. Save Model
    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), "models/multimodal_amc_v3.pt")
    print("Training complete. Model saved to models/multimodal_amc_v3.pt")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Running a short training for demonstration
    train_model(epochs=3)
