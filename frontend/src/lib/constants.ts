import { SampleModel, Severity } from "./types";

export const SEVERITY_COLORS: Record<Severity, { bg: string; text: string; border: string; dot: string }> = {
  supported: {
    bg: "bg-green-900/30",
    text: "text-green-400",
    border: "border-green-800/50",
    dot: "bg-green-500",
  },
  partial: {
    bg: "bg-amber-900/30",
    text: "text-amber-400",
    border: "border-amber-800/50",
    dot: "bg-amber-500",
  },
  unsupported: {
    bg: "bg-red-900/30",
    text: "text-red-400",
    border: "border-red-800/50",
    dot: "bg-red-500",
  },
};

export const SEVERITY_LABELS: Record<Severity, string> = {
  supported: "Supported",
  partial: "Partial Support",
  unsupported: "Unsupported",
};

export const EFFORT_COLORS: Record<string, string> = {
  low: "bg-green-900/30 text-green-400 border-green-800/50",
  medium: "bg-amber-900/30 text-amber-400 border-amber-800/50",
  high: "bg-red-900/30 text-red-400 border-red-800/50",
};

export const EFFORT_LABELS: Record<string, string> = {
  low: "Low Effort",
  medium: "Medium Effort",
  high: "High Effort",
};

export const DEFAULT_API_BASE_URL = "http://localhost:8000";

export const SAMPLE_MODELS: SampleModel[] = [
  {
    id: "simple-cnn",
    name: "SimpleCNN",
    description: "A basic convolutional neural network with conv, pool, and linear layers",
    code: `import torch
import torch.nn as nn
import torch.nn.functional as F


class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.25)
        self.fc1 = nn.Linear(64 * 8 * 8, 256)
        self.fc2 = nn.Linear(256, num_classes)

    def forward(self, x):
        x = self.pool(F.relu(self.bn1(self.conv1(x))))
        x = self.pool(F.relu(self.bn2(self.conv2(x))))
        x = x.view(x.size(0), -1)
        x = self.dropout(x)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# Usage
model = SimpleCNN(num_classes=10)
dummy_input = torch.randn(1, 3, 32, 32)
output = model(dummy_input)
print(f"Output shape: {output.shape}")
`,
  },
  {
    id: "transformer-block",
    name: "TransformerBlock",
    description: "A single transformer encoder block with multi-head attention",
    code: `import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model=512, n_heads=8):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        batch_size, seq_len, _ = x.shape

        Q = self.W_q(x).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        K = self.W_k(x).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        V = self.W_v(x).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)

        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        attn = F.softmax(scores, dim=-1)
        context = torch.matmul(attn, V)

        context = context.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
        return self.W_o(context)


class TransformerBlock(nn.Module):
    def __init__(self, d_model=512, n_heads=8, d_ff=2048, dropout=0.1):
        super().__init__()
        self.attention = MultiHeadAttention(d_model, n_heads)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ff = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout),
        )

    def forward(self, x, mask=None):
        attn_out = self.attention(self.norm1(x), mask)
        x = x + attn_out
        ff_out = self.ff(self.norm2(x))
        x = x + ff_out
        return x


# Usage
block = TransformerBlock(d_model=512, n_heads=8)
dummy_input = torch.randn(2, 128, 512)
output = block(dummy_input)
print(f"Output shape: {output.shape}")
`,
  },
  {
    id: "resnet-basic",
    name: "ResNet BasicBlock",
    description: "A ResNet-style basic residual block with skip connections",
    code: `import torch
import torch.nn as nn
import torch.nn.functional as F


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_channels, out_channels, stride=1, downsample=None):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3,
                               stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3,
                               stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.downsample = downsample
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        identity = x

        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)
        return out


class SimpleResNet(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleResNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.layer1 = BasicBlock(64, 64)
        self.layer2 = BasicBlock(64, 128, stride=2,
                                 downsample=nn.Sequential(
                                     nn.Conv2d(64, 128, 1, stride=2, bias=False),
                                     nn.BatchNorm2d(128)))

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.maxpool(self.relu(self.bn1(self.conv1(x))))
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x


# Usage
model = SimpleResNet(num_classes=10)
dummy_input = torch.randn(1, 3, 224, 224)
output = model(dummy_input)
print(f"Output shape: {output.shape}")
`,
  },
];
