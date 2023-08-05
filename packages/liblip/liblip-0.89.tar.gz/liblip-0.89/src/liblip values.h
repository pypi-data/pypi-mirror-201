


LIBEXP double	LipIntValues( int id, int* Dim, int* Ndata, double* x, double* Xd,double* y,  double* Lipconst, int* Index, int num, double* results);
LIBEXP double	LipIntValue( int id, int* Dim, int* Ndata, double* x, double* Xd,double* y,  double* Lipconst, int* Index);

LIBEXP double	LipIntValuesAuto( int id, int* Dim, int* Ndata, double* x,double* Xd, double* y, int* Index, int num, double* results);
LIBEXP double	LipIntValuesCons( int id, int* Dim, int* Ndata, int* Cons, double* x, double* Xd,double* y,  double* Lipconst, int* Index, int num, double* results);
LIBEXP double	LipIntValuesConsLeftRegion( int id, int* Dim, int* Ndata, int* Cons, double* x, double* Xd,double* y,  double* Lipconst, double* Region, int* Index, int num, double* results);
LIBEXP double	LipIntValuesConsRightRegion( int id, int* Dim, int* Ndata, int* Cons, double* x, double* Xd,double* y,  double* Lipconst, double* Region, int* Index, int num, double* results);
LIBEXP double	LipIntValuesLocal( int id, int *Dim, int *Ndata, double* x, double* Xd,double* y, int num, double* results);
LIBEXP double	LipIntValuesLocalCons( int id, int *Dim, int *Ndata,int* Cons, double* x, double* Xd,double* y, int num, double* results);
LIBEXP double	LipIntValuesLocalConsLeftRegion( int id, int *Dim, int *Ndata,int* Cons, double* x, double* Xd,double* y, double* Region, int num, double* results);
LIBEXP double	LipIntValuesLocalConsRightRegion( int id, int *Dim, int *Ndata,int* Cons, double* x, double* Xd,double* y, double* Region, int num, double* results);
LIBEXP double	LipIntInfValues( int id, int *Dim, int *Ndata, double* x, double* Xd,double* y,  double* Lipconst, int* Index, int num, double* results);
LIBEXP double	LipIntInfValuesAuto( int id, int *Dim, int *Ndata, double* x,double* Xd, double* y, int* Index, int num, double* results);
LIBEXP double	LipIntInfValuesCons( int id, int *Dim, int *Ndata, int* Cons, double* x, double* Xd,double* y,  double *LipIntInfVerifyMonotonicityLeftRegionLipconst, int* Index, int num, double* results);
LIBEXP double	LipIntInfValuesConsLeftRegion( int id, int *Dim, int *Ndata, int* Cons, double* x, double* Xd,double* y,  double* Lipconst, double* Region, int* Index, int num, double* results);
LIBEXP double	LipIntInfValuesConsRightRegion( int id, int *Dim, int *Ndata, int* Cons, double* x, double* Xd,double* y,  double* Lipconst, double* Region, int* Index, int num, double* results);
LIBEXP double	LipIntInfValuesLocal( int id, int *Dim, int *Ndata, double* x, double* Xd,double* y, int num, double* results);
LIBEXP double	LipIntInfValuesLocalCons( int id, int *Dim, int *Ndata,int* Cons, double* x, double* Xd,double* y, int num, double* results);
LIBEXP double	LipIntInfValuesLocalConsLeftRegion( int id, int *Dim, int *Ndata,int* Cons, double* x, double* Xd,double* y, double* Region, int num, double* results);
LIBEXP double	LipIntInfValuesLocalConsRightRegion( int id, int *Dim, int *Ndata,int* Cons, double* x, double* Xd,double* y, double* Region, int num, double* results);
LIBEXP  double	STCValues( int id, double* x, int num, double* results );
LIBEXP  double	STCValuesExplicit( int id, double* x, int num, double* results );
LIBEXP double LipIntValuesExplicitDim( int id, int dim, double* x, int num, double* results);
LIBEXP double LipIntValuesDim( int id, int dim, double* x, int num, double* results);
