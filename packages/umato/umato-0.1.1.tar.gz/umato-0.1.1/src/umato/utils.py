# Author: Leland McInnes <leland.mcinnes@gmail.com>
#
# License: BSD 3 clause

import time
import os
import numba
import numpy as np
import scipy.sparse
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import pandas as pd


def init_position(x, label, dname, init_type=None):
    if init_type == "pca":
        init = PCA(n_components=2).fit_transform(x)
    elif init_type == "spectral":
        path = os.path.join(os.getcwd(), "visualization", "public", "results", "init", f"{dname}_init.csv")
        init = pd.read_csv(path)
        init = np.array(init)
        # init = SpectralEmbedding(n_components=2, n_jobs=-1).fit_transform(x)
    elif init_type == "class":
        init = np.empty(shape=(0,2))
        z1 = [1,2,2,1]
        z2 = [1,1,2,2]
        for i in range(int(len(label))):
            l = int(label[i] % 4)
            init = np.append(init, np.array([[(-1)**z1[l] * label[i] * 1.5, (-1)**z2[l] * label[i] * 1.5]]), axis=0)
        init += np.random.normal(
            scale=0.1, size=[len(label), 2]
        ).astype(np.float32)
    elif init_type == "random":
        init = np.random.normal(
            loc=0.0, scale=0.05, size=list((len(label), 2))
        ).astype(np.float32)
    else:
        Warning("should set this")
    # init_normed = init / init.max(axis=0)
    init_normed = (init - init.mean()) / init.max()
    return init_normed


def plot_tmptmp(data, label, name):

    plt.scatter(data[:, 0], data[:, 1], s=2.0, c=label, cmap="Spectral", alpha=1.0)
    cbar = plt.colorbar(boundaries=np.arange(11) - 0.5)
    cbar.set_ticks(np.arange(11))
    plt.title("Embedded")
    plt.savefig(f"./figures/{name}.png")
    plt.close()


@numba.njit(
    locals={
        "matrix": numba.types.float32[:, ::1],
    },
    parallel=True,
    fastmath=True,
)
def adjacency_matrix(data):
    n = data.shape[0]
    dim = data.shape[1]
    matrix = np.zeros((n, n), dtype=np.float32)

    for i in numba.prange(n):
        for j in numba.prange(i):
            for d in numba.prange(dim):
                matrix[i, j] += (data[i][d] - data[j][d]) ** 2

    matrix = matrix + matrix.T
    return np.sqrt(matrix)


@numba.njit(parallel=True)
def fast_knn_indices(X, n_neighbors):
    """A fast computation of knn indices.

    Parameters
    ----------
    X: array of shape (n_samples, n_features)
        The input data to compute the k-neighbor indices of.

    n_neighbors: int
        The number of nearest neighbors to compute for each sample in ``X``.

    Returns
    -------
    knn_indices: array of shape (n_samples, n_neighbors)
        The indices on the ``n_neighbors`` closest points in the dataset.
    """
    knn_indices = np.empty((X.shape[0], n_neighbors), dtype=np.int32)
    for row in numba.prange(X.shape[0]):
        # v = np.argsort(X[row])  # Need to call argsort this way for numba
        v = X[row].argsort(kind="quicksort")
        v = v[:n_neighbors]
        knn_indices[row] = v
    return knn_indices


@numba.njit("i4(i8[:])")
def tau_rand_int(state):
    """A fast (pseudo)-random number generator.

    Parameters
    ----------
    state: array of int64, shape (3,)
        The internal state of the rng

    Returns
    -------
    A (pseudo)-random int32 value
    """
    state[0] = (((state[0] & 4294967294) << 12) & 0xFFFFFFFF) ^ (
        (((state[0] << 13) & 0xFFFFFFFF) ^ state[0]) >> 19
    )
    state[1] = (((state[1] & 4294967288) << 4) & 0xFFFFFFFF) ^ (
        (((state[1] << 2) & 0xFFFFFFFF) ^ state[1]) >> 25
    )
    state[2] = (((state[2] & 4294967280) << 17) & 0xFFFFFFFF) ^ (
        (((state[2] << 3) & 0xFFFFFFFF) ^ state[2]) >> 11
    )

    return state[0] ^ state[1] ^ state[2]


