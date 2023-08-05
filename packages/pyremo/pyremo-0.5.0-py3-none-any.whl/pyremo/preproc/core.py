"""core module for preprocessing

This module wraps the pyintorg interfaces into xr.apply_ufunc.

"""

import warnings

import cf_xarray as cfxr
import numpy as np
import xarray as xr

xr.set_options(keep_attrs=True)

try:
    from pyintorg import interface as intf
except Exception:
    warnings.warn(
        "could not find pyintorg, you need this for preprocessing. Please consider installing it from https://gitlab.dkrz.de/remo/pyintorg.git"
    )

from .constants import lev, lev_gm, lev_i


class const:
    """constants used for unit conversion"""

    grav_const = 9.806805923
    absolute_zero = 273.5


def pbl_index(akgm, bkgm):
    return intf.pbl_index(akgm, bkgm)


def open_mfdataset(
    files,
    use_cftime=True,
    parallel=True,
    data_vars="minimal",
    chunks={},
    coords="minimal",
    compat="override",
    drop=None,
    **kwargs
):
    """optimized function for opening CMIP6 6hrLev 3d datasets

    based on https://github.com/pydata/xarray/issues/1385#issuecomment-561920115

    """

    def drop_all_coords(ds):
        # ds = ds.drop(drop)
        return ds.reset_coords(drop=True)

    ds = xr.open_mfdataset(
        files,
        parallel=parallel,
        decode_times=False,
        combine="by_coords",
        preprocess=drop_all_coords,
        decode_cf=False,
        chunks=chunks,
        data_vars=data_vars,
        coords="minimal",
        compat="override",
        **kwargs,
    )
    return xr.decode_cf(ds, use_cftime=use_cftime)


def get_akbkem(vc):
    """create vertical coordinate dataset"""
    akbk = vc.to_xarray().drop("index")
    # bkem = pr.tables.vc.tables['vc_27lev']
    akem = akbk.ak.swap_dims({"index": lev_i})
    bkem = akbk.bk.swap_dims({"index": lev_i})
    akhem = (0.5 * (akbk.ak[:-1] + akbk.ak[1:])).swap_dims({"index": lev})
    bkhem = (0.5 * (akbk.bk[:-1] + akbk.bk[1:])).swap_dims({"index": lev})
    akem[lev_i] = xr.DataArray(np.arange(1, akem.size + 1), dims=lev_i)
    bkem[lev_i] = xr.DataArray(np.arange(1, bkem.size + 1), dims=lev_i)
    akhem[lev] = xr.DataArray(np.arange(1, akhem.size + 1), dims=lev, name="akh")
    bkhem[lev] = xr.DataArray(np.arange(1, bkhem.size + 1), dims=lev, name="bkh")
    akhem.name = "akh"
    bkhem.name = "bkh"
    return xr.merge([akem, bkem, akhem, bkhem])
    # return akem, bkem, akhem, bkhem


def horizontal_dims(da):
    for dim in da.dims:
        if "lon" in dim:
            lon_dim = dim
        if "lat" in dim:
            lat_dim = dim
    return (lon_dim, lat_dim)


def intersect(lamgm, phigm, lamem, phiem):
    gcm_dims = list(horizontal_dims(lamgm))
    rcm_dims = list(horizontal_dims(lamem))
    rcm_dims.append("pos")
    out_dims = rcm_dims
    result = xr.apply_ufunc(
        intf.intersection_points,  # first the function
        lamgm * 1.0 / 57.296,  # now arguments in the order expected by 'druint'
        phigm * 1.0 / 57.296,
        lamem * 1.0 / 57.296,
        phiem * 1.0 / 57.296,
        input_core_dims=[
            gcm_dims,
            gcm_dims,
            rcm_dims,
            rcm_dims,
        ],  # list with one entry per arg
        # returned data has 3 dimensions
        output_core_dims=[out_dims, out_dims],
        dask="parallelized",
        output_dtypes=[lamgm.dtype],
    )
    return result


