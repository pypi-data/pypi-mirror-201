/*
 * Copyright (c) 2021-2023, NVIDIA CORPORATION & AFFILIATES
 * SPDX-License-Identifier: BSD-3-Clause
*/

#include <cutensornet.h> // cutensornet public header

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#define ENABLE_MPI

#ifdef ENABLE_MPI
#include <mpi.h> // MPI library header
#endif

#ifdef ENABLE_MPI
/** Converts CUDA data type to the corresponding MPI data type */
static MPI_Datatype convertCudaToMpiDataType(const cudaDataType_t cudaDataType)
{
    MPI_Datatype mpiDataType;
    switch (cudaDataType)
    {
        case CUDA_R_8I: mpiDataType = MPI_INT8_T; break;
        case CUDA_R_16I: mpiDataType = MPI_INT16_T; break;
        case CUDA_R_32I: mpiDataType = MPI_INT32_T; break;
        case CUDA_R_64I: mpiDataType = MPI_INT64_T; break;
        case CUDA_R_32F: mpiDataType = MPI_FLOAT; break;
        case CUDA_R_64F: mpiDataType = MPI_DOUBLE; break;
        case CUDA_C_32F: mpiDataType = MPI_C_FLOAT_COMPLEX; break;
        case CUDA_C_64F: mpiDataType = MPI_C_DOUBLE_COMPLEX; break;
        default:
            printf("#ERROR(cutensornet::mpi): Unknown CUDA data type: %d\n",(int)(cudaDataType));
            exit(EXIT_FAILURE);
    }
    return mpiDataType;
}

/** Unpacks the MPI_Comm object */
static MPI_Comm unpackMpiCommunicator(const cutensornetDistributedCommunicator_t* comm)
{
    if(comm->commPtr == NULL) return MPI_COMM_NULL;
    assert(sizeof(MPI_Comm) == comm->commSize);
    return *((MPI_Comm*)(comm->commPtr));
}
#endif // ENABLE_MPI

#ifdef __cplusplus
extern "C" {
#endif

/** MPI_Comm_size wrapper */
int cutensornetMpiCommSize(const cutensornetDistributedCommunicator_t* comm,
                           int32_t* numRanks)
{
#ifdef ENABLE_MPI
    int nranks = 0;
    int mpiErr = MPI_Comm_size(unpackMpiCommunicator(comm), &nranks);
    *numRanks = nranks;
    return mpiErr;
#else
    *numRanks = 1;
    return 0;
#endif
}

/** MPI_Comm_size wrapper */
int cutensornetMpiCommRank(const cutensornetDistributedCommunicator_t* comm,
                           int32_t* procRank)
{
#ifdef ENABLE_MPI
    int prank = -1;
    int mpiErr = MPI_Comm_rank(unpackMpiCommunicator(comm), &prank);
    *procRank = prank;
    return mpiErr;
#else
    *procRank = 0;
    return 0;
#endif
}

/** MPI_Barrier wrapper */
int cutensornetMpiBarrier(const cutensornetDistributedCommunicator_t* comm)
{
#ifdef ENABLE_MPI
    return MPI_Barrier(unpackMpiCommunicator(comm));
#else
    return 0;
#endif
}

/** MPI_Bcast wrapper */
int cutensornetMpiBcast(
    const cutensornetDistributedCommunicator_t* comm,
    void* buffer,
    int32_t count,
    cudaDataType_t datatype,
    int32_t root)
{
#ifdef ENABLE_MPI
    return MPI_Bcast(buffer, (int)count,
        convertCudaToMpiDataType(datatype),
        (int)root, unpackMpiCommunicator(comm));
#else
    return 0;
#endif
}

/** MPI_Allreduce wrapper */
int cutensornetMpiAllreduce(
    const cutensornetDistributedCommunicator_t* comm,
    const void* bufferIn,
    void* bufferOut,
    int32_t count,
    cudaDataType_t datatype)
{
#ifdef ENABLE_MPI
    return MPI_Allreduce(bufferIn, bufferOut, (int)count,
        convertCudaToMpiDataType(datatype),
        MPI_SUM, unpackMpiCommunicator(comm));
#else
    return 0;
#endif
}

/** MPI_Allreduce IN_PLACE wrapper */
int cutensornetMpiAllreduceInPlace(
    const cutensornetDistributedCommunicator_t* comm,
    void* buffer,
    int32_t count,
    cudaDataType_t datatype)
{
#ifdef ENABLE_MPI
    return MPI_Allreduce(MPI_IN_PLACE, buffer, (int)count,
        convertCudaToMpiDataType(datatype),
        MPI_SUM, unpackMpiCommunicator(comm));
#else
    return 0;
#endif
}

/** MPI_Allreduce IN_PLACE MIN wrapper */
int cutensornetMpiAllreduceInPlaceMin(
    const cutensornetDistributedCommunicator_t* comm,
    void* buffer,
    int32_t count,
    cudaDataType_t datatype)
{
#ifdef ENABLE_MPI
    return MPI_Allreduce(MPI_IN_PLACE, buffer, (int)count,
        convertCudaToMpiDataType(datatype),
        MPI_MIN, unpackMpiCommunicator(comm));
#else
    return 0;
#endif
}

/** MPI_Allreduce DOUBLE_INT MINLOC wrapper */
int cutensornetMpiAllreduceDoubleIntMinloc(
    const cutensornetDistributedCommunicator_t* comm,
    const void* bufferIn, // *struct {double; int;}
    void* bufferOut)      // *struct {double; int;}
{
#ifdef ENABLE_MPI
    return MPI_Allreduce(bufferIn, bufferOut, 1,
                         MPI_DOUBLE_INT,
                         MPI_MINLOC, unpackMpiCommunicator(comm));
#else
    typedef struct {
        double cost;
        int prank;
    } DoubleIntStruct_t;
    DoubleIntStruct_t* src = (DoubleIntStruct_t*)bufferIn;
    DoubleIntStruct_t* dst = (DoubleIntStruct_t*)bufferOut;
    *dst = *src;
    return 0;
#endif
}

/** 
 * Distributed communication service API wrapper binding table (imported by cuTensorNet).
 * The exposed C symbol must be named as "cutensornetCommInterface".
 */
cutensornetDistributedInterface_t cutensornetCommInterface = {
    CUTENSORNET_DISTRIBUTED_INTERFACE_VERSION,
    cutensornetMpiCommSize,
    cutensornetMpiCommRank,
    cutensornetMpiBarrier,
    cutensornetMpiBcast,
    cutensornetMpiAllreduce,
    cutensornetMpiAllreduceInPlace,
    cutensornetMpiAllreduceInPlaceMin,
    cutensornetMpiAllreduceDoubleIntMinloc
};

#ifdef __cplusplus
} // extern "C"
#endif
