#include <stdlib.h>
#include <stdio.h>
#include <mpi.h>
#include <time.h>
#include <unistd.h>

int main(int argc, char* argv[]){
    int task=0;
    MPI_Initialized(&task);
    if(task==0)
        if(MPI_Init(&argc,&argv)!=MPI_SUCCESS){
            printf("Wrong initialisation\n");
            return 1;
        }

    int rank;
    if(MPI_Comm_rank(MPI_COMM_WORLD,&rank)!=MPI_SUCCESS){
        printf("Error in obtaining rank\n");
        return 1;
    }

    int size;
    if(MPI_Comm_size(MPI_COMM_WORLD,&size)!=MPI_SUCCESS){
        printf("Error on obtaining size\n");
        return 1;
    }

    srand(rank+1+time(NULL));
    int flag=0,lider_rank=0,m=0;
    MPI_Status status;

    const int any_msg = 1,
              voting = 2,
              ok = 3,
              lider = 4;

    usleep(rand()%5+1);
    if(rank!=0){
        usleep(rand()%10+1);
        MPI_Send(&m,1,MPI_INT,lider_rank,any_msg,MPI_COMM_WORLD);
        usleep(100);

        MPI_Iprobe(lider_rank,any_msg,MPI_COMM_WORLD,&flag,&status);
        if(flag!=0){
            MPI_Recv(&m,1,MPI_INT,lider_rank,any_msg,MPI_COMM_WORLD,&status);
            return 0;
        }
        printf("%d: Viva Revolution!\n", rank);

        int counter = 0,
            key = 0,
            old_lider = lider_rank;

        for(;lider_rank==old_lider;){
            printf("%d iteration #\n", rank);
            MPI_Iprobe(MPI_ANY_SOURCE,MPI_ANY_TAG,MPI_COMM_WORLD,&flag,&status);
            if ((flag==0)&&(key==0)){
                for(int i=rank;i<size;i++){
                    MPI_Send(&m,1,MPI_INT,i,voting,MPI_COMM_WORLD);
                    printf("%d asked to %d\n", rank, i);
                }
                counter++;
                if (counter>size/3){
                    lider_rank=rank;
                    m=rank;
                    for(int i=0;i<size;i++)
                        MPI_Send(&m,1,MPI_INT,i,lider,MPI_COMM_WORLD);
                    printf("%d: LIDER\n", rank);
                    key++;
                }
            }

            MPI_Iprobe(MPI_ANY_SOURCE,voting,MPI_COMM_WORLD,&flag,&status);
            if ((flag!=0)&&(key==0)){
                MPI_Recv(&m,1,MPI_INT,status.MPI_SOURCE,voting,MPI_COMM_WORLD,&status);
                if (status.MPI_SOURCE!=rank)
                    MPI_Send(&m,1,MPI_INT,status.MPI_SOURCE,ok,MPI_COMM_WORLD);
                printf("%d agree with voting\n", rank);
            }

            MPI_Iprobe(MPI_ANY_SOURCE,ok,MPI_COMM_WORLD,&flag,&status);
            if ((flag!=0)&&(key==0)){
                MPI_Recv(&m,1,MPI_INT,status.MPI_SOURCE,ok,MPI_COMM_WORLD,&status);
                printf("%d recieved \"ok\" from %d\n", rank, status.MPI_SOURCE);
            }

            MPI_Iprobe(MPI_ANY_SOURCE,lider,MPI_COMM_WORLD,&flag,&status);
            if ((flag!=0)&&(key==0)){
                MPI_Recv(&m,1,MPI_INT,status.MPI_SOURCE,lider,MPI_COMM_WORLD,&status);
                lider_rank=m;
                printf("%d: new lider is %d\n", rank, lider_rank);
                key++;
            }

        }

    }



    MPI_Barrier(MPI_COMM_WORLD);
    printf("%d: new_lider is %d\n", rank, lider_rank);
    MPI_Finalize();
    return 0;
}