def compute_relative_pol(polphihm, pollamhm, polphiem, pollamem):
    """python implementation of pol calculation in readni"""
    import intorg
    import numpy as np

    if polphihm == polphiem and pollamhm == pollamem:
        pollam = 0.0
        polphi = 90.0
        polgam = 180.0
    else:
        # SK      POLGAM = - ZRPI18*ASIN(SIN(POLLAM*ZPIR18)  *
        # SK     1                     COS(POLPHIEM*ZPIR18)/COS(POLPHIHM*ZPIR18))
        # SK     2         - 180.0
        zrpi18 = 57.2957795  # rad2deg
        zpir18 = 0.0174532925  # deg2rad
        polgam = -zrpi18 * np.arcsin(
            np.cos(zpir18 * polphiem)
            * np.sin(zpir18 * (pollamhm - pollamem))
            / np.cos(zpir18 * intorg.phtophs(polphiem, pollamem, polphihm, pollamhm))
        )
        polphi = intorg.phtophs(polphihm, pollamhm, polphiem, pollamem)
        pollam = intorg.lmtolms(polphihm, pollamhm, polphiem, pollamem)
    return {"pollam": pollam, "polphi": polphi, "polgam": polgam}


def intersect_regional(em, hm):
    def get_arguments(em, hm):
        args = {}
        args["lamluem"] = em["ll_lon"]
        args["philuem"] = em["ll_lat"]
        args["lamluhm"] = hm["ll_lon"]
        args["philuhm"] = hm["ll_lat"]
        args["dlamem"] = em["dlon"]
        args["dlamhm"] = hm["dlon"]
        args["dphiem"] = em["dlat"]
        args["dphihm"] = hm["dlat"]
        args["pollamem"] = em["pollon"]
        args["polphiem"] = em["pollat"]
        args["pollamhm"] = hm["pollon"]
        args["polphihm"] = hm["pollat"]
        args["ieem"] = em["nlon"]
        args["jeem"] = em["nlat"]
        args["ie2hm"] = hm["nlon"] + 2
        args["je2hm"] = hm["nlat"] + 2
        return args

    args = get_arguments(em, hm)
    args.update(
        compute_relative_pol(
            args["polphihm"], args["pollamhm"], args["polphiem"], args["pollamem"]
        )
    )
    indemi, indemj, dxemhm, dyemhm = intf.intersection_points_regional(**args)
    dims = ("rlon", "rlat", "pos")
    indemi = xr.DataArray(indemi, dims=dims, name="indemi")
    indemj = xr.DataArray(indemj, dims=dims, name="indemj")
    dxemhm = xr.DataArray(dxemhm, dims=dims, name="dxemhm")
    dyemhm = xr.DataArray(dyemhm, dims=dims, name="dyemhm")
    return indemi, indemj, dxemhm, dyemhm


def interpolate_horizontal(
    da,
    lamem,
    phiem,
    lamgm,
    phigm,
    name=None,
    igr=None,
    blagm=None,
    blaem=None,
    indii=None,
    indjj=None,
):
    if name is None:
        name = da.name
    if igr is None:
        igr = 0
    if indii is None or indjj is None:
        indii, indjj = intersect(lamgm, phigm, lamem, phiem)
    if blagm is None or blaem is None:
        return interp_horiz(
            da,
            lamgm,
            phigm,
            lamem.isel(pos=igr),
            phiem.isel(pos=igr),
            indii.isel(pos=igr),
            indjj.isel(pos=igr),
            name,
        )
    else:
        return interp_horiz_cm(
            da,
            lamgm,
            phigm,
            lamem.isel(pos=igr),
            phiem.isel(pos=igr),
            indii.isel(pos=igr),
            indjj.isel(pos=igr),
            name,
            blagm,
            blaem,
        )


def interpolate_horizontal_remo(
    da, indemi, indemj, dxemhm, dyemhm, name=None, igr=None, blaem=None, blahm=None
):
    if name is None:
        name = da.name
    if igr is None:
        igr = 0
    if blaem is None or blahm is None:
        return interp_horiz_remo(
            da,
            indemi.isel(pos=igr),
            indemj.isel(pos=igr),
            dxemhm.isel(pos=igr),
            dyemhm.isel(pos=igr),
            name,
        )
    else:
        return interp_horiz_remo_cm(
            da,
            indemi.isel(pos=igr),
            indemj.isel(pos=igr),
            dxemhm.isel(pos=igr),
            dyemhm.isel(pos=igr),
            name,
            blaem,
            blahm,
        )


# def interp_horiz_2d(field, lamgm, phigm, lamem, phiem, indii, indjj, name):
#     """interpolates 2d global data horizontally.

#     Interpolates 2d data from the global grid to the regional grid.
#     """
#     #from intorg import intorg
#     return intf.hiobla(field, lamgm, phigm, lamem, phiem, indii, indjj, name)


# def interp_horiz_2d_cm(field, lamgm, phigm, lamem, phiem, indii, indjj, name):
#     """interpolates 2d global data horizontally.

