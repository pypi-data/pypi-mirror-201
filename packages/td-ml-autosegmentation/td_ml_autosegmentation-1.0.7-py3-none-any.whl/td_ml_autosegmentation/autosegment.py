import os
import sys
import pytd
import tdclient
import requests
import json
from pandiet import Reducer

import numpy as np
import pandas as pd

import plotly.express as px
from plotly.offline import init_notebook_mode, iplot
from plotly.subplots import make_subplots
import plotly.graph_objects as go  

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import faiss
import shap

def get_table(table, db, apikey, td_api_server):
    """Retrieve table from TD account.

    Args:
        table (str): Table to retrieve data from. may also include additional SQL clauses; anything after the FROM in a query.
        db (str): Database to retrieve table from.
        apikey (str): Master API key from TD account, must have query permissions.
        td_api_server (str): TD API server.

    Returns:
        Pandas DataFrame: query result.
    """
    with tdclient.Client(apikey=apikey, endpoint=td_api_server) as td:
        job = td.query(db, f"SELECT * FROM {table}", type='presto')
        job.wait()
        data = job.result()
        columns = [f[0] for f in job.result_schema]
        df = pd.DataFrame(data, columns=columns)
    return df


def k_from_fi(feat_impt, plot=True):
    """Generating WSS and Silhouette Score plots from feature importance table.

    Args:
        feat_impt (DataFrame): DF containing WSS and Silhouette Scores, returned by the get_fi function.
        plot (bool, optional): Whether to generate Plotly graph. Defaults to True.

    Returns:
        _type_: _description_
    """
    
    eval_k = make_subplots(rows=1, cols=2, subplot_titles=['Inertia / Within-Cluster Sum of Squares', 'Silhouette Scores'])
    
    wss_line = px.line(feat_impt[feat_impt['kind']=='wss'], x='feature', y='impt')
    sil_line = px.line(feat_impt[feat_impt['kind']=='silhouette'], x='feature', y='impt')

    best_k = feat_impt.cluster.nunique() -1

    if plot==True:

        wss_trace = [wss_line["data"][i] for i in range(len(wss_line["data"]))]
        sil_trace = [sil_line["data"][i] for i in range(len(sil_line["data"]))]

        for t in wss_trace:
            eval_k.append_trace(t, row=1, col=1)
        for t in sil_trace:
            eval_k.append_trace(t, row=1, col=2)

        for i in eval_k['layout']['annotations']:
            i['font'] = dict(size=13)

        eval_k.update_layout(height=400, width=800, 
                            title_text=f"Evaluating Best Number of Clusters: Best K = {best_k}", showlegend=False)
        eval_k.show()

    return best_k
    

def prioritize_df(df, prioritize):
    """Adjusts input data for prioritization (semi-supervised) methods.

    Args:
        df (DataFrame): DataFrame containing features, be sure column names are features.
        prioritize (dict): Dictionary containing features to prioritize and prioritization coefficients.

    Returns:
        DataFrame: Input data, rescaled for prioritization.
    """
    hc =int(prioritize.get('high_coeff', 1))
    mc =int(prioritize.get('med_coeff', 1))
    lc =int(prioritize.get('low_coeff', 1))
    if prioritize['high'] != "":
        df.loc[:,df.filter(regex=prioritize['high']).columns] = hc*df.loc[:,df.filter(regex=prioritize['high']).columns]
    if prioritize['med'] != "":
        df.loc[:,df.filter(regex=prioritize['med']).columns] = mc*df.loc[:,df.filter(regex=prioritize['med']).columns]
    if prioritize['low'] != "":
        df.loc[:,df.filter(regex=prioritize['low']).columns] = lc*df.loc[:,df.filter(regex=prioritize['low']).columns]
    return df