@numba.njit("f4(i8[:])")
def tau_rand(state):
    """A fast (pseudo)-random number generator for floats in the range [0,1]

    Parameters
    ----------
    state: array of int64, shape (3,)
        The internal state of the rng

    Returns
    -------
    A (pseudo)-random float32 in the interval [0, 1]
    """
    integer = tau_rand_int(state)
    return abs(float(integer) / 0x7FFFFFFF)


@numba.njit()
def norm(vec):
    """Compute the (standard l2) norm of a vector.

    Parameters
    ----------
    vec: array of shape (dim,)

    Returns
    -------
    The l2 norm of vec.
    """
    result = 0.0
    for i in range(vec.shape[0]):
        result += vec[i] ** 2
    return np.sqrt(result)


@numba.njit()
def rejection_sample(n_samples, pool_size, rng_state):
    """Generate n_samples many integers from 0 to pool_size such that no
    integer is selected twice. The duplication constraint is achieved via
    rejection sampling.

    Parameters
    ----------
    n_samples: int
        The number of random samples to select from the pool

    pool_size: int
        The size of the total pool of candidates to sample from

    rng_state: array of int64, shape (3,)
        Internal state of the random number generator

    Returns
    -------
    sample: array of shape(n_samples,)
        The ``n_samples`` randomly selected elements from the pool.
    """
    result = np.empty(n_samples, dtype=np.int64)
    for i in range(n_samples):
        reject_sample = True
        j = 0
        while reject_sample:
            j = tau_rand_int(rng_state) % pool_size
            for k in range(i):
                if j == result[k]:
                    break
            else:
                reject_sample = False
        result[i] = j
    return result


@numba.njit()
def make_heap(n_points, size):
    """Constructor for the numba enabled heap objects. The heaps are used
    for approximate nearest neighbor search, maintaining a list of potential
    neighbors sorted by their distance. We also flag if potential neighbors
    are newly added to the list or not. Internally this is stored as
    a single ndarray; the first axis determines whether we are looking at the
    array of candidate indices, the array of distances, or the flag array for
    whether elements are new or not. Each of these arrays are of shape
    (``n_points``, ``size``)

    Parameters
    ----------
    n_points: int
        The number of data points to track in the heap.

    size: int
        The number of items to keep on the heap for each data point.

    Returns
    -------
    heap: An ndarray suitable for passing to other numba enabled heap functions.
    """
    result = np.zeros(
        (np.int64(3), np.int64(n_points), np.int64(size)), dtype=np.float64
    )
    result[0] = -1
    result[1] = np.infty
    result[2] = 0

    return result


@numba.njit("i8(f8[:,:,:],i8,f8,i8,i8)")
def heap_push(heap, row, weight, index, flag):
    """Push a new element onto the heap. The heap stores potential neighbors
    for each data point. The ``row`` parameter determines which data point we
    are addressing, the ``weight`` determines the distance (for heap sorting),
    the ``index`` is the element to add, and the flag determines whether this
    is to be considered a new addition.

    Parameters
    ----------
    heap: ndarray generated by ``make_heap``
        The heap object to push into

    row: int
        Which actual heap within the heap object to push to

    weight: float
        The priority value of the element to push onto the heap

    index: int
        The actual value to be pushed

    flag: int
        Whether to flag the newly added element or not.

    Returns
    -------
    success: The number of new elements successfully pushed into the heap.
    """
    row = int(row)
    indices = heap[0, row]
    weights = heap[1, row]
    is_new = heap[2, row]

    if weight >= weights[0]:
        return 0

    # break if we already have this element.
    for i in range(indices.shape[0]):
        if index == indices[i]:
            return 0

    # insert val at position zero
    weights[0] = weight
    indices[0] = index
    is_new[0] = flag

    # descend the heap, swapping values until the max heap criterion is met
    i = 0
    while True:
        ic1 = 2 * i + 1
        ic2 = ic1 + 1

        if ic1 >= heap.shape[2]:
            break
        elif ic2 >= heap.shape[2]:
            if weights[ic1] > weight:
                i_swap = ic1
            else:
                break
        elif weights[ic1] >= weights[ic2]:
            if weight < weights[ic1]:
                i_swap = ic1
            else:
                break
        else:
            if weight < weights[ic2]:
                i_swap = ic2
            else:
                break

        weights[i] = weights[i_swap]
        indices[i] = indices[i_swap]
        is_new[i] = is_new[i_swap]

        i = i_swap

    weights[i] = weight
    indices[i] = index
    is_new[i] = flag

    return 1


@numba.njit("i8(f8[:,:,:],i8,f8,i8,i8)")
def unchecked_heap_push(heap, row, weight, index, flag):
    """Push a new element onto the heap. The heap stores potential neighbors
    for each data point. The ``row`` parameter determines which data point we
    are addressing, the ``weight`` determines the distance (for heap sorting),
    the ``index`` is the element to add, and the flag determines whether this
    is to be considered a new addition.

    Parameters
    ----------
    heap: ndarray generated by ``make_heap``
        The heap object to push into

    row: int
        Which actual heap within the heap object to push to

    weight: float
        The priority value of the element to push onto the heap

    index: int
        The actual value to be pushed

    flag: int
        Whether to flag the newly added element or not.

    Returns
    -------
    success: The number of new elements successfully pushed into the heap.
    """
    if weight >= heap[1, row, 0]:
        return 0

    indices = heap[0, row]
    weights = heap[1, row]
    is_new = heap[2, row]

    # insert val at position zero
    weights[0] = weight
    indices[0] = index
    is_new[0] = flag

    # descend the heap, swapping values until the max heap criterion is met
    i = 0
    while True:
        ic1 = 2 * i + 1
        ic2 = ic1 + 1

        if ic1 >= heap.shape[2]:
            break
        elif ic2 >= heap.shape[2]:
            if weights[ic1] > weight:
                i_swap = ic1
            else:
                break
        elif weights[ic1] >= weights[ic2]:
            if weight < weights[ic1]:
                i_swap = ic1
            else:
                break
        else:
            if weight < weights[ic2]:
                i_swap = ic2
            else:
                break

        weights[i] = weights[i_swap]
        indices[i] = indices[i_swap]
        is_new[i] = is_new[i_swap]

        i = i_swap

    weights[i] = weight
    indices[i] = index
    is_new[i] = flag

    return 1


@numba.njit()
def siftdown(heap1, heap2, elt):
    """Restore the heap property for a heap with an out of place element
    at position ``elt``. This works with a heap pair where heap1 carries
    the weights and heap2 holds the corresponding elements."""
    while elt * 2 + 1 < heap1.shape[0]:
        left_child = elt * 2 + 1
        right_child = left_child + 1
        swap = elt

        if heap1[swap] < heap1[left_child]:
            swap = left_child

        if right_child < heap1.shape[0] and heap1[swap] < heap1[right_child]:
            swap = right_child

        if swap == elt:
            break
        else:
            heap1[elt], heap1[swap] = (heap1[swap], heap1[elt])
            heap2[elt], heap2[swap] = (heap2[swap], heap2[elt])
            elt = swap


