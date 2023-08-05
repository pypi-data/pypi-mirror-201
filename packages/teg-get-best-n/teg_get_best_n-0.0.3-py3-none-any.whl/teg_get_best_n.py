import numpy as np

# Estimate the true/generating number of components/dimensions.

# Generate test data
def make_sim_data(nObs, nVar, nL, noise):
    X = noise * np.random.rand(nObs, nVar)
    for iL in range(nL):
        coeffs = np.random.rand(nVar).reshape(1, nVar)
        coeffs = (coeffs - np.mean(coeffs)) / np.sqrt(np.var(coeffs))
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
        sims.append(Sims[most_sim_ind, iL])
        #Sims[most_sim_ind, iL] = 0
    sims.sort()
    sims = sims[::-1]
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
    m = np.median(Sims, axis=0)
    return m

def sims_split(sims):
    if len(sims) < 2:
        return 0
    k_v = [0]
    scores = [1]
    scores_unadjusted = [1]
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
        scores_unadjusted.append(score)
        score = score * (1 - k/len(sims))
        scores.append(score)
        k_v.append(k)
    if np.max(scores) > 1:
        nComp = k_v[np.argmax(scores_unadjusted)]
    else:
        nComp = k_v[np.argmax(scores)]
    return nComp, np.max(scores)

def get_n_components(X, nIts=10):
    eigenvalues, eigenvectors = run_PCA(X)
    sims = sim_per_component(X, nIts=nIts)
    nComp, max_score = sims_split(sims)
    return {'nComponents': nComp, 'eigenvalues': eigenvalues, 'eigenvectors': eigenvectors}