def column_clean(df, user_id, excl=None, semi_supervised='no', prioritize=None):
    """Complete data cleaning function.

    Args:
        df (DataFrame): Raw data in DataFrame format.
        user_id (str): Unique identifier column name.
        excl (str, optional): In Regex format, columns to ignore for modeling. Defaults to None.
        semi_supervised (str, optional): If 'no', nothing happens. If any other value, perform rescaling for prioritization. Defaults to 'no'.
        prioritize (dict, optional): Prioritization dictionary, only used if semi_supervised != 'no'. Defaults to None.

    Returns:
        DataFrame: Numerical DataFrame for modeling.
        DataFrame: Clean DataFrame for calculating certain metrics and certain visualizations.
        dict: Dictionary containing data processing methods used.
        MinMaxScaler object.
    """
    # removing ignore
    df = df.drop(df.filter(regex=excl).columns, axis=1)
    to_drop = []
    for col in df.columns:
        try:
            df[col].nunique()
        except:
            to_drop.append(col)
        try:
            df[col] = df[col].astype(float)
        except:
            pass

    df = df.drop(to_drop, axis=1)
    
    # removing columns with 1 unique value
    df = df[df.columns[df.nunique() != 1]]
    
    # removing columns with more than 25% nulls
    df = df[df.columns[df.isna().sum() < df.shape[0]*0.25]]
    df_clean = df.copy()
    
    # identify object columns to process
    objs = df.select_dtypes(exclude=['int64', 'float64']).columns
    
    data_dict = {}
    to_dummy = []
    too_unique = []

    data_dict['categorical'] = {}
    
    for c in objs:
        keep, others = [], []
        # binary variables
        if df[c].nunique() == 2:
            zero, one = df[c].value_counts().index
            df[c] = df[c].apply(lambda v: 0 if v == zero else 1)
            data_dict['categorical'][c] = {zero: 0, one: 1}
        # to_dummy if fewer than 5 unique values
        elif 2 < df[c].nunique() <= 5:
            to_dummy.append(c)
            for k, v in df[c].value_counts().iteritems():
                if 'other' not in k:
                    keep.append((k, v))
                else: 
                    others.append((k, v))
                data_dict['categorical'][c] = {'kept': keep, 'others': others}

        # to_dummy, but changing values that take up less than 5% of values to "other"
        elif 5 < df[c].nunique() < df.shape[0]:
            for k, v in df[c].value_counts().iteritems():
                if v > df.shape[0]/20 and 'other' not in k:
                    keep.append((k, v))
                else:
                    others.append((k, v))
            if keep != []:
                to_dummy.append(c)
                data_dict['categorical'][c] = {'kept': keep, 'others': others}
                df[c] = df[c].apply(lambda v: 'other' if not any(v == x[0] for x in keep) else v)
                df_clean[c] = df_clean[c].apply(lambda v: 'other' if not any(v == x[0] for x in keep) else v)
            else:
                too_unique.append(c)

        # identifier columns (to drop for modeling)
        else:
            too_unique.append(c)
    
    data_dict['too_unique'] = too_unique
            
    # create dummy vars, scaling based on the number of unique values
    for d in to_dummy:
        df = df.join(pd.get_dummies(df[d], prefix=d)).drop(d, axis=1)
        
    df = df.set_index(user_id).drop([u for u in too_unique if u!=user_id], axis=1).dropna()
    df_clean = df_clean.set_index(user_id).drop([u for u in too_unique if u!=user_id], axis=1).dropna()
    
    # scale features for modeling
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
                     
    for d in to_dummy:
        c = df_scaled.filter(regex=f'^{d}').columns
        df_scaled[c] = df_scaled[c]/len(c)
    if semi_supervised!='no':
        df_scaled = prioritize_df(df_scaled, prioritize)
        
    return df_scaled, df_clean, data_dict, scaler

def process_data_dict(data_dict):
    """Function for processing data dictionary into DataFrame format for data cleaning reproduction.

    Args:
        data_dict (dict): Data dictionary output from column_clean function.

    Returns:
        DataFrame: Table with data cleaning rules.
    """
    processing = []
    for k, v in data_dict['categorical'].items():
        out = {'feature': k}
        if list(v.values()) == [0, 1]:
            out['type'] = 'boolean'
            out['kept'] = None
            out['others'] = None
            for kk, vv in v.items():
                if vv == 0:
                    out['zero'] = kk
                elif vv == 1:
                    out['one'] = kk
        else:
            out['type'] = 'dummy'
            out['kept'] = [vv[0] for vv in v['kept']]
            out['others'] = [vv[0] for vv in v['others']]
            out['zero'] = None 
            out['one'] = None

        processing.append(out)
    return pd.DataFrame(processing)

