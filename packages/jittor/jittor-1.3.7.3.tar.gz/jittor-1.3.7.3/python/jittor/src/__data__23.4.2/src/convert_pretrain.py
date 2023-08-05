import jittor as jt

import torch
from torchvision import models as tc_models

from jittor import models
import os

def run_cmd(cmd):
    print("[run cmd]", cmd)
    assert os.system(cmd) == 0

cache_path = jt.compiler.cache_path
ck_path = os.path.join(cache_path, "checkpoints")
os.makedirs(ck_path, exist_ok=True)

print(cache_path)

keys = []

for k, v in models.__dict__.items():
    if not callable(v): continue
    if not hasattr(tc_models, k): continue
    v2 = getattr(tc_models, k)
    if not callable(v2): continue
    # if k != "resnet18": continue
    try:
        print(k)
        model2 = v2(pretrained=True)
        model = v()
    except:
        continue
    model.load_parameters(model2.state_dict())
    model.save(os.path.join(ck_path, k+".pkl"))
    model.load(os.path.join(ck_path, k+".pkl"))
    print("ok", k)
    keys.append(k)

# run_cmd(f"rsync -avPu {ck_path} jittor-web:Documents/jittor-blog/assets/build/")
# assert os.system(f"ssh jittor-web Documents/jittor-blog.git/hooks/post-update")==0
# run_cmd(f"rm {ck_path}/*.pkl")

for k in keys:
    print("check", k)
    v = getattr(models, k)
    try:
        model = v(pretrained=True)
    except:
        print("failed", k)
        continue
    print("ok", k)


resnet50 = models.resnet50(pretrained=True)