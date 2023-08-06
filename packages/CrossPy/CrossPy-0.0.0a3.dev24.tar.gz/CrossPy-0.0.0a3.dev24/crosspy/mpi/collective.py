from contextlib import nullcontext
from functools import lru_cache

import cupy

def alltoallv(sendbuf, sdispls, recvbuf, debug=False):
    """
    sendbuf [[] [] []]
    sdispls [. . .]
    """
    source_bounds = sendbuf._bounds
    target_bounds = recvbuf._bounds

    @lru_cache(maxsize=len(recvbuf._original_data))
    def _cached(j):
        g_sdispls = cupy.asarray(sdispls[(target_bounds[j-1] if j else 0):target_bounds[j]])
        source_block_ids = cupy.sum(cupy.expand_dims(g_sdispls, axis=-1) >= cupy.asarray(source_bounds), axis=-1, keepdims=False)
        return g_sdispls, source_block_ids

    for i in range(len(sendbuf._original_data)):
        for j in range(len(recvbuf._original_data)):
            # gather
            with getattr(sendbuf._original_data[i], 'device', nullcontext()):
                g_sdispls, source_block_ids = _cached(j)
                gather_mask = (cupy.asarray(source_block_ids) == i)
                gather_indices_local = cupy.asarray(g_sdispls)[gather_mask] - (source_bounds[i-1] if i else 0)
                # assert sum(scatter_mask) == len(gather_indices_local)
                buf = sendbuf._original_data[i][gather_indices_local]
            # scatter
            with getattr(recvbuf._original_data[j], 'device', nullcontext()):
                scatter_mask = cupy.asarray(gather_mask)
                assert not debug or cupy.allclose(recvbuf._original_data[j][scatter_mask], cupy.asarray(buf))
                recvbuf._original_data[j][scatter_mask] = cupy.asarray(buf)

def all2ints(sendbuf, recvbuf, rdispls, debug=False):
    """
    sendbuf [[] [] []]
    sdispls [. . .]
    """
    target_bounds = recvbuf._bounds
    source_bounds = sendbuf._bounds

    @lru_cache(maxsize=len(sendbuf._original_data))
    def _cached(i):
        i_target_indices = cupy.asarray(rdispls[(source_bounds[i-1] if i else 0):source_bounds[i]])
        i_target_block_ids = cupy.sum(cupy.expand_dims(i_target_indices, axis=-1) >= cupy.asarray(target_bounds), axis=-1, keepdims=False)
        return i_target_indices, i_target_block_ids

    for i in range(len(sendbuf._original_data)):
        for j in range(len(recvbuf._original_data)):
            # gather
            with getattr(sendbuf._original_data[i], 'device', nullcontext()):
                i_target_indices, i_target_block_ids = _cached(i)
                gather_mask = (cupy.asarray(i_target_block_ids) == j)
                buf = sendbuf._original_data[i][gather_mask]
            with getattr(recvbuf._original_data[j], 'device', nullcontext()):
                scatter_mask = cupy.asarray(gather_mask)
                scatter_indices_local = cupy.asarray(i_target_indices)[scatter_mask] - (target_bounds[j-1] if j else 0)
                # assert sum(scatter_mask) == len(scatter_indices_local)
                assert not debug or cupy.allclose(recvbuf._original_data[j][scatter_indices_local], cupy.asarray(buf))
                recvbuf._original_data[j][scatter_indices_local] = cupy.asarray(buf)
            # scatter

def alltoall(target, target_indices, source, source_indices):
    with getattr(target_indices, 'device', nullcontext()):
        target_block_ids = target_indices
    with getattr(source_indices, 'device', nullcontext()):
        source_block_ids = source_indices

    for i in range(len(sendbuf._original_data)):
        for j in range(len(recvbuf._original_data)):
            # gather
            with getattr(sendbuf._original_data[i], 'device', nullcontext()):
                if target_indices is None:
                    source_indices[(target_bounds[j-1] if j else 0):target_bounds[j]]
                g_source_indices = source_indices[target_block_id == j] 
                j_source_block_id = g_source_indices

                ij_source_mask = (j_source_block_id == i)
                ij_gather_indices_global = g_source_indices[source_mask]
                ij_gather_indices_local = ij_gather_indices_global
                buf = sendbuf._original_data[i][gather_indices_local]
            # scatter
            with getattr(recvbuf._original_data[j], 'device', nullcontext()):
                j_global_indices = target_indices[target_block_id == j][ij_source_mask]
                j_local_indices = j_global_indices
                recvbuf._original_data[j][j_local_indices] = buf


def assignment(left, left_indices, right, right_indices):
    if left_indices is None:
        alltoallv(right, right_indices, left)
    elif right_indices is None:
        all2ints(right, left, left_indices)
    else:
        alltoall(left, left_indices, right, right_indices)