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