import matplotlib as mpl, matplotlib.pyplot as plt, numpy as np, pandas as pd, scipy as sci, cmasher as cmr, os
from sklearn.preprocessing import StandardScaler
# plot function consts

shplots = dict(gridspec_kw={'height_ratios': [0.5, 2], 'width_ratios': [2, 0.5], 'wspace':0.1, 'hspace':0.1}, sharex='col', sharey='row')
defaults={
    'scatter':dict(zorder=4),
    'plot_trisurf':dict(color='white',alpha=0.5,zorder=2),
    'plot_surface':dict(alpha=0.5, edgecolor='black', color='grey',zorder=2),
    'contour':dict(offset=0,stride=10,zorder=0.5),
    'contourf':dict(offset=0,stride=10,zorder=0.5,levels=7),
    'clabel':dict(inline=True, fontsize=8,manual=False, inline_spacing=2),
    'interp_grid':dict(method='linear'),
    'interp_rbf':dict(smoothing=0.3, kernel='thin_plate_spline', epsilon=0.1),
}
def kwupdated(kws, defkey):
    if not isinstance(kws,dict): return defaults[defkey]
    else: 
        kws_ = defaults[defkey].copy()
        kws_.update(kws)
        return kws_

FILE = "volcanoB"
fpath = lambda x: "E:/Repositories/physicstools/volcano/" + x + ".csv"
cols = ['vent size', 'gas mass frac', 'velocity', 'indep', 'lo','hi']
pcols =['vent size','gas mass frac', 'velocity', 'indep', 'bound','color']
def normalmk():
    df = pd.read_csv(fpath(FILE))
    df_proc = df.copy()
    df_proc = df_proc[df_proc.columns[0:7]]
    for ind, row in df_proc.iterrows():
        if row['modified gp'] != 0 and row['modified gp'] != '0':
            df_proc.at[ind, 'gas percentage'] = row['modified gp']
    df_proc = df_proc.drop(columns=['modified gp'])
    df_proc.columns = cols
    df_proc = df_proc.reset_index(drop=True)
    df_proc = df_proc.replace('always', np.nan)
    df_proc = df_proc.dropna()
    # vent size, gas mass fraction, velocity, indep, i1, i2
    # rand(1-5000), rand(0-1), rand(1-500), rand(vent size, gas mass fraction, velocity), lower bound, upper bound --> (of indep)
    # generate points, if has i1 and i2, generate points (x,y,z) where x,y,z are consts in first 3 cols, and replace i1 and i2 with the col in indep
    gen_points = [[],[],[],[],[],[]]
    gen_mids = [[],[],[],[]]
    for ind,row in df_proc.iterrows():
        indepi = pcols.index(row['indep'])
        if isinstance(row['lo'], str) or isinstance(row['hi'], str): continue 
        for b in ('lo','hi'):
            const = [row['vent size'], row['gas mass frac'], row['velocity'], row['indep'], 0 if b == 'lo' else 1, 'blue' if b == 'lo' else 'red']
            const[indepi] = row[b]
            _ = [gen_points[i].append(vtype(const[i])) for i,vtype in enumerate((float,float,float,str,int,str))]
            const2 = [row['vent size'], row['gas mass frac'], row['velocity'], row['indep']]
            const2[indepi] = (float(row['lo']) + float(row['hi']))/2
            _ = [gen_mids[i].append(vtype(const2[i])) for i,vtype in enumerate((float,float,float,str))]
    df_lims = pd.DataFrame(gen_points).T 
    df_lims.columns = pcols 
    df_mids = pd.DataFrame({k:gen_mids[i] for i,k in enumerate(pcols[0:4])})
    lims = {k:(df_lims[i].min(), df_lims[i].max()) for k,i in zip(('vsz','gmf','svl'), cols[0:3])}
    return df_proc, df_lims, df_mids,lims

 
