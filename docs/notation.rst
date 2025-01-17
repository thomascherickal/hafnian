.. role:: raw-latex(raw)
   :format: latex

.. role:: html(raw)
   :format: html

.. _notation:


Notation
========
.. sectionauthor:: Nicolás Quesada <nicolas@xanadu.ai>


Matrices and vectors
********************

In this section we introduce the notation that is used in the rest of the documentation.

We deal with so-called bivectors in which the second half of their components is the complex conjugate of the first half. Thus if :math:`\mathbf{u} = (u_1,\ldots u_\ell) \in \mathbb{C}^{\ell}` then :math:`\vec{\alpha} = (\mathbf{u},\mathbf{u}^*) = (u_1,\ldots,u_\ell,u_1^*,\ldots,u_\ell^*)` is a bivector. We use uppercase letters for (multi)sets such as :math:`S = \{1,1,2\}`.

Following standard Python and C convention, we index starting from zero, thus the first :math:`\ell` natural numbers are :math:`[\ell]:=\{0,1,\ldots,\ell-1\}`.
We define the :math:`\text{diag}` function as follows: When acting on a vector :math:`\mathbf{u}` it returns a square diagonal matrix :math:`\mathbf{u}`. When acting on a square matrix it returns a vector with its diagonal entries.

Finally, we define the vector in diagonal (:math:`\text{vid}`) operation, that takes a matrix :math:`\mathbf{A}` of size :math:`n \times n` and a vector :math:`\mathbf{u}` of size :math:`n` and returns the matrix

.. math::
	\text{vid}(\mathbf{A},\mathbf{u}) = \mathbf{A} - \text{diag}(\text{diag}( \mathbf{A})) + \text{diag}(\mathbf{u}),

which is simply the matrix :math:`\mathbf{A}` with the vector :math:`\mathbf{u}` placed along its diagonal.


The reduction operation
***********************

It is very useful to have compact notation to deal with matrices that are constructed by removing or repeating rows and column of a given primitive matrix.
Imagine for example a given :math:`4 \times 4` matrix

.. math::
	\mathbf{A} = \left(
	\begin{array}{cccc}
	 A_{0,0} & A_{0,1} & A_{0,2} & A_{0,3} \\
	 A_{1,0} & A_{1,1} & A_{1,2} & A_{1,3} \\
	 A_{2,0} & A_{2,1} & A_{2,2} & A_{2,3} \\
	 A_{3,0} & A_{3,1} & A_{3,2} & A_{3,3} \\
	\end{array}
	\right),

and that you want to construct the following matrix

.. math::
	\mathbf{A}'= \left(
	\begin{array}{c|ccc||cc}
	 A_{0,0} & A_{0,1} & A_{0,1} & A_{0,1} & A_{0,3} & A_{0,3} \\
	 \hline
	 A_{1,0} & A_{1,1} & A_{1,1} & A_{1,1} & A_{1,3} & A_{1,3} \\
	 A_{1,0} & A_{1,1} & A_{1,1} & A_{1,1} & A_{1,3} & A_{1,3} \\
	 A_{1,0} & A_{1,1} & A_{1,1} & A_{1,1} & A_{1,3} & A_{1,3} \\
	 \hline
	 \hline
	 A_{3,0} & A_{3,1} & A_{3,1} & A_{3,1} & A_{3,3} & A_{3,3} \\
	 A_{3,0} & A_{3,1} & A_{3,1} & A_{3,1} & A_{3,3} & A_{3,3} \\
	\end{array}
	\right),

where the first row and column have been kept as they were, the second row and column have been repeated 3 times, the third row and column have been eliminated and the fourth and the last row and column have been repeated twice. To specify the number of repetitions (or elimination) of a given row-column we simply specify a vector of integers where each value tells us the number of repetitions, and we use the value 0 to indicate that a given row-column is removed. Thus defining :math:`\mathbf{m}=(1,3,0,2)` we find its reduction by :math:`\mathbf{m}` to be precisely the matrix in the last equation

.. math::
	\mathbf{A}' = \mathbf{A}_{\mathbf{n}}.

One can also define the reduction operation on vectors. For instance if :math:`\mathbf{u}=(u_0,u_1,u_2,u_3)` and :math:`\mathbf{m}=(1,3,0,2)` then :math:`\mathbf{u}_\mathbf{n} = (u_0,u_1,u_1,u_1,u_3,u_3)`.

.. tip::

   * The reduction operation is implemented as :func:`hafnian.reduction`.


Reduction on block matrices
***************************
When dealing with Gaussian states one typically encounters :math:`2\ell \times 2 \ell` block matrices of the following form