#     Interpolates 2d data from the global grid to the regional grid.
#     """
#     from intorg import intorg
#     return intorg.hiobla(field, lamgm, phigm, lamem, phiem, indii, indjj, name)


def interp_horiz(da, lamgm, phigm, lamem, phiem, indii, indjj, name, keep_attrs=False):
    """main interface"""
    gcm_dims = list(horizontal_dims(lamgm))
    rcm_dims = list(horizontal_dims(lamem))
    input_core_dims = [
        gcm_dims,
        gcm_dims,
        gcm_dims,
        rcm_dims,
        rcm_dims,
        rcm_dims,
        rcm_dims,
        [],
    ]
    result = xr.apply_ufunc(
        intf.interp_horiz_2d,  # first the function
        da,  # now arguments in the order expected
        lamgm * 1.0 / 57.296,
        phigm * 1.0 / 57.296,
        lamem * 1.0 / 57.296,
        phiem * 1.0 / 57.296,
        indii,
        indjj,
        name,
        input_core_dims=input_core_dims,  # list with one entry per arg
        output_core_dims=[rcm_dims],  # returned data has 3 dimensions
        vectorize=True,  # loop over non-core dims, in this case: time
        #  exclude_dims=set(("lev",)),  # dimensions allowed to change size. Must be a set!
        dask="parallelized",
        dask_gufunc_kwargs={"allow_rechunk": True},
        output_dtypes=[da.dtype],
    )

    result.name = name
    # result = result.to_dataset()
    if keep_attrs:
        result.attrs = da.attrs
    # result = result.transpose(..., *spatial_dims(da)[::-1])
    return result


def interp_horiz_remo(da, indemi, indemj, dxemhm, dyemhm, name, keep_attrs=False):
    """main interface"""
    em_dims = list(horizontal_dims(da))
    hm_dims = list(horizontal_dims(indemj))
    input_core_dims = [em_dims] + 4 * [hm_dims] + [[]]
    # return
    result = xr.apply_ufunc(
        intf.interp_horiz_remo_2d,  # first the function
        da,  # now arguments in the order expected
        indemi,
        indemj,
        dxemhm,
        dyemhm,
        name,
        input_core_dims=input_core_dims,  # list with one entry per arg
        output_core_dims=[hm_dims],  # returned data has 3 dimensions
        vectorize=True,  # loop over non-core dims, in this case: time, lev
        #  exclude_dims=set(("lev",)),  # dimensions allowed to change size. Must be a set!
        dask="parallelized",
        dask_gufunc_kwargs={"allow_rechunk": True},
        output_dtypes=[da.dtype],
    )

    result.name = name
    # result = result.to_dataset()
    if keep_attrs:
        result.attrs = da.attrs
    # result = result.transpose(..., *spatial_dims(da)[::-1])
    return result


def interp_horiz_cm(
    da, lamgm, phigm, lamem, phiem, indii, indjj, name, blagm, blaem, keep_attrs=False
):
    """main interface"""
    gcm_dims = list(horizontal_dims(lamgm))
    rcm_dims = list(horizontal_dims(lamem))
    input_core_dims = [
        gcm_dims,
        gcm_dims,
        rcm_dims,
        gcm_dims,
        gcm_dims,
        rcm_dims,
        rcm_dims,
        rcm_dims,
        rcm_dims,
        [],
    ]
    result = xr.apply_ufunc(
        intf.interp_horiz_2d_cm,  # first the function
        da,  # now arguments in the order expected
        blagm,
        blaem,
        lamgm * 1.0 / 57.296,
        phigm * 1.0 / 57.296,
        lamem * 1.0 / 57.296,
        phiem * 1.0 / 57.296,
        indii,
        indjj,
        name,
        # dataset_fill_value=1.e20,
        input_core_dims=input_core_dims,  # list with one entry per arg
        output_core_dims=[rcm_dims],  # returned data has 3 dimensions
        vectorize=True,  # loop over non-core dims, in this case: time
        #  exclude_dims=set(("lev",)),  # dimensions allowed to change size. Must be a set!
        dask="parallelized",
        dask_gufunc_kwargs={"allow_rechunk": True},
        output_dtypes=[da.dtype],
    )

    result.name = name
    # result = result.to_dataset()
    if keep_attrs:
        result.attrs = da.attrs
    # result = result.transpose(..., *spatial_dims(da)[::-1])
    return result


