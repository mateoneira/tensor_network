import numpy as np

def create_grid_tensor_field(shape, direction=(1, 0)):
    tensor_field = np.zeros((shape[0], shape[1], 2, 2))
    for i in range(shape[0]):
        for j in range(shape[1]):
            theta = np.arctan2(direction[1], direction[0])
            tensor_field[i, j] = np.array([[np.cos(2*theta), np.sin(2*theta)],
                                           [np.sin(2*theta), -np.cos(2*theta)]])
    return tensor_field

shape = (100, 100)
grid_tensor_field = create_grid_tensor_field(shape)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.imshow(grid_tensor_field[:, :, 0, 0])
    plt.colorbar()
    plt.show()