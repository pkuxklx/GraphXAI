import ipdb
import random
import torch
import argparse
from graphxai.gnn_models.node_classification.testing import GCN_3layer_basic, GIN_3layer_basic, test, train, val
from graphxai.datasets.shape_graph import ShapeGraph
from graphxai.datasets  import load_ShapeGraph


parser = argparse.ArgumentParser()
parser.add_argument('--expt_name', required=True, help='name of the explanation method')
args = parser.parse_args()


# Load ShapeGraph dataset
if args.expt_name == 'homophily':
    bah = torch.load(open('/home/cha567/GraphXAI/data/ShapeGraph/SG_homophilic.pickle', 'rb'))
elif args.expt_name == 'heterophily':
    bah = torch.load(open('/home/cha567/GraphXAI/data/ShapeGraph/SG_heterophilic.pickle', 'rb'))
elif args.expt_name == 'triangle':
    bah = torch.load(open('/home/cha567/GraphXAI/data/ShapeGraph/SG_triangles.pickle', 'rb'))
else:
    print('Invalid Input!!')
    exit(0)

data = bah.get_graph(use_fixed_split=True)
inhouse = (data.y == 1).nonzero(as_tuple=True)[0]

# Test on 3-layer basic GCN, 16 hidden dim:
model = GIN_3layer_basic(16, input_feat = 11, classes = 2)

# Train the model:
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = torch.nn.CrossEntropyLoss()

best_f1=0
for epoch in range(1, 1001):
    loss = train(model, optimizer, criterion, data)
    f1, acc, precision, recall, auroc, auprc = val(model, data, get_auc=True)
    if f1 > best_fc:
        best_f1 = f1
        torch.save(model.state_dict(), f'model_{args.expt_name}.pth')

    print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}, Val F1: {f1:.4f}, Val AUROC: {auroc:.4f}')

# Testing performance
f1, acc, precision, recall, auroc, auprc = test(model, data, get_auc=True)
print(f'Test F1: {f1:.4f}, Test AUROC: {auroc:.4f}')