def interp_horiz_remo_cm(
    da,
    indemi,
    indemj,
    dxemhm,
    dyemhm,
    blaem,
    blahm,
    phiem,
    lamem,
    phihm,
    lamhm,
    name,
    lice=None,
    siceem=None,
    sicehm=None,
    keep_attrs=False,
):
    """main interface"""
    em_dims = list(horizontal_dims(da))
    hm_dims = list(horizontal_dims(indemj))
    input_core_dims = (
        [em_dims]
        + 4 * [hm_dims]
        + [em_dims]
        + [hm_dims]
        + 2 * [em_dims]
        + 2 * [hm_dims]
        + [[]]
    )
    ice_args = ()
    if lice is False:
        input_core_dims += [[]] + [em_dims] + [hm_dims]
        ice_args = (lice, siceem, sicehm)
    # return
    result = xr.apply_ufunc(
        intf.interp_horiz_remo_2d_cm,  # first the function
        da,  # now arguments in the order expected
        indemi.isel(pos=0),
        indemj.isel(pos=0),
        dxemhm.isel(pos=0),
        dyemhm.isel(pos=0),
        blaem,
        blahm,
        phiem * 1.0 / 57.296,
        lamem * 1.0 / 57.296,
        phihm.isel(pos=0) * 1.0 / 57.296,
        lamhm.isel(pos=0) * 1.0 / 57.296,
        name,
        *ice_args,
        input_core_dims=input_core_dims,  # list with one entry per arg
        output_core_dims=[hm_dims],  # returned data has 3 dimensions
        vectorize=True,  # loop over non-core dims, in this case: time, lev
        #  exclude_dims=set(("lev",)),  # dimensions allowed to change size. Must be a set!
        dask="parallelized",
        dask_gufunc_kwargs={"allow_rechunk": True},
        output_dtypes=[da.dtype],
    )

    result.name = name
    # result = result.to_dataset()
    if keep_attrs:
        result.attrs = da.attrs
    # result = result.transpose(..., *spatial_dims(da)[::-1])
    return result


def geopotential(fibgm, tgm, qdgm, psgm, akgm, bkgm):
    """main interface"""
    # gcm_dims = list(spatial_dims(lamgm))
    twoD_dims = list(horizontal_dims(fibgm))
    threeD_dims = list(horizontal_dims(fibgm))
    threeD_dims.append(lev_gm)
    # lev_dims.append("lev")
    # plev_dims = list(spatial_dims(da))
    # plev_dims.append("plev")
    # nlev = a.dims[0]
    input_core_dims = [
        twoD_dims,
        threeD_dims,
        threeD_dims,
        twoD_dims,
        list(akgm.dims),
        list(bkgm.dims),
        # [],
        # []
    ]
    # print(input_core_dims)
    result = xr.apply_ufunc(
        intf.geopotential,  # first the function
        fibgm,  # now arguments in the order expected
        tgm,
        qdgm,
        psgm,
        akgm,
        bkgm,
        input_core_dims=input_core_dims,  # list with one entry per arg
        #  output_core_dims=[threeD_dims],  # returned data has 3 dimensions
        output_core_dims=[twoD_dims],  # returned data has 3 dimensions
        vectorize=True,  # loop over non-core dims, in this case: time
        # exclude_dims=set(("lev",)),  # dimensions allowed to change size. Must be a set!
        dask="parallelized",
        dask_gufunc_kwargs={"allow_rechunk": True},
        output_dtypes=[fibgm.dtype],
    )
    return result


def relative_humidity(qdgm, tgm, psgm, akgm, bkgm, qwgm=None):
    """main interface"""
    if qwgm is None:
        qwgm = xr.zeros_like(qdgm)
    twoD_dims = list(horizontal_dims(qdgm))
    threeD_dims = list(horizontal_dims(qdgm)) + [lev_gm]
    #  print(twoD_dims)
    # threeD_dims.append("lev")
    input_core_dims = [
        threeD_dims,
        threeD_dims,
        twoD_dims,
        [akgm.dims[0]],
        [bkgm.dims[0]],
        threeD_dims,
    ]
    result = xr.apply_ufunc(
        intf.relative_humidity,  # first the function
        qdgm,  # now arguments in the order expected
        tgm,
        psgm,
        akgm,
        bkgm,
        qwgm,
        input_core_dims=input_core_dims,  # list with one entry per arg
        #  output_core_dims=[threeD_dims],  # returned data has 3 dimensions
        output_core_dims=[threeD_dims],  # returned data has 3 dimensions
        vectorize=True,  # loop over non-core dims, in this case: time
        # exclude_dims=set(("lev",)),  # dimensions allowed to change size. Must be a set!
        dask="parallelized",
        dask_gufunc_kwargs={"allow_rechunk": True},
        output_dtypes=[qdgm.dtype],
    )
    return result