def extremesmk(lims='minmax'):
    df = pd.read_csv(fpath(FILE))
    df_proc = df.copy()
    df_proc = df_proc[df_proc.columns[0:7]]
    for ind, row in df_proc.iterrows():
        if row['modified gp'] != 0 and row['modified gp'] != '0':
            df_proc.at[ind, 'gas percentage'] = row['modified gp']
    df_proc = df_proc.drop(columns=['modified gp'])
    df_proc.columns = cols
    df_proc = df_proc.reset_index(drop=True)
    # first extract correct lims
    df_proc_clean = df_proc.replace(['always','posinf','neginf'], np.nan).dropna()
    gen_points_clean = [[],[],[],[],[],[]]
    gen_mids_clean = [[],[],[],[]]
    for ind,row in df_proc_clean.iterrows():
        indepi = pcols.index(row['indep'])
        for b in ('lo','hi'):
            const = [row['vent size'], row['gas mass frac'], row['velocity'], row['indep'], 0 if b == 'lo' else 1, 'blue' if b == 'lo' else 'red']
            const[indepi] = row[b]
            _ = [gen_points_clean[i].append(vtype(const[i])) for i,vtype in enumerate((float,float,float,str,int,str))]
            const2 = [row['vent size'], row['gas mass frac'], row['velocity'], row['indep']]
            const2[indepi] = (float(row['lo']) + float(row['hi']))/2
            _ = [gen_mids_clean[i].append(vtype(const2[i])) for i,vtype in enumerate((float,float,float,str))]
    df_lims = pd.DataFrame(gen_points_clean).T 
    df_lims.columns = pcols 
    df_mids = pd.DataFrame({k:gen_mids_clean[i] for i,k in enumerate(pcols[0:4])})
    rlims = {i:(-np.inf, np.inf) for i in cols[0:3]} if lims == 'infs' else {i:(df_lims[i].min(), df_lims[i].max()) for i in cols[0:3]} 
    lims = {k:(df_lims[i].min(), df_lims[i].max()) for k,i in zip(('vsz','gmf','svl'), cols[0:3])}

    # now remake the df_proc, taking into account the new lims, such that neginf --> min_i or -np.inf, posinf --> max_i or np.inf, always --> np.nan (to be dropped)
    df_proc = df_proc.replace('always', np.nan).dropna()
    gen_points = [[],[],[],[],[],[]]
    gen_mids = [[],[],[],[]]
    for ind,row in df_proc.iterrows():
        indepi = pcols.index(row['indep'])
        for b in ('lo','hi'):
            row[b]= rlims[row['indep']][0] if row[b] == 'neginf' else rlims[row['indep']][1] if row[b] == 'posinf' else row[b]
        for b in ('lo','hi'):
            
            const = [row['vent size'], row['gas mass frac'], row['velocity'], row['indep'], 0 if b == 'lo' else 1, 'blue' if b == 'lo' else 'red']
            const[indepi] = row[b]
            _ = [gen_points[i].append(vtype(const[i])) for i,vtype in enumerate((float,float,float,str,int,str))]
        const2 = [row['vent size'], row['gas mass frac'], row['velocity'], row['indep']]
        const2[indepi] = (float(row['lo']) + float(row['hi']))/2
        _ = [gen_mids[i].append(vtype(const2[i])) for i,vtype in enumerate((float,float,float,str))]
    df_lims = pd.DataFrame(gen_points).T 
    df_lims.columns = pcols 
    df_mids = pd.DataFrame({k:gen_mids[i] for i,k in enumerate(pcols[0:4])})
    return df_proc, df_lims, df_mids, lims
df_proc, df_lims, df_mids, lims = normalmk()

# Naming convention::::
#               V->vsz -> Vent SiZe         -> vent size        
#               S->svl -> Source VeLocity   -> velocity        
#               G->gmf -> Gas Mass Fraction -> gas mass frac
#
#               gridVG_gmf -> grid of X=vent size, Y=gas mass frac containing gas mass frac (as its also the Y axis, the grid is just a meshgrid)  )

# quantity limits, labels, formatters, locations, colors, colormaps.