def cluster(df, df_clean, n, user_id, model):
    """Main clustering function that trains clustering model.

    Args:
        df (DataFrame): Numerical cleaned data from column_clean.
        df_clean (DataFrame): Cleaned data from column_clean.
        n (int): Number of clusters to generate.
        user_id (str): Unique identifier column name.
        model (str): Either 'kmeans' (memory efficient) or 'faiss' (time efficient).

    Returns:
        DataFrame: Numerical cleaned data with cluster labels,
        DataFrame: Cleaned data with cluster labels,
        Trained model object.
    """

    if model!='faiss':
        model = KMeans(n_clusters=n, random_state=0).fit(df)
        res = model.labels_
    else:
        d = df.values.copy(order='C').astype(np.float32)
        model = faiss.Kmeans(d=d.shape[1], k=3, niter=300, nredo=10)
        model.train(d)
        res = model.index.search(d, 1)[1].flatten()
        
    out, out_clean = df.copy(), df_clean.copy()
    out['cluster'] = res
    out_clean = out_clean.merge(out[['cluster']].reset_index(), left_index=True, right_on=user_id).set_index(user_id)

    out = Reducer().reduce(out, verbose=False)
    out_clean = Reducer().reduce(out_clean, verbose=False)
    return out, out_clean, model

def save_model(model, scaler, col_names, semi_supervised, prioritize, df, transforms_df):
    """Saving model parameters (centroids, scaler) to DataFrame.

    Args:
        model (obj): Trained model object.
        scaler (obj): Trained MinMaxScaler object.
        col_names (list): List of column names, for best results use cleaned numerical data's column names.
        semi_supervised (bool): Whether the model took in prioritized data.
        prioritize (dict): Prioritization features and coefficients.
        df (DataFrame): Numerical input data (binarized).
        transforms_df (DataFrame): DataFrame of column transforms.

    Returns:
        _type_: _description_
    """
    
    col_names = [c.lower().replace('-', '_') for c in col_names]
    vals = pd.DataFrame([scaler.scale_], columns=col_names, index=['scaler'])

    # additionally scale categorical variables (dividing values by number of unique vals)
    try: 
        dummies = transforms_df.dropna(subset=['kept'])
        to_save = []
        for f in dummies.itertuples(index=False):
            if isinstance(f.kept, list):
                unique = len(f.kept)
            else:
                unique = len(f.kept.split(', '))
            to_save.append({'nunique': unique, 'cols': vals.filter(regex=f'^{f.feature}').columns, 'feat': f.feature})
            vals[vals.filter(regex=f'^{f.feature}').columns] = vals[vals.filter(regex=f'^{f.feature}').columns]/unique
    except: 
        pass

    if semi_supervised=='yes':
        vals = prioritize_df(vals, prioritize).T
    else:
        vals = vals.T

    try:
        centroid_df = pd.DataFrame(model.cluster_centers_, columns=col_names, index=[f'cluster_{i}' for i in range(len(model.cluster_centers_))]).T
    except:
        centroid_df = df.groupby('cluster').mean().T
        centroid_df.columns = [f'cluster_{i}' for i in range(centroid_df.shape[1])]
    
    model_df = pd.concat([vals, centroid_df],axis=1).reset_index()
    model_df.columns = ['features'] + model_df.columns.tolist()[1:]
    return model_df

