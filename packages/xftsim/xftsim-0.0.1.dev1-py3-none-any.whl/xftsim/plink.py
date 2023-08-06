import warnings
import numpy as np
import numba as nb
import pandas as pd
import nptyping as npt
import xarray as xr
from nptyping import NDArray, Int8, Int64, Float64, Bool, Shape, Float, Int
from typing import Any, Hashable, List, Iterable, Callable, Union, Dict
from functools import cached_property
import pandas_plink as pp
from dask.diagnostics import ProgressBar
pbar= ProgressBar()

import xftsim as xft

path = "/u/scratch/r/ribo7412/plinksub/random16k_merged.bed"
def plink_bfile_to_pseduo_haplotypes(path: str):

delayed_plink = pp.read_plink1_bin(path)
plink1_variant_index

@nb.njit
def _genotypes_to_pseudo_haplotypes(genotypes):
    haplotypes = np.zeros((genotypes.shape[0],genotypes.shape[1]*2), dtype=np.int8)
    zero_one = np.array([0,1], dtype=np.int8)
    one_one = np.array([1,1], dtype=np.int8)
    zero_zero = np.array([1,1], dtype=np.int8)
    for j in nb.prange(genotypes.shape[1]):
        for i in range(genotypes.shape[0]):
            if genotypes[i,j]==1:
                haplotypes[i,(2*j):(2*j+2)] = np.random.permutation(zero_one)
            elif genotypes[i,j]==2:
                haplotypes[i,(2*j):(2*j+2)] = one_one
    return haplotypes


def genotypes_to_pseudo_haplotypes(x):
    out = x[:,np.repeat(np.arange(x.shape[1]),2)]
    out.values = _genotypes_to_pseudo_haplotypes(x.values)
    return out



def plink1_variant_index(ppxr: xr.DataArray) -> xft.index.DiploidVariantIndex:
    return xft.index.DiploidVariantIndex(
                                         vid = ppxr.snp.values,
                                         chrom = ppxr.chrom.values,
                                         zero_allele = ppxr.a0.values,
                                         one_allele = ppxr.a1.values,
                                         pos_bp = ppxr.pos,
                                         )

def plink1_sample_index(ppxr: xr.DataArray, 
                       generation: int = 0) -> xft.index.SampleIndex:
    return xft.index.SampleIndex(
                                 iid = ppxr.iid.values.astype(str),
                                 fid = ppxr.fid.values.astype(str),
                                 sex = 2 - ppxr.gender.values.astype(int),
                                 generation = generation,
                                 )

class SampleIndex(XftIndex):
    def __init__(self,
                 iid: Iterable = None, ## individual id
                 fid: Iterable = None, ## family id
                 sex: Iterable = None, ## biological sex
                 frame: pd.DataFrame = None,
                 n: int = None,
                 generation: int = 0,
                 ):



def plink_variant_index(ppxr: xr.DataArray):
    return xft.index.DiploidVariantIndex(
                                         vid = ppxr.snp.values,
                                         chrom = ppxr.chrom.values,
                                         zero_allele = ppxr.a0.values,
                                         one_allele = ppxr.a1.values,
                                         pos_bp = ppxr.pos,
                                         )



    @staticmethod
    def from_pandas_plink_xr(ppxr: xr.DataArray):
        return HaploidVariantIndex(
                                   vid = ppxr.snp.values,
                                   chrom = ppxr.chrom.values,
                                   zero_allele = ppxr.a0.values,
                                   one_allele = ppxr.a1.values,
                                   pos_bp = ppxr.pos,
                                   )