def geo_coords(domain_info, rlon, rlat):
    import numpy as np

    ll_lam = domain_info["ll_lon"]  # * 1.0/57.296
    ll_phi = domain_info["ll_lat"]  # * 1.0/57.296
    dlam = domain_info["dlon"]
    dphi = domain_info["dlat"]
    nlam = domain_info["nlon"]
    nphi = domain_info["nlat"]
    pollam = domain_info["pollon"]
    polphi = domain_info["pollat"]
    lamem, phiem = intf.geo_coords(
        ll_lam, ll_phi, dlam, dphi, pollam, polphi, nlam + 2, nphi + 2
    )
    lamda = xr.DataArray(
        np.rad2deg(lamem),
        dims=("rlon", "rlat", "pos"),
        coords={"rlon": rlon, "rlat": rlat},
    )
    phida = xr.DataArray(
        np.rad2deg(phiem),
        dims=("rlon", "rlat", "pos"),
        coords={"rlon": rlon, "rlat": rlat},
    )
    return lamda, phida


# def get_vc(ds):
#    """Reads the vertical hybrid coordinate from a dataset."""
#    ak_valid = ["ap_bnds", "a_bnds"]
#    bk_valid = ["b_bnds"]
#    ak_bnds = None
#    bk_bnds = None
#    for ak_name in ak_valid:
#        if ak_name in ds:
#            ak_bnds = ds[ak_name]
#            print("using {} for akgm".format(ak_name))
#    for bk_name in bk_valid:
#        if bk_name in ds:
#            bk_bnds = ds[bk_name]
#            print("using {} for bkgm".format(bk_name))
#    #    if not all([ak_bnds, bk_bnds]):
#    #        print('could not identify vertical coordinate, tried: {}, {}'.format(ak_valid, bk_valid))
#    #        raise Exception('incomplete input dataset')
#    #        ak_bnds, bk_bnds  = (ak_bnds[:1], bk_bnds[:,1])
#    nlev = ak_bnds.shape[0]
#    ak = np.zeros([nlev + 1], dtype=np.float64)
#    bk = np.ones([nlev + 1], dtype=np.float64)
#    if ds.lev.positive == "down":
#        ak[:-1] = np.flip(ak_bnds[:, 1])
#        bk[:-1] = np.flip(bk_bnds[:, 1])
#    else:
#        ak[1:] = np.flip(ak_bnds[:, 1])
#        bk[1:] = np.flip(bk_bnds[:, 1])
#
#    return xr.DataArray(ak, dims="lev_2"), xr.DataArray(bk, dims="lev_2")


def get_vc(ds):
    """Reads the vertical hybrid coordinate from a dataset."""
    ak_valid = ["ap_bnds", "a_bnds"]
    bk_valid = ["b_bnds"]
    ak_bnds = None
    bk_bnds = None
    for ak_name in ak_valid:
        if ak_name in ds:
            ak_bnds = ds[ak_name]
            print("using {} for akgm".format(ak_name))
    for bk_name in bk_valid:
        if bk_name in ds:
            bk_bnds = ds[bk_name]
            print("using {} for bkgm".format(bk_name))
    #    if not all([ak_bnds, bk_bnds]):
    #        print('could not identify vertical coordinate, tried: {}, {}'.format(ak_valid, bk_valid))
    #        raise Exception('incomplete input dataset')
    #        ak_bnds, bk_bnds  = (ak_bnds[:1], bk_bnds[:,1])
    nlev = ak_bnds.shape[0]
    ak = np.zeros([nlev + 1], dtype=np.float64)
    bk = np.ones([nlev + 1], dtype=np.float64)
    if ds.lev.positive == "down":
        ak[:-1] = np.flip(ak_bnds[:, 1])
        bk[:-1] = np.flip(bk_bnds[:, 1])
    else:
        ak[1:] = np.flip(ak_bnds[:, 1])
        bk[1:] = np.flip(bk_bnds[:, 1])

    return xr.DataArray(ak, dims="lev_2"), xr.DataArray(bk, dims="lev_2")


def get_ab_bnds(ds):
    ak_valid = ["ap_bnds", "a_bnds", "hyai"]
    bk_valid = ["b_bnds", "hybi"]
    ak_bnds = None
    bk_bnds = None
    for ak_name in ak_valid:
        if ak_name in ds:
            ak_bnds = ds[ak_name]
            print("using {} for akgm".format(ak_name))
    for bk_name in bk_valid:
        if bk_name in ds:
            bk_bnds = ds[bk_name]
            print("using {} for bkgm".format(bk_name))
    return ak_bnds, bk_bnds


