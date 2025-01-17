# Copyright 2019 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for the hafnian sampling functions"""
# pylint: disable=no-self-use,redefined-outer-name
import pytest

import numpy as np
from scipy.stats import nbinom

from hafnian.samples import (
    hafnian_sample_state,
    hafnian_sample_graph,
    torontonian_sample_state,
    hafnian_sample_classical_state,
    torontonian_sample_classical_state,
    seed,
)
from hafnian.quantum import gen_Qmat_from_graph, density_matrix_element

seed(137)

rel_tol = 3.0
abs_tol = 1.0e-10


def TMS_cov(r, phi):
    """returns the covariance matrix of a TMS state"""
    cp = np.cos(phi)
    sp = np.sin(phi)
    ch = np.cosh(r)
    sh = np.sinh(r)

    S = np.array(
        [
            [ch, cp * sh, 0, sp * sh],
            [cp * sh, ch, sp * sh, 0],
            [0, sp * sh, ch, -cp * sh],
            [sp * sh, 0, -cp * sh, ch],
        ]
    )

    return S @ S.T


class TestHafnianSampling:
    """Tests for hafnian sampling"""

    def test_TMS_hafnian_sample_states(self):
        """test sampling from TMS hafnians is correlated"""
        m = 0.432
        phi = 0.546
        V = TMS_cov(np.arcsinh(m), phi)
        res = hafnian_sample_state(V, samples=20)
        assert np.allclose(res[:, 0], res[:, 1])

    def test_TMS_hafnian_sample_states_cutoff(self):
        """test sampling from TMS hafnians is correlated"""
        m = 0.432
        phi = 0.546
        V = TMS_cov(np.arcsinh(m), phi)
        res = hafnian_sample_state(V, samples=20, cutoff=5)
        assert np.allclose(res[:, 0], res[:, 1])

    def test_hafnian_sample_states_nonnumpy(self):
        """test exception is raised if not a numpy array"""
        with pytest.raises(TypeError):
            hafnian_sample_state(5, samples=20)

    def test_hafnian_sample_states_nonsquare(self):
        """test exception is raised if not a numpy array"""
        with pytest.raises(ValueError, match="Covariance matrix must be square."):
            hafnian_sample_state(np.array([[0, 5, 3], [0, 1, 2]]), samples=20)

    def test_hafnian_sample_states_nans(self):
        """test exception is raised if not a numpy array"""
        with pytest.raises(ValueError, match="Covariance matrix must not contain NaNs."):
            hafnian_sample_state(np.array([[0, 5], [0, np.NaN]]), samples=20)

    def test_single_squeezed_state_hafnian(self):
        """Test the sampling routines by comparing the photon number frequencies and the exact
        probability distribution of a single mode squeezed vacuum state
        """
        n_samples = 1000
        mean_n = 1.0
        r = np.arcsinh(np.sqrt(mean_n))
        sigma = np.array([[np.exp(2 * r), 0.0], [0.0, np.exp(-2 * r)]])

        n_cut = 10
        samples = hafnian_sample_state(sigma, samples=n_samples, cutoff=n_cut)
        bins = np.arange(0, max(samples) + 1, 1)
        (freq, _) = np.histogram(samples, bins=bins)
        rel_freq = freq / n_samples
        nm = max(samples) // 2

        x = nbinom.pmf(np.arange(0, nm, 1), 0.5, np.tanh(np.arcsinh(np.sqrt(mean_n))) ** 2)
        x2 = np.zeros(2 * len(x))
        x2[::2] = x
        rel_freq = freq[0:-1] / n_samples
        x2 = x2[0 : len(rel_freq)]

        assert np.allclose(
            rel_freq, x2, atol=rel_tol / np.sqrt(n_samples), rtol=rel_tol / np.sqrt(n_samples)
        )

    def test_two_mode_squeezed_state_hafnian(self):
        """Test the sampling routines by comparing the photon number frequencies and the exact
        probability distribution of a two mode squeezed vacuum state
        """
        n_samples = 1000
        n_cut = 5
        mean_n = 1.0
        r = np.arcsinh(np.sqrt(mean_n))
        c = np.cosh(2 * r)
        s = np.sinh(2 * r)
        sigma = np.array([[c, s, 0, 0], [s, c, 0, 0], [0, 0, c, -s], [0, 0, -s, c]])

        samples = hafnian_sample_state(sigma, samples=n_samples, cutoff=n_cut)
        assert np.all(samples[:, 0] == samples[:, 1])

        samples1d = samples[:, 0]
        bins = np.arange(0, max(samples1d) + 1, 1)

        (freq, _) = np.histogram(samples1d, bins=bins)
        rel_freq = freq / n_samples

        probs = (1.0 / (1.0 + mean_n)) * (mean_n / (1.0 + mean_n)) ** bins[0:-1]
        probs[-1] = 1.0 - np.sum(
            probs[0:-1]
        )  # Coarse grain all the probabilities past the threshold

        assert np.allclose(
            rel_freq, probs, atol=rel_tol / np.sqrt(n_samples), rtol=rel_tol / np.sqrt(n_samples)
        )

    def test_displaced_two_mode_squeezed_state_hafnian(self):
        """Test the sampling routines by comparing the photon number frequencies and the exact
        probability distribution of a displaced two mode squeezed vacuum state
        """
        n_samples = 1000
        n_cut = 10
        mean_n = 1
        r = np.arcsinh(np.sqrt(mean_n))
        c = np.cosh(2 * r)
        s = np.sinh(2 * r)
        sigma = np.array([[c, s, 0, 0], [s, c, 0, 0], [0, 0, c, -s], [0, 0, -s, c]])
        mean = 2 * np.array([0.1, 0.25, 0.1, 0.25])
        samples = hafnian_sample_state(sigma, samples=n_samples, mean=mean, cutoff=n_cut)

        probs = np.real_if_close(
            np.array(
                [
                    [density_matrix_element(mean, sigma, [i, j], [i, j]) for i in range(n_cut)]
                    for j in range(n_cut)
                ]
            )
        )
        freq, _, _ = np.histogram2d(samples[:, 1], samples[:, 0], bins=np.arange(0, n_cut + 1))
        rel_freq = freq / n_samples

        assert np.allclose(
            rel_freq, probs, rtol=rel_tol / np.sqrt(n_samples), atol=rel_tol / np.sqrt(n_samples)
        )

    @pytest.mark.parametrize("sample_func", [hafnian_sample_state, hafnian_sample_classical_state])
    def test_displaced_single_mode_state_hafnian(self, sample_func):
        """Test the sampling routines by comparing the photon number frequencies and the exact
        probability distribution of a single mode coherent state
        """
        n_samples = 1000
        n_cut = 6
        sigma = np.identity(2)
        mean = 10 * np.array([0.1, 0.25])

        samples = sample_func(sigma, samples=n_samples, mean=mean, cutoff=n_cut)

        probs = np.real_if_close(
            np.array([density_matrix_element(mean, sigma, [i], [i]) for i in range(n_cut)])
        )
        freq, _ = np.histogram(samples[:, 0], bins=np.arange(0, n_cut + 1))
        rel_freq = freq / n_samples
        assert np.allclose(
            rel_freq, probs, rtol=rel_tol / np.sqrt(n_samples), atol=rel_tol / np.sqrt(n_samples)
        )

    @pytest.mark.parametrize("sample_func", [hafnian_sample_state, hafnian_sample_classical_state])
    def test_displaced_two_mode_state_hafnian(self, sample_func):
        """Test the sampling routines by comparing the photon number frequencies and the exact
        probability distribution of a two mode coherent state
        """
        n_samples = 1000
        n_cut = 6
        sigma = np.identity(4)
        mean = 5 * np.array([0.1, 0.25, 0.1, 0.25])
        samples = sample_func(sigma, samples=n_samples, mean=mean, cutoff=n_cut)
        # samples = hafnian_sample_classical_state(sigma, mean = mean, samples = n_samples)
        probs = np.real_if_close(
            np.array(
                [
                    [density_matrix_element(mean, sigma, [i, j], [i, j]) for i in range(n_cut)]
                    for j in range(n_cut)
                ]
            )
        )
        freq, _, _ = np.histogram2d(samples[:, 1], samples[:, 0], bins=np.arange(0, n_cut + 1))
        rel_freq = freq / n_samples

        assert np.allclose(
            rel_freq, probs, rtol=rel_tol / np.sqrt(n_samples), atol=rel_tol / np.sqrt(n_samples)
        )

    def test_hafnian_sample_graph(self):
        """Test hafnian sampling from a graph"""
        A = np.array([[0, 3.0 + 4j], [3.0 + 4j, 0]])
        n_samples = 1000
        mean_n = 0.5
        samples = hafnian_sample_graph(A, mean_n, samples=n_samples)
        approx_mean_n = np.sum(samples) / n_samples
        assert np.allclose(mean_n, approx_mean_n, rtol=2e-1)

    def test_single_pm_graphs(self):
        """Tests that the number of photons is the same for modes i and n-i
        in the special case of a graph with one single perfect matching
        """
        n = 10  # size of the graph
        approx_samples = 1e3  # number of samples in the hafnian approximation
        A = np.eye(n)[::-1]
        n_mean = 2
        nr_samples = 10

        samples = hafnian_sample_graph(
            A, n_mean, cutoff=5, approx=True, approx_samples=approx_samples, samples=nr_samples
        )

        test_passed = True
        for i in range(nr_samples):
            s = samples[i]
            for k in range(len(s) // 2):
                if s[k] + s[-(k + 1)] % 2 == 1:
                    test_passed = False

        assert test_passed

    def test_probability_vacuum(self):
        """Tests that the probability of zero photons is correct"""

        n = 4  # n is the size of the graph
        approx_samples = 1e3  # number of samples in the hafnian approximation
        A = np.random.binomial(1, 0.5, (n, n))

        A = np.triu(A)
        A = A + np.transpose(A)
        n_mean = 1.0
        Q = gen_Qmat_from_graph(A, n_mean)
        prob0 = np.abs(1 / (np.sqrt(np.linalg.det(Q))))

        nr_samples = 100
        samples = hafnian_sample_graph(
            A, n_mean, cutoff=5, approx=True, approx_samples=approx_samples, samples=nr_samples
        )
        nr_zeros = 0

        for i in range(nr_samples):
            photons = np.sum(samples[i])
            if photons == 0:
                nr_zeros += 1

        prob0_estimate = nr_zeros / nr_samples
        # allowed error in estimation
        delta = 0.2

        assert np.abs(prob0 - prob0_estimate) < delta

    @pytest.mark.parametrize("sample_func", [hafnian_sample_state, hafnian_sample_classical_state])
    def test_multimode_vacuum_state_hafnian(self, sample_func):
        """Test the sampling routines by checking the samples for pure vacuum
        using the sampler for classical states
        """
        n_samples = 100
        n_modes = 10
        sigma = np.identity(2 * n_modes)
        zeros = np.zeros(n_modes, dtype=np.int)
        samples = sample_func(
            sigma, samples=n_samples
        )  # hafnian_sample_classical_state(sigma, samples=n_samples)
        for i in range(n_samples):
            assert np.all(samples[i] == zeros)

    @pytest.mark.parametrize("sample_func", [hafnian_sample_state, hafnian_sample_classical_state])
    def test_thermal_state_hafnian(self, sample_func):
        """Test the sampling routines by checking the samples for a single mode
        thermal state
        """
        n_samples = 10000
        mean_n = 0.5
        sigma = (2 * mean_n + 1) * np.identity(2)
        samples = sample_func(sigma, samples=n_samples)
        bins = np.arange(0, max(samples), 1)
        (freq, _) = np.histogram(samples, bins=bins)
        rel_freq = freq / n_samples

        probs = (1.0 / (1.0 + mean_n)) * (mean_n / (1.0 + mean_n)) ** bins[0:-1]
        assert np.all(np.abs(rel_freq - probs) < rel_tol / np.sqrt(n_samples))


class TestTorontonianSampling:
    """Tests for torontonian sampling"""

    def test_torontonian_samples_nonnumpy(self):
        """test exception is raised if not a numpy array"""
        with pytest.raises(TypeError):
            torontonian_sample_state(5, samples=20)

    def test_torontonian_samples_nonsquare(self):
        """test exception is raised if not a numpy array"""
        with pytest.raises(ValueError, match="Covariance matrix must be square."):
            torontonian_sample_state(np.array([[0, 5, 3], [0, 1, 2]]), samples=20)

    def test_torontonian_samples_nans(self):
        """test exception is raised if not a numpy array"""
        with pytest.raises(ValueError, match="Covariance matrix must not contain NaNs."):
            torontonian_sample_state(np.array([[0, 5], [0, np.NaN]]), samples=20)

    def test_single_squeezed_state_torontonian(self):
        """Test the sampling routines by comparing the photon number frequencies and the exact
        probability distribution of a single mode squeezed vacuum state
        """
        n_samples = 10000
        mean_n = 1.0
        r = np.arcsinh(np.sqrt(mean_n))
        sigma = np.array([[np.exp(2 * r), 0.0], [0.0, np.exp(-2 * r)]])
        samples = torontonian_sample_state(sigma, samples=n_samples)
        samples_list = list(samples)

        rel_freq = np.array([samples_list.count(0), samples_list.count(1)]) / n_samples
        x2 = np.empty([2])

        x2[0] = 1.0 / np.sqrt(1.0 + mean_n)
        x2[1] = 1.0 - x2[0]
        assert np.allclose(
            rel_freq, x2, atol=rel_tol / np.sqrt(n_samples), rtol=rel_tol / np.sqrt(n_samples)
        )

    def test_two_mode_squeezed_state_torontonian(self):
        """Test the sampling routines by comparing the photon number frequencies and the exact
        probability distribution of a two mode squeezed vacuum state
        """
        n_samples = 1000
        mean_n = 1.0
        r = np.arcsinh(np.sqrt(mean_n))
        c = np.cosh(2 * r)
        s = np.sinh(2 * r)
        sigma = np.array([[c, s, 0, 0], [s, c, 0, 0], [0, 0, c, -s], [0, 0, -s, c]])

        samples = torontonian_sample_state(sigma, samples=n_samples)
        assert np.all(samples[:, 0] == samples[:, 1])

        samples1d = samples[:, 0]
        bins = np.arange(0, max(samples1d), 1)
        (freq, _) = np.histogram(samples1d, bins=bins)
        rel_freq = freq / n_samples

        probs = np.empty([2])
        probs[0] = 1.0 / (1.0 + mean_n)
        probs[1] = 1.0 - probs[0]
        assert np.allclose(
            rel_freq,
            probs[0:-1],
            atol=rel_tol / np.sqrt(n_samples),
            rtol=rel_tol / np.sqrt(n_samples),
        )

    @pytest.mark.parametrize(
        "sample_func", [torontonian_sample_state, torontonian_sample_classical_state]
    )
    def test_multimode_vacuum_state_torontonian(self, sample_func):
        """Test the sampling routines by checking the samples for pure vacuum
        """
        n_samples = 100
        n_modes = 10
        sigma = np.identity(2 * n_modes)
        zeros = np.zeros(n_modes, dtype=np.int)
        samples = sample_func(sigma, samples=n_samples)
        for i in range(n_samples):
            assert np.all(samples[i] == zeros)

    @pytest.mark.parametrize(
        "sample_func", [torontonian_sample_state, torontonian_sample_classical_state]
    )
    def test_thermal_state_torontonian(self, sample_func):
        """Test the sampling routines by checking the samples for a single mode
        thermal state
        """
        n_samples = 10000
        mean_n = 0.5
        sigma = (2 * mean_n + 1) * np.identity(2)
        samples = sample_func(sigma, samples=n_samples)
        bins = np.array([0, 1, 2])
        (freq, _) = np.histogram(samples, bins=bins)
        rel_freq = freq / n_samples

        probs = np.zeros([2])
        probs[0] = 1.0 / (1.0 + mean_n)
        probs[1] = 1 - probs[0]
        assert np.all(np.abs(rel_freq - probs) < rel_tol / np.sqrt(n_samples))


def test_seed():
    """Tests that seed method does reset the random number generators"""
    n_samples = 10
    mean_n = 1.0
    r = np.arcsinh(np.sqrt(mean_n))
    V = np.array([[np.exp(2 * r), 0.0], [0.0, np.exp(-2 * r)]])
    seed(137)
    first_sample = hafnian_sample_state(V, n_samples)
    second_sample = hafnian_sample_state(V, n_samples)
    seed(137)
    first_sample_p = hafnian_sample_state(V, n_samples)
    second_sample_p = hafnian_sample_state(V, n_samples)
    assert np.array_equal(first_sample, first_sample_p)
    assert np.array_equal(second_sample, second_sample_p)