def score_k(data, k_min, k_max, plot=True):
    """Picking mathematically optimal number of clusters.

    Args:
        data (DataFrame): Input numerical data.
        k_min (int): Minimum number of clusters to test.
        k_max (int): Maximum number of clusters to test
        plot (bool, optional): Whether to output Plotly visualizations. Defaults to True.

    Returns:
        dict: Dictionary containing metrics across different cluster numbers.
    """
    k_range = range(k_min, k_max+1)

    if data.shape[0] >= 10000:
        data = data.sample(n=10000)
        
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)
    wss = []
    sil = []
    for k in k_range:
        model = KMeans(n_clusters=k, random_state=0).fit(data_scaled)
        wss.append(model.inertia_)
        sil.append(silhouette_score(data_scaled, model.labels_))
        
    # to determine best k
    elbow, dec, best_ind = 0, 0, 0
    for i, k in enumerate(k_range):
        diff = wss[i] - wss[i-1]
        if diff < dec:
            elbow = k
            dec = diff
            best_ind = i
    
    out = {'best_k': elbow, 'best_k_ind': best_ind, 'wss': wss, 'sil': sil}
    
    if plot==True:
        eval_k = make_subplots(rows=1, cols=2, subplot_titles=['Inertia / Within-Cluster Sum of Squares', 'Silhouette Scores'])
        
        wss_line = px.line(x=k_range, y=wss)
        sil_line = px.line(x=k_range, y=sil)

        wss_trace = [wss_line["data"][i] for i in range(len(wss_line["data"]))]
        sil_trace = [sil_line["data"][i] for i in range(len(sil_line["data"]))]

        for t in wss_trace:
            eval_k.append_trace(t, row=1, col=1)
        for t in sil_trace:
            eval_k.append_trace(t, row=1, col=2)

        for i in eval_k['layout']['annotations']:
            i['font'] = dict(size=13)

        eval_k.update_layout(height=400, width=800, title_text=f"Evaluating Best Number of Clusters: Best K = {out['best_k']}", showlegend=False)
        eval_k.show()
    
    return out

def create_out(data_clean, impts):
    out = {'cat_information_gain': list(impts[impts['kind']=='info_gain'][['feature', 'impt']].itertuples(index=False, name=None))}
    
    val_counts = data_clean.cluster.value_counts().to_dict()
    for k, v in val_counts.items():
        out[f'cluster_{k}'] = {'n': v}
        
    for c in impts.cluster.unique():
        if c.startswith('cluster_'):
            vals = impts[(impts['kind']=='feature_compactness')&(impts['cluster']==c)][['feature', 'impt']].itertuples(index=False, name=None)
            out[c]['compact_features'] = {v[0]: v[1] for v in vals}
    return out

def get_fi(data, client, plot=False):
    """Obtain feature importances and write SHAP values to TD.

    Args:
        data (DatFrame): Input numerical data.
        client (obj): TD Client object.
        plot (bool, optional): Whether to plot Random Forest feature importances. Defaults to False.

    Returns:
        DataFrame: DataFrame containing feature importances.
        DataFrame: DataFrame containing SHAP values.
    """
    X = data.drop('cluster', axis=1)
    y = data['cluster']
    model = RandomForestClassifier(n_estimators=50, max_depth=5)
    model.fit(X, y)

    fi = pd.DataFrame(X.columns, columns = ['feature'])
    fi['impt'] = model.feature_importances_
    
    # getting SHAP values
    ss = []
    for c in data.cluster.unique():
        s = data[data.cluster==c].sample(min([2000, sum(data.cluster==c)]))
        ss.append(s)
    sample = pd.concat(ss)
    
    explainer = shap.Explainer(model, sample)
    shap_values = explainer(sample, check_additivity=False)
    shaps = []
    X_c = pd.melt((sample > sample.median()).replace({True: 'high', False: 'low'}))
    for i in range(shap_values.shape[-1]):
        vals = shap_values.values[:,:,i]
        shap_df = pd.DataFrame(vals, columns=shap_values.feature_names)
        shap_df = pd.melt(shap_df)
        shap_df.columns = ['feature', 'shap_value']
        shap_df['cluster'] = i
        shap_df['feature_value'] = X_c['value']
        shaps.append(shap_df)
        if plot==True:
            shap.plots.bar(shap_values[:,:,i])
            shap.plots.beeswarm(shap_values[:,:,i])
            
    shaps = pd.concat(shaps)
    shap_stats = shaps.groupby(by=["feature", "cluster", "feature_value"], dropna=False, as_index=False).agg(['sum', 'count', 'mean'])
    shap_stats.columns = [item[0] + '_' + item[1] for item in shap_stats.columns]
    # client.load_table_from_dataframe(shap_stats.reset_index(), 'as_shap_temp', writer='bulk_import', if_exists='overwrite')

    if plot==True:
        fig = px.bar(fi.sort_values('impt'), x='impt', y='feature', title='Overall Proportional Feature Importances', 
        labels={'impt': 'Proportional Importance', 'feature': 'Feature'})
        fig.show()

    return fi, shap_stats.reset_index()

    