def get_vc2(ds):
    """Reads the vertical hybrid coordinate from a dataset."""
    ak_bnds, bk_bnds = get_ab_bnds(ds)
    if ak_bnds.ndim > 1:
        ak = cfxr.bounds_to_vertices(ak_bnds, bounds_dim="bnds")
        bk = cfxr.bounds_to_vertices(bk_bnds, bounds_dim="bnds")
    else:
        ak = ak_bnds
        bk = bk_bnds
    try:
        if ak_bnds.cf["vertical"].positive == "down":
            ak = np.flip(ak)
    except Exception:
        pass
    try:
        if bk_bnds.cf["vertical"].positive == "down":
            bk = np.flip(bk)
    except Exception:
        pass
    ak.name = "akgm"
    bk.name = "bkgm"
    return ak, bk


def map_sst(tos, ref_ds, resample="6H", regrid=True):
    from datetime import timedelta as td

    import xesmf as xe

    try:
        tos = tos.to_dataset()
    except Exception:
        pass
    # tos_res = tos
    attrs = tos.tos.attrs
    tos_times = (ref_ds.time.min() - td(days=1), ref_ds.time.max() + td(days=1))
    tos = tos.sel(time=slice(tos_times[0], tos_times[1]))
    # return tos_res
    # tos = tos.resample(time=resample).interpolate("linear").chunk({"time": 1})
    tos = tos.resample(time=resample).interpolate("linear")
    tos = tos.sel(time=ref_ds.time)

    if regrid:
        ref_ds["mask"] = ~(ref_ds.sftlf > 0)
        tos["mask"] = ~tos.tos.isel(time=0).isnull().squeeze(drop=True)
        regridder = xe.Regridder(tos, ref_ds, "nearest_s2d")
        tos = regridder(tos.tos)
    tos.attrs.update(attrs)

    return tos


def convert_units(ds):
    """convert units for use in the preprocessor"""
    try:
        if ds.sftlf.units == "%":
            print("converting sftlf units to fractional")
            attrs = ds.sftlf.attrs
            ds["sftlf"] = ds.sftlf * 0.01
            attrs["units"] = 1
            ds.sftlf.attrs = attrs
    except Exception:
        warnings.warn("sftlf has no units attribute, must be fractional.")
    try:
        if ds.tos.units == "degC":
            print("converting tos units to K")
            attrs = ds.tos.attrs
            ds["tos"] = ds.tos + const.absolute_zero
            attrs["units"] = "K"
            ds.tos.attrs = attrs
    except Exception:
        warnings.warn("tos has no units attribute, must be Kelvin!")
    try:
        if ds.orog.units == "m":
            print("converting orography to geopotential")
            attrs = ds.orog.attrs
            ds["orog"] = ds.orog * const.grav_const
            attrs["units"] = "m2 s-2"
            ds.orog.attrs = attrs
    except Exception:
        warnings.warn("orog has no units attribute, must be m2 s-2")
    return ds


def check_lev(ds):
    if "vertical" in ds.cf:
        positive = ds.cf["vertical"].attrs.get("positive", None)
    else:
        positive = None
    if positive is None:
        warnings.warn("could not determine positive attribute of vertical axis.")
        return ds
    elif positive == "down":
        kwargs = {ds.cf["vertical"].name: ds.cf["vertical"][::-1]}
        return ds.reindex(**kwargs)
    return ds


def open_datasets(datasets, ref_ds=None, time_range=None):
    """Creates a virtual gfile"""
    if ref_ds is None:
        try:
            ref_ds = open_mfdataset(datasets["ta"])
        except Exception:
            raise Exception("ta is required in the datasets dict if no ref_ds is given")
    lon, lat = horizontal_dims(ref_ds)
    # ak_bnds, bk_bnds = get_ab_bnds(ref_ds)
    if time_range is None:
        time_range = ref_ds.time
    dsets = []
    for var, f in datasets.items():
        try:
            da = open_mfdataset(f, chunks={"time": 1})[var]
            da = da.sel(time=time_range)
        except Exception:
            da = open_mfdataset(f, chunks={})[var]
        if "vertical" in da.cf:
            da = check_lev(da)
        dsets.append(da)
    dsets += list(get_vc2(ref_ds))
    output = xr.merge(dsets, compat="override", join="override")
    output.attrs = ref_ds.attrs
    return output


