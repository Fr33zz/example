#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<math.h>
#include<mpi.h>

float f_pi(int n, int size, int rank)
{
	double a = 1.0/size,
		   b = a*rank+a;
		   a *= rank;
	float sum=0,
		x=a,
		d=(b-a)/n;

	for(;x<b;x+=d)	sum+=sqrt(1-x*x)*d;
	return 4*sum;
}

int main(int argc, char* argv[])
{
	int task;
	MPI_Initialized(&task);
	if (task == 0){
		if (MPI_Init(&argc,&argv)!=MPI_SUCCESS){
			printf("Wrong initialization");
			return 1;
		}
	}

	int rank;
	if(MPI_Comm_rank(MPI_COMM_WORLD, &rank)!=MPI_SUCCESS){
		printf("Error in obtaining rank");
		return 1;
	}

	int size;
	if(MPI_Comm_size(MPI_COMM_WORLD, &size)!=MPI_SUCCESS){
		printf("Error in obtaining size");
		return 1;
	}

	int	n = 1e3;
	float a=1,
	      accuracy,
		  prev = 0,
		  sum = 0;

	if (rank == 0) {
		printf("accuracy: \n");
		scanf("%f",&accuracy);
		printf("%f\n\n", accuracy);
	}
	MPI_Bcast(&accuracy,1,MPI_FLOAT,0,MPI_COMM_WORLD);

	for(;a>accuracy;){
		prev = sum;
		sum = f_pi(n,size,rank);
		n*=2;
		a = 2*fabs(sum-prev)/(sum+prev);
	}

	printf("Hi! I'm the %d, my sum is %f\n", rank, sum);

	MPI_Barrier(MPI_COMM_WORLD);
	MPI_Reduce(&sum,&prev,1,MPI_FLOAT,MPI_SUM,0,MPI_COMM_WORLD);
	if (rank == 0)
		printf("\nHi! I'm the %d, pi is %f\n", rank, prev);

	MPI_Finalize();

	return 0;
}