quals = dict(
vsz=dict(lims=lims['vsz'], 
    c='vent size', label='Vent Size (m)',         
    fmt=lambda x,p:f"{np.round((x/1000*(lims['vsz'][1]-lims['vsz'][0])+lims['vsz'][0])/100)*100 :.0f}", 
    loc=200,                         
    cmap=cmr.cosmic
    ),
gmf=dict(lims=lims['gmf'], 
    c='gas mass frac', label='Gas Mass Fraction',     
    fmt=lambda x,p:f"{x/1000*(lims['gmf'][1]-lims['gmf'][0])+lims['gmf'][0]:.2f}",                      
    loc=(0.02/lims['gmf'][1]*1000), 
    cmap=cmr.emerald
    ),
svl=dict(lims=lims['svl'], 
    c='velocity', label='Source Velocity (m/s)', 
    fmt=lambda x,p:f"{np.round((x/1000*(lims['svl'][1]-lims['svl'][0])+lims['svl'][0])/10)*10:.0f}",    
    loc=200,                         
    cmap=cmr.ember
    )
)
def interpolator(xs,ys,zs,mode='grid',norm=True, **kwargs):
    xx,yy =np.mgrid[quals[xs]['lims'][0]:quals[xs]['lims'][1]:1000j,quals[ys]['lims'][0]:quals[ys]['lims'][1]:1000j] # x,y=vent size, gas mass frac
    kws = kwupdated(kwargs, 'interp_rbf') if mode == 'rbf' else kwupdated(kwargs, 'interp_grid')
    if mode == 'rbf': 
        dfin = df_mids.drop_duplicates(subset=[quals[xs]['c'], quals[ys]['c']])
    else:
        dfin = df_mids
    xyv = dfin[[quals[xs]['c'], quals[ys]['c']]].values
    zv = dfin[quals[zs]['c']].values
    xxyy = np.column_stack([xx.ravel(), yy.ravel()])
    if norm:
        scaler = StandardScaler()
        xyv = scaler.fit_transform(xyv)
        xxyy = scaler.transform(xxyy)
        z_scaler = StandardScaler()
        zv = z_scaler.fit_transform(zv.reshape(-1, 1)).flatten()  # Ensure proper shape

    if mode == 'grid':
        zz = sci.interpolate.griddata(xyv, zv, xxyy,**kws).reshape(xx.shape)
    elif mode == 'rbf':
        rbf = sci.interpolate.RBFInterpolator(xyv, zv,**kws)
        zz = rbf(xxyy).reshape(xx.shape)
    if norm:
        zz = z_scaler.inverse_transform(zz)
    zz = np.clip(zz, quals[zs]['lims'][0], quals[zs]['lims'][1])
    return xx,yy,zz 
shplots = dict(gridspec_kw={'height_ratios': [0.5, 2], 'width_ratios': [2, 0.5], 'wspace':0.1, 'hspace':0.1}, sharex='col', sharey='row')

defaults={
    'scatter':dict(zorder=4),
    'plot_trisurf':dict(color='white',alpha=0.5,zorder=2),
    'plot_surface':dict(alpha=0.5, edgecolor='black', color='grey',zorder=2),
    'contour':dict(offset=0,stride=10,zorder=0.5),
    'contourf':dict(offset=0,stride=10,zorder=0.5,levels=7),
    'clabel':dict(inline=True, fontsize=8,manual=False, inline_spacing=2),
    'interp_grid':dict(method='linear'),
    'interp_rbf':dict(smoothing=0.3, kernel='thin_plate_spline', epsilon=0.1),
}
def kwupdated(kws, defkey):
    if not isinstance(kws,dict): return defaults[defkey]
    else: 
        kws_ = defaults[defkey].copy()
        kws_.update(kws)
        return kws_
        
def interpolator(xs,ys,zs,mode='grid',norm=True, **kwargs):
    xx,yy =np.mgrid[quals[xs]['lims'][0]:quals[xs]['lims'][1]:1000j,quals[ys]['lims'][0]:quals[ys]['lims'][1]:1000j] # x,y=vent size, gas mass frac
    kws = kwupdated(kwargs, 'interp_rbf') if mode == 'rbf' else kwupdated(kwargs, 'interp_grid')
    if mode == 'rbf': 
        dfin = df_mids.drop_duplicates(subset=[quals[xs]['c'], quals[ys]['c']])
    else:
        dfin = df_mids
    xyv = dfin[[quals[xs]['c'], quals[ys]['c']]].values
    zv = dfin[quals[zs]['c']].values
    xxyy = np.column_stack([xx.ravel(), yy.ravel()])
    if norm:
        scaler = StandardScaler()
        xyv = scaler.fit_transform(xyv)
        xxyy = scaler.transform(xxyy)
        z_scaler = StandardScaler()
        zv = z_scaler.fit_transform(zv.reshape(-1, 1)).flatten()  # Ensure proper shape

    if mode == 'grid':
        zz = sci.interpolate.griddata(xyv, zv, xxyy,**kws).reshape(xx.shape)
    elif mode == 'rbf':
        rbf = sci.interpolate.RBFInterpolator(xyv, zv,**kws)
        zz = rbf(xxyy).reshape(xx.shape)
    if norm:
        zz = z_scaler.inverse_transform(zz)
    zz = np.clip(zz, quals[zs]['lims'][0], quals[zs]['lims'][1])
    return xx,yy,zz 
        
      