def gfile(ds, ref_ds=None, tos=None, time_range=None, attrs=None):
    """Creates a global dataset ready for preprocessing.

    This function creates a homogenized global dataset. If neccessary,
    units are converted and the sea surface temperature ``tos`` is
    interpolated spatially and temporally to the atmospheric grid.

    Parameters
    ----------
    ds : xarray.Dataset or dict of filenames
        Input dataset from a global model according to CF conventions.

    ref_ds : xarray.Dataset
        Reference datasets that is used for determining the grid and vertical
        coordinates and the global attributes. If ``ref_ds=None``, ``ta`` from
        the input dataset is used as a reference.

    tos : xarray.Dataset
        Sea surface dataset.

    time_rage :
        The common time range from the input and sst that should be used.

    attrs:
        Global attributes for the output dataset. If ``attrs=None``, the global
        attributes from ``ref_ds`` are used.

    Returns
    -------
    gfile : xarray.Dataset
        Global dataset ready for preprocessing.

    """
    if isinstance(ds, dict):
        ds = open_datasets(ds, ref_ds, time_range)
        if time_range is None:
            time_range = ds.time
    else:
        ds = ds.copy()
        if time_range is None:
            time_range = ds.time
        ds = ds.sel(time=time_range)
        ds["akgm"], ds["bkgm"] = get_vc2(ds)
        ds = check_lev(ds)
    if tos is not None:
        ds["tos"] = map_sst(tos, ds.sel(time=time_range))
    ds = ds.rename({"lev": lev_gm})
    ds = convert_units(ds)
    # if "sftlf" in ds:
    #    ds["sftlf"] = np.around(ds.sftlf)
    if attrs is None:
        attrs = ds.attrs
    return ds


def rotate_uv(uge, vge, uvge, vuge, lamem, phiem, pollam, polphi):
    ulamem, uphiem = lamem.isel(pos=1), phiem.isel(pos=1)
    vlamem, vphiem = lamem.isel(pos=2), phiem.isel(pos=2)
    twoD_dims = list(horizontal_dims(uge))
    input_core_dims = 4 * [twoD_dims + [lev_gm]] + 4 * [twoD_dims] + 2 * [[]]

    uge_rot, vge_rot = xr.apply_ufunc(
        intf.rotate_uv,  # first the function
        uge,  # now arguments in the order expected
        vge,
        uvge,
        vuge,
        ulamem * 1.0 / 57.296,  # pi/180 (deg2rad)
        uphiem * 1.0 / 57.296,
        vlamem * 1.0 / 57.296,
        vphiem * 1.0 / 57.296,
        pollam,
        polphi,
        input_core_dims=input_core_dims,  # list with one entry per arg
        #  output_core_dims=[threeD_dims],  # returned data has 3 dimensions
        # returned data has 3 dimensions
        output_core_dims=2 * [twoD_dims + [lev_gm]],
        vectorize=True,  # loop over non-core dims, in this case: time
        # exclude_dims=set(("lev",)),  # dimensions allowed to change size. Must be a set!
        dask="parallelized",
        dask_gufunc_kwargs={"allow_rechunk": True},
        output_dtypes=(uge.dtype, vge.dtype),
    )
    return uge_rot, vge_rot


def pressure_correction_em(psge, tge, arfge, fibge, fibem, akgm, bkgm, kpbl):
    twoD_dims = list(horizontal_dims(psge))
    threeD_dims = list(horizontal_dims(psge)) + [lev_gm]
    input_core_dims = (
        [twoD_dims]
        + 2 * [threeD_dims]
        + 2 * [twoD_dims]
        + [[akgm.dims[0]], [bkgm.dims[0]], []]
    )
    # print(input_core_dims)
    result = xr.apply_ufunc(
        intf.pressure_correction_em,  # first the function
        psge,  # now arguments in the order expected
        tge,
        arfge,
        fibge,
        fibem,
        akgm,
        bkgm,
        kpbl,
        input_core_dims=input_core_dims,  # list with one entry per arg
        output_core_dims=[twoD_dims],  # returned data has 3 dimensions
        vectorize=True,  # loop over non-core dims, in this case: time
        dask="parallelized",
        dask_gufunc_kwargs={"allow_rechunk": True},
        output_dtypes=[psge.dtype],
    )
    return result