def info_gain(df, feature, label='cluster'):
    
    initial_vc = df[feature].value_counts(normalize=True)
    initial_ent = -(initial_vc * np.log(initial_vc)/np.log(np.e)).sum()
    
    gain = []
    
    for l in df[label].unique():
        vals = df[df[label]==l][feature]
        vc = vals.value_counts(normalize=True)
        prop = vals.shape[0] / df.shape[0]
        ent = -(vc * np.log(vc)/np.log(np.e)).sum()
        gain.append(prop*ent)
        
    return initial_ent - sum(gain)


def plot_pie(out):
    """Plotting cluster distribution pie chart.

    Args:
        out (dict): Model output.
    """
    cl = sorted([c for c in out.keys() if c.startswith('cluster_')])
    colors = px.colors.qualitative.Plotly[:len(cl)]
    pie = go.Figure(data=[go.Pie(values=[out[c]['n'] for c in cl], labels=cl)])
    pie.update_layout(title_text="Cluster Distribution of Customers", width=500, height=500)
    pie.update_traces(marker={'colors': colors})
    pie.show()
    
def cat_info_gain(out):
    cat_gain = dict(out['cat_information_gain'])
    cat_bar = px.bar(x=cat_gain.values(), y=cat_gain.keys(), 
       labels={'x': 'Information Gain', 'y': 'Feature'}, title="Categorical Important Features: By Information Gain")
    cat_bar.show()
    