.. math::
	\mathbf{A} = \left(\begin{array}{c|c}
	\mathbf{C} & \mathbf{D} \\
	\hline
	\mathbf{E} & \mathbf{F} \\
	\end{array}
	\right),

where :math:`\mathbf{C},\mathbf{D},\mathbf{E},\mathbf{F}` are of size :math:`\ell \times \ell`.
Now imagine that one applies the reduction operation by a vector :math:`\mathbf{n} \in \mathbb{N}^{\ell}` to each of the blocks. We introduce the following notation

.. math::
	\mathbf{A}_{(\mathbf{n})} = \left(\begin{array}{c|c}
	\mathbf{C}_{\mathbf{n}} & \mathbf{D}_{\mathbf{n}} \\
	\hline
	\mathbf{E}_{\mathbf{n}} & \mathbf{F}_{\mathbf{n}} \\
	\end{array}
	\right),

where we have used the notation :math:`(\mathbf{n})` with the round brackets :math:`()` to indicate that the reduction is applied to the **blocks** of the matrix :math:`\mathbf{A}`.

Similarly to block matrices, one can also define a reduction operator for bivectors. Thus if :math:`\vec \beta = (u_0,u_1,u_2,u_3,u_0^*,u_1^*,u_2^*,u_3^*)` and :math:`\mathbf{m}=(1,3,0,2)`, then

.. math::
	\vec \beta_{(\mathbf{n} ) } = (u_0,u_1,u_1,u_1,u_3,u_3,u_0^*,u_1^*,u_1^*,u_1^*,u_3^*,u_3^*).


The reduction operation in terms of sets
****************************************

A different way of specifying how many times a given row and column must me repeated is by giving a set in which we simply list the columns to be repeated. Thus for example the reduction index vector :math:`\mathbf{n} = (1,3,0,2)` can alternatively be given as the (multiset)set :math:`S=\{0,1,1,1,3,3 \}` where the element 0 appears once to indicate the first row and column is repeated once, the index 1 appears three times to indicate that this row and column are repeated three times, etcetera.

Similarly for matrices of even size for which the following partition makes sense

.. math::
	\mathbf{A} = \left(\begin{array}{c|c}
	\mathbf{C} & \mathbf{D} \\
	\hline
	\mathbf{E} & \mathbf{F} \\
	\end{array}
	\right),

where :math:`\mathbf{A}` is of size :math:`2\ell \times 2\ell` and :math:`\mathbf{C},\mathbf{D},\mathbf{E},\mathbf{F}` are of size :math:`\ell \times \ell` we define

.. math::
	\mathbf{A}_{(S)} = \left(\begin{array}{c|c}
	\mathbf{C}_S & \mathbf{D}_S \\
	\hline
	\mathbf{E}_S & \mathbf{F}_S \\
	\end{array}
	\right).

This implies that if the index :math:`i` appears :math:`m_i` times in :math:`S` then the columns :math:`i` and :math:`i+\ell` of :math:`\mathbf{A}` will be repeated :math:`m_i` times in :math:`\mathbf{A}_S`.

For instance if

.. math::
	\mathbf{A} = \left(
	\begin{array}{ccc|ccc}
	 A_{0,0} & A_{0,1} & A_{0,2} & A_{0,3} & A_{0,4} & A_{0,5} \\
	 A_{1,0} & A_{1,1} & A_{1,2} & A_{1,3} & A_{1,4} & A_{1,5} \\
	 A_{2,0} & A_{2,1} & A_{2,2} & A_{2,3} & A_{2,4} & A_{2,5} \\
	 \hline
	 A_{3,0} & A_{3,1} & A_{3,2} & A_{3,3} & A_{3,4} & A_{3,5} \\
	 A_{4,0} & A_{4,1} & A_{4,2} & A_{4,3} & A_{4,4} & A_{4,5} \\
	 A_{5,0} & A_{5,1} & A_{5,2} & A_{5,3} & A_{5,4} & A_{5,5} \\
	\end{array}
	\right),

and :math:`S=\{0,0,2,2,2\}` one finds

