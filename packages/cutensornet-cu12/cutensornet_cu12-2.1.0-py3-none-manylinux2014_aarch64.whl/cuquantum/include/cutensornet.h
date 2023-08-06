/*
 * Copyright 2021-2023 NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
 *
 * NOTICE TO LICENSEE:
 *
 * This source code and/or documentation ("Licensed Deliverables") are
 * subject to NVIDIA intellectual property rights under U.S. and
 * international Copyright laws.
 *
 * These Licensed Deliverables contained herein is PROPRIETARY and
 * CONFIDENTIAL to NVIDIA and is being provided under the terms and
 * conditions of a form of NVIDIA software license agreement by and
 * between NVIDIA and Licensee ("License Agreement") or electronically
 * accepted by Licensee.  Notwithstanding any terms or conditions to
 * the contrary in the License Agreement, reproduction or disclosure
 * of the Licensed Deliverables to any third party without the express
 * written consent of NVIDIA is prohibited.
 *
 * NOTWITHSTANDING ANY TERMS OR CONDITIONS TO THE CONTRARY IN THE
 * LICENSE AGREEMENT, NVIDIA MAKES NO REPRESENTATION ABOUT THE
 * SUITABILITY OF THESE LICENSED DELIVERABLES FOR ANY PURPOSE.  IT IS
 * PROVIDED "AS IS" WITHOUT EXPRESS OR IMPLIED WARRANTY OF ANY KIND.
 * NVIDIA DISCLAIMS ALL WARRANTIES WITH REGARD TO THESE LICENSED
 * DELIVERABLES, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY,
 * NONINFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.
 * NOTWITHSTANDING ANY TERMS OR CONDITIONS TO THE CONTRARY IN THE
 * LICENSE AGREEMENT, IN NO EVENT SHALL NVIDIA BE LIABLE FOR ANY
 * SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, OR ANY
 * DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
 * WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
 * ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
 * OF THESE LICENSED DELIVERABLES.
 *
 * U.S. Government End Users.  These Licensed Deliverables are a
 * "commercial item" as that term is defined at 48 C.F.R. 2.101 (OCT
 * 1995), consisting of "commercial computer software" and "commercial
 * computer software documentation" as such terms are used in 48
 * C.F.R. 12.212 (SEPT 1995) and is provided to the U.S. Government
 * only as a commercial end item.  Consistent with 48 C.F.R.12.212 and
 * 48 C.F.R. 227.7202-1 through 227.7202-4 (JUNE 1995), all
 * U.S. Government End Users acquire the Licensed Deliverables with
 * only those rights set forth herein.
 *
 * Any use of the Licensed Deliverables in individual and commercial
 * software must include, in the user documentation and internal
 * comments to the code, the above Disclaimer and U.S. Government End
 * Users Notice.
 * </blockquote>}
 */


/**
 * @file
 * @brief This file contains all public function declarations of the cuTensorNet
 * library.
 */
#pragma once

#define CUTENSORNET_MAJOR 2 //!< cuTensorNet major version.
#define CUTENSORNET_MINOR 1 //!< cuTensorNet minor version.
#define CUTENSORNET_PATCH 0 //!< cuTensorNet patch version.
#define CUTENSORNET_VERSION (CUTENSORNET_MAJOR * 10000 + CUTENSORNET_MINOR * 100 + CUTENSORNET_PATCH)

#include <cutensornet/types.h>
#include <cutensornet/typesDistributed.h>

#if defined(__cplusplus)
#include <cstdint>
#include <cstdio>

