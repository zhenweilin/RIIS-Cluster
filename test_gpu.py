import torch


if torch.cuda.is_available():
    print("cuda可使用")
else:
    print("cuda不可使用")
    