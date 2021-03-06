"""
CIFAR10 classification
======================

example of image classification
"""
import symjax.tensor as T
import symjax as sj
import numpy as np
import matplotlib.pyplot as plt


# load the dataset
cifar10 = sj.data.cifar10.load()

# some renormalization
cifar10["train_set/images"] /= cifar10["train_set/images"].max((1, 2, 3), keepdims=True)
cifar10["test_set/images"] /= cifar10["test_set/images"].max((1, 2, 3), keepdims=True)

# create the network
BATCH_SIZE = 32
images = T.Placeholder((BATCH_SIZE, 3, 32, 32), "float32")
labels = T.Placeholder((BATCH_SIZE,), "int32")
deterministic = T.Placeholder((1,), "bool")

layer = [
    sj.layers.RandomCrop(
        images,
        crop_shape=(3, 32, 32),
        padding=[(0, 0), (4, 4), (4, 4)],
        deterministic=deterministic,
    )
]

for l in range(8):
    layer.append(sj.layers.Conv2D(layer[-1], 32, (3, 3), b=None, pad="SAME"))
    layer.append(sj.layers.BatchNormalization(layer[-1], [0, 2, 3], deterministic))
    layer.append(sj.layers.Lambda(layer[-1], T.leaky_relu))
    if l % 3 == 0:
        layer.append(sj.layers.Pool2D(layer[-1], (2, 2)))

layer.append(sj.layers.Pool2D(layer[-1], layer[-1].shape[2:], pool_type="AVG"))

layer.append(sj.layers.Dense(layer[-1], 10))

# each layer is itself a tensor which represents its output and thus
# any tensor operation can be used on the layer instance, for example
for l in layer:
    print(l.shape)


loss = sj.losses.sparse_crossentropy_logits(labels, layer[-1]).mean()
accuracy = sj.losses.accuracy(labels, layer[-1])

lr = sj.schedules.PiecewiseConstant(0.01, {15: 0.001, 25: 0.0001})
opt = sj.optimizers.Adam(loss, lr)

network_updates = sj.layers.get_updates(layer)

test = sj.function(images, labels, deterministic, outputs=[loss, accuracy])

train = sj.function(
    images,
    labels,
    deterministic,
    outputs=[loss, accuracy],
    updates={**opt.updates, **network_updates},
)

test_accuracy = []

for epoch in range(3):
    L = list()
    for x, y in sj.data.batchify(
        cifar10["test_set/images"],
        cifar10["test_set/labels"],
        batch_size=BATCH_SIZE,
        option="continuous",
    ):
        L.append(test(x, y, 1))
    print("Test Loss and Accu:", np.mean(L, 0))
    test_accuracy.append(np.mean(L, 0))
    L = list()
    for x, y in sj.data.batchify(
        cifar10["train_set/images"],
        cifar10["train_set/labels"],
        batch_size=BATCH_SIZE,
        option="random_see_all",
    ):
        L.append(train(x, y, 0))
    print("Train Loss and Accu", np.mean(L, 0))
    lr.update()

plt.plot(test_accuracy)
plt.xlabel("epochs")
plt.ylabel("accuracy")
plt.title("CIFAR10 classification task")