.. math::
	\mathbf{A}_{(S)} = \left(
	\begin{array}{cc|ccc|cc|ccc}
	 A_{0,0} & A_{0,0} & A_{0,2} & A_{0,2} & A_{0,2} & A_{0,3} & A_{0,3} & A_{0,5} & A_{0,5} & A_{0,5} \\
	 A_{0,0} & A_{0,0} & A_{0,2} & A_{0,2} & A_{0,2} & A_{0,3} & A_{0,3} & A_{0,5} & A_{0,5} & A_{0,5} \\
	 \hline
	 A_{2,0} & A_{2,0} & A_{2,2} & A_{2,2} & A_{2,2} & A_{2,3} & A_{2,3} & A_{2,5} & A_{2,5} & A_{2,5} \\
	 A_{2,0} & A_{2,0} & A_{2,2} & A_{2,2} & A_{2,2} & A_{2,3} & A_{2,3} & A_{2,5} & A_{2,5} & A_{2,5} \\
	 A_{2,0} & A_{2,0} & A_{2,2} & A_{2,2} & A_{2,2} & A_{2,3} & A_{2,3} & A_{2,5} & A_{2,5} & A_{2,5} \\
	 \hline
	 A_{3,0} & A_{3,0} & A_{3,2} & A_{3,2} & A_{3,2} & A_{3,3} & A_{3,3} & A_{3,5} & A_{3,5} & A_{3,5} \\
	 A_{3,0} & A_{3,0} & A_{3,2} & A_{3,2} & A_{3,2} & A_{3,3} & A_{3,3} & A_{3,5} & A_{3,5} & A_{3,5} \\
	 \hline
	 A_{5,0} & A_{5,0} & A_{5,2} & A_{5,2} & A_{5,2} & A_{5,3} & A_{5,3} & A_{5,5} & A_{5,5} & A_{5,5} \\
	 A_{5,0} & A_{5,0} & A_{5,2} & A_{5,2} & A_{5,2} & A_{5,3} & A_{5,3} & A_{5,5} & A_{5,5} & A_{5,5} \\
	 A_{5,0} & A_{5,0} & A_{5,2} & A_{5,2} & A_{5,2} & A_{5,3} & A_{5,3} & A_{5,5} & A_{5,5} & A_{5,5} \\
	\end{array}
	\right).

The notation also extends in a straightforward fashion for bivectors. For example :math:`\vec \beta = (u_0,u_1,u_2,u_3,u_0^*,u_1^*,u_2^*,u_3^*)` and :math:`S=\{1,1,2\}` then
:math:`\vec \beta_{(S)} = (u_1,u_1,u_2,u_1^*,u_1^*,u_2^*)`.



This notation becomes handy when describing certain algorithms for the calculation of the hafnian and torontonian introduced in the rest of the documentation.


Combining reduction and vector in diagonal
******************************************

Here we show some basic examples of how the reduction and vector in diagonal operations work together

Consider the following matrix

.. math::
	\Sigma = \left(
	\begin{array}{ccc|ccc}
	 A_{0,0} & A_{0,1} & A_{0,2} & B_{0,0} & B_{0,1} & B_{0,2} \\
	 A_{1,0} & A_{1,1} & A_{1,2} & B_{1,0} & B_{1,1} & B_{1,2} \\
	 A_{2,0} & A_{2,1} & A_{2,2} & B_{2,0} & B_{2,1} & B_{2,2} \\
	 \hline
	 C_{0,0} & C_{0,1} & C_{0,2} & D_{0,0} & D_{0,1} & D_{0,2} \\
	 C_{1,0} & C_{1,1} & C_{1,2} & D_{1,0} & D_{1,1} & D_{1,2} \\
	 C_{2,0} & C_{2,1} & C_{2,2} & D_{2,0} & D_{2,1} & D_{2,2} \\
	\end{array}
	\right),

and bivector :math:`\vec{\beta} = (\beta_0,\beta_1,\beta_2,\beta_0^*,\beta_1^*,\beta_2^*)` and we are given the index vector :math:`\mathbf{u} = (1,0,3)`. Then we can calculate the following

.. math::
	\Sigma_{(\mathbf{u})} &= \left(
	\begin{array}{cccc|cccc}
	 A_{0,0} & A_{0,2} & A_{0,2} & A_{0,2} & B_{0,0} & B_{0,2} & B_{0,2} & B_{0,2} \\
	 A_{2,0} & A_{2,2} & A_{2,2} & A_{2,2} & B_{2,0} & B_{2,2} & B_{2,2} & B_{2,2} \\
	 A_{2,0} & A_{2,2} & A_{2,2} & A_{2,2} & B_{2,0} & B_{2,2} & B_{2,2} & B_{2,2} \\
	 A_{2,0} & A_{2,2} & A_{2,2} & A_{2,2} & B_{2,0} & B_{2,2} & B_{2,2} & B_{2,2} \\
	 \hline
	 C_{0,0} & C_{0,2} & C_{0,2} & C_{0,2} & D_{0,0} & D_{0,2} & D_{0,2} & D_{0,2} \\
	 C_{2,0} & C_{2,2} & C_{2,2} & C_{2,2} & D_{2,0} & D_{2,2} & D_{2,2} & D_{2,2} \\
	 C_{2,0} & C_{2,2} & C_{2,2} & C_{2,2} & D_{2,0} & D_{2,2} & D_{2,2} & D_{2,2} \\
	 C_{2,0} & C_{2,2} & C_{2,2} & C_{2,2} & D_{2,0} & D_{2,2} & D_{2,2} & D_{2,2} \\
	\end{array}
	\right),\\
	\vec \beta_{(\mathbf{u})} &= (\beta_0,\beta_2,\beta_2,\beta_2,\beta_0^*,\beta_2^*,\beta_2^*,\beta_2^*),