@numba.njit()
def deheap_sort(heap):
    """Given an array of heaps (of indices and weights), unpack the heap
    out to give and array of sorted lists of indices and weights by increasing
    weight. This is effectively just the second half of heap sort (the first
    half not being required since we already have the data in a heap).

    Parameters
    ----------
    heap : array of shape (3, n_samples, n_neighbors)
        The heap to turn into sorted lists.

    Returns
    -------
    indices, weights: arrays of shape (n_samples, n_neighbors)
        The indices and weights sorted by increasing weight.
    """
    indices = heap[0]
    weights = heap[1]

    for i in range(indices.shape[0]):

        ind_heap = indices[i]
        dist_heap = weights[i]

        for j in range(ind_heap.shape[0] - 1):
            ind_heap[0], ind_heap[ind_heap.shape[0] - j - 1] = (
                ind_heap[ind_heap.shape[0] - j - 1],
                ind_heap[0],
            )
            dist_heap[0], dist_heap[dist_heap.shape[0] - j - 1] = (
                dist_heap[dist_heap.shape[0] - j - 1],
                dist_heap[0],
            )

            siftdown(
                dist_heap[: dist_heap.shape[0] - j - 1],
                ind_heap[: ind_heap.shape[0] - j - 1],
                0,
            )

    return indices.astype(np.int64), weights


@numba.njit("i8(f8[:, :, :],i8)")
def smallest_flagged(heap, row):
    """Search the heap for the smallest element that is
    still flagged.

    Parameters
    ----------
    heap: array of shape (3, n_samples, n_neighbors)
        The heaps to search

    row: int
        Which of the heaps to search

    Returns
    -------
    index: int
        The index of the smallest flagged element
        of the ``row``th heap, or -1 if no flagged
        elements remain in the heap.
    """
    ind = heap[0, row]
    dist = heap[1, row]
    flag = heap[2, row]

    min_dist = np.inf
    result_index = -1

    for i in range(ind.shape[0]):
        if flag[i] == 1 and dist[i] < min_dist:
            min_dist = dist[i]
            result_index = i

    if result_index >= 0:
        flag[result_index] = 0.0
        return int(ind[result_index])
    else:
        return -1


@numba.njit(parallel=True)
def build_candidates(current_graph, n_vertices, n_neighbors, max_candidates, rng_state):
    """Build a heap of candidate neighbors for nearest neighbor descent. For
    each vertex the candidate neighbors are any current neighbors, and any
    vertices that have the vertex as one of their nearest neighbors.

    Parameters
    ----------
    current_graph: heap
        The current state of the graph for nearest neighbor descent.

    n_vertices: int
        The total number of vertices in the graph.

    n_neighbors: int
        The number of neighbor edges per node in the current graph.

    max_candidates: int
        The maximum number of new candidate neighbors.

    rng_state: array of int64, shape (3,)
        The internal state of the rng

    Returns
    -------
    candidate_neighbors: A heap with an array of (randomly sorted) candidate
    neighbors for each vertex in the graph.
    """
    candidate_neighbors = make_heap(n_vertices, max_candidates)
    for i in range(n_vertices):
        for j in range(n_neighbors):
            if current_graph[0, i, j] < 0:
                continue
            idx = current_graph[0, i, j]
            isn = current_graph[2, i, j]
            d = tau_rand(rng_state)
            heap_push(candidate_neighbors, i, d, idx, isn)
            heap_push(candidate_neighbors, idx, d, i, isn)
            current_graph[2, i, j] = 0

    return candidate_neighbors


@numba.njit()
def new_build_candidates(
    current_graph, n_vertices, n_neighbors, max_candidates, rng_state, rho=0.5
):  # pragma: no cover
    """Build a heap of candidate neighbors for nearest neighbor descent. For
    each vertex the candidate neighbors are any current neighbors, and any
    vertices that have the vertex as one of their nearest neighbors.

    Parameters
    ----------
    current_graph: heap
        The current state of the graph for nearest neighbor descent.

    n_vertices: int
        The total number of vertices in the graph.

    n_neighbors: int
        The number of neighbor edges per node in the current graph.

    max_candidates: int
        The maximum number of new candidate neighbors.

    rng_state: array of int64, shape (3,)
        The internal state of the rng

    Returns
    -------
    candidate_neighbors: A heap with an array of (randomly sorted) candidate
    neighbors for each vertex in the graph.
    """
    new_candidate_neighbors = make_heap(n_vertices, max_candidates)
    old_candidate_neighbors = make_heap(n_vertices, max_candidates)

    for i in range(n_vertices):
        for j in range(n_neighbors):
            if current_graph[0, i, j] < 0:
                continue
            idx = current_graph[0, i, j]
            isn = current_graph[2, i, j]
            d = tau_rand(rng_state)
            if tau_rand(rng_state) < rho:
                c = 0
                if isn:
                    c += heap_push(new_candidate_neighbors, i, d, idx, isn)
                    c += heap_push(new_candidate_neighbors, idx, d, i, isn)
                else:
                    heap_push(old_candidate_neighbors, i, d, idx, isn)
                    heap_push(old_candidate_neighbors, idx, d, i, isn)

                if c > 0:
                    current_graph[2, i, j] = 0

    return new_candidate_neighbors, old_candidate_neighbors