# plot and fig functions
def p_3d(ax3d,x,y,z,sets=dict(),cmap='coolwarm',**kwargs):
    """
        Plots a 3D plot with specified axis info and formatting.
        Parameters:
        x,y,z (dict): Dictionary containing axis info.
        sets (dict, optional): Additional settings to apply to the plot. Default is an empty dictionary.
        cmap (str, optional): Colormap to use for the plot. Default is 'coolwarm'.
        **kwargs: Additional keyword arguments to pass to the plot.
        Returns:
        tuple: The figure and 3D axes objects.
    """
    if isinstance(cmap, str):
        cmap=[cmap,cmap,cmap]
    if "scatter" in kwargs:
        kws = kwupdated(kwargs['scatter'],'scatter')
        ax3d.scatter(df_lims[x['c']],df_lims[y['c']],df_lims[z['c']], c=df_lims['color'], **kws)
    if "plot_trisurf" in kwargs:
        kws = kwupdated(kwargs['plot_trisurf'],'plot_trisurf')
        ax3d.plot_trisurf(df_mids[x['c']],df_mids[y['c']],df_mids[z['c']], **kws)
    if "plot_surface" in kwargs:
        kws = kwupdated(kwargs['plot_surface'],'plot_surface')
        ax3d.plot_surface(x['v'],y['v'],z['v'], **kws)
    if "contour" in kwargs or "contourf" in kwargs:
        if "altcontour" in kwargs:v = kwargs['altcontour']
        else:v = dict(x=[x['v'],y['v'],z['v']],y=[x['v'],y['v'],z['v']],z=[x['v'],y['v'],z['v']])     
    if "contour" in kwargs:
        kws = kwupdated(kwargs['contour'],'contour')
        cx,cy,cz = [ax3d.contour(*v[n], zdir=n, cmap=cmap[i], **kws) for i,n in enumerate(('x','y','z'))]
    if "contourf" in kwargs:
        kws = kwupdated(kwargs['contourf'],'contourf')
        cfx,cfy,cfz = [ax3d.contourf(*v[n], zdir=n, cmap=cmap[i], **kws) for i,n in enumerate(('x','y','z'))]  
    ax3d.set(xlim=x['lims'],ylim=y['lims'],zlim=z['lims'], xlabel=x['label'],ylabel=y['label'],zlabel=z['label'],**sets)
    return ax3d

def p_im(ax,x,y,z,cmap='viridis',color_exts=None,cmapor='horizontal', **kwargs):
    """
        Plots an image on the given axes with specified colormap and formatting.
        Parameters:
        ax (matplotlib.axes.Axes): The axes on which to plot the image.
        x,y,z (dict): Dictionary containing axis info.
        cmap (str, optional): Colormap to use for the image. Default is 'viridis'.
        color_exts (optional): Not used in the current implementation.
        cmapor (str, optional): Orientation of the colorbar. Default is 'horizontal'.
        Returns:
        tuple: The image and colorbar objects.
    """
    cmap = mpl.colormaps.get_cmap(cmap)
    norm = mpl.colors.Normalize(vmin=z['lims'][0],vmax=z['lims'][1])
    im =ax.imshow(z['v'],  cmap=cmap,origin='lower', norm=norm)
    ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(x['fmt']))
    ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(y['fmt']))
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(x['loc']))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(y['loc']))
    ax.set(xlabel=x['label'],ylabel=y['label'])
    cbar = plt.colorbar(im,ax=ax, shrink=0.7, orientation=cmapor)
    cbar.set_label(z['label'])
    return im,cbar
def p_cont(ax,x,y,z,cmap='inferno',clabel=True, **kwargs):
    """
        Plots contours on the given axes with specified colormap and formatting.
        Parameters:
        ax (matplotlib.axes.Axes): The axes on which to plot the contours.
        x,y,z (dict): Dictionary containing axis info.
        cmap (str, optional): Colormap to use for the contours. Default is 'inferno'.
        clabels (bool, optional): Whether to plot contour labels. Default is True.
        Returns:
        tuple: The contour and contour label objects.
    """
    cmap = mpl.colormaps.get_cmap(cmap)
    norm = mpl.colors.Normalize(vmin=z['lims'][0],vmax=z['lims'][1])
    ctr = ax.contour(x['v'],y['v'],z['v'], cmap=cmap, norm=norm,**kwupdated(kwargs,'contour'))
    ctlab = ax.clabel(ctr, **kwupdated(clabel,'clabel')) if clabel else None
    return ctr, ctlab