and finally write

.. math::
	\text{vid}(\Sigma_{(\mathbf{u})},\vec \beta_{(\mathbf{u})})=  \left(
	\begin{array}{cccc|cccc}
	 \beta_{0} & A_{0,2} & A_{0,2} & A_{0,2} & B_{0,0} & B_{0,2} & B_{0,2} & B_{0,2} \\
	 A_{2,0} & \beta_{2} & A_{2,2} & A_{2,2} & B_{2,0} & B_{2,2} & B_{2,2} & B_{2,2} \\
	 A_{2,0} & A_{2,2} & \beta_{2} & A_{2,2} & B_{2,0} & B_{2,2} & B_{2,2} & B_{2,2} \\
	 A_{2,0} & A_{2,2} & A_{2,2} & \beta_{2} & B_{2,0} & B_{2,2} & B_{2,2} & B_{2,2} \\
	 \hline
	 C_{0,0} & C_{0,2} & C_{0,2} & C_{0,2} & \beta_{0}^* & D_{0,2} & D_{0,2} & D_{0,2} \\
	 C_{2,0} & C_{2,2} & C_{2,2} & C_{2,2} & D_{2,0} & \beta_{2}^* & D_{2,2} & D_{2,2} \\
	 C_{2,0} & C_{2,2} & C_{2,2} & C_{2,2} & D_{2,0} & D_{2,2} & \beta_{2}^* & D_{2,2} \\
	 C_{2,0} & C_{2,2} & C_{2,2} & C_{2,2} & D_{2,0} & D_{2,2} & D_{2,2} & \beta_{2}^* \\
	\end{array}
	\right).

Note that because there are repetitions, the diagonal elements of the matrix :math:`\mathbf{A}` appear off diagonal in :math:`\mathbf{A}_{(\mathbf{n})}` and also in :math:`\text{vid}(\mathbf{A}_{(\mathbf{n})},\vec{\beta}_{\mathbf{n}})`.

One can ignore the block structure of the matrix :math:`A` and bivector :math:`\vec{\beta}`, and treat them as 6 dimensional objects and use an index vector of the same length. If we now define :math:`\mathbf{p} = (1,0,3,0,2,2)` one finds

.. math::
	\Sigma_{\mathbf{p}} &= \left(
	\begin{array}{cccccccc}
	 A_{0,0} & A_{0,2} & A_{0,2} & A_{0,2} & B_{0,1} & B_{0,1} & B_{0,2} & B_{0,2} \\
	 A_{2,0} & A_{2,2} & A_{2,2} & A_{2,2} & B_{2,1} & B_{2,1} & B_{2,2} & B_{2,2} \\
	 A_{2,0} & A_{2,2} & A_{2,2} & A_{2,2} & B_{2,1} & B_{2,1} & B_{2,2} & B_{2,2} \\
	 A_{2,0} & A_{2,2} & A_{2,2} & A_{2,2} & B_{2,1} & B_{2,1} & B_{2,2} & B_{2,2} \\
	 C_{1,0} & C_{1,2} & C_{1,2} & C_{1,2} & D_{1,1} & D_{1,1} & D_{1,2} & D_{1,2} \\
	 C_{1,0} & C_{1,2} & C_{1,2} & C_{1,2} & D_{1,1} & D_{1,1} & D_{1,2} & D_{1,2} \\
	 C_{2,0} & C_{2,2} & C_{2,2} & C_{2,2} & D_{2,1} & D_{2,1} & D_{2,2} & D_{2,2} \\
	 C_{2,0} & C_{2,2} & C_{2,2} & C_{2,2} & D_{2,1} & D_{2,1} & D_{2,2} & D_{2,2} \\
	\end{array}
	\right),\\
	\vec{\beta}_{\mathbf{p}}&=(\beta_0,\beta_2,\beta_2,\beta_2,\beta_1^*,\beta_1^*,\beta_2^*,\beta_2^*).

Note that we wrote :math:`\Sigma_{\mathbf{p}}` and **not** :math:`\Sigma_{(\mathbf{p})}` to indicate that we ignore the block structure of the matrix :math:`\Sigma`.