@numba.njit(parallel=True)
def submatrix(dmat, indices_col, n_neighbors):
    """Return a submatrix given an orginal matrix and the indices to keep.

    Parameters
    ----------
    dmat: array, shape (n_samples, n_samples)
        Original matrix.

    indices_col: array, shape (n_samples, n_neighbors)
        Indices to keep. Each row consists of the indices of the columns.

    n_neighbors: int
        Number of neighbors.

    Returns
    -------
    submat: array, shape (n_samples, n_neighbors)
        The corresponding submatrix.
    """
    n_samples_transform, n_samples_fit = dmat.shape
    submat = np.zeros((n_samples_transform, n_neighbors), dtype=dmat.dtype)
    for i in numba.prange(n_samples_transform):
        for j in numba.prange(n_neighbors):
            submat[i, j] = dmat[i, indices_col[i, j]]
    return submat


# Generates a timestamp for use in logging messages when verbose=True
def ts():
    return time.ctime(time.time())


# I'm not enough of a numba ninja to numba this successfully.
# np.arrays of lists, which are objects...
def csr_unique(matrix, return_index=True, return_inverse=True, return_counts=True):
    """Find the unique elements of a sparse csr matrix.
    We don't explicitly construct the unique matrix leaving that to the user
    who may not want to duplicate a massive array in memory.
    Returns the indices of the input array that give the unique values.
    Returns the indices of the unique array that reconstructs the input array.
    Returns the number of times each unique row appears in the input matrix.

    matrix: a csr matrix
    return_index = bool, optional
        If true, return the row indices of 'matrix'
    return_inverse: bool, optional
        If true, return the the indices of the unique array that can be
           used to reconstruct 'matrix'.
    return_counts = bool, optional
        If true, returns the number of times each unique item appears in 'matrix'

    The unique matrix can computed via
    unique_matrix = matrix[index]
    and the original matrix reconstructed via
    unique_matrix[inverse]
    """
    lil_matrix = matrix.tolil()
    rows = [x + y for x, y in zip(lil_matrix.rows, lil_matrix.data)]
    return_values = return_counts + return_inverse + return_index
    return np.unique(
        rows,
        return_index=return_index,
        return_inverse=return_inverse,
        return_counts=return_counts,
    )[1 : (return_values + 1)]


@numba.njit()
def clip(val, cutoff):
    """Standard clamping of a value into a fixed range

    Parameters
    ----------
    val: float
        The value to be clamped.

    Returns
    -------
    The clamped value, now fixed to be in the range -cutoff to cutoff.
    """
    if val > cutoff:
        return cutoff
    elif val < -cutoff:
        return -cutoff
    else:
        return val


@numba.njit(
    "f4(f4[::1],f4[::1])",
    fastmath=True,
    cache=True,
    locals={
        "result": numba.types.float32,
        "diff": numba.types.float32,
        "dim": numba.types.int64,
    },
)
def rdist(x, y):
    """Reduced Euclidean distance.

    Parameters
    ----------
    x: array of shape (embedding_dim,)
    y: array of shape (embedding_dim,)

    Returns
    -------
    The squared euclidean distance between x and y
    """
    result = 0.0
    dim = x.shape[0]
    for i in range(dim):
        diff = x[i] - y[i]
        result += diff * diff

    return result