def interpolate_vertical(
    xge, psge, ps1em, akhgm, bkhgm, akhem, bkhem, varname, kpbl, ptop=0.0
):
    twoD_dims = list(horizontal_dims(psge))
    threeD_dims = list(horizontal_dims(psge)) + [lev_gm]
    input_core_dims = (
        [threeD_dims]
        + 2 * [twoD_dims]
        + [
            [akhgm.dims[0]],
            [bkhgm.dims[0]],
            [akhem.dims[0]],
            [bkhem.dims[0]],
            [],
            [],
            [],
        ]
    )
    output_core_dims = [twoD_dims + [akhem.dims[0]]]
    # print(output_core_dims)
    result = xr.apply_ufunc(
        intf.interp_vert,  # first the function
        xge,  # now arguments in the order expected
        psge,
        ps1em,
        akhgm,
        bkhgm,
        akhem,
        bkhem,
        varname,
        kpbl,
        ptop,
        input_core_dims=input_core_dims,  # list with one entry per arg
        output_core_dims=output_core_dims,  # returned data has 3 dimensions
        # exclude_dims=set(("index",)),
        vectorize=True,  # loop over non-core dims, in this case: time
        dask="parallelized",
        dask_gufunc_kwargs={"allow_rechunk": True},
        output_dtypes=[xge.dtype],
    )
    result.name = varname
    return result


def interpolate_vertical_remo(
    xge, psge, ps1em, akhgm, bkhgm, akhem, bkhem, varname, kpbl
):
    twoD_dims = list(horizontal_dims(psge))
    threeD_dims = list(horizontal_dims(psge)) + [lev_gm]
    input_core_dims = (
        [threeD_dims]
        + 2 * [twoD_dims]
        + [[akhgm.dims[0]], [bkhgm.dims[0]], [akhem.dims[0]], [bkhem.dims[0]], [], []]
    )
    output_core_dims = [twoD_dims + [akhem.dims[0]]]
    # print(output_core_dims)
    result = xr.apply_ufunc(
        intf.interp_vert2,  # first the function
        xge,  # now arguments in the order expected
        psge,
        ps1em,
        akhgm,
        bkhgm,
        akhem,
        bkhem,
        varname,
        kpbl,
        input_core_dims=input_core_dims,  # list with one entry per arg
        output_core_dims=output_core_dims,  # returned data has 3 dimensions
        # exclude_dims=set(("index",)),
        vectorize=True,  # loop over non-core dims, in this case: time
        dask="parallelized",
        dask_gufunc_kwargs={"allow_rechunk": True},
        output_dtypes=[xge.dtype],
    )
    result.name = varname
    return result


def pressure_correction_ge(ps1em, tem, arfem, ficge, fibem, akem, bkem):
    twoD_dims = list(horizontal_dims(ps1em))
    threeD_dims = list(horizontal_dims(ps1em)) + [lev]
    input_core_dims = (
        [twoD_dims]
        + 2 * [threeD_dims]
        + 2 * [twoD_dims]
        + [[akem.dims[0]], [bkem.dims[0]]]
    )
    # print(input_core_dims)
    result = xr.apply_ufunc(
        intf.pressure_correction_ge,  # first the function
        ps1em,  # now arguments in the order expected
        tem,
        arfem,
        ficge,
        fibem,
        akem,
        bkem,
        input_core_dims=input_core_dims,  # list with one entry per arg
        output_core_dims=[twoD_dims],  # returned data has 3 dimensions
        vectorize=True,  # loop over non-core dims, in this case: time
        dask="parallelized",
        output_dtypes=[ps1em.dtype],
    )
    return result


def correct_uv(uem, vem, psem, akem, bkem, lamem, phiem, ll_lam, dlam, dphi):
    twoD_dims = list(horizontal_dims(uem))
    input_core_dims = (
        2 * [twoD_dims + [lev]]
        + 1 * [twoD_dims]
        + [[akem.dims[0]], [bkem.dims[0]]]
        + 3 * [[]]
    )
    # print(input_core_dims)
    uge_corr, vge_corr = xr.apply_ufunc(
        intf.correct_uv,  # first the function
        uem,  # now arguments in the order expected
        vem,
        psem,
        akem,
        bkem,
        ll_lam,
        dlam,
        dphi,
        input_core_dims=input_core_dims,  # list with one entry per arg
        #  output_core_dims=[threeD_dims],  # returned data has 3 dimensions
        # returned data has 3 dimensions
        output_core_dims=2 * [twoD_dims + [lev]],
        vectorize=True,  # loop over non-core dims, in this case: time
        # exclude_dims=set(("lev",)),  # dimensions allowed to change size. Must be a set!
        dask="parallelized",
        #  dask_gufunc_kwargs = {'allow_rechunk':True},
        output_dtypes=(uem.dtype, vem.dtype),
    )
    uge_corr.name = "U"
    vge_corr.name = "V"
    return uge_corr, vge_corr