def cat_feat_impt(df, out, n_impt):
    
    titles = [cat[0] for cat in out['cat_information_gain'][::-1]][:n_impt]
    fig_titles = [f'#{i+1}: {titles[i]}' for i in range(len(titles))]
    fig = make_subplots(rows=(n_impt-1)//3+1, cols=3, subplot_titles=fig_titles, vertical_spacing = 0.1)

    for i in range(n_impt):
        ct = pd.crosstab(df[titles[i]], df['cluster'])
        colors = px.colors.qualitative.Plotly[:len(ct.columns)]
        for c in range(len(ct.columns)):
            fig.add_trace(go.Bar(x=ct.index, y=ct[ct.columns[c]], name=f'Cluster {ct.columns[c]}', 
                                 marker_color=colors[c]), row=i//3+1, col=i%3 +1)

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=13)

    fig.update_layout(height=300*((n_impt+1)//3), width=900, title_text="Categorical Important Features", 
                      barmode='stack', showlegend=False)
    fig.show()

def compact_summary(out):
    
    cl = sorted([c for c in out.keys() if c.startswith('cluster_')])
    titles = [f'{c}' for c in cl]
    
    fig = make_subplots(rows=len(cl), cols=1, subplot_titles=titles, vertical_spacing = 0.1)
    colors = px.colors.qualitative.Plotly[:len(cl)]

    for c in range(len(cl)):
        tr = px.bar(x=out[cl[c]]['compact_features'].values(), y=out[cl[c]]['compact_features'].keys(),
                   range_x=[-1, 1], color_discrete_sequence=[colors[c]])
        traces = [tr['data'][t] for t in range(len(tr['data']))]
        for t in traces:
            fig.append_trace(t, row=c+1, col=1)

    fig.update_layout(height=350*len(cl), title_text="Per-Cluster Relative Feature Compactness", showlegend=False)
    fig.update_xaxes(range=[-1, 1])
    fig.show()
    

def cont_impt_box(df, out, n_impt):
    
    cl = sorted([k for k in out.keys() if k.startswith('cluster_')])
    titles = []
    for i in range(n_impt):
        for cluster in range(len(cl)):
            f = list(out[cl[cluster]]["compact_features"].keys())[-(i+1)]
            titles.append(f"Cluster {cluster} #{i+1}: {f}")

    fig = make_subplots(rows=n_impt, cols=len(cl), subplot_titles=titles, vertical_spacing = 0.05)
    colors = px.colors.qualitative.Plotly[:len(cl)]
    cdm = dict(zip([int(c[-1]) for c in cl], colors)) 

    for cluster in range(len(cl)):
        for i in range(n_impt):
            f = list(out[cl[cluster]]["compact_features"].keys())[-(i+1)]
            tr = px.box(df, x="cluster", y=f, color="cluster", color_discrete_map=cdm, points=False)
            traces = []
            for trace in range(len(tr["data"])):
                traces.append(tr["data"][trace])
            for t in traces:
                fig.append_trace(t, row=i+1, col=cluster+1)

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=12)

    fig.update_layout(height=200*n_impt, width=300*len(cl), title_text="Continuous Important Features: Boxplots", 
                      showlegend=False)
    fig.show()
    
    
def cont_impt_hist(df, out, n_impt):

    cl = sorted([k for k in out.keys() if k.startswith('cluster_')])
    titles = []
    for i in range(n_impt):
        for c in range(len(cl)):
            f = list(out[cl[c]]["compact_features"].keys())[-(i+1)]
            titles.append(f"Cluster {c} #{i+1}: {f}")
            
    fig = make_subplots(rows=n_impt, cols=len(cl), vertical_spacing = 0.05, subplot_titles=titles)
    colors = px.colors.qualitative.Plotly[:len(cl)]

    for i in range(n_impt):
        for c in range(len(cl)):
            for cc in range(len(cl)):
                
                f = list(out[cl[c]]["compact_features"].keys())[-(i+1)]
                cn = cl[cc][-1]
                fig.add_trace(go.Histogram(x=df[df.cluster==int(cn)][f], name=f'{cl[cc]}', 
                                     marker_color=colors[cc]), row=i+1, col=c+1)

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=13)

    fig.update_layout(height=250*n_impt, width=300*len(cl), title_text="Continuous Important Features: Histograms", 
                      barmode='stack', showlegend=False)
    fig.show()
    
    
def score_clusters(df, df_clean, data_dict):
    """Scoring final clustering model.

    Args:
        df (DataFrame): Numerical DF with cluster labels.
        df_clean (DataFrame): DF with cluster labels.
        data_dict (dict): Dictionary contatining data changes.

    Returns:
        DataFrame: Numerical DF with cluster labels.
        dict: Dictionary containing cluster performance metrics.
    """
    out = {}
    
    val_counts = df.cluster.value_counts().to_dict()
    
    for k, v in val_counts.items():
        out[f'cluster_{k}'] = {'n': v}
        
    categorical = list(data_dict['categorical'].keys())
    continuous = []
    for f in df_clean.drop(categorical+['cluster'], axis=1).columns:
        if df_clean[f].nunique() == 2:
            categorical.append(f)
        else:
            continuous.append(f)
            
    # information gain of categorical features
    information_gain = []
    for cat in categorical:
        information_gain.append((cat, info_gain(df_clean, cat)))
    information_gain = sorted(information_gain, key=lambda x: x[1])
    
    out['cat_information_gain'] = information_gain
    
    # relative feature compactness
    cont = df[continuous+['cluster']]
    rel_std = 1 - cont.groupby('cluster').std() / cont.drop('cluster', axis=1).std()
    
    for c in rel_std.index:
        t = rel_std.loc[c]
        out[f'cluster_{c}']['compact_features'] = t[t != 0].sort_values().to_dict()
    
    return df, out


