# Copyright 2020 Jean-Marie Mirebeau, University Paris-Sud, CNRS, University Paris-Saclay
# Distributed WITHOUT ANY WARRANTY. Licensed under the Apache License, Version 2.0, see http://www.apache.org/licenses/LICENSE-2.0

import numpy as np
import copy

from ... import LinearParallel as lp
from ... import AutomaticDifferentiation as ad
from ... import FiniteDifferences as fd
from .. import misc
from ..riemann import Riemann
from .implicit_base import ImplicitBase
from .thomsen_data import ThomsenElasticMaterial, ThomsenGeometricMaterial


class TTI(ImplicitBase):
	"""
	A family of reduced models, known as Tilted Transversally Anisotropic,
	and arising in seismic tomography.

	The *dual* unit ball is defined by an equation of the form
	$$
	l(X^2+Y^2,Z^2) + (1/2)*q(X^2+Y^2,Z^2) = 1,
	$$
	where $l$ is linear and $q$ is quadratic, where $X,Y,Z$ are the coefficients 
	of the input vector, usually altered by a linear transformation.
	In two dimensions, ignore the $Y^2$ term.

	The primal norm is obtained implicitly, by solving an optimization problem.

	Member fields and __init__ arguments : 
	- linear : an array of shape (2,n1,...,nk) encoding the linear part l
	- quadratic : an array of shape (2,2,n1,...,nk) encoding the quadratic part q
	- vdim (optional) : the ambient space dimension
	- *args,**kwargs (optional) : passed to implicit_base
	"""

	def __init__(self,linear,quadratic,vdim=None,*args,**kwargs):
		super(TTI,self).__init__(*args,**kwargs)
		self.linear = ad.asarray(linear)
		self.quadratic = ad.asarray(quadratic)
		assert len(self.linear) == 2
		assert self.quadratic.shape[:2] == (2,2)
		self._to_common_field()
		
		if vdim is None:
			if self.inverse_transformation is not None: vdim=len(self.inverse_transformation)
			elif self.linear.ndim>1: vdim = self.linear.ndim-1
			else: raise ValueError("Unspecified dimension")
		self._vdim=vdim

	@property
	def vdim(self): return self._vdim
	
	@property
	def shape(self): return self.linear.shape[1:]

	def _dual_level(self,v,params=None,relax=0.):
		l,q = self._dual_params(v.shape[1:]) if params is None else params
		v2 = v**2
		if self.vdim==3: v2 = ad.array([v2[:2].sum(axis=0),v2[2]])
		return lp.dot_VV(l,v2) + 0.5*np.exp(-relax)*lp.dot_VAV(v2,q,v2) - 1.
	
	def cost_bound(self):
		# Ignoring the quadratic term for now.
		return self.Riemann_approx().cost_bound()

	def _dual_params(self,shape=None):
		return fd.common_field((self.linear,self.quadratic),depths=(1,2),shape=shape)

	def __iter__(self):
		yield self.linear
		yield self.quadratic
		yield self._vdim
		for x in super(TTI,self).__iter__(): yield x

	def _to_common_field(self,shape=None):
		self.linear,self.quadratic,self.inverse_transformation = fd.common_field(
			(self.linear,self.quadratic,self.inverse_transformation),
			depths=(1,2,2),shape=shape)

	@classmethod
	def from_cast(cls,metric):
		if isinstance(metric,cls): return metric
		else: raise ValueError("No casting operations supported towards the TTI model")
		# Even cast from Riemann is non-canonical

	def model_HFM(self):
		return f"TTI{self.vdim}"

	def extract_xz(self):
		"""
		Extract a two dimensional Hooke tensor from a three dimensional one, 
		corresponding to a slice through the X and Z axes.
		Axes transformation information (rotation) is discarded.
 		"""
		if len(self.shape)==3: raise ValueError("Three dimensional field")
		if self.inverse_transformation is not None:
			raise ValueError("Cannot extract XZ slice from tilted norms")
		other = copy.copy(self)
		other._vdim = 2
		return other

	def flatten(self,transposed_transformation=False):
		linear = self.linear
		quad = self.quadratic 

		if self.inverse_transformation is None: 
			xp = ad.cupy_generic.get_array_module(linear)
			trans = fd.as_field(xp.eye(self.vdim,dtype=linear.dtype),self.shape,depth=2) 
		else: trans = self.inverse_transformation
		if transposed_transformation: trans = lp.transpose(lp.inverse(trans))

		return np.concatenate(
			(self.linear,misc.flatten_symmetric_matrix(quad),
				trans.reshape((self.vdim**2,)+self.shape)),
			axis=0)

	@classmethod
	def expand(cls,arr):
		vdim = np.sqrt(len(arr)-(2+3))
		assert(vdim==int(vdim))
		vdim = int(vdim)
		shape = arr.shape[1:]

		linear = arr[0:2]
		quadratic = misc.expand_symmetric_matrix(arr[2:5])
		inv_trans = arr[5:].reshape((vdim,vdim)+shape)
		return cls(linear,quadratic,vdim=vdim,inverse_transformation=inv_trans)

	@classmethod
	def from_hexagonal(cls,c11,_,c13,c33,c44,vdim=3):
		linear = [c11+c44,c33+c44]
		mixed = c13**2-c11*c33+2.*c13*c44
		quadratic = [[-2.*c11*c44,mixed],[mixed,-2.*c33*c44]]
		return cls(linear,quadratic,vdim=vdim)

	@classmethod
	def from_ThomsenElastic(cls,tem,vdim=3):
		"""Produces a norm from the given Thomsem elasticity parameters."""
		if not isinstance(tem,ThomsenElasticMaterial): tem = ThomsenElasticMaterial(*tem)
		hex,ρ = tem.to_hexagonal()
		return cls.from_hexagonal(*hex,vdim),ρ

	@classmethod
	def from_ThomsenGeometric(cls,tgm,vdim=3):
		"""Produces a norm from the given Thomsen geometric paramters."""
		if not isinstance(tgm,ThomsenGeometricMaterial): tgm = ThomsenGeometricMaterial(*tgm)
		c11,c13,c33,c44 = tgm.to_c()
		return cls.from_hexagonal(c11,None,c13,c33,c44,vdim=vdim)

	def α_bounds():
		assert False 		