def p_contf(ax,x,y,z,cmap='inferno',clabel=True, **kwargs):
    """
        Plots filled contours on the given axes with specified colormap and formatting.
        Parameters:
        ax (matplotlib.axes.Axes): The axes on which to plot the filled contours.
        x,y,z (dict): Dictionary containing axis info.
        cmap (str, optional): Colormap to use for the filled contours. Default is 'inferno'.
        clabels (bool, optional): Whether to plot contour labels. Default is True.
        Returns:
        tuple: The filled contour and contour label objects.
    """
    ctrf = ax.contourf(x['v'],y['v'],z['v'], cmap=cmap, **kwupdated(kwargs,'contourf'))
    ctlab = ax.clabel(ctrf, **kwupdated(clabel,'clabel')) if clabel else None
    return ctrf, ctlab
def p_scatterlims(ax,x,y,z, **kwargs):
    """
        Plots a scatter plot on the given axes with specified formatting.
        Parameters:
        ax (matplotlib.axes.Axes): The axes on which to plot the scatter plot.
        x,y,z (dict): Dictionary containing axis info.
        **kwargs: Additional keyword arguments to pass to the scatter plot.
        Returns:
        matplotlib.collections.PathCollection: The scatter plot object.
    """
    if 'cmap' in kwargs:
        cmap = kwargs.pop('cmap')
        sc = ax.scatter(df_lims[x['c']],df_lims[y['c']],c=df_lims[z['c']],cmap=cmap, **kwupdated(kwargs,'scatter'))
    else:
        sc = ax.scatter(df_lims[x['c']],df_lims[y['c']],c=df_lims[z['color']], **kwupdated(kwargs,'scatter'))
    ax.set(xlabel=x['label'],ylabel=y['label'])
    return sc
def p_scattermids(ax,x,y,z, **kwargs):
    """
        Plots a scatter plot on the given axes with specified formatting.
        Parameters:
        ax (matplotlib.axes.Axes): The axes on which to plot the scatter plot.
        x,y,z (dict): Dictionary containing axis info.
        **kwargs: Additional keyword arguments to pass to the scatter plot.
        Returns:
        matplotlib.collections.PathCollection: The scatter plot object.
    """
    if 'cmap' in kwargs:
        cmap = kwargs.pop('cmap')
        sc = ax.scatter(df_mids[x['c']],df_mids[y['c']],c=df_mids[z['c']],cmap=cmap, **kwupdated(kwargs,'scatter'))
    else:
        sc = ax.scatter(df_mids[x['c']],df_mids[y['c']],c=df_mids[z['color']], **kwupdated(kwargs,'scatter'))
    ax.set(xlabel=x['label'],ylabel=y['label'])
    return sc