def impt_df(out, rf=None, k_search=None, k_min=None):
    """Create a combined importances DataFrame.

    Args:
        out (dict): Dictionary with several importances metrics.
        rf (DataFrame, optional): DataFrame with Rnadom Forest feature importances from get_fi function. Defaults to None.
        k_search (dict, optional): Dictionary with metrics from score_k function. Defaults to None.
        k_min (int, optional): Minimum k value from score_k function. Defaults to None.

    Returns:
        DataFrame: Consolidated feature importances.
    """
    impts = []
    for k, v in out.items():
        if k.startswith('cluster_'):
            impts.append({'cluster': int(k[-1]), 'feature': 'all',
                        'impt': out[k]['n'], 'kind': 'num'})
            for feat, impt in v['compact_features'].items():
                impts.append({'cluster': int(k[-1]), 'feature': feat, 
                              'impt': impt, 'kind': 'feature_compactness'})
        elif k == 'cat_information_gain':
            impts.extend([{'cluster': -99, 'feature': feat, 'impt': impt, 
                          'kind': 'info_gain'} for feat, impt in v])
    out = pd.DataFrame.from_records(impts)
    
    if isinstance(rf, pd.DataFrame):
        rf['cluster'] = -99
        rf['kind'] = 'random_forest'
        out = pd.concat([out, rf])
    if isinstance(k_search, dict):
        wss = pd.DataFrame(range(k_min, k_min+len(k_search['wss'])), columns=['feature'])
        wss['impt'] = k_search['wss']
        wss['kind'] = 'wss'
        wss['cluster'] = -99
        
        ss = pd.DataFrame(range(k_min, k_min+len(k_search['sil'])), columns=['feature'])
        ss['impt'] = k_search['sil']
        ss['kind'] = 'silhouette'
        ss['cluster'] = -99
        
        out = pd.concat([out, wss, ss])

    out["rnk"] = out.groupby(["kind", "cluster"])["impt"].rank("dense", ascending=False)
        
    return out.reset_index(drop=True)

def add_attribute_to_parent(audienceId, td_api_key, db, table, user_id, td_api_server,
            col_name='autosegmentation_cluster', rerun_master_segment='no'):
    
    source_headers = {
    'Authorization': 'TD1 '+ td_api_key}

    segment_api = td_api_server.replace('api', 'api-cdp')
    parent = f'{segment_api}/audiences/{audienceId}'
    parent_all = requests.put(parent, headers=source_headers).json()
    parent_attr = parent_all['attributes']
    
    new_attr = {'audienceId': audienceId,
         'name': col_name,
         'type': 'string',
         'parentDatabaseName': db,
         'parentTableName': table,
         'parentColumn': 'cluster_label',
         'parentKey': user_id,
         'foreignKey': user_id,
         'matrixColumnName': col_name,
         'groupingName': None}
    
    parent_attr.append(new_attr)
    
    update_ms = requests.put(parent, headers=source_headers, json=parent_all)
    
    if update_ms.status_code == 200:
        print("Successfully added attribute to Parent Segment")
    else:
        try: 
            'not unique' in update_ms.json()['base'][0]
            print("Attribute already exists in Parent Segment")
        except:
            print(update_ms.json())
            
    # condition to rerun master segment
    if rerun_master_segment=='yes':
        run_master = requests.post(f'{segment_api}/audiences/{audienceId}/run', headers=source_headers)
        if run_master.status_code == 200:
            print('Successfully triggered rerun of Master Segment')
        else:
            print(run_master.json())
        
    return update_ms