#		l,q = self.linear,self.Q
#		a,b = _axes_intersections()
#		ga,gb = _grad_ratio(


	def μ(α):
		a = (1-α,α)
		l,q = self.linear,self.Q
		l = self.linear
		Q = self.Q
		δ = lp.det(Q)
		R = [[Q[1,1],-Q[0,1]],[-Q[1,0],Q[0,0]]]
		Rl = lp.dot_AV(R,l)
		s = 2*δ+lp.dot_VV(l,Rl)
		ε = np.sign(s)
		aRa = lp.dot_VAV(a,R,a)
		return (lp.det([a,l])**2+2*aRa)/(ε*np.sqrt(aRa*s)+lp.dot_VV(a,Rl))

	def Riemann_approx(self,compare=None):
		"""
		Riemannian approximation of the TTI norm.
		Input : 
		  - compare 
		    * None (default) : neglect the quadratic term in the TTI equation
		    * 1 : Riemannian approximation is larger than the TTI norm
		    * 0 : Riemannian approximation is closest, neither larger or smaller
		    *-1 : Riemannian approximation is smaller than the TTI norm
		"""
		if compare is None:
			diag = 1/self.linear
		else:
			l,q = self.linear,self._q()
			a,b = _axes_intersections(l,q)
			diag_ab = (1./a,1./b)
			diag_a,diag_b = _diags(l,q,(0,1),(a,b))
			mix_is_min = lp.det((diag_a,diag_b))>0
			assert False
#			t = 

		if self.vdim==3: diag = diag[0],diag[0],diag[1] 
		riem = Riemann.from_diagonal(diag)
		if self.inverse_transformation is not None : riem = riem.inv_transform(self.inverse_transformation)
		return riem

