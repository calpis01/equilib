#!/usr/bin/env python3

import numpy as np

import torch

from equilib.torch_utils.func import get_device

from tests.grid_sample.numpy.bicubic import (
    faster_bicubic as faster_bicubic_numpy,
)
from tests.grid_sample.torch.native import native_bicubic
from tests.grid_sample.helpers import create_batch_data, make_copies
from tests.helpers.benchmarking import check_close, mae, mse
from tests.helpers.timer import func_timer


def naive_bicubic(img: torch.Tensor, grid: torch.Tensor) -> torch.Tensor:
    ...


def faster_bicubic(
    img: torch.Tensor, grid: torch.Tensor, out: torch.Tensor
) -> torch.Tensor:

    b_in, c_in, h_in, w_in = img.shape
    b_out, _, h_out, w_out = out.shape
    dtype = out.dtype
    device = get_device(out)

    # NOTE: hardcoded since pytorch uses -0.75
    a = -0.75

    def kernel(s, a):
        out = torch.zeros_like(s)
        s = torch.abs(s)
        mask1 = torch.logical_and(0 <= s, s <= 1)
        mask2 = torch.logical_and(1 < s, s <= 2)
        out[mask1] = (a + 2) * (s[mask1] ** 3) - (a + 3) * (s[mask1] ** 2) + 1
        out[mask2] = (
            a * (s[mask2] ** 3)
            - (5 * a) * (s[mask2] ** 2)
            + (8 * a) * s[mask2]
            - 4 * a
        )
        return out

    int_dtype = torch.int64

    min_grid = torch.floor(grid).type(int_dtype)

    d1 = 1 + (grid - min_grid)
    d2 = grid - min_grid
    d3 = min_grid + 1 - grid
    d4 = min_grid + 2 - grid

    c1 = (grid - d1).type(int_dtype)
    c2 = (grid - d2).type(int_dtype)
    c3 = (grid + d3).type(int_dtype)
    c4 = (grid + d4).type(int_dtype)

    c1[:, 0, ...] %= h_in
    c1[:, 1, ...] %= w_in
    c2[:, 0, ...] %= h_in
    c2[:, 1, ...] %= w_in
    c3[:, 0, ...] %= h_in
    c3[:, 1, ...] %= w_in
    c4[:, 0, ...] %= h_in
    c4[:, 1, ...] %= w_in

    k1 = kernel(d1, a).type(dtype)
    k2 = kernel(d2, a).type(dtype)
    k3 = kernel(d3, a).type(dtype)
    k4 = kernel(d4, a).type(dtype)

    mat_l = torch.stack(
        [k1[:, 1, ...], k2[:, 1, ...], k3[:, 1, ...], k4[:, 1, ...]], dim=-1
    ).to(device)
    mat_r = torch.stack(
        [k1[:, 0, ...], k2[:, 0, ...], k3[:, 0, ...], k4[:, 0, ...]], dim=-1
    ).to(device)

    mat_m = torch.empty(
        (b_out, c_in, h_out, w_out, 4, 4), dtype=dtype, device=device
    )
    for b in range(b_out):
        y1 = c1[b, 0, ...]  # (h, w)
        y2 = c2[b, 0, ...]
        y3 = c3[b, 0, ...]
        y4 = c4[b, 0, ...]

        x1 = c1[b, 1, ...]
        x2 = c2[b, 1, ...]
        x3 = c3[b, 1, ...]
        x4 = c4[b, 1, ...]

        mat_m_x1 = torch.stack(
            [
                img[b][:, y1, x1],  # (c, h, w)
                img[b][:, y2, x1],
                img[b][:, y3, x1],
                img[b][:, y4, x1],
            ],
            dim=-1,
        )
        mat_m_x2 = torch.stack(
            [
                img[b][:, y1, x2],
                img[b][:, y2, x2],
                img[b][:, y3, x2],
                img[b][:, y4, x2],
            ],
            dim=-1,
        )
        mat_m_x3 = torch.stack(
            [
                img[b][:, y1, x3],
                img[b][:, y2, x3],
                img[b][:, y3, x3],
                img[b][:, y4, x3],
            ],
            dim=-1,
        )
        mat_m_x4 = torch.stack(
            [
                img[b][:, y1, x4],
                img[b][:, y2, x4],
                img[b][:, y3, x4],
                img[b][:, y4, x4],
            ],
            dim=-1,
        )

        mat_m[b, ...] = torch.stack(
            [mat_m_x1, mat_m_x2, mat_m_x3, mat_m_x4], dim=-2
        )

    mat_l = mat_l.unsqueeze(1).unsqueeze(-2)
    mat_r = mat_r.unsqueeze(1).unsqueeze(-1)
    out = (mat_l @ mat_m @ mat_r).squeeze(-1).squeeze(-1)

    return out


def compare_baseline():

    dtype_img = dtype_grid = np.dtype(np.float32)
    b = 1
    c = 3
    h = 256
    w = 512
    h_grid = 64
    w_grid = 128

    img, grid, out = create_batch_data(
        b=b,
        c=c,
        h=h,
        w=w,
        h_grid=h_grid,
        w_grid=w_grid,
        move_grid=True,
        rand_img=False,
        rand_grid=False,
        dtype_img=dtype_img,
        dtype_grid=dtype_grid,
    )

    # initialize outputs:
    out_numpy = make_copies(out)
    out_native = make_copies(out)
    out_torch = torch.from_numpy(make_copies(out))

    out_numpy = func_timer(faster_bicubic_numpy)(img, grid, out_numpy)
    out_numpy = torch.from_numpy(out_numpy)

    img = torch.from_numpy(img)
    grid = torch.from_numpy(grid)

    out_torch = func_timer(faster_bicubic)(img, grid, out_torch)

    print("\nChecking: numpy vs torch")
    print("close?", check_close(out_numpy, out_torch))
    print("MSE", mse(out_numpy, out_torch))
    print("MAE", mae(out_numpy, out_torch))

    out_native = func_timer(native_bicubic)(img.clone(), grid.clone())

    print("\nChecking: numpy vs native")
    print("close?", check_close(out_numpy, out_native))
    print("MSE", mse(out_numpy, out_native))
    print("MAE", mae(out_numpy, out_native))


if __name__ == "__main__":
    compare_baseline()
