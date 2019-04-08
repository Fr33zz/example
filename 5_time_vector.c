#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <unistd.h>
#include <time.h>


int main(int argc, char* argv[])
{
	int task;
	MPI_Initialized(&task);
	if (task == 0)
		if (MPI_Init(&argc,&argv)!=MPI_SUCCESS){
				printf("Wrong initialization");
				return 1;
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

	int mytime[size],msg[size];
	MPI_Status status;
	for(int i=0;i<size;i++){
		mytime[i]=0;
		msg[i]=0;
	}

	if(rank==0){
		mytime[rank]++;

		mytime[rank]++;
		MPI_Recv(&msg,3,MPI_INT,1,1,MPI_COMM_WORLD,&status);
		for(int i=0;i<size;i++) if((msg[i]>mytime[i])) mytime[i]=msg[i];

		mytime[rank]++;
		MPI_Recv(&msg,3,MPI_INT,1,1,MPI_COMM_WORLD,&status);
		for(int i=0;i<size;i++) if((msg[i]>mytime[i])) mytime[i]=msg[i];

		mytime[rank]++;
		MPI_Send(&mytime,3,MPI_INT,2,1,MPI_COMM_WORLD);
	}
	if(rank==1){
		mytime[rank]++;
		MPI_Send(&mytime,3,MPI_INT,0,1,MPI_COMM_WORLD);

		mytime[rank]++;

		mytime[rank]++;
		MPI_Send(&mytime,3,MPI_INT,0,1,MPI_COMM_WORLD);

		mytime[rank]++;
		MPI_Recv(&msg,3,MPI_INT,2,1,MPI_COMM_WORLD,&status);
		for(int i=0;i<size;i++) if((msg[i]>mytime[i])) mytime[i]=msg[i];

		mytime[rank]++;
		MPI_Recv(&msg,3,MPI_INT,2,1,MPI_COMM_WORLD,&status);
		for(int i=0;i<size;i++) if((msg[i]>mytime[i])) mytime[i]=msg[i];

		mytime[rank]++;
	}
	if(rank==2){
		mytime[rank]++;

		mytime[rank]++;
		MPI_Send(&mytime,3,MPI_INT,1,1,MPI_COMM_WORLD);

		mytime[rank]++;

		mytime[rank]++;
		MPI_Recv(&msg,3,MPI_INT,0,1,MPI_COMM_WORLD,&status);
		for(int i=0;i<size;i++) if((msg[i]>mytime[i])) mytime[i]=msg[i];

		mytime[rank]++;
		MPI_Send(&mytime,3,MPI_INT,1,1,MPI_COMM_WORLD);
	}

	MPI_Barrier(MPI_COMM_WORLD);
	printf("%d: %d %d %d\n", rank, mytime[0], mytime[1], mytime[2]);
	MPI_Finalize();
	return 0;
}
