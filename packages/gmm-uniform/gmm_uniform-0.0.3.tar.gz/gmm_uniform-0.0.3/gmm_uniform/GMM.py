import numpy as np
from scipy.stats import multivariate_normal, wishart


class GMM_Uniform:
  def __init__(self, K, n_init=20, uniform=True):
    self.K = K
    self.n_init = n_init
    self.uniform = uniform

  def _initialization(self, X):
    p = X.shape[1]
    self.p = np.random.dirichlet([1]*(self.K + (1 if self.uniform else 0)))
    self.mean =  np.random.permutation(X)[:self.K]
    self.cov = np.zeros((self.K, p, p))
    for k in range(self.K):
      self.cov[k] = wishart.rvs(df=p, scale=[0.1]*p)

    self.a = X.max(axis=0)
    self.b = X.min(axis=0)
    self.uniform_proba = np.prod(1/(self.a - self.b))

  def fit(self, X, max_iter=100):
    n_tries = 0
    max_ll = -np.inf
    while n_tries < self.n_init:
      try:
        likelihood_history, p, mean, cov = self._fit(X, max_iter)
        ll = likelihood_history[-1]
        if ll > max_ll:
          max_ll = ll
          max_p = p
          max_mean = mean
          max_cov = cov
          max_likelihood_history = likelihood_history

        n_tries += 1
      except:
        pass

    self.p = max_p
    self.mean = max_mean
    self.cov = max_cov
    self.likelihood_history = max_likelihood_history


  def _fit(self, X, max_iter=100):
    likelihood_history = []
    self._initialization(X)
    for i in range(max_iter):
      P = self.expectation(X)
      self.maximization(X, P)
      likelihood_history.append(self.log_likelihood(X))
    return likelihood_history, self.p, self.mean, self.cov

  def maximization(self, X, P):
    n = len(X)
    d = X.shape[1]
    nk = P.sum(axis=0)
    self.p = nk / n
    self.mean = (P.T @ X) / nk[None].T
    for k in range(self.K):
      p = P[:, k]
      X_ = X - self.mean[k]
      self.cov[k] = ((X_ * p[None].T).T @ X_) / p.sum()

  def expectation(self, X):
    n = len(X)
    fk = np.zeros((self.K + (1 if self.uniform else 0), n))
    for k in range(self.K):
      fk[k, :] = multivariate_normal.pdf(X, self.mean[k], self.cov[k]) 

    if self.uniform:
      fk[self.K, :] = self.uniform_proba
    
    f = fk.T @ self.p
    P = ((fk.T * self.p).T / f).T
    return P
  
  def probas(self, X):
    n = len(X)
    fk = np.zeros((self.K + (1 if self.uniform else 0), n))
    for k in range(self.K):
      fk[k, :] = multivariate_normal.pdf(X, self.mean[k], self.cov[k])

    if self.uniform:
      fk[self.K, :] = self.uniform_proba
    
    P = fk.T * self.p
    return P
    
  def predict(self, X):
    n = len(X)
    fk = np.zeros((self.K + (1 if self.uniform else 0), n))
    for k in range(self.K):
      fk[k, :] = multivariate_normal.pdf(X, self.mean[k], self.cov[k])

    if self.uniform:
      fk[self.K, :] = self.uniform_proba
    
    P = fk.T * self.p
    y_hat = P.argmax(axis=1) + 1
    return y_hat

  def log_likelihood(self, X):
    n = len(X)
    fk = np.zeros((self.K + (1 if self.uniform else 0), n))
    for k in range(self.K):
      fk[k, :] = multivariate_normal.pdf(X, self.mean[k], self.cov[k])

    if self.uniform:
      fk[self.K, :] = self.uniform_proba
    
    f = fk.T @ self.p
    return np.log(f).sum()


  def log_likelihood_completed(self, X):
    n = len(X)
    fk = np.zeros((self.K + (1 if self.uniform else 0), n))
    for k in range(self.K):
      fk[k, :] = multivariate_normal.logpdf(X, self.mean[k], self.cov[k])

    if self.uniform:
      fk[self.K, :] = np.log(self.uniform_proba)

    P = fk.T + np.log(self.p)
    Z = P.argmax(axis=1)
    mask = Z[:, None] == np.array([np.arange(self.K + (1 if self.uniform else 0))])
    return P[mask].sum()

  def BIC(self, X):
    p = X.shape[1]
    log_likelihood = self.log_likelihood(X)
    n = len(X)
    v = self.K - 1 + (self.K * p) + (self.K * p * (p+1)/2)
    return 2 * log_likelihood - v * np.log(n) + ((2*p) if self.uniform else 0)
    
  def ICL(self, X):
    p = X.shape[1]
    log_likelihood_completed = self.log_likelihood_completed(X)
    v = self.K - 1 + (self.K * p) + (self.K * p * (p+1)/2)
    return log_likelihood_completed - v * np.log(np.pi*2) / 2 + ((2*p) if self.uniform else 0)
  


def auto_gmm(X, k, n_init=20):
  gmm_uniform = GMM_Uniform(k, n_init=n_init, uniform=True)
  gmm_uniform.fit(X, max_iter=100)
  bic_uniform = gmm_uniform.BIC(X)

  gmm_non_uniform = GMM_Uniform(k, n_init=n_init, uniform=False)
  gmm_non_uniform.fit(X, max_iter=100)
  bic_non_uniform = gmm_non_uniform.BIC(X)

  if bic_non_uniform > bic_uniform:
    chosen_model = gmm_non_uniform
    bic = bic_non_uniform
    uniform_component = False
  else:
    chosen_model = gmm_uniform
    bic = bic_uniform
    uniform_component = True

  probas = chosen_model.probas(X)
  labels = chosen_model.predict(X)

  
  return {
      "uniform_component": uniform_component,
      "probas": probas,
      "labels": labels,
      "likelihood_history": chosen_model.likelihood_history,
      "BIC": bic,
      "param_proportion": chosen_model.p,
      "param_means": chosen_model.mean,
      "param_cov": chosen_model.cov
  }
