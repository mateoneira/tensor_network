import numpy as np

def create_grid_tensor_field(shape, direction=(1, 0)):
    tensor_field = np.zeros((shape[0], shape[1], 2, 2))
    for i in range(shape[0]):
        for j in range(shape[1]):
            theta = np.arctan2(direction[1], direction[0])
            tensor_field[i, j] = np.array([[np.cos(2*theta), np.sin(2*theta)],
                                           [np.sin(2*theta), -np.cos(2*theta)]])
    return tensor_field

def create_radial_tensor_field(shape, center):
    tensor_field = np.zeros((shape[0], shape[1], 2, 2))
    for i in range(shape[0]):
        for j in range(shape[1]):
            x, y = i - center[0], j - center[1]
            theta = np.arctan2(y, x)
            tensor_field[i, j] = np.array([[np.cos(2*theta), np.sin(2*theta)],
                                           [np.sin(2*theta), -np.cos(2*theta)]])
    return tensor_field

def combine_basis_fields(basis_fields, positions, decay_constant=1.0):
    combined_field = np.zeros_like(basis_fields[0])
    for i, field in enumerate(basis_fields):
        pos = positions[i]
        distance = np.sqrt((np.arange(combined_field.shape[0])[:, None] - pos[0]) ** 2 +
                           (np.arange(combined_field.shape[1])[None, :] - pos[1]) ** 2)
        weight = np.exp(-decay_constant * distance ** 2)
        combined_field += weight[:, :, None, None] * field
    return combined_field


def trace_hyperstreamline(tensor_field, start_point, dsep=1):
    # A simple example of tracing a streamline
    streamline = [start_point]
    current_point = start_point
    
    while True:
        i, j = int(current_point[0]), int(current_point[1])
        if i < 0 or j < 0 or i >= tensor_field.shape[0] or j >= tensor_field.shape[1]:
            break
        tensor = tensor_field[i, j]
        direction = np.array([tensor[0, 0], tensor[0, 1]])
        next_point = current_point + dsep * direction / np.linalg.norm(direction)
        streamline.append(next_point)
        if np.linalg.norm(next_point - current_point) < 0.01:
            break
        current_point = next_point
    
    return np.array(streamline)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    shape = (100, 100)
    grid_tensor_field = create_grid_tensor_field(shape)
    radial_tensor_field = create_radial_tensor_field(shape, (50, 50))

    combined_field = combine_basis_fields(
        [grid_tensor_field, radial_tensor_field],
        [(50, 50), (75, 75)],
        decay_constant=0.01
)   

    start_point = np.array([50, 50])
    streamline = trace_hyperstreamline(combined_field, start_point)

    plt.figure(figsize=(8, 8))
    plt.quiver(np.arange(shape[0]), np.arange(shape[1]), combined_field[..., 0, 0], combined_field[..., 0, 1])
    plt.plot(streamline[:, 1], streamline[:, 0], 'r')
    plt.xlim(0, shape[1])
    plt.ylim(0, shape[0])
    plt.gca().invert_yaxis()
    plt.show()
    print('Done!')