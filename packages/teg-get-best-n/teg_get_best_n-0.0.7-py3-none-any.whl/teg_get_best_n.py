import numpy as np

# Estimate the true/generating number of components/dimensions.

# Generate test data
def make_sim_data(nObs, nVar, nL, noise):
    X = noise * np.random.rand(nObs, nVar)
    for iL in range(nL):
        coeffs = np.random.rand(nVar).reshape(1, nVar)
        y1 = np.random.rand(nObs, 1)
        X = X + y1 @ coeffs
    return X

# Similarity of eigenvectors over split-halves
def run_PCA(X):
    X = X - np.mean(X, axis=0)
    C = np.cov(np.transpose(X))
    eigenvalues, eigenvectors = np.linalg.eig(C)
    return eigenvalues, eigenvectors

def get_eigenvector_sims(X1, X2):
    eigenvalues1, eigenvectors1 = run_PCA(X1)
    eigenvalues2, eigenvectors2 = run_PCA(X2)
    Sims = np.abs(np.transpose(eigenvectors1) @ eigenvectors2)
    sims = []
    for iL in range(Sims.shape[1]):
        most_sim_ind = np.argmax(Sims[:, iL])
        s = Sims[most_sim_ind, iL]
        sims.append(s)
        Sims[most_sim_ind, iL] = 0
    return sims

def sim_per_component(X, nIts = 20):
    nObs, nVar = X.shape
    Sims = np.zeros((nIts, nVar))
    for iIt in range(nIts):
        rng = np.random.default_rng()
        indices = rng.choice(range(nObs), size=nObs, replace=False)
        half = np.floor(len(indices)/2).astype(int)
        X1 = X[indices[:half],:]
        X2 = X[indices[(half + 1):],:]
        sims = get_eigenvector_sims(X1, X2)
        Sims[iIt,:] = sims
    m = np.mean(Sims, axis=0)
    return m

def sims_split(sims):
    if len(sims) < 2:
        return 0
    k_v = []
    scores = []
    scores_adjusted = []
    for k in range(1, len(sims) - 1):
        lhs = sims[:k]
        rhs = sims[(k + 1):]
        ws_left = np.var(lhs)
        ws_right = np.var(rhs)
        m_lhs = np.mean(lhs)
        m_rhs = np.mean(rhs)
        betw_v = [m_lhs for n in lhs]
        betw_v = betw_v + [m_rhs for n in rhs]
        bs = np.var(betw_v)
        score = bs / (ws_left + ws_right)
        scores.append(score)
        score_adjusted = score * (1 - (k - 1)/len(sims))
        scores_adjusted.append(score_adjusted)
        k_v.append(k)
    nComp = k_v[np.argmax(scores)]
    zeroComp = False
    if nComp > 0:
        if scores_adjusted[nComp - 1] < 1:
            zeroComp = True
    return nComp, zeroComp

def get_n_components(X, nIts=30):
    eigenvalues, eigenvectors = run_PCA(X)
    sims = sim_per_component(X, nIts=nIts)
    nComp, zeroComp = sims_split(sims)
    return {'nComponents': nComp, 'zeroComponents': zeroComp, 'eigenvalues': eigenvalues, 'eigenvectors': eigenvectors}