#	def Riemann_approx(self):
#		"""A tangent Riemannian approximation"""
#		_,(riem,) = self.Riemann_envelope(1)
#		return riem

	def Riemann_envelope(self,nmix):
		"""
		Approximation of a TTI norm using an envelope of Riemannian norms.
		- nmix : number of ellipses used for the approximation.

		returns
		- riems : a list of nmix Riemannian norms.
		- mix_is_min : wether to take the minimum or the maximum of the Riemannian norms.
		"""
		# Set the interpolation times 
		if isinstance(nmix,int):
			if nmix==1: ts=[0.5]
			else: ts = np.linspace(0,1,nmix)
		else: ts = nmix # Hack to get specific interpolation times, must be sorted

		l,q = self.linear,self._q()
		ab = _axes_intersections(l,q)
		diags = _diags(l,q,ts,ab)
		mix_is_min = lp.det([diags[0],diags[-1]])>0 if len(diags) else None
		if self.vdim==3: diags = [(a,a,b) for a,b in diags]

		riems = [Riemann.from_diagonal(1./ad.array(diag)) for diag in diags]
		if self.inverse_transformation is not None:
			riems = [riem.inv_transform(self.inverse_transformation) for riem in riems]
		
		return mix_is_min, riems

	def _q():
		"""
		Quadratic part, in format compatible with the C routines adapted below
		"""
		return self.quadratic[((0,0,1),(0,1,1))]

# ----- The following code is adapted from agd/Eikonal/HFM_CUDA/cuda/TTI_.h -----
# It computes the approximation of the TTI norm with an envelope of riemannian norms

def _solve2(a,b,c):
	#Returns the two roots of a quadratic equation, a + 2 b t + c t^2.
	#The discriminant must be non-negative, but aside from that the equation may be degenerate.
	sdelta = np.sqrt(b*b-a*c);
	u = -b + sdelta 
	v = -b - sdelta
	b0 = np.abs(c)>np.abs(a)
	b1 = a!=0
	return (np.where(b0,u/c,np.where(b1,a/u,0.)), np.where(b0,v/c,np.where(b1,a/v,np.inf))) 

def _solve2_above(a, b, c, above):
	#Returns the smallest root of the considered quadratic equation above the given threshold.
	#Such a root is assumed to exist.
	r = np.sort(_solve2(a,b,c),axis=0)
	return np.where(r[0]>=above, r[0], r[1])

def _axes_intersections(l,q):
	"""
	Finds the intersections (a,0) and (0,b) of the curve f(x)=0
	with the axes (the closest intersections to the origin).
	"""
	return _solve2_above(-2,l[0],q[0],0.), _solve2_above(-2,l[1],q[2],0.)

def _grad_ratio(l,q,x):
	"""
	Returns g(x) := df(x)/<x,df(x)> where f(x):= C + 2 <l,x> + <qx,x> 
	Note that the curve tangent to the level line of f at x is 
	<y-x,df(x)> ≥ 0, equivalently <y,g(x)> ≥ 1
	"""
	hgrad = ad.array([q[0]*x[0]+q[1]*x[1]+l[0], q[1]*x[0]+q[2]*x[1]+l[1]]) #lp.dot_AV(q,x)+l # df(x)/2
	return hgrad/lp.dot_VV(x,hgrad)

def _diags(l, q, ts, axes_intersections):
	"""
	Samples the curve defined by {x≥0|f(x)=0}, 
	(the connected component closest to the origin)
	where f(x):= -2 + 2 <l,x> + <qx,x>,
	and returns diag(i) := grad f(x)/<x,grad f(x)>.
	"""
	a,b=axes_intersections
	zero = np.zeros_like(a)

	# Change of basis in f, with e0 = {1/2.,1/2.}, e1 = {1/2.,-1/2.}
	L = ad.array([l[0]+l[1], l[0]-l[1]])/2.
	Q = ad.array([q[0]+2*q[1]+q[2], q[0]-q[2], q[0]-2*q[1]+q[2]])/4.

	diags=[]
	for t in ts:
		if   t==0.: x=(a,zero)
		elif t==1.: x=(zero,b)
		else :
			v = (1.-t)*a - t*b
			# Solving f(u e0+ v e_1) = 0 w.r.t u
			u = _solve2_above(-2.+2.*L[1]*v+Q[2]*v*v, L[0]+Q[1]*v, Q[0], np.abs(v))
			# Inverse change of basis
			x = ad.array([u+v, u-v])/2.
		diags.append(_grad_ratio(l,q,x))

	return diags


# ---- Some instances of TTI metrics ----

# See Hooke.py file for reference
TTI.mica = TTI.from_hexagonal(178.,42.4,14.5,54.9,12.2), 2.79
# Stishovite is tetragonal, but the P-Wave velocity in the XZ plane 
# is equivalent to an hexagonal model.
TTI.stishovite2 = TTI.from_hexagonal(453,np.nan,203,776,252).extract_xz(), 4.29 



