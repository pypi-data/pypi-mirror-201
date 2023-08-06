import numpy as np
from sklearn.cluster import DBSCAN

# still need to check what to do with non-beam simulation

def get_t0(packets):

    t0 = []
    pckts_t0 = packets[packets['packet_type'] == 7]['timestamp'] # external trigger # by default larnd-sim fills external trigger for each event

    pckts_t0_db = pckts_t0.reshape(-1,1)

    db = DBSCAN(eps=50, min_samples=2).fit(pckts_t0_db)
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    for i_ct in range(n_clusters_):
        ct_mask = labels == i_ct
        t0.append(np.min(pckts_t0[ct_mask]))

    return np.array(t0)

def get_t0_spill(vertices, run_config):
    dt_beam = run_config['beam_duration']
    return (np.unique(vertices['t_spill']) + dt_beam *0.5) * 10

def packet_to_eventid(assn, tracks, ifspill):
    '''
    Assoiciate packet to eventID.
    
    Arguments
    ---------
    assn : array_like
        packet to track association (`mc_packets_assn`) from `larnd-sim` output
        
    tracks: array_like
        list of track segments
        
    Returns
    -------
    event_ids: ndarray (N,)
        array of eventID.
        `len(event_ids)` equals to `len(packets)`
    '''
    track_ids = assn['track_ids'].max(axis=-1)

    event_ids = np.full_like(track_ids, -1, dtype=int)
    mask = track_ids != -1

    if not ifspill:
        event_ids[mask] = tracks['eventID'][track_ids[mask]]
    if ifspill:
        event_ids[mask] = tracks['spillID'][track_ids[mask]]
        
    return event_ids