def create_new_segments(folderId, td_api_key, as_values, td_api_server):
    """_summary_

    Args:
        folderId (_type_): _description_
        td_api_key (_type_): _description_
        as_values (_type_): _description_
        td_api_server (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    destination_headers = {
    'Authorization': 'TD1 '+ td_api_key,
    'content-type': 'application/json'}

    segment_api = td_api_server.replace('api', 'api-cdp')
    
    new_folder = {'attributes': {'name': 'Auto-Segmentation Segments', 
                                 'description': 'Segments automatically created.'},
                 'relationships': {'parentFolder': {'data': {'id': folderId, 'type': "folder-segment"}}}}
    try: 
        audience = requests.post(f'{segment_api}/entities/folders/', 
                                 headers=destination_headers, json=new_folder)
    
        if audience.status_code == 200:
            print('Auto-Segmentation folder successfully created')
            folder_id = audience.json()['id']
            
        else:
            # if folder already exists
            try:
                objs = requests.get(f'{segment_api}/entities/by-folder/{folderId}', 
                                              headers=destination_headers, json={'depth':2}).json()

                folder_id = [o for o in objs['data'] if o['attributes']['name']=='Auto-Segmentation Segments v5'][0]['id']
                print('Segment folder already exists, creating segments...')
                
            except:
                print("Unable to create segment folder")
                print(audience.json())
                
    except Exception as e: 
        print(e)
    
    segments_json = []
    for cl in as_values:
        
        rule = {'type': 'And',
                 'conditions': [{'conditions': [{'type': 'Value',
                     'leftValue': {'name': 'cluster_label', 'visibility': 'clear'},
                     'operator': {'not': False, 'rightValue': cl, 'type': 'Equal'},
                     'arrayMatching': None,
                     'exclude': False}],
                   'type': 'And',
                   'description': '',
                   'expr': ''}],
                 'expr': ''}
        
        json_payload = {
                'attributes': {'name': cl.title(), 
                               'description': 'Segment Created by Autosegmentation Workflow', 
                               'rule': rule,},
                'relationships': {'parentFolder': {'data': {'id': folder_id, 'type': 'folder-segment'}}
            }
        }
        
        segment_creation = requests.post(f'{segment_api}/entities/segments',
                                         headers=destination_headers, json=json_payload)
        if segment_creation.status_code == 200:
            print(f'Segment successfully created: {cl}')
            segments_json.append(segment_creation.json())
        else:
            try:
                segment_creation.json()['errors']['name'][0] == 'has already been taken'
                print(f'Segment {cl.title()} already exists')
            except:
                print(segment_creation.json()) ### check to see if segment already exists
            
    return segments_json

def get_histo(df_clean, impt_df, user_id, n=50):
    
    cont = impt_df[impt_df.kind=='feature_compactness']['feature'].unique().tolist()

    histo = df_clean.copy()[cont+['cluster']]

    for c in cont:
        bins = n
        hist = pd.qcut(histo[c], n, duplicates='drop')
        while hist.nunique() == 1:
            bins = bins + n
            hist = pd.qcut(histo[c], bins, duplicates='drop')
        histo[c] = hist

    histos = []
    for c in cont:
        h = histo.reset_index()[[c, 'cluster', user_id]].groupby(['cluster', c]).count().reset_index()
        h.columns = ['cluster', 'range', 'freq']
        h['feature'] = c
        histos.append(h)

    out = pd.concat(histos)
    out['lower'] = out['range'].map(lambda x: x.left)
    out['upper'] = out['range'].map(lambda x: x.right)
    
    cat = impt_df[impt_df.kind == 'info_gain']['feature'].tolist()
    
    cats = []
    for c in cat:
        ct = df_clean.reset_index()[[user_id, 'cluster', c]].groupby(['cluster', c]).count().reset_index()
        ct.columns = ['cluster', 'range', 'freq']
        ct['feature'] = c
        cats.append(ct)
    cats = pd.concat(cats)
    out = pd.concat([out, cats])
    
    return out.reset_index(drop=True)

def obj_size_fmt(num):
    if num<10**3:
        return "{:.2f}{}".format(num,"B")
    elif ((num>=10**3)&(num<10**6)):
        return "{:.2f}{}".format(num/(1.024*10**3),"KB")
    elif ((num>=10**6)&(num<10**9)):
        return "{:.2f}{}".format(num/(1.024*10**6),"MB")
    else:
        return "{:.2f}{}".format(num/(1.024*10**9),"GB")


def memory_usage():
    memory_usage_by_variable=pd.DataFrame({k:sys.getsizeof(v)\
    for (k,v) in globals().items()},index=['Size'])
    memory_usage_by_variable=memory_usage_by_variable.T
    memory_usage_by_variable=memory_usage_by_variable.sort_values(by='Size',ascending=False).head(10)
    memory_usage_by_variable['Size']=memory_usage_by_variable['Size'].apply(lambda x: obj_size_fmt(x))
    return memory_usage_by_variable
