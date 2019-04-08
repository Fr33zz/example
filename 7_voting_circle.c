#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <unistd.h>
#include <time.h>

int main(int argc,char *argv[]){

    int task;
    MPI_Initialized(&task);
    if (task==0)
        if(MPI_Init(&argc,&argv)!=MPI_SUCCESS){
            printf("wrong initialization\n");
            return -1;
        }

    int rank;
    if (MPI_Comm_rank(MPI_COMM_WORLD,&rank)!=MPI_SUCCESS) {
        printf("error in getting rank\n");
        return -1;
    }

    int size;
    if (MPI_Comm_size(MPI_COMM_WORLD,&size)!=MPI_SUCCESS) {
        printf("error in getting siez\n");
        return -1;
    }

    srand(rank+1+time(NULL));

    MPI_Status status;
    int flag=0;

    int msg[size],muu=0;
    for(int i=0;i<size;i++) msg[i]=0;

    int next_r,prev_r;
    next_r = (rank+1)%size;
    prev_r = (rank-1)%size;
    if (rank==0) prev_r=size-1;

    const int tag_any_msg = 1,
              tag_voting = 2,
              tag_ok = 3,
              tag_lider = 4,
              some_dreams = 5;

    int old_lider = rand()%size;
    MPI_Barrier;
    MPI_Bcast(&old_lider,1,MPI_INT,0,MPI_COMM_WORLD);
    int new_lider=old_lider;

    if(rank==(old_lider+1)%size){
            msg[rank]=1;
            MPI_Send(&msg,size,MPI_INT,next_r,tag_voting,MPI_COMM_WORLD);
            printf("%d: lider(%d) doesn\'t answer, I start voting\n \n", rank, old_lider);
    }
    MPI_Barrier(MPI_COMM_WORLD);
//------------------------------------------------------------------------------------------
    if(rank!=old_lider){
        int key=0; // флаг завершения
        for(;key==0;){
        // принимаем "голосование"
            MPI_Iprobe(MPI_ANY_SOURCE,tag_voting,MPI_COMM_WORLD,&flag,&status);
            if (flag!=0){
                MPI_Recv(&msg,size,MPI_INT,status.MPI_SOURCE,tag_voting,MPI_COMM_WORLD,&status);
                printf("%d: recieved \"voting\" from %d\n", rank, status.MPI_SOURCE);
                MPI_Send(&muu,1,MPI_INT,status.MPI_SOURCE,tag_ok,MPI_COMM_WORLD);
                printf("%d: sended \"ok\" to %d\n", rank, status.MPI_SOURCE);
            }
        // передаем "голосование"
            if((flag!=0)&&(msg[rank]==0)){
                msg[rank]++;
                if (next_r==old_lider) next_r=(next_r+1)%size;
                if (msg[next_r]==0){
                    MPI_Send(&msg,size,MPI_INT,next_r,tag_voting,MPI_COMM_WORLD);
                    printf("%d: sended \"voting\" to %d\n", rank,next_r);
                } else printf("%d: no send to %d \n", rank, next_r);

                usleep(some_dreams);
                MPI_Iprobe(MPI_ANY_SOURCE,tag_ok,MPI_COMM_WORLD,&flag,&status);
                if (flag!=0)
                    MPI_Recv(&muu,1,MPI_INT,status.MPI_SOURCE,tag_ok,MPI_COMM_WORLD,&status);
                else printf("%d: didn't recieve \"ok\" \n", rank);
                flag=0;
            }
        // передаем "я - лидер"
            if ((flag!=0)&&(msg[rank]!=0)){
                key++;
                new_lider=rank;
                MPI_Send(&new_lider,1,MPI_INT,next_r,tag_lider,MPI_COMM_WORLD);
                printf("%d: I'm new_lider\n", rank);
            }

        // передаем "он лидер"
            MPI_Iprobe(MPI_ANY_SOURCE,tag_lider,MPI_COMM_WORLD,&flag,&status);
            if(flag!=0){
                MPI_Recv(&new_lider,1,MPI_INT,status.MPI_SOURCE,tag_lider,MPI_COMM_WORLD,&status);
                printf("%d: let %d be the new_lider\n", rank, new_lider);
                key++;
                MPI_Send(&new_lider,1,MPI_INT,next_r,tag_lider,MPI_COMM_WORLD);
            }
        }
    }
//------------------------------------------------------------------------------------------
    // MPI_Barrier(MPI_COMM_WORLD);
    // printf("\n");
    MPI_Barrier(MPI_COMM_WORLD);
    printf("%d: lider is %d \n", rank, new_lider);
    MPI_Finalize();
    return 0;
}


// for(;old_lider==new_lider;){
//
//     //tag_ok
//     flag=0;
//     MPI_Iprobe(MPI_ANY_SOURCE,tag_ok,MPI_COMM_WORLD,&flag,&status);
//     if(flag!=0){
//         MPI_Recv(&muu,1,MPI_INT,status.MPI_SOURCE,tag_ok,MPI_COMM_WORLD,&status);
//         printf("%d recieved ok from %d\n", rank,status.MPI_SOURCE);
//     }
//
//     //tag_lider
//     flag=0;
//     MPI_Iprobe(MPI_ANY_SOURCE,tag_lider,MPI_COMM_WORLD,&flag,&status);
//     if (flag!=0){
//         MPI_Recv(&new_lider,1,MPI_INT,status.MPI_SOURCE,tag_lider,MPI_COMM_WORLD,&status);
//         MPI_Send(&muu,1,MPI_INT,status.MPI_SOURCE,tag_ok,MPI_COMM_WORLD);
//         printf("%d agree that lider is %d\n", rank, new_lider);
//         msg[size]=1;
//     }
//
//     //tag_voting
//     flag=0;
//     MPI_Iprobe(MPI_ANY_SOURCE,tag_voting,MPI_COMM_WORLD,&flag,&status);
//     if((flag!=0)&&(msg[size]==0)){
//         MPI_Recv(&msg,size+1,MPI_INT,status.MPI_SOURCE,tag_voting,MPI_COMM_WORLD,&status);
//         MPI_Send(&muu,1,MPI_INT,status.MPI_SOURCE,tag_ok,MPI_COMM_WORLD);
//         printf("%d: recieved voting from %d and sended ok\n", rank,status.MPI_SOURCE);
//     }
//
//
// }