extern "C" {
#else
#include <stdint.h>
#include <stdio.h>

#endif /* __cplusplus */

#if defined(__GNUC__)
    #define CUTENSORNET_DEPRECATED(new_func)     __attribute__((deprecated("please use " #new_func " instead")))
#else
    #define CUTENSORNET_DEPRECATED(new_func)
#endif

/**
 * \brief Initializes the cuTensorNet library
 *
 * \details The device associated with a particular cuTensorNet handle is assumed to remain
 * unchanged after the cutensornetCreate() call. In order for the cuTensorNet library to 
 * use a different device, the application must set the new device to be used by
 * calling cudaSetDevice() and then create another cuTensorNet handle, which will
 * be associated with the new device, by calling cutensornetCreate().
 *
 * \param[out] handle Pointer to ::cutensornetHandle_t
 *
 * \returns ::CUTENSORNET_STATUS_SUCCESS on success and an error code otherwise
 * \remarks blocking, no reentrant, and thread-safe
 */
cutensornetStatus_t cutensornetCreate(cutensornetHandle_t* handle);

/**
 * \brief Destroys the cuTensorNet library handle
 *
 * \details This function releases resources used by the cuTensorNet library handle. This function is the last call with a particular handle to the cuTensorNet library.
 * Calling any cuTensorNet function which uses ::cutensornetHandle_t after cutensornetDestroy() will return an error.
 *
 * \param[in,out] handle Opaque handle holding cuTensorNet's library context.
 */
cutensornetStatus_t cutensornetDestroy(cutensornetHandle_t handle);

/**
 * \mainpage cuTensorNet: A high-level CUDA library that is dedicated to operations on tensor networks (i.e., a collection of tensors) 
 */

/**
 * \brief Initializes a ::cutensornetNetworkDescriptor_t, describing the connectivity (i.e., network topology) between the tensors.
 *
 * Note that this function allocates data on the heap; hence, it is critical that cutensornetDestroyNetworkDescriptor() is called once \p descNet is no longer required.
 * 
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] numInputs Number of input tensors.
 * \param[in] numModesIn Array of size \p numInputs; ``numModesIn[i]`` denotes the number of modes available in the i-th tensor.
 * \param[in] extentsIn Array of size \p numInputs; ``extentsIn[i]`` has ``numModesIn[i]`` many entries with ``extentsIn[i][j]`` (``j`` < ``numModesIn[i]``) corresponding to the extent of the j-th mode of tensor ``i``.
 * \param[in] stridesIn Array of size \p numInputs; ``stridesIn[i]`` has ``numModesIn[i]`` many entries with ``stridesIn[i][j]`` (``j`` < ``numModesIn[i]``) corresponding to the linearized offset -- in physical memory -- between two logically-neighboring elements w.r.t the j-th mode of tensor ``i``.
 * \param[in] modesIn Array of size \p numInputs; ``modesIn[i]`` has ``numModesIn[i]`` many entries -- each entry corresponds to a mode. Each mode that does not appear in the input tensor is implicitly contracted.
 * \param[in] qualifiersIn Array of size \p numInputs; ``qualifiersIn[i]`` denotes the qualifiers of i-th input tensor. Refer to ::cutensornetTensorQualifiers_t
 * \param[in] numModesOut number of modes of the output tensor. On entry, if this value is ``-1`` and the output modes are not provided, the network will infer the output modes. If this value is ``0``, the network is force reduced.
 * \param[in] extentsOut Array of size \p numModesOut; ``extentsOut[j]`` (``j`` < ``numModesOut``) corresponding to the extent of the j-th mode of the output tensor.
 * \param[in] stridesOut Array of size \p numModesOut; ``stridesOut[j]`` (``j`` < ``numModesOut``) corresponding to the linearized offset -- in physical memory -- between two logically-neighboring elements w.r.t the j-th mode of the output tensor.
 * \param[in] modesOut Array of size \p numModesOut; ``modesOut[j]`` denotes the j-th mode of the output tensor.
 * output tensor.
 * \param[in] dataType Denotes the data type for all input an output tensors.
 * \param[in] computeType Denotes the compute type used throughout the computation.
 * \param[out] descNet Pointer to a ::cutensornetNetworkDescriptor_t.
 *
 * \note If \p stridesIn (\p stridesOut) is set to 0 (\p NULL), it means the input tensors (output tensor) are in the Fortran (column-major) layout.
 * \note \p numModesOut can be set to ``-1`` for cuTensorNet to infer the output modes based on the input modes, or to ``0`` to perform a full reduction.
 * \note If \p qualifiersIn is set to 0 (\p NULL), cuTensorNet will use the defaults in ::cutensornetTensorQualifiers_t .
 *
 * Supported data-type combinations are:
 *
 * \verbatim embed:rst:leading-asterisk
 * +-------------+--------------------------+-------------+
 * |  Data type  |       Compute type       | Tensor Core |
 * +=============+==========================+=============+
 * | CUDA_R_16F  | CUTENSORNET_COMPUTE_32F  |   Volta+    |
 * +-------------+--------------------------+-------------+
 * | CUDA_R_16BF | CUTENSORNET_COMPUTE_32F  |   Ampere+   |
 * +-------------+--------------------------+-------------+
 * | CUDA_R_32F  | CUTENSORNET_COMPUTE_32F  |   No        |
 * +-------------+--------------------------+-------------+
 * | CUDA_R_32F  | CUTENSORNET_COMPUTE_TF32 |   Ampere+   |
 * +-------------+--------------------------+-------------+
 * | CUDA_R_32F  | CUTENSORNET_COMPUTE_16BF |   Ampere+   |
 * +-------------+--------------------------+-------------+
 * | CUDA_R_32F  | CUTENSORNET_COMPUTE_16F  |   Volta+    |
 * +-------------+--------------------------+-------------+
 * | CUDA_R_64F  | CUTENSORNET_COMPUTE_64F  |   Ampere+   |
 * +-------------+--------------------------+-------------+
 * | CUDA_R_64F  | CUTENSORNET_COMPUTE_32F  |   No        |
 * +-------------+--------------------------+-------------+
 * | CUDA_C_32F  | CUTENSORNET_COMPUTE_32F  |   No        |
 * +-------------+--------------------------+-------------+
 * | CUDA_C_32F  | CUTENSORNET_COMPUTE_TF32 |   Ampere+   |
 * +-------------+--------------------------+-------------+
 * | CUDA_C_64F  | CUTENSORNET_COMPUTE_64F  |   Ampere+   |
 * +-------------+--------------------------+-------------+
 * | CUDA_C_64F  | CUTENSORNET_COMPUTE_32F  |   No        |
 * +-------------+--------------------------+-------------+
 * \endverbatim

 */
cutensornetStatus_t cutensornetCreateNetworkDescriptor(const cutensornetHandle_t handle,
                                                       int32_t numInputs,
                                                       const int32_t numModesIn[],
                                                       const int64_t* const extentsIn[],
                                                       const int64_t* const stridesIn[],
                                                       const int32_t* const modesIn[],
                                                       const cutensornetTensorQualifiers_t qualifiersIn[],
                                                       int32_t numModesOut,
                                                       const int64_t extentsOut[],
                                                       const int64_t stridesOut[],
                                                       const int32_t modesOut[],
                                                       cudaDataType_t dataType,
                                                       cutensornetComputeType_t computeType,
                                                       cutensornetNetworkDescriptor_t* descNet);

/**
 * \brief Frees all the memory associated with the network descriptor.
 *
 * \param[in,out] desc Opaque handle to a tensor network descriptor.
 */
cutensornetStatus_t cutensornetDestroyNetworkDescriptor(cutensornetNetworkDescriptor_t desc);

/**
 * \brief DEPRECATED: Gets the number of output modes, data size, modes, extents, and strides of the output tensor.
 *
 * If all information regarding the output tensor is needed by the user, this function should be called twice
 * (the first time to retrieve \p numModesOut for allocating memory, and the second to retrieve \p modesOut, \p extentsOut, and \p stridesOut).
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] descNet Pointer to a ::cutensornetNetworkDescriptor_t.
 * \param[out] numModes on return, holds the number of modes of the output tensor. Cannot be null.
 * \param[out] dataSize if not null on return, holds the size (in bytes) of the memory needed for the output tensor. Optionally, can be null.
 * \param[out] modeLabels if not null on return, holds the modes of the output tensor. Optionally, can be null.
 * \param[out] extents if not null on return, holds the extents of the output tensor. Optionally, can be null.
 * \param[out] strides if not null on return, holds the strides of the output tensor. Optionally, can be null.
 */
CUTENSORNET_DEPRECATED(cutensornetGetOutputTensorDescriptor)
cutensornetStatus_t cutensornetGetOutputTensorDetails(const cutensornetHandle_t handle,
                                                      const cutensornetNetworkDescriptor_t descNet,
                                                      int32_t* numModes,
                                                      size_t*  dataSize,
                                                      int32_t* modeLabels,
                                                      int64_t* extents,
                                                      int64_t* strides);

/**
 * \brief Creates a ::cutensornetTensorDescriptor_t representing the output tensor of the network.
 *
 * This function will create a descriptor pointed to by \p outputTensorDesc. The user is responsible for calling 
 * ::cutensornetDestroyTensorDescriptor to destroy the descriptor.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] descNet Pointer to a ::cutensornetNetworkDescriptor_t.
 * \param[out] outputTensorDesc an opaque ::cutensornetTensorDescriptor_t struct. Cannot be null. On return, a new ::cutensornetTensorDescriptor_t holds the meta-data of the \p descNet output tensor.
 */
cutensornetStatus_t cutensornetGetOutputTensorDescriptor(const cutensornetHandle_t handle, 
                                                         const cutensornetNetworkDescriptor_t descNet, 
                                                         cutensornetTensorDescriptor_t* outputTensorDesc); 
 
/**
 * \brief Gets the number of output modes, data size, mode labels, extents, and strides of a tensor.
 *
 * If all information regarding the tensor is needed by the user, this function should be called twice
 * (the first time to retrieve \p numModes for allocating memory, and the second to retrieve \p modeLabels, \p extents, and \p strides).
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] tensorDesc Opaque handle to a tensor descriptor.
 * \param[out] numModes On return, holds the number of modes of the tensor. Cannot be null.
 * \param[out] dataSize If not null on return, holds the size (in bytes) of the memory needed for the tensor. Optionally, can be null.
 * \param[out] modeLabels If not null on return, holds the modes of the tensor. Optionally, can be null.
 * \param[out] extents If not null on return, holds the extents of the tensor. Optionally, can be null.
 * \param[out] strides If not null on return, holds the strides of the tensor. Optionally, can be null.
 */
cutensornetStatus_t cutensornetGetTensorDetails(const cutensornetHandle_t handle,
                                                const cutensornetTensorDescriptor_t tensorDesc,
                                                int32_t* numModes,
                                                size_t*  dataSize,
                                                int32_t* modeLabels,
                                                int64_t* extents,
                                                int64_t* strides);

/**
 * \brief Creates a workspace descriptor that holds information about the user provided memory buffer.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[out] workDesc Pointer to the opaque workspace descriptor.
 */
cutensornetStatus_t cutensornetCreateWorkspaceDescriptor(const cutensornetHandle_t handle,
                                                         cutensornetWorkspaceDescriptor_t *workDesc);

/**
 * \brief DEPRECATED: Computes the workspace size needed to contract the input tensor network using the provided contraction path.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] descNet Describes the tensor network (i.e., its tensors and their connectivity).
 * \param[in] optimizerInfo Opaque structure.
 * \param[out] workDesc The workspace descriptor in which the information is collected.
 */
 CUTENSORNET_DEPRECATED(cutensornetWorkspaceComputeContractionSizes)
cutensornetStatus_t cutensornetWorkspaceComputeSizes(const cutensornetHandle_t handle,
                                                     const cutensornetNetworkDescriptor_t descNet,
                                                     const cutensornetContractionOptimizerInfo_t optimizerInfo,
                                                     cutensornetWorkspaceDescriptor_t workDesc);

/**
 * \brief Computes the workspace size needed to contract the input tensor network using the provided contraction path.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] descNet Describes the tensor network (i.e., its tensors and their connectivity).
 * \param[in] optimizerInfo Opaque structure.
 * \param[out] workDesc The workspace descriptor in which the information is collected.
 */
cutensornetStatus_t cutensornetWorkspaceComputeContractionSizes(const cutensornetHandle_t handle,
                                                                const cutensornetNetworkDescriptor_t descNet,
                                                                const cutensornetContractionOptimizerInfo_t optimizerInfo,
                                                                cutensornetWorkspaceDescriptor_t workDesc);

/**
 * \brief DEPRECATED: Retrieves the needed workspace size for the given workspace preference and memory space.
 * 
 * The needed sizes for different tasks must be pre-calculated by calling the corresponding API, e.g, 
 * cutensornetWorkspaceComputeContractionSizes(), cutensornetWorkspaceComputeQRSizes(), 
 * cutensornetWorkspaceComputeSVDSizes() and cutensornetWorkspaceComputeGateSplitSizes().
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] workDesc Opaque structure describing the workspace.
 * \param[in] workPref Preference of workspace for planning.
 * \param[in] memSpace The memory space where the workspace is allocated.
 * \param[out] workspaceSize Needed workspace size.
 */
CUTENSORNET_DEPRECATED(cutensornetWorkspaceGetMemorySize)
cutensornetStatus_t cutensornetWorkspaceGetSize(const cutensornetHandle_t handle,
                                                const cutensornetWorkspaceDescriptor_t workDesc,
                                                cutensornetWorksizePref_t workPref,
                                                cutensornetMemspace_t memSpace,
                                                uint64_t* workspaceSize);

/**
 * \brief Retrieves the needed workspace size for the given workspace preference, memory space, workspace kind.
 * 
 * The needed sizes for different tasks must be pre-calculated by calling the corresponding API, e.g, 
 * cutensornetWorkspaceComputeContractionSizes(), cutensornetWorkspaceComputeQRSizes(), 
 * cutensornetWorkspaceComputeSVDSizes() and cutensornetWorkspaceComputeGateSplitSizes().
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] workDesc Opaque structure describing the workspace.
 * \param[in] workPref Preference of workspace for planning.
 * \param[in] memSpace The memory space where the workspace is allocated.
 * \param[in] workKind The kind of workspace.
 * \param[out] memorySize Needed workspace size.
 */
cutensornetStatus_t cutensornetWorkspaceGetMemorySize(const cutensornetHandle_t handle,
                                                      const cutensornetWorkspaceDescriptor_t workDesc,
                                                      cutensornetWorksizePref_t workPref,
                                                      cutensornetMemspace_t memSpace,
                                                      cutensornetWorkspaceKind_t workKind,
                                                      int64_t* memorySize);

/**
 * \brief DEPRECATED: Sets the memory address and workspace size of workspace provided by user.
 *
 * A workspace is valid in the following cases:
 *
 *   - \p workspacePtr is valid and \p workspaceSize > 0 
 *   - \p workspacePtr is null and \p workspaceSize > 0 (used during cutensornetCreateContractionPlan() to provide the available workspace).
 *   - \p workspacePtr is null and \p workspaceSize = 0 (workspace memory will be drawn from the user's mempool)
 *
 * A workspace will be validated against the minimal required at usage (cutensornetCreateContractionPlan(), cutensornetContractionAutotune(), cutensornetContraction())
 * 
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in,out] workDesc Opaque structure describing the workspace.
 * \param[in] memSpace The memory space where the workspace is allocated.
 * \param[in] workspacePtr Workspace memory pointer, may be null.
 * \param[in] workspaceSize Workspace size, must be >= 0.
 */
CUTENSORNET_DEPRECATED(cutensornetWorkspaceSetMemory)
cutensornetStatus_t cutensornetWorkspaceSet(const cutensornetHandle_t handle,
                                            cutensornetWorkspaceDescriptor_t workDesc,
                                            cutensornetMemspace_t memSpace,
                                            void* const workspacePtr,
                                            uint64_t workspaceSize);
/**
 * \brief Sets the memory address and workspace size of the workspace provided by user.
 *
 * A workspace is valid in the following cases:
 *
 *   - \p memoryPtr is valid and \p memorySize > 0 
 *   - \p memoryPtr is null and \p memorySize > 0: used to indicate memory with the indicated \p memorySize should be drawn from the mempool, or for cutensornetCreateContractionPlan() to indicate the available workspace size.
 *   - \p memoryPtr is null and \p memorySize = 0: indicates the workspace of the specified kind is disabled (currently applies to CACHE kind only).
 *   - \p memoryPtr is null and \p memorySize < 0: indicates workspace memory should be drawn from the user's mempool with the ::CUTENSORNET_WORKSIZE_PREF_RECOMMENDED size (see ::cutensornetWorksizePref_t).
 *
 * The \p memorySize will be validated against the minimal required at usage (cutensornetCreateContractionPlan(), cutensornetContractionAutotune(), cutensornetContraction(), cutensornetContractSlices())
 * 
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in,out] workDesc Opaque structure describing the workspace.
 * \param[in] memSpace The memory space where the workspace is allocated.
 * \param[in] workKind The kind of workspace.
 * \param[in] memoryPtr Workspace memory pointer, may be null.
 * \param[in] memorySize Workspace size.
 */
cutensornetStatus_t cutensornetWorkspaceSetMemory(const cutensornetHandle_t handle,
                                                  cutensornetWorkspaceDescriptor_t workDesc,
                                                  cutensornetMemspace_t memSpace,
                                                  cutensornetWorkspaceKind_t workKind,
                                                  void* const memoryPtr,
                                                  int64_t memorySize);

/**
 * \brief DEPRECATED: Retrieves the memory address and workspace size of workspace hosted in the workspace descriptor.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] workDesc Opaque structure describing the workspace.
 * \param[in] memSpace The memory space where the workspace is allocated.
 * \param[out] workspacePtr Workspace memory pointer.
 * \param[out] workspaceSize Workspace size.
 */
CUTENSORNET_DEPRECATED(cutensornetWorkspaceGetMemory)
cutensornetStatus_t cutensornetWorkspaceGet(const cutensornetHandle_t handle,
                                            const cutensornetWorkspaceDescriptor_t workDesc,
                                            cutensornetMemspace_t memSpace,
                                            void** workspacePtr,
                                            uint64_t* workspaceSize);

/**
 * \brief Retrieves the memory address and workspace size of workspace hosted in the workspace descriptor.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] workDesc Opaque structure describing the workspace.
 * \param[in] memSpace The memory space where the workspace is allocated.
 * \param[in] workKind The kind of workspace.
 * \param[out] memoryPtr Workspace memory pointer.
 * \param[out] memorySize Workspace size.
 */
cutensornetStatus_t cutensornetWorkspaceGetMemory(const cutensornetHandle_t handle,
                                                  const cutensornetWorkspaceDescriptor_t workDesc,
                                                  cutensornetMemspace_t memSpace,
                                                  cutensornetWorkspaceKind_t workKind,
                                                  void** memoryPtr,
                                                  int64_t* memorySize);

/**
 * \brief Frees the workspace descriptor.
 * 
 * Note that this API does not free the memory provided by cutensornetWorkspaceSetMemory().
 *
 * \param[in,out] desc Opaque structure.
 */
cutensornetStatus_t cutensornetDestroyWorkspaceDescriptor( cutensornetWorkspaceDescriptor_t desc );

/**
 * \brief Sets up the required hyper-optimization parameters for the contraction order solver (see cutensornetContractionOptimize())
 * 
 * Note that this function allocates data on the heap; hence, it is critical that cutensornetDestroyContractionOptimizerConfig() is called once \p optimizerConfig is no longer required.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[out] optimizerConfig This data structure holds all information about the user-requested hyper-optimization parameters.
 */
cutensornetStatus_t cutensornetCreateContractionOptimizerConfig(const cutensornetHandle_t handle,
                                                cutensornetContractionOptimizerConfig_t* optimizerConfig);

/**
 * \brief Frees all the memory associated with \p optimizerConfig.
 *
 * \param[in,out] optimizerConfig Opaque structure.
 */
cutensornetStatus_t cutensornetDestroyContractionOptimizerConfig(cutensornetContractionOptimizerConfig_t optimizerConfig);

/**
 * \brief Gets attributes of \p optimizerConfig.
 *
 * \param[in] handle Opaque handle holding cuTENSORNet's library context.
 * \param[in] optimizerConfig Opaque structure that is accessed.
 * \param[in] attr Specifies the attribute that is requested.
 * \param[out] buf On return, this buffer (of size \p sizeInBytes) holds the value that corresponds to \p attr within \p optimizerConfig.
 * \param[in] sizeInBytes Size of \p buf (in bytes).
 */
cutensornetStatus_t cutensornetContractionOptimizerConfigGetAttribute(const cutensornetHandle_t handle,
                                                const cutensornetContractionOptimizerConfig_t optimizerConfig,
                                                cutensornetContractionOptimizerConfigAttributes_t attr,
                                                void *buf,
                                                size_t sizeInBytes);
/**
 * \brief Sets attributes of \p optimizerConfig.
 *
 * \param[in] handle Opaque handle holding cuTENSORNet's library context.
 * \param[in] optimizerConfig Opaque structure that is accessed.
 * \param[in] attr Specifies the attribute that is requested.
 * \param[in] buf This buffer (of size \p sizeInBytes) determines the value to which \p attr will be set.
 * \param[in] sizeInBytes Size of \p buf (in bytes).
 */
cutensornetStatus_t cutensornetContractionOptimizerConfigSetAttribute(const cutensornetHandle_t handle,
                                                cutensornetContractionOptimizerConfig_t optimizerConfig,
                                                cutensornetContractionOptimizerConfigAttributes_t attr,
                                                const void *buf,
                                                size_t sizeInBytes);

/**
 * \brief Frees all the memory associated with \p optimizerInfo
 *
 * \param[in,out] optimizerInfo Opaque structure.
 */
cutensornetStatus_t cutensornetDestroyContractionOptimizerInfo(cutensornetContractionOptimizerInfo_t optimizerInfo);

/**
 * \brief Allocates resources for \p optimizerInfo.
 *
 * Note that this function allocates data on the heap; hence, it is critical that cutensornetDestroyContractionOptimizerInfo() is called once \p optimizerInfo is no longer required.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] descNet Describes the tensor network (i.e., its tensors and their connectivity) for which \p optimizerInfo is created.
 * \param[out] optimizerInfo Pointer to ::cutensornetContractionOptimizerInfo_t.
 */
cutensornetStatus_t cutensornetCreateContractionOptimizerInfo(const cutensornetHandle_t handle,
                                             const cutensornetNetworkDescriptor_t descNet,
                                             cutensornetContractionOptimizerInfo_t *optimizerInfo);

/**
 * \brief Computes an "optimized" contraction order as well as slicing info (for more information see Overview section) for a given tensor network such that the total time to solution is minimized while adhering to the user-provided memory constraint.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] descNet Describes the topology of the tensor network (i.e., all tensors, their connectivity and modes).
 * \param[in] optimizerConfig Holds all hyper-optimization parameters that govern the search for an "optimal" contraction order.
 * \param[in] workspaceSizeConstraint Maximal device memory that will be provided by the user (i.e., cuTensorNet has to find a viable path/slicing solution within this user-defined constraint).
 * \param[in,out] optimizerInfo On return, this object will hold all necessary information about the optimized path and the related slicing information. \p optimizerInfo will hold information including (see ::cutensornetContractionOptimizerInfoAttributes_t):
 *      - Total number of slices.
 *      - Total number of sliced modes.
 *      - Information about the sliced modes (i.e., the IDs of the sliced modes (see \p modesIn w.r.t. cutensornetCreateNetworkDescriptor()) as well as their extents (see Overview section for additional documentation).
 *      - Optimized path.
 *      - FLOP count.
 *      - Total number of elements in the largest intermediate tensor.
 *      - The mode labels for all intermediate tensors.
 *      - The estimated runtime and "effective" flops.
 */
cutensornetStatus_t cutensornetContractionOptimize(const cutensornetHandle_t handle,
                                            const cutensornetNetworkDescriptor_t descNet,
                                            const cutensornetContractionOptimizerConfig_t optimizerConfig,
                                            uint64_t workspaceSizeConstraint,
                                            cutensornetContractionOptimizerInfo_t optimizerInfo);

/**
 * \brief Gets attributes of \p optimizerInfo.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] optimizerInfo Opaque structure that is accessed.
 * \param[in] attr Specifies the attribute that is requested.
 * \param[out] buf On return, this buffer (of size \p sizeInBytes) holds the value that corresponds to \p attr within \p optimizeInfo.
 * \param[in] sizeInBytes Size of \p buf (in bytes).
 */
cutensornetStatus_t cutensornetContractionOptimizerInfoGetAttribute(
        const cutensornetHandle_t handle,
        const cutensornetContractionOptimizerInfo_t optimizerInfo,
        cutensornetContractionOptimizerInfoAttributes_t attr,
        void *buf,
        size_t sizeInBytes);

/**
 * \brief Sets attributes of optimizerInfo.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] optimizerInfo Opaque structure that is accessed.
 * \param[in] attr Specifies the attribute that is requested.
 * \param[in] buf This buffer (of size \p sizeInBytes) determines the value to which \p attr will be set.
 * \param[in] sizeInBytes Size of \p buf (in bytes).
 */
cutensornetStatus_t cutensornetContractionOptimizerInfoSetAttribute(
        const cutensornetHandle_t handle,
        cutensornetContractionOptimizerInfo_t optimizerInfo,
        cutensornetContractionOptimizerInfoAttributes_t attr,
        const void *buf,
        size_t sizeInBytes);

/**
 * \brief Gets the packed size of the \p optimizerInfo object.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] optimizerInfo Opaque structure of type cutensornetContractionOptimizerInfo_t.
 * \param[out] sizeInBytes The packed size (in bytes).
 */
cutensornetStatus_t cutensornetContractionOptimizerInfoGetPackedSize(
        const cutensornetHandle_t handle,
        const cutensornetContractionOptimizerInfo_t optimizerInfo,
        size_t *sizeInBytes);

/**
 * \brief Packs the \p optimizerInfo object into the provided buffer.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] optimizerInfo Opaque structure of type cutensornetContractionOptimizerInfo_t.
 * \param[out] buffer On return, this buffer holds the contents of optimizerInfo in packed form.
 * \param[in] sizeInBytes The size of the buffer (in bytes).
 */
cutensornetStatus_t cutensornetContractionOptimizerInfoPackData(
        const cutensornetHandle_t handle,
        const cutensornetContractionOptimizerInfo_t optimizerInfo,
        void *buffer,
        size_t sizeInBytes);

/**
 * \brief Create an optimizerInfo object from the provided buffer.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] descNet Describes the tensor network (i.e., its tensors and their connectivity) for which \p optimizerInfo is created.
 * \param[in] buffer A buffer with the contents of optimizerInfo in packed form.
 * \param[in] sizeInBytes The size of the buffer (in bytes).
 * \param[out] optimizerInfo Pointer to ::cutensornetContractionOptimizerInfo_t.
 */
cutensornetStatus_t cutensornetCreateContractionOptimizerInfoFromPackedData(
        const cutensornetHandle_t handle,
        const cutensornetNetworkDescriptor_t descNet,
        const void *buffer,
        size_t sizeInBytes,
        cutensornetContractionOptimizerInfo_t *optimizerInfo);

/**
 * \brief Update the provided \p optimizerInfo object from the provided buffer.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] buffer A buffer with the contents of optimizerInfo in packed form.
 * \param[in] sizeInBytes The size of the buffer (in bytes).
 * \param[in,out] optimizerInfo Opaque object of type ::cutensornetContractionOptimizerInfo_t that will be updated.
 */
cutensornetStatus_t cutensornetUpdateContractionOptimizerInfoFromPackedData(
                                         const cutensornetHandle_t handle,
                                         const void *buffer,
                                         size_t sizeInBytes,
                                         cutensornetContractionOptimizerInfo_t optimizerInfo);
/**
 * \brief Initializes a ::cutensornetContractionPlan_t.
 *
 * Note that this function allocates data on the heap; hence, it is critical that cutensornetDestroyContractionPlan() is called once \p plan is no longer required.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] descNet Describes the tensor network (i.e., its tensors and their connectivity).
 * \param[in] optimizerInfo Opaque structure.
 * \param[in] workDesc Opaque structure describing the workspace. At the creation of the contraction plan, only the workspace size is needed; the pointer to the workspace memory may be left null. 
 * If a device memory handler is set, \p workDesc can be set either to null (in which case the "recommended" workspace size is inferred, see ::CUTENSORNET_WORKSIZE_PREF_RECOMMENDED) or to a valid ::cutensornetWorkspaceDescriptor_t with the desired workspace size set and a null workspace pointer, see Memory Management API section.
 * \param[out] plan cuTensorNet's contraction plan holds all the information required to perform
 * the tensor contractions; to be precise, it initializes a \p cutensorContractionPlan_t for
 * each tensor contraction that is required to contract the entire tensor network.
*/
cutensornetStatus_t cutensornetCreateContractionPlan(const cutensornetHandle_t handle,
                                                     const cutensornetNetworkDescriptor_t descNet,
                                                     const cutensornetContractionOptimizerInfo_t optimizerInfo,
                                                     const cutensornetWorkspaceDescriptor_t workDesc,
                                                     cutensornetContractionPlan_t* plan);

/**
 * \brief Frees all resources owned by \p plan.
 *
 * \param[in,out] plan Opaque structure.
 */
cutensornetStatus_t cutensornetDestroyContractionPlan(cutensornetContractionPlan_t plan);

/**
 * \brief Auto-tunes the contraction plan to find the best \p cutensorContractionPlan_t for each pair-wise contraction.
 *
 * \note This function is blocking due to the nature of the auto-tuning process.
 * \note Input and output data pointers are recommended to be 256-byte aligned for best performance.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in,out] plan The plan must already be created (see cutensornetCreateContractionPlan()); the individual contraction plans will be fine-tuned.
 * \param[in] rawDataIn Array of N pointers (N being the number of input tensors specified cutensornetCreateNetworkDescriptor()); ``rawDataIn[i]`` points to the data associated with the i-th input tensor (in device memory).
 * \param[out] rawDataOut Points to the raw data of the output tensor (in device memory).
 * \param[in] workDesc Opaque structure describing the workspace. The provided workspace must be \em valid (the workspace size must be the same as or larger than both the minimum needed and the value provided at plan creation). See cutensornetCreateContractionPlan(), cutensornetWorkspaceGetMemorySize() & cutensornetWorkspaceSetMemory(). 
 * If a device memory handler is set, the \p workDesc can be set to null, or the workspace pointer in \p workDesc can be set to null, and the workspace size can be set either to 0 (in which case the "recommended" size is used, see ::CUTENSORNET_WORKSIZE_PREF_RECOMMENDED) or to a \em valid size. A workspace of the specified size will be drawn from the user's mempool and released back once done.
 * \param[in] pref Controls the auto-tuning process and gives the user control over how much time is spent in this routine.
 * \param[in] stream The CUDA stream on which the computation is performed.
 */
cutensornetStatus_t cutensornetContractionAutotune(const cutensornetHandle_t handle,
                                                   cutensornetContractionPlan_t plan,
                                                   const void* const rawDataIn[],
                                                   void* rawDataOut,
                                                   const cutensornetWorkspaceDescriptor_t workDesc,
                                                   const cutensornetContractionAutotunePreference_t pref,
                                                   cudaStream_t stream);

/**
 * \brief Sets up the required auto-tune parameters for the contraction plan
 * 
 * Note that this function allocates data on the heap; hence, it is critical that cutensornetDestroyContractionAutotunePreference() is called once \p autotunePreference is no longer required.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[out] autotunePreference This data structure holds all information about the user-requested auto-tune parameters.
 */
cutensornetStatus_t cutensornetCreateContractionAutotunePreference(const cutensornetHandle_t handle,
                                                cutensornetContractionAutotunePreference_t* autotunePreference);

/**
 * \brief Gets attributes of \p autotunePreference.
 *
 * \param[in] handle Opaque handle holding cuTENSORNet's library context.
 * \param[in] autotunePreference Opaque structure that is accessed.
 * \param[in] attr Specifies the attribute that is requested.
 * \param[out] buf On return, this buffer (of size \p sizeInBytes) holds the value that corresponds to \p attr within \p autotunePreference.
 * \param[in] sizeInBytes Size of \p buf (in bytes).
 */
cutensornetStatus_t cutensornetContractionAutotunePreferenceGetAttribute(const cutensornetHandle_t handle,
                                                const cutensornetContractionAutotunePreference_t autotunePreference,
                                                cutensornetContractionAutotunePreferenceAttributes_t attr,
                                                void *buf,
                                                size_t sizeInBytes);
/**
 * \brief Sets attributes of \p autotunePreference.
 *
 * \param[in] handle Opaque handle holding cuTENSORNet's library context.
 * \param[in] autotunePreference Opaque structure that is accessed.
 * \param[in] attr Specifies the attribute that is requested.
 * \param[in] buf This buffer (of size \p sizeInBytes) determines the value to which \p attr will be set.
 * \param[in] sizeInBytes Size of \p buf (in bytes).
 */
cutensornetStatus_t cutensornetContractionAutotunePreferenceSetAttribute(const cutensornetHandle_t handle,
                                                cutensornetContractionAutotunePreference_t autotunePreference,
                                                cutensornetContractionAutotunePreferenceAttributes_t attr,
                                                const void *buf,
                                                size_t sizeInBytes);

/**
 * \brief Frees all the memory associated with \p autotunePreference
 *
 * \param[in,out] autotunePreference Opaque structure.
 */
cutensornetStatus_t cutensornetDestroyContractionAutotunePreference(cutensornetContractionAutotunePreference_t autotunePreference);

/**
 * \brief DEPRECATED: Performs the actual contraction of the tensor network.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in,out] plan Encodes the execution of a tensor network contraction (see cutensornetCreateContractionPlan() and cutensornetContractionAutotune()). Some internal meta-data may be updated upon contraction.
 * \param[in] rawDataIn Array of N pointers (N being the number of input tensors specified cutensornetCreateNetworkDescriptor()); ``rawDataIn[i]`` points to the data associated with the i-th input tensor (in device memory).
 * \param[out] rawDataOut Points to the raw data of the output tensor (in device memory).
 * \param[in] workDesc Opaque structure describing the workspace. The provided workspace must be \em valid (the workspace size must be the same as or larger than both the minimum needed and the value provided at plan creation). See cutensornetCreateContractionPlan(), cutensornetWorkspaceGetMemorySize() & cutensornetWorkspaceSetMemory()). 
 * If a device memory handler is set, then \p workDesc can be set to null, or the workspace pointer in \p workDesc can be set to null, and the workspace size can be set either to 0 (in which case the "recommended" size is used, see ::CUTENSORNET_WORKSIZE_PREF_RECOMMENDED) or to a \em valid size. A workspace of the specified size will be drawn from the user's mempool and released back once done.
 * \param[in] sliceId The ID of the slice that is currently contracted (this value ranges between ``0`` and ``optimizerInfo.numSlices``); use ``0`` if no slices are used.
 * \param[in] stream The CUDA stream on which the computation is performed.
 *
 * \note If multiple slices are created, the order of contracting over slices using cutensornetContraction() should be ascending
 * starting from slice 0. If parallelizing over slices manually (in any fashion: streams, devices, processes, etc.), please make
 * sure the output tensors (that are subject to a global reduction) are zero-initialized.
 * 
 * \note Input and output data pointers are recommended to be 256-byte aligned for best performance.
 *
 * \note This function is asynchronous w.r.t. the calling CPU thread. The user should guarantee that the memory buffer provided in \p workDesc is valid until a synchronization with the stream or the device is executed.
 */
CUTENSORNET_DEPRECATED(cutensornetContractSlices)
cutensornetStatus_t cutensornetContraction(const cutensornetHandle_t handle,
                                           cutensornetContractionPlan_t plan,
                                           const void* const rawDataIn[],
                                           void* rawDataOut,
                                           const cutensornetWorkspaceDescriptor_t workDesc,
                                           int64_t sliceId,
                                           cudaStream_t stream);

/**
 * \brief Create a `cutensornetSliceGroup_t` object from a range, which produces a sequence of slice IDs from the specified start (inclusive) to the specified stop (exclusive) values with the specified step. The sequence can be increasing or decreasing depending on the start and stop values.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] sliceIdStart The start slice ID.
 * \param[in] sliceIdStop The final slice ID is the largest (smallest) integer that excludes this value and all those above (below) for an increasing (decreasing) sequence.
 * \param[in] sliceIdStep The step size between two successive slice IDs. A negative step size should be specified for a decreasing sequence.
 * \param[out] sliceGroup Opaque object specifying the slice IDs.
 */
cutensornetStatus_t cutensornetCreateSliceGroupFromIDRange(const cutensornetHandle_t handle,
                                                           int64_t sliceIdStart,
                                                           int64_t sliceIdStop,
                                                           int64_t sliceIdStep,
                                                           cutensornetSliceGroup_t *sliceGroup);
/**
 * \brief Create a `cutensornetSliceGroup_t` object from a sequence of slice IDs. Duplicates in the input slice ID sequence will be removed.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] beginIDSequence A pointer to the beginning of the slice ID sequence.
 * \param[in] endIDSequence A pointer to the end of the slice ID sequence.
 * \param[out] sliceGroup Opaque object specifying the slice IDs.
 */
cutensornetStatus_t cutensornetCreateSliceGroupFromIDs(const cutensornetHandle_t handle,
                                                       const int64_t *beginIDSequence,
                                                       const int64_t *endIDSequence,
                                                       cutensornetSliceGroup_t *sliceGroup);

/**
 * \brief  Releases the resources associated with a `cutensornetSliceGroup_t` object and sets its value to null.
 *
 * \param[in,out] sliceGroup Opaque object specifying the slices to be contracted (see cutensornetCreateSliceGroupFromIDRange() and cutensornetCreateSliceGroupFromIDs()).
 */
cutensornetStatus_t cutensornetDestroySliceGroup(cutensornetSliceGroup_t sliceGroup);

/**
 * \brief Performs the actual contraction of the tensor network.
 *
 * \warning In the current release, this function will synchronize the stream
 * in case distributed execution is activated (via ::cutensornetDistributedResetConfiguration)
 * 
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in,out] plan Encodes the execution of a tensor network contraction (see cutensornetCreateContractionPlan() and cutensornetContractionAutotune()). Some internal meta-data may be updated upon contraction.
 * \param[in] rawDataIn Array of N pointers (N being the number of input tensors specified cutensornetCreateNetworkDescriptor()); ``rawDataIn[i]`` points to the data associated with the i-th input tensor (in device memory).
 * \param[out] rawDataOut Points to the raw data of the output tensor (in device memory).
 * \param[in] accumulateOutput If 0, write the contraction result into rawDataOut; otherwise accumulate the result into rawDataOut.
 * \param[in] workDesc Opaque structure describing the workspace. 
 * The provided ::CUTENSORNET_WORKSPACE_SCRATCH workspace must be \em valid (the workspace size must be the same as or larger than both the minimum needed and the value provided at plan creation). See cutensornetCreateContractionPlan(), cutensornetWorkspaceGetMemorySize() & cutensornetWorkspaceSetMemory().
 * The provided ::CUTENSORNET_WORKSPACE_CACHE workspace can be of any size, the larger the better, up to the size that can be queried with cutensornetWorkspaceGetMemorySize().
 * If a device memory handler is set, then \p workDesc can be set to null, or the memory pointer in \p workDesc of either the workspace kinds can be set to null, and the workspace size can be set either to a negative value (in which case the "recommended" size is used, see ::CUTENSORNET_WORKSIZE_PREF_RECOMMENDED) or to a \em valid size. 
 * For a workspace of kind ::CUTENSORNET_WORKSPACE_SCRATCH, a memory buffer with the specified size will be drawn from the user's mempool and released back once done.
 * For a workspace of kind ::CUTENSORNET_WORKSPACE_CACHE, a memory buffer with the specified size will be drawn from the user's mempool and released back once the \p workDesc is destroyed, if \p workDesc != NULL, otherwise, once the \p plan is destroyed, or an alternative \p workDesc with a different memory address/size is provided in a subsequent cutensornetContractSlices() call.
 * \param[in] sliceGroup Opaque object specifying the slices to be contracted (see cutensornetCreateSliceGroupFromIDRange() and cutensornetCreateSliceGroupFromIDs()). *If set to null, all slices will be contracted.*
 * \param[in] stream The CUDA stream on which the computation is performed.
 *
 * \note Input and output data pointers are recommended to be 256-byte aligned for best performance.
 */
cutensornetStatus_t cutensornetContractSlices(const cutensornetHandle_t handle,
                                              cutensornetContractionPlan_t plan,
                                              const void* const rawDataIn[],
                                              void* rawDataOut,
                                              int32_t accumulateOutput,
                                              const cutensornetWorkspaceDescriptor_t workDesc,
                                              const cutensornetSliceGroup_t sliceGroup,
                                              cudaStream_t stream);

/**
 * \brief Initializes a ::cutensornetTensorDescriptor_t, describing the information of a tensor. 
 *
 * Note that this function allocates data on the heap; hence, it is critical that cutensornetDestroyTensorDescriptor() is called once \p descTensor is no longer required.
 * 
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] numModes The number of modes of the tensor. 
 * \param[in] extents Array of size \p numModes; ``extents[j]`` corresponding to the extent of the j-th mode of the tensor.
 * \param[in] strides Array of size \p numModes; ``strides[j]`` corresponding to the linearized offset -- in physical memory -- between two logically-neighboring elements w.r.t the j-th mode of the tensor.
 * \param[in] modes Array of size \p numModes; ``modes[j]`` denotes the j-th mode of the tensor.
 * \param[in] dataType Denotes the data type for the tensor.
 * \param[out] descTensor Pointer to a ::cutensornetTensorDescriptor_t.
 *
 * \note If \p strides is set to \p NULL, it means the tensor is in the Fortran (column-major) layout.
 */
cutensornetStatus_t cutensornetCreateTensorDescriptor(const cutensornetHandle_t handle,
                                                      int32_t numModes,
                                                      const int64_t extents[],
                                                      const int64_t strides[],
                                                      const int32_t modes[],
                                                      cudaDataType_t dataType,
                                                      cutensornetTensorDescriptor_t* descTensor);

/**
 * \brief Frees all the memory associated with the tensor descriptor.
 *
 * \param[in,out] descTensor Opaque handle to a tensor descriptor.
 */
cutensornetStatus_t cutensornetDestroyTensorDescriptor(cutensornetTensorDescriptor_t descTensor);

/**
 * \brief Sets up the options for singular value decomposition and truncation.
 * 
 * Note that this function allocates data on the heap; hence, it is critical that cutensornetDestroyTensorSVDConfig() is called once \p svdConfig is no longer required.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[out] svdConfig This data structure holds the user-requested svd parameters.
 */
cutensornetStatus_t cutensornetCreateTensorSVDConfig(const cutensornetHandle_t handle,
                                                     cutensornetTensorSVDConfig_t* svdConfig);

/**
 * \brief Frees all the memory associated with the tensor svd configuration.
 *
 * \param[in,out] svdConfig Opaque handle to a tensor svd configuration.
 */
cutensornetStatus_t cutensornetDestroyTensorSVDConfig(cutensornetTensorSVDConfig_t svdConfig);

/**
 * \brief Gets attributes of \p svdConfig.
 *
 * \param[in] handle Opaque handle holding cuTENSORNet's library context.
 * \param[in] svdConfig Opaque structure that is accessed.
 * \param[in] attr Specifies the attribute that is requested.
 * \param[out] buf On return, this buffer (of size \p sizeInBytes) holds the value that corresponds to \p attr within \p svdConfig.
 * \param[in] sizeInBytes Size of \p buf (in bytes).
 */
cutensornetStatus_t cutensornetTensorSVDConfigGetAttribute(const cutensornetHandle_t handle,
                                                           const cutensornetTensorSVDConfig_t svdConfig,
                                                           cutensornetTensorSVDConfigAttributes_t attr,
                                                           void *buf,
                                                           size_t sizeInBytes);

/**
 * \brief Sets attributes of \p svdConfig.
 *
 * \param[in] handle Opaque handle holding cuTENSORNet's library context.
 * \param[in] svdConfig Opaque structure that is accessed.
 * \param[in] attr Specifies the attribute that is requested.
 * \param[in] buf This buffer (of size \p sizeInBytes) determines the value to which \p attr will be set.
 * \param[in] sizeInBytes Size of \p buf (in bytes).
 */
cutensornetStatus_t cutensornetTensorSVDConfigSetAttribute(const cutensornetHandle_t handle,
                                                           cutensornetTensorSVDConfig_t svdConfig,
                                                           cutensornetTensorSVDConfigAttributes_t attr,
                                                           const void *buf,
                                                           size_t sizeInBytes);

/**
 * \brief Computes the workspace size needed to perform the tensor SVD operation.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] descTensorIn Describes the modes, extents and other metadata information for a tensor. 
 * \param[in] descTensorU Describes the modes, extents and other metadata information for the output tensor U.
 * \param[in] descTensorV Describes the modes, extents and other metadata information for the output tensor V. 
 * \param[in] svdConfig This data structure holds the user-requested svd parameters.
 * \param[out] workDesc The workspace descriptor in which the information is collected.
 */
cutensornetStatus_t cutensornetWorkspaceComputeSVDSizes(const cutensornetHandle_t handle,
                                                        const cutensornetTensorDescriptor_t descTensorIn,
                                                        const cutensornetTensorDescriptor_t descTensorU,
                                                        const cutensornetTensorDescriptor_t descTensorV,
                                                        const cutensornetTensorSVDConfig_t svdConfig,
                                                        cutensornetWorkspaceDescriptor_t workDesc);
/**
 * \brief Computes the workspace size needed to perform the tensor QR operation.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] descTensorIn Describes the modes, extents and other metadata information for a tensor. 
 * \param[in] descTensorQ Describes the modes, extents and other metadata information for the output tensor Q.
 * \param[in] descTensorR Describes the modes, extents and other metadata information for the output tensor R.
 * \param[out] workDesc The workspace descriptor in which the information is collected.
 */
cutensornetStatus_t cutensornetWorkspaceComputeQRSizes(const cutensornetHandle_t handle,
                                                       const cutensornetTensorDescriptor_t descTensorIn,
                                                       const cutensornetTensorDescriptor_t descTensorQ,
                                                       const cutensornetTensorDescriptor_t descTensorR,
                                                       cutensornetWorkspaceDescriptor_t workDesc);

/**
 * \brief Sets up the information for singular value decomposition.
 * 
 * Note that this function allocates data on the heap; hence, it is critical that cutensornetDestroyTensorSVDInfo() is called once \p svdInfo is no longer required.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[out] svdInfo This data structure holds all information about the trucation at runtime.
 */
cutensornetStatus_t cutensornetCreateTensorSVDInfo(const cutensornetHandle_t handle,
                                                   cutensornetTensorSVDInfo_t *svdInfo);

/**
 * \brief Gets attributes of \p svdInfo.
 *
 * \param[in] handle Opaque handle holding cuTENSORNet's library context.
 * \param[in] svdInfo Opaque structure that is accessed.
 * \param[in] attr Specifies the attribute that is requested.
 * \param[out] buf On return, this buffer (of size \p sizeInBytes) holds the value that corresponds to \p attr within \p svdConfig.
 * \param[in] sizeInBytes Size of \p buf (in bytes).
 */
cutensornetStatus_t cutensornetTensorSVDInfoGetAttribute(const cutensornetHandle_t handle,
                                                         const cutensornetTensorSVDInfo_t svdInfo,
                                                         cutensornetTensorSVDInfoAttributes_t attr,
                                                         void *buf,
                                                         size_t sizeInBytes);

/**
 * \brief Frees all the memory associated with the TensorSVDInfo object.
 *
 * \param[in,out] svdInfo Opaque handle to a TensorSVDInfo object.
 */
cutensornetStatus_t cutensornetDestroyTensorSVDInfo(cutensornetTensorSVDInfo_t svdInfo);

/**
 * \brief Performs SVD decomposition of a tensor.
 *
 * \details The partition of all input modes in \p descTensorIn is specified in \p descTensorU and \p descTensorV.
 * \p descTensorU and \p descTensorV are expected to share exactly one mode. The extent of the shared mode shall not exceed the minimum of m (row dimension) 
 * and n (column dimension) for the equivalent combined matrix SVD. 
 * The following variants of tensor SVD are supported: 
 *   - 1. Exact SVD: This can be specified by setting the extent of the shared mode in \p descTensorU and \p descTensorV to be the mininum of m and n, and setting \p svdConfig to \p NULL.
 *   - 2. SVD with fixed extent truncation: This can be specified by setting the extent of the shared mode in \p descTensorU and \p descTensorV to be lower than the mininum of m and n.
 *   - 3. SVD with value-based truncation: This can be specified by setting ::CUTENSORNET_TENSOR_SVD_CONFIG_ABS_CUTOFF or ::CUTENSORNET_TENSOR_SVD_CONFIG_REL_CUTOFF attribute of \p svdConfig. 
 *   - 4. SVD with a combination of fixed extent and value-based truncation as described above. 
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] descTensorIn Describes the modes, extents, and other metadata information of a tensor. 
 * \param[in] rawDataIn Pointer to the raw data of the input tensor (in device memory).
 * \param[in,out] descTensorU Describes the modes, extents, and other metadata information of the output tensor U. 
 * The extents for uncontracted modes are expected to be consistent with \p descTensorIn. 
 * \param[out] u Pointer to the output tensor data U (in device memory).
 * \param[out] s Pointer to the output tensor data S (in device memory). 
 * Can be \p NULL when the ::CUTENSORNET_TENSOR_SVD_CONFIG_S_PARTITION attribute of \p svdConfig is not set to default (::CUTENSORNET_TENSOR_SVD_PARTITION_NONE).
 * \param[in,out] descTensorV Describes the modes, extents, and other metadata information of the output tensor V.
 * \param[out] v Pointer to the output tensor data V (in device memory).
 * \param[in] svdConfig This data structure holds the user-requested SVD parameters.
 * Can be \p NULL if users do not need to perform value-based truncation or singular value partitioning.
 * \param[out] svdInfo Opaque structure holding all information about the trucation at runtime. Can be \p NULL if runtime information on singular value truncation is not needed.
 * \param[in] workDesc Opaque structure describing the workspace. The provided workspace must be \em valid (the workspace size must be the same as or larger than the minimum needed). See cutensornetWorkspaceGetMemorySize() & cutensornetWorkspaceSetMemory().
 * \param[in] stream The CUDA stream on which the computation is performed.
 * 
 * \note In the case of exact SVD or SVD with fixed extent truncation, \p descTensorU and \p descTensorV will remain constant after the execution. 
 * The data in \p u and \p v will respect the \p extent and \p stride in these tensor descriptors.
 * \note When value-based truncation is requested in \p svdConfig, `cutensornetTensorSVD` searches for the minimal extent that satifies both the value-based truncation and fixed extent requirement.
 * If the resulting extent is found to be the same as the one specified in U/V tensor descriptors, the \p extent and \p stride from the tensor descriptors will be respected.
 * If the resulting extent is found to be lower than the one specified in U/V tensor descriptors, the data in \p u and \p v will adopt a new Fortran-layout matching the reduced extent found. 
 * The \p extent and \p stride in \p descTensorU and \p descTensorV will also be overwritten to reflect this change. 
 * The user can query the reduced extent with cutensornetTensorSVDInfoGetAttribute() or cutensornetGetTensorDetails() (which also returns the new strides).
 * \note As the reduced size for value-based truncation is not known until runtime, the user should always allocate based on the full data size specified by the initial \p descTensorU and \p descTensorV for \p u and \p v.
 *
 */
cutensornetStatus_t cutensornetTensorSVD(const cutensornetHandle_t handle,
                                         const cutensornetTensorDescriptor_t descTensorIn,
                                         const void* const rawDataIn,
                                         cutensornetTensorDescriptor_t descTensorU,
                                         void *u,
                                         void *s,
                                         cutensornetTensorDescriptor_t descTensorV,
                                         void *v,
                                         const cutensornetTensorSVDConfig_t svdConfig,
                                         cutensornetTensorSVDInfo_t svdInfo,
                                         const cutensornetWorkspaceDescriptor_t workDesc,
                                         cudaStream_t stream);

/**
 * \brief Performs QR decomposition of a tensor.
 *
 * \details The partition of all input modes in \p descTensorIn is specified in \p descTensorQ and \p descTensorR.
 * \p descTensorQ and \p descTensorR are expected to share exactly one mode and the extent of that mode shall not exceed the minimum of m (row dimension) 
 * and n (column dimension) of the equivalent combined matrix QR. 
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] descTensorIn Describes the modes, extents, and other metadata information of a tensor. 
 * \param[in] rawDataIn Pointer to the raw data of the input tensor (in device memory).
 * \param[in] descTensorQ Describes the modes, extents, and other metadata information of the output tensor Q.
 * \param[out] q Pointer to the output tensor data Q (in device memory).
 * \param[in] descTensorR Describes the modes, extents, and other metadata information of the output tensor R.
 * \param[out] r Pointer to the output tensor data R (in device memory).
 * \param[in] workDesc Opaque structure describing the workspace. The provided workspace must be \em valid (the workspace size must be the same as or larger than the minimum needed). See cutensornetWorkspaceGetMemorySize() & cutensornetWorkspaceSetMemory().
 * \param[in] stream The CUDA stream on which the computation is performed.
 */
cutensornetStatus_t cutensornetTensorQR(const cutensornetHandle_t handle,
                                        const cutensornetTensorDescriptor_t descTensorIn,
                                        const void* const rawDataIn,
                                        const cutensornetTensorDescriptor_t descTensorQ,
                                        void *q,
                                        const cutensornetTensorDescriptor_t descTensorR,
                                        void *r,
                                        const cutensornetWorkspaceDescriptor_t workDesc,
                                        cudaStream_t stream);

/**
 * \brief Computes the workspace size needed to perform the gating operation.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] descTensorInA Describes the modes, extents, and other metadata information of the input tensor A.
 * \param[in] descTensorInB Describes the modes, extents, and other metadata information of the input tensor B.
 * \param[in] descTensorInG Describes the modes, extents, and other metadata information of the input gate tensor.
 * \param[in] descTensorU Describes the modes, extents, and other metadata information of the output U tensor.
 * The extents of uncontracted modes are expected to be consistent with \p descTensorInA and \p descTensorInG. 
 * \param[in] descTensorV Describes the modes, extents, and other metadata information of the output V tensor.
 * The extents of uncontracted modes are expected to be consistent with \p descTensorInB and \p descTensorInG. 
 * \param[in] gateAlgo The algorithm to use for splitting the gate tensor onto tensor A and B.
 * \param[in] svdConfig Opaque structure holding the user-requested SVD parameters.
 * \param[in] computeType Denotes the compute type used throughout the computation.
 * \param[out] workDesc Opaque structure describing the workspace. 
 * 
 */

cutensornetStatus_t cutensornetWorkspaceComputeGateSplitSizes(const cutensornetHandle_t handle,
                                                              const cutensornetTensorDescriptor_t descTensorInA,
                                                              const cutensornetTensorDescriptor_t descTensorInB,
                                                              const cutensornetTensorDescriptor_t descTensorInG,
                                                              const cutensornetTensorDescriptor_t descTensorU,
                                                              const cutensornetTensorDescriptor_t descTensorV,
                                                              const cutensornetGateSplitAlgo_t gateAlgo,
                                                              const cutensornetTensorSVDConfig_t svdConfig,
                                                              cutensornetComputeType_t computeType,
                                                              cutensornetWorkspaceDescriptor_t workDesc);

/**
 * \brief Performs gate split operation.
 *
 * \details \p descTensorInA, \p descTensorInB, and \p descTensorInG are expected to form a fully connected graph where the uncontracted modes are partitioned 
 * onto \p descTensorU and \p descTensorV via tensor SVD. \p descTensorU and \p descTensorV are expected to share exactly one mode. The extent of that mode shall not exceed the minimum of m (row dimension) 
 * and n (column dimension) of the smallest equivalent matrix SVD problem. 
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] descTensorInA Describes the modes, extents, and other metadata information of the input tensor A.
 * \param[in] rawDataInA Pointer to the raw data of the input tensor A (in device memory).
 * \param[in] descTensorInB Describes the modes, extents, and other metadata information of the input tensor B.
 * \param[in] rawDataInB Pointer to the raw data of the input tensor B (in device memory).
 * \param[in] descTensorInG Describes the modes, extents, and other metadata information of the input gate tensor.
 * \param[in] rawDataInG Pointer to the raw data of the input gate tensor G (in device memory).
 * \param[in] descTensorU Describes the modes, extents, and other metadata information of the output U tensor.
 * The extents of uncontracted modes are expected to be consistent with \p descTensorInA and \p descTensorInG. 
 * \param[out] u Pointer to the output tensor data U (in device memory).
 * \param[out] s Pointer to the output tensor data S (in device memory). 
 * Can be \p NULL when the ::CUTENSORNET_TENSOR_SVD_CONFIG_S_PARTITION attribute of \p svdConfig is not set to default (::CUTENSORNET_TENSOR_SVD_PARTITION_NONE).
 * \param[in] descTensorV Describes the modes, extents, and other metadata information of the output V tensor.
 * The extents of uncontracted modes are expected to be consistent with \p descTensorInB and \p descTensorInG. 
 * \param[out] v Pointer to the output tensor data V (in device memory).
 * \param[in] gateAlgo The algorithm to use for splitting the gate tensor into tensor A and B.
 * \param[in] svdConfig Opaque structure holding the user-requested SVD parameters.
 * \param[in] computeType Denotes the compute type used throughout the computation.
 * \param[out] svdInfo Opaque structure holding all information about the truncation at runtime.
 * \param[in] workDesc Opaque structure describing the workspace. 
 * \param[in] stream The CUDA stream on which the computation is performed.
 * 
 * \note The options for truncation and the treatment of \p extent and \p stride follows the same logic as tensor SVD, see cutensornetTensorSVD().
 */

cutensornetStatus_t cutensornetGateSplit(const cutensornetHandle_t handle,
                                         const cutensornetTensorDescriptor_t descTensorInA,
                                         const void* rawDataInA,
                                         const cutensornetTensorDescriptor_t descTensorInB,
                                         const void* rawDataInB,
                                         const cutensornetTensorDescriptor_t descTensorInG,
                                         const void* rawDataInG,
                                         cutensornetTensorDescriptor_t descTensorU,
                                         void* u,
                                         void* s,
                                         cutensornetTensorDescriptor_t descTensorV,
                                         void* v,
                                         const cutensornetGateSplitAlgo_t gateAlgo,
                                         const cutensornetTensorSVDConfig_t svdConfig,
                                         cutensornetComputeType_t computeType,
                                         cutensornetTensorSVDInfo_t svdInfo,
                                         const cutensornetWorkspaceDescriptor_t workDesc,
                                         cudaStream_t stream);                       

/**
 * \brief Get the current device memory handler.
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[out] devMemHandler If previously set, the struct pointed to by \p handler is filled in, otherwise ::CUTENSORNET_STATUS_NO_DEVICE_ALLOCATOR is returned.
 */
cutensornetStatus_t cutensornetGetDeviceMemHandler(const cutensornetHandle_t      handle,
                                                   cutensornetDeviceMemHandler_t* devMemHandler); 
 
/**
 * \brief Set the current device memory handler.
 *
 * Once set, when cuTensorNet needs device memory in various API calls it will allocate from the user-provided memory pool
 * and deallocate at completion. See ::cutensornetDeviceMemHandler_t and APIs that require ::cutensornetWorkspaceDescriptor_t
 * for further detail.
 *
 * The internal stream order is established using the user-provided stream passed to cutensornetContractionAutotune() and
 * cutensornetContraction().
 *
 * \warning It is <em> undefined behavior </em> for the following scenarios:
 *   - the library handle is bound to a memory handler and subsequently to another handler
 *   - the library handle outlives the attached memory pool
 *   - the memory pool is not <em> stream-ordered </em>
 *
 * \param[in] handle Opaque handle holding cuTensorNet's library context.
 * \param[in] devMemHandler the device memory handler that encapsulates the user's mempool. The struct content is copied internally.
 */
cutensornetStatus_t cutensornetSetDeviceMemHandler(cutensornetHandle_t                  handle, 
                                                   const cutensornetDeviceMemHandler_t* devMemHandler); 

/**
 * \brief This function sets the logging callback routine.
 * \param[in] callback Pointer to a callback function. Check ::cutensornetLoggerCallback_t.
 */
cutensornetStatus_t cutensornetLoggerSetCallback(cutensornetLoggerCallback_t callback);

/**
 * \brief This function sets the logging callback routine, along with user data.
 * \param[in] callback Pointer to a callback function. Check ::cutensornetLoggerCallbackData_t.
 * \param[in] userData Pointer to user-provided data to be used by the callback.
 */
cutensornetStatus_t cutensornetLoggerSetCallbackData(cutensornetLoggerCallbackData_t callback,
                                                     void* userData);

/**
 * \brief This function sets the logging output file.
 * \param[in] file An open file with write permission.
 */
cutensornetStatus_t cutensornetLoggerSetFile(FILE* file);

/**
 * \brief This function opens a logging output file in the given path.
 * \param[in] logFile Path to the logging output file.
 */
cutensornetStatus_t cutensornetLoggerOpenFile(const char* logFile);

/**
 * \brief This function sets the value of the logging level.
 * \param[in] level Log level, should be one of the following:
 * Level| Summary           | Long Description
 * -----|-------------------|-----------------
 *  "0" | Off               | logging is disabled (default)
 *  "1" | Errors            | only errors will be logged
 *  "2" | Performance Trace | API calls that launch CUDA kernels will log their parameters and important information
 *  "3" | Performance Hints | hints that can potentially improve the application's performance
 *  "4" | Heuristics Trace  | provides general information about the library execution, may contain details about heuristic status
 *  "5" | API Trace         | API Trace - API calls will log their parameter and important information
 */
cutensornetStatus_t cutensornetLoggerSetLevel(int32_t level);

/**
 * \brief This function sets the value of the log mask.
 *
 * \param[in]  mask  Value of the logging mask.
 * Masks are defined as a combination (bitwise OR) of the following masks:
 * Level| Description       |
 * -----|-------------------|
 *  "0" | Off               |
 *  "1" | Errors            |
 *  "2" | Performance Trace |
 *  "4" | Performance Hints |
 *  "8" | Heuristics Trace  |
 *  "16"| API Trace         |
 *
 * Refer to cutensornetLoggerSetLevel() for details.
 */
cutensornetStatus_t cutensornetLoggerSetMask(int32_t mask);

/**
 * \brief This function disables logging for the entire run.
 */
cutensornetStatus_t cutensornetLoggerForceDisable();

/**
 * \brief Returns Version number of the cuTensorNet library
 */
size_t cutensornetGetVersion();

/**
 * \brief Returns version number of the CUDA runtime that cuTensorNet was compiled against
 * \details Can be compared against the CUDA runtime version from cudaRuntimeGetVersion().
 */
size_t cutensornetGetCudartVersion();

/**
 * \brief Returns the description string for an error code
 * \param[in] error Error code to convert to string.
 * \returns the error string
 * \remarks non-blocking, no reentrant, and thread-safe
 */
const char *cutensornetGetErrorString(cutensornetStatus_t error);

/**
 * \brief Resets the distributed MPI parallelization configuration.
 * 
 * \details This function accepts a user-provided MPI communicator in a type-erased form
 * and stores a copy of it inside the cuTensorNet library handle. The provided MPI communicator
 * must be explicitly created by calling MPI_Comm_dup (please see the MPI specification).
 * The subsequent calls to the contraction path finder, contraction plan autotuning, and
 * contraction execution will be parallelized across all MPI processes in the provided
 * MPI communicator. The provided MPI communicator is owned by the user, it should stay
 * alive until the next reset call with a different MPI communicator. If NULL is provided
 * as the pointer to the MPI communicator, no parallelization will be applied to the above
 * mentioned procedures such that those procedures will execute redundantly across all MPI
 * processes. As an example, please refer to the tensornet_example_mpi_auto.cu sample.
 *
 * To enable distributed parallelism, cuTensorNet requires users to set an environment variable
 * \p \$CUTENSORNET_COMM_LIB containing the path to a shared library wrapping the communication
 * primitives. For MPI users, we ship a wrapper file \p cutensornet_distributed_interface_mpi.c
 * that can be compiled against the MPI library. cuTensorNet will use the included function
 * pointers to perform inter-process communication.
 *
 * \warning This is a collective call that must be executed by all MPI processes.
 * Note that one can still provide different (non-NULL) MPI communicators to different
 * subgroups of MPI processes (to create concurrent cuTensorNet distributed subgroups).
 *
 * \warning The provided MPI communicator must not be used by more than one
 * cuTensorNet library handle. This is automatically ensured by using MPI_Comm_dup.
 *
 * \warning The current library implementation assumes one GPU instance per MPI rank
 * since the cutensornet library handle is associated with a single GPU instance.
 * In case of multiple GPUs per node, each MPI process running on the same node
 * may still see all GPU devices if CUDA_VISIBLE_DEVICES was not set to provide an exclusive
 * access to each GPU. In such a case, the cutensornet library runtime will assign
 * GPU #(processRank % numVisibleDevices), where processRank is the rank of the current
 * process in its MPI communicator, and numVisibleDevices is the number of GPU devices
 * visible to the current MPI process. The assigned GPU must coincide with the one
 * associated with the cutensornet library handle, otherwise resulting in an error.
 * To ensure consistency, the user must call cudaSetDevice in each MPI process to
 * select the correct GPU device prior to creating a cutensornet library handle.
 *
 * \warning It is user's responsibility to ensure that each MPI process in each provided
 * MPI communicator executes exactly the same sequence of cutensornet API calls, which
 * otherwise will result in an undefined behavior.
 *
 * \param[in] handle cuTensorNet library handle.
 * \param[in] commPtr A pointer to the provided MPI communicator created by MPI_Comm_dup.
 * \param[in] commSize The size of the provided MPI communicator: sizeof(MPI_Comm).
 */
cutensornetStatus_t cutensornetDistributedResetConfiguration(
    cutensornetHandle_t handle,
    const void* commPtr,
    size_t commSize);

/**
 * \brief Queries the number of MPI ranks in the current distributed MPI configuration.
 * 
 * \param[in] handle cuTensorNet library handle.
 * \param[out] numRanks Number of MPI ranks in the current distributed MPI configuration.
 * \warning The number of ranks corresponds to the MPI communicator used by the current
 * MPI process. If different subgroups of MPI processes used different MPI communicators,
 * the reported number will refer to their specific MPI communicators.
 */
cutensornetStatus_t cutensornetDistributedGetNumRanks(
    const cutensornetHandle_t handle,
    int32_t* numRanks);

/**
 * \brief Queries the rank of the current MPI process in the current distributed MPI configuration.
 * 
 * \param[in] handle cuTensorNet library handle.
 * \param[out] procRank Rank of the current MPI process in the current distributed MPI configuration.
 * \warning The MPI process rank corresponds to the MPI communicator used by that MPI process.
 * If different subgroups of MPI processes used different MPI communicators, the reported number
 * will refer to their specific MPI communicators.
 */
cutensornetStatus_t cutensornetDistributedGetProcRank(
    const cutensornetHandle_t handle,
    int32_t* procRank);

/**
 * \brief Globally synchronizes all MPI processes in the current distributed MPI configuration,
 * ensuring that all preceding cutensornet API calls have completed across all MPI processes.
 * \warning This is a collective call that must be executed by all MPI processes.
 * \warning Prior to performing the global synchronization, the user is still required
 * to synchronize GPU operations locally (via CUDA stream synchronization). 
 * \param[in] handle cuTensorNet library handle.
 */
cutensornetStatus_t cutensornetDistributedSynchronize(
    const cutensornetHandle_t handle);

#if defined(__cplusplus)
}
#endif /* __cplusplus */