def f_mult(x,y,num,dir='rows',title=None,suptitle=None, space=None, constrained=None):
    """
        Creates a figure with multiple subplots.
        Parameters:
        x (float): Width of the figure.
        y (float): Height of the figure.
        num (int): Number of subplots to create.
        dir (str, optional): Direction in which to create the subplots. Default is 'rows'.
        title (str, optional): Title of the figure. Default is None.
        wspace (float, optional): Width space between subplots. Default is None.
        constrained (bool, optional): Whether to use constrained layout. Default is None.
        Returns:
        tuple: The figure and axes objects.
    """
    fig, ax = plt.subplots(1,num, figsize=(x,y),layout="constrained" if constrained else None) if dir == 'rows' else plt.subplots(num,1, figsize=(x,y),layout="constrained" if constrained else None)
    if suptitle is not None:fig.suptitle(suptitle)
    if title is not None: [ax[num//2 if dir == 'rows' else 0].set_title(title, size=20)]
    if space is not None:fig.subplots_adjust(wspace=space) if dir == 'rows' else fig.subplots_adjust(hspace=space)
    return fig, ax
def f_simple(x,y,title=None,constrained=None, **kwargs):
    """
        Creates a simple figure with a single subplot.
        Parameters:
        x (float): Width of the figure.
        y (float): Height of the figure.
        title (str, optional): Title of the figure. Default is None.
        constrained (bool, optional): Whether to use constrained layout. Default is None.
        **kwargs: Additional keyword arguments to pass to the axes.
        Returns:
        tuple: The figure and axes objects.
    """
    fig, ax = plt.subplots(1,1, figsize=(x,y),layout="constrained" if constrained else None)
    if title is not None:fig.suptitle(title)
    if kwargs:ax.set(**kwargs)
    return fig, ax
def f_3d(x,y,proj='ortho',**kwargs):
    fig =plt.figure(figsize=(x,y))
    ax3d = fig.add_subplot(1,1,1, projection="3d", **kwargs)
    ax3d.set_proj_type('ortho')
    return fig, ax3d


def Figure_3D_contourlines():
    fig,ax3d = f_3d(10,10, computed_zorder=False)
    ax3d = p_3d(ax3d,**gs[0],cmap='coolwarm',scatter=True, contour=True, plot_trisurf=True, plot_surface=True)
    return fig
def Figure_3D_cmaps():
    fig,ax3d = f_3d(10,10, computed_zorder=False)
    ax3d = p_3d(ax3d,**gs[0],cmap=[k['cmap'] for k in gs[0].values()],contourf={'levels':20}, altcontours=altcontours_v2, plot_trisurf=True)
    return fig

#Figure_3D_contourlines().show()
#Figure_3D_cmaps().show()

def Figure_individual_imshow():
    ret =[[],[],[]]
    for i in range(3):
        fig,ax = f_simple(12,9)
        im = p_im(ax,**gs[i],cmap=gs[i]['z']['cmap'], cmapor='vertical')
        for i,ob in enumerate((fig,ax,im)):
            ret[i].append(ob) 
    return ret[0],ret[1]
def Figure_grouped_imshow(dirc='rows'):
    fig,ax = f_mult(16,5,3,dir=dirc,title='Volcano Plots', constrained=True)
    ims = [p_im(ax_,**g_,cmap=g_['z']['cmap'], cmapor='vertical', ) for ax_,g_ in zip(ax,gs)]
    return fig,ax
def Figure_individual_contour():
    ret =[[],[],[]]
    for i in range(3):
        fig,ax = f_simple(12,9)
        ctr = p_cont(ax,cmap=gs[i]['z']['cmap'],**gs[i])
        for i,ob in enumerate((fig,ax,ctr)):
            ret[i].append(ob) 
    return ret[0],ret[1]
def Figure_grouped_contour(dirc='rows'):
    fig,ax = f_mult(16,5,3,dir=dirc,title='Volcano Plots', constrained=True)
    ims = [p_cont(ax,cmap=g_['z']['cmap'], **g_, levels=20) for ax,g_ in zip(ax,gs)]
    return fig,ax
def Figure_grouped_contour_scatter(dirc='rows'):
    fig,ax = f_mult(16,5,3,dir=dirc,title='Volcano Plots', constrained=True)
    ims = [p_cont(ax,cmap=g_['z']['cmap'],**g_) for ax,g_ in zip(ax,gs)]
    sct = [p_scattermids(ax,cmap=g['z']['cmap'],marker="o",s=2,**g) for ax,g in zip(ax,gs)]
    return fig, ax
def Figure_individual_contour_scatter():
    ret =[[],[],[],[]]
    for i in range(3):
        fig,ax = f_simple(10,8)
        ctr = p_cont(ax,cmap=gs[i]['z']['cmap'],**gs[i])
        sct = p_scattermids(ax,cmap=gs[i]['z']['cmap'],marker="o",s=2,**gs[i])
        for i,ob in enumerate((fig,ax,ctr,sct)):
            ret[i].append(ob) 
    return ret[0],ret[1]
def Figure_grouped_contourf_scatter(dirc='rows'):
    fig,ax = f_mult(16,5,3,dir=dirc,title='Volcano Plots', constrained=True)
    ims = [p_contf(ax,cmap=g_['z']['cmap'],levels=30,**g_) for ax,g_ in zip(ax,gs)]
    sct = [p_scattermids(ax,cmap=g['z']['cmap'].reversed(),marker="o",s=2,**g) for ax,g in zip(ax,gs)]
    return fig, ax
def set_grouped(axes, sets=gs, **kwargs):
    for ax,kws in zip(axes, sets):
            ax.set_xlabel(kws['x']['label'])
            ax.set_ylabel(kws['y']['label'])
def set_individual(ax, sets=gs[0], **kwargs):
    ax.set_xlabel(sets['x']['label'])
    ax.set_ylabel(sets['y']['label'])
