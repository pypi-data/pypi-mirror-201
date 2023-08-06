#pragma once

#include "GeometryT.h"
// Classes for first and second order dense automatic differentiation

// Until now I avoided C++ with cuda, but it seems to work after all.
// Pasted from HamiltonFastMarching/ LinearAlgebra/FriendOperators.h
// Overload operators
template<typename TDifferentiation, typename TScalar> struct DifferentiationTypeOperators {
	typedef TDifferentiation AD;
	typedef TScalar K;
	friend AD operator + (AD a, AD const & b) { a += b; return a; }
	friend AD operator + (AD a, K const & b)  { a += b; return a; }
	friend AD operator + (K const & a, AD b)  { b += a; return b; }

	friend AD operator - (AD a, AD const & b) { a -= b; return a; }
	friend AD operator - (AD a, K const & b)  { a -= b; return a; }
	friend AD operator - (K const & a, AD b)  { b -= a; return -b; }

	friend AD operator * (AD a, AD const & b) { a *= b; return a; }
	friend AD operator * (AD a, K const & b)  { a *= b; return a; }
	friend AD operator * (K const & a, AD b)  { b *= a; return b; }
	
	friend AD operator / (const AD & a, const AD & b){return a*b.Inverse();}
	friend AD operator / (const K & a,  const AD & b){return a*b.Inverse();}
	friend AD operator / (AD a, const K & b) {a/=b; return a;}
	friend void operator /= (AD & a, const AD & b){a*=b.Inverse();}

	// Totally ordered
	friend bool operator >  (AD const & a, AD const & b) { return b < a; }
	friend bool operator >= (AD const & a, AD const & b) { return !(a < b); }
	friend bool operator <= (AD const & a, AD const & b) { return !(a > b); }

	// Totally ordered 2
	friend bool operator <= (const AD & a, const K & b) { return !(a > b); }
	friend bool operator >= (const AD & a, const K & b) { return !(a < b); }

	friend bool operator <  (const K & b, const AD & a) { return a > b; }
	friend bool operator >  (const K & b, const AD & a) { return a < b; }
	friend bool operator <= (const K & b, const AD & a) { return a >= b; }
	friend bool operator >= (const K & b, const AD & a) { return a <= b; }

	friend bool operator != (const AD &a, const AD &b) { return !(a == b); }
};

/**
A class for second order dense automatic differentiation.

A element x = (a,v,m) of this class represents 
x = a + <v,h> + <h,m h>/2 + o(|h|^2), 
where h is an infinitesimal perturbation in dimension ndim. 

Note that a is a scalar, v is a vector of dimension ndim, and m is a symmetric matrix of shape 
(ndim,ndim) which is stored in compact format with ndim*(ndim+1)/2 entries.
*/
template<typename Scalar, int ndim>
struct Dense2 : DifferentiationTypeOperators<Dense2<Scalar,ndim>,Scalar> {
	typedef GeometryT<ndim> V;
	static const int symdim = V::symdim;
	typedef GeometryT<symdim> M;

	Scalar a;
	Scalar v[ndim];
	Scalar m[symdim];

	Dense2(){};
	Dense2(Scalar a_){a=a_;V::zero(v);M::zero(m);}

	void operator += (const Dense2 & y){a+=y.a; V::add(y.v,v); M::add(y.m,m);}
	void operator -= (const Dense2 & y){a-=y.a; V::sub(y.v,v); M::sub(y.m,m);}
	void operator *= (const Dense2 & y){
		for(int i=0,k=0; i<ndim; ++i){for(int j=0;j<=i; ++j,++k){
			m[k]=y.a*m[k]+a*y.m[k]+y.v[i]*v[j]+y.v[j]*v[i];}}
		for(int i=0; i<ndim;++i){v[i]=y.a*v[i]+a*y.v[i];}
		a = a*y.a;
	}
	void operator /= (const Dense2 & y){*this*=y.Inverse();}
	Dense2 Inverse() const {
		const Scalar ai = 1./a, ai2=ai*ai;
		Dense2 r;
		r.a = ai;
		V::mul(-ai2,v,r.v);
		V::self_outer(v,r.m);
		M::mul(2*ai,r.m);
		M::sub(m,r.m);
		M::mul(ai2,r.m);
		return r;
	}
	Dense2 operator - () const {Dense2 y; y.a=-a; V::neg(v,y.v); M::neg(m,y.m); return y; } 
	void operator += (const Scalar & y){a+=y;}
	void operator -= (const Scalar & y){a-=y;}
	void operator *= (const Scalar & y){a*=y; V::mul(y,v); M::mul(y,m);}
	void operator /= (const Scalar & y){*this*=(1/y);}

	static void Identity(Dense2 id[ndim]){
		for(int i=0; i<ndim; ++i){
			id[i].a=0;V::zero(id[i].v);M::zero(id[i].m);
			id[i].v[i]=1;
		}
	}

	void showself() const {
		printf("{"); 
		show(a);      printf(",");
		V::show_v(v); printf(","); 
		V::show_m(m); printf("}");
	}
};

template<typename Scalar,int ndim> void show(const Dense2<Scalar,ndim> & x){x.showself();}


/**
A class for second order dense automatic differentiation.

A element x = (a,v) of this class represents 
x = a + <v,h> + o(|h|), 
where h is an infinitesimal perturbation in dimension ndim. 

Note that a is a scalar, and v is a vector of dimension ndim.
*/
template<typename Scalar, int ndim>
struct Dense1 : DifferentiationTypeOperators<Dense1<Scalar,ndim>,Scalar> {
	typedef GeometryT<ndim> V;

	Scalar a;
	Scalar v[ndim];

	Dense1(){};
	Dense1(Scalar a_){a=a_;V::zero(v);}

	void operator += (const Dense1 & y){a+=y.a; V::add(y.v,v);}
	void operator -= (const Dense1 & y){a-=y.a; V::sub(y.v,v);}
	void operator *= (const Dense1 & y){
		for(int i=0; i<ndim;++i){v[i]=y.a*v[i]+a*y.v[i];}
		a = a*y.a;
	}
	void operator /= (const Dense1 & y){*this*=y.Inverse();}
	Dense1 Inverse() const {
		Dense1 r;
		r.a = Scalar(1)/a;
		V::mul(-r.a*r.a,v,r.v);
		return r;
	}
	Dense1 operator - () const {Dense1 y; y.a=-a; V::neg(v,y.v); return y; } 
	void operator += (const Scalar & y){a+=y;}
	void operator -= (const Scalar & y){a-=y;}
	void operator *= (const Scalar & y){a*=y; V::mul(y,v);}
	void operator /= (const Scalar & y){*this*=(1/y);}

	static void Identity(Dense1 id[ndim]){
		for(int i=0; i<ndim; ++i){id[i].a=0; V::zero(id[i].v); id[i].v[i]=1;}
	}
	
	// in : Ah+b, out = -A^{-1}b
	static void solve(Dense1 in[ndim], Scalar out[ndim]){ 
		Scalar A[ndim][ndim], b[ndim];
		for(int i=0; i<ndim; ++i){
			b[i] = in[i].a;
			for(int j=0; j<ndim; ++j){A[i][j]=in[i].v[j];}
		}
		V::solve_av(A,b,out);
		V::neg(out,out);
	}

	void showself() const {
		printf("{"); 
		show(a);      printf(",");
		V::show_v(v); printf("}");
	}
};

template<typename Scalar,int ndim> void show(const Dense1<Scalar,ndim> & x){x.showself();}
