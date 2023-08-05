// ***************************************************************
// Copyright (c) 2021 Jittor. All Rights Reserved.
// Maintainers: Zheng-Ning Liu <lzhengning@gmail.com>.
// This file is subject to the terms and conditions defined in
// file 'LICENSE.txt', which is part of this source code package.
// ***************************************************************
#include "rocm_jittor.h"
#include "rocm_config.h"
#include "utils/str_utils.h"
#include <chrono>
#include <thread>

namespace jittor {

/* ========================= PROCESS CUDNN ========================= */
static const vector<string> kCudnnList = {
    "cudnnConvolutionDescriptor_t",
    "cudnnConvolutionMode_t",
    "cudnnCreate",
    "cudnnCreateConvolutionDescriptor",
    "cudnnCreateDropoutDescriptor",
    "cudnnCreateRNNDescriptor",
    "cudnnCreateTensorDescriptor",
    "cudnnDataType_t",
    "cudnnDestroy",
    "cudnnDestroyConvolutionDescriptor",
    "cudnnDestroyDropoutDescriptor",
    "cudnnDestroyRNNDescriptor",
    "cudnnDestroyTensorDescriptor",
    "cudnnDropoutDescriptor_t",
    "cudnnDropoutGetStatesSize",
    "cudnnGetErrorString",
    "cudnnGetRNNParamsSize",
    "cudnnGetRNNTrainingReserveSize",
    "cudnnGetRNNWorkspaceSize",
    "cudnnSetConvolutionGroupCount",
    "cudnnHandle_t",
    "cudnnRNNDescriptor_t",
    "cudnnRNNMode_t",
    "cudnnStatus_t",
    "cudnnTensorDescriptor_t"
};

static const map<string, string> kCudnnToMiopenDict {
    // Data types
    {"CUDNN_DATA_HALF", "miopenHalf"},
    {"CUDNN_DATA_FLOAT", "miopenFloat"},
    {"CUDNN_DATA_INT32", "miopenInt32"},
    {"CUDNN_DATA_INT8", "miopenInt8"},
    {"CUDNN_DATA_INT8x4", "miopenInt8x4"},
    {"CUDNN_DATA_BFLOAT16", "miopenBFloat16"},

    // Status
    {"CUDNN_STATUS_SUCCESS", "miopenStatusSuccess"},
    // {"CUDNN_STATUS_NOT_INITIALIZED", "miopenStatusNotInitialized"},
    // {"CUDNN_STATUS_ALLOC_FAILED", "miopenStatusAllocFailed"},
    // {"CUDNN_STATUS_BAD_PARAM", "miopenStatusBadParm"},
    // {"CUDNN_STATUS_ARCH_MISMATCH", "miopenStatusUnknownError"},
    // {"CUDNN_STATUS_MAPPING_ERROR", "miopenStatusUnknownError"},
    // {"CUDNN_STATUS_EXECUTION_FAILED", "miopenStatusUnknownError"},
    // {"CUDNN_STATUS_INTERNAL_ERROR", "miopenStatusInternalError"},
    // {"CUDNN_STATUS_NOT_SUPPORTED", "miopenStatusUnsupportedOp"},
    // {"CUDNN_STATUS_LICENSE_ERROR", "miopenStatusUnknownError"},
    // {"CUDNN_STATUS_RUNTIME_PREREQUISITE_MISSING", "miopenStatusUnknownError"},
    // {"CUDNN_STATUS_RUNTIME_IN_PROGRESS", "miopenStatusUnknownError"},
    // {"CUDNN_STATUS_RUNTIME_FP_OVERFLOW", "miopenStatusUnknownError"},

    // Activations
    {"CUDNN_ACTIVATION_SIGMOID", "miopenActivationLOGISTIC"},
    {"CUDNN_ACTIVATION_RELU", "miopenActivationRELU"},
    {"CUDNN_ACTIVATION_TANH", "miopenActivationTANH"},
    {"CUDNN_ACTIVATION_CLIPPED_RELU", "miopenActivationCLIPPEDRELU"},
    {"CUDNN_ACTIVATION_ELU", "miopenActivationELU"},
    {"CUDNN_ACTIVATION_IDENTITY", "__undefined"},
    {"CUDNN_ACTIVATION_SWISH", "__undefined"},
    
    // RNN
    {"cudnnGetRNNLinLayerBiasParams", "miopenGetRNNLayerBias"},
    {"cudnnGetRNNLinLayerMatrixParams", "miopenGetRNNLayerParam"},
    {"CUDNN_LINEAR_INPUT", "miopenRNNlinear"},
    {"CUDNN_SKIP_INPUT", "miopenRNNskip"},
    {"CUDNN_RNN_RELU", "miopenRNNRELU"},
    {"CUDNN_RNN_TANH", "miopenRNNTANH"},
    {"CUDNN_LSTM", "miopenLSTM"},
    {"CUDNN_GRU", "miopenGRU"},
    {"CUDNN_BIDIRECTIONAL", "miopenRNNbidirection"},
    {"CUDNN_UNIDIRECTIONAL", "miopenRNNunidirection"},
    {"CUDNN_RNN_ALGO_STANDARD", "miopenRNNdefault"},
    {"CUDNN_RNN_ALGO_PERSIST_STATIC", "miopenRNNdefault"},
    {"CUDNN_RNN_ALGO_PERSIST_DYNAMIC", "miopenRNNdefault"},

    // Convolution
    // TODO: check algorithm corresponding
    {"cudnnConvolutionFwdAlgo_t", "miopenConvFwdAlgorithm_t"},
    {"cudnnConvolutionBwdDataAlgo_t", "miopenConvBwdDataAlgorithm_t"},
    {"cudnnConvolutionBwdFilterAlgo_t", "miopenConvBwdWeightsAlgorithm_t"},
    {"cudnnConvolutionFwdAlgoPerf_t", "miopenConvAlgoPerf_t"},
    {"cudnnConvolutionBwdDataAlgoPerf_t", "miopenConvAlgoPerf_t"},
    {"cudnnConvolutionBwdFilterAlgoPerf_t", "miopenConvAlgoPerf_t"},
    {"CUDNN_CONVOLUTION", "miopenConvolution"},
    {"CUDNN_CROSS_CORRELATION", "miopenConvolution"},
    {"CUDNN_CONVOLUTION_FWD_ALGO_IMPLICIT_GEMM", "miopenConvolutionFwdAlgoImplicitGEMM"},
    {"CUDNN_CONVOLUTION_FWD_ALGO_IMPLICIT_PRECOMP_GEMM", "miopenConvolutionFwdAlgoImplicitGEMM"},
    {"CUDNN_CONVOLUTION_FWD_ALGO_GEMM", "miopenConvolutionFwdAlgoGEMM"},
    {"CUDNN_CONVOLUTION_FWD_ALGO_DIRECT", "miopenConvolutionFwdAlgoDirect"},
    {"CUDNN_CONVOLUTION_FWD_ALGO_FFT", "miopenConvolutionFwdAlgoFFT"},
    {"CUDNN_CONVOLUTION_FWD_ALGO_FFT_TILING", "miopenConvolutionFwdAlgoFFT"},
    {"CUDNN_CONVOLUTION_FWD_ALGO_WINOGRAD", "miopenConvolutionFwdAlgoWinograd"},
    {"CUDNN_CONVOLUTION_FWD_ALGO_WINOGRAD_NONFUSED", "miopenConvolutionFwdAlgoWinograd"},
    {"CUDNN_CONVOLUTION_BWD_DATA_ALGO_0", "miopenConvolutionBwdDataAlgoGEMM"},
    {"CUDNN_CONVOLUTION_BWD_DATA_ALGO_1", "miopenConvolutionBwdDataAlgoDirect"},
    {"CUDNN_CONVOLUTION_BWD_DATA_ALGO_FFT", "miopenConvolutionBwdDataAlgoFFT"},
    {"CUDNN_CONVOLUTION_BWD_DATA_ALGO_FFT_TILING", "miopenConvolutionBwdDataAlgoFFT"},
    {"CUDNN_CONVOLUTION_BWD_DATA_ALGO_WINOGRAD", "miopenConvolutionBwdDataAlgoWinograd"},
    {"CUDNN_CONVOLUTION_BWD_DATA_ALGO_WINOGRAD_NONFUSED", "miopenConvolutionBwdDataAlgoWinograd"},
    {"CUDNN_CONVOLUTION_BWD_FILTER_ALGO_0", "miopenConvolutionBwdWeightsAlgoGEMM"},
    {"CUDNN_CONVOLUTION_BWD_FILTER_ALGO_1", "miopenConvolutionBwdWeightsAlgoDirect"},
    {"CUDNN_CONVOLUTION_BWD_FILTER_ALGO_FFT", "miopenConvolutionBwdWeightsAlgoGEMM"},
    {"CUDNN_CONVOLUTION_BWD_FILTER_ALGO_3", "miopenConvolutionBwdWeightsAlgoImplicitGEMM"},
    {"CUDNN_CONVOLUTION_BWD_FILTER_WINOGRAD_NONFUSED", "miopenConvolutionBwdWeightsAlgoWinograd"},
    {"CUDNN_CONVOLUTION_BWD_FILTER_ALGO_FFT_TILING", "miopenConvolutionBwdWeightsAlgoImplicitGEMM"},

    // Tensor & Filter
    {"cudnnSetTensorNdDescriptor", "miopenSetTensorDescriptor"},
    {"cudnnFilterDescriptor_t", "miopenTensorDescriptor_t"},
    {"cudnnCreateFilterDescriptor", "miopenCreateTensorDescriptor"},
    {"cudnnDestroyFilterDescriptor", "miopenDestroyTensorDescriptor"}
};


static const map<string, pair<string, string>> kCudnnToMiopenPatterns {
    {"cudnnSetRNNDescriptor_v6", std::make_pair("cudnnSetRNNDescriptor_v6($1,$2,$3,$4,$5,$6,$7,$8,$9,$x)", "miopenSetRNNDescriptor_V2($2,$3,$4,$5,$6,$7,$8,miopenRNNwithBias,$9,$x)")},

    // Convolution
    {"cudnnConvolutionForward", std::make_pair("cudnnConvolutionForward($1,$2,$3,$4,$5,$6,$7,$8,$9,$x,$a,$b,$c));", "miopenConvolutionForward($1,$2,$3,$4,$5,$6,$7,$8,$a,$b,$c,$9,$x));")},
    {"cudnnConvolutionBackwardData", std::make_pair("cudnnConvolutionBackwardData($1,$2,$3,$4,$5,$6,$7,$8,$9,$x,$a,$b,$c));", "miopenConvolutionBackwardData($1,$2,$5,$6,$3,$4,$7,$8,$a,$b,$c,$9,$x));")},
    {"cudnnConvolutionBackwardFilter", std::make_pair("cudnnConvolutionBackwardFilter($1,$2,$3,$4,$5,$6,$7,$8,$9,$x,$a,$b,$c));", "miopenConvolutionBackwardWeights($1,$2,$5,$6,$3,$4,$7,$8,$a,$b,$c,$9,$x));")},
    {"cudnnFindConvolutionForwardAlgorithmEx", std::make_pair("cudnnFindConvolutionForwardAlgorithmEx($1,$2,$3,$4,$5,$6,$7,$8,$9,$x,$a,$b,$c)", "miopenFindConvolutionForwardAlgorithm($1,$2,$3,$4,$5,$6,$7,$8,$9,$x,$a,$b,$c,0)")},
    {"cudnnFindConvolutionBackwardDataAlgorithmEx", std::make_pair("cudnnFindConvolutionBackwardDataAlgorithmEx($1,$2,$3,$4,$5,$6,$7,$8,$9,$x,$a,$b,$c)", "miopenFindConvolutionBackwardDataAlgorithm($1,$4,$5,$2,$3,$6,$7,$8,$9,$x,$a,$b,$c,0)")},
    {"cudnnFindConvolutionBackwardFilterAlgorithmEx", std::make_pair("cudnnFindConvolutionBackwardFilterAlgorithmEx($1,$2,$3,$4,$5,$6,$7,$8,$9,$x,$a,$b,$c)", "miopenFindConvolutionBackwardWeightsAlgorithm($1,$4,$5,$2,$3,$6,$7,$8,$9,$x,$a,$b,$c,0)")},
    {"cudnnGetConvolutionForwardAlgorithm_v7", std::make_pair("cudnnGetConvolutionForwardAlgorithm_v7($1,$2,$3,$4,$5,$6,$7,$8)", "miopenStatusNotImplemented")},
    {"cudnnGetConvolutionBackwardDataAlgorithm_v7", std::make_pair("cudnnGetConvolutionBackwardDataAlgorithm_v7($1,$2,$3,$4,$5,$6,$7,$8)", "miopenStatusNotImplemented")},
    {"cudnnGetConvolutionBackwardFilterAlgorithm_v7", std::make_pair("cudnnGetConvolutionBackwardFilterAlgorithm_v7($1,$2,$3,$4,$5,$6,$7,$8)", "miopenStatusNotImplemented")},

    {"cudnnSetConvolutionNdDescriptor", std::make_pair("cudnnSetConvolutionNdDescriptor($1,$2,$3,$4,$5,$6,$7));", "miopenInitConvolutionNdDescriptor($1,$2,$3,$4,$5,$6));")},
    {"cudnnGetConvolutionForwardWorkspaceSize", std::make_pair("cudnnGetConvolutionForwardWorkspaceSize($1,$2,$3,$4,$5,$6, &$7)", "miopenConvolutionForwardGetWorkSpaceSize($1,$3,$2,$4,$5, &$7)")},
    {"cudnnGetConvolutionBackwardDataWorkspaceSize", std::make_pair("cudnnGetConvolutionBackwardDataWorkspaceSize($1,$2,$3,$4,$5,$6, &$7)", "miopenConvolutionBackwardDataGetWorkSpaceSize($1,$3,$2,$4,$5, &$7)")},
    {"cudnnGetConvolutionBackwardFilterWorkspaceSize", std::make_pair("cudnnGetConvolutionBackwardFilterWorkspaceSize($1,$2,$3,$4,$5,$6, &$7)", "miopenConvolutionBackwardWeightsGetWorkSpaceSize($1,$3,$2,$4,$5, &$7)")},

    // Disable TensorCore
    {"cudnnSetConvolutionMathType", std::make_pair("cudnnSetConvolutionMathType($1,$2)", "hipSuccess")},
    {"cudnnSetDropoutDescriptor", std::make_pair("cudnnSetDropoutDescriptor($1,$2,$3,$4,$5,$6));", "miopenSetDropoutDescriptor($1,$2,$3,$4,$5,$6,false,false,MIOPEN_RNG_PSEUDO_XORWOW$7));")}
};

bool process_cudnn(vector<string> &tokens) {
    // Before token mapping    
    for (int i = 0; i < tokens.size(); i++) {
        auto &token = tokens[i];
        if (token == "cudnnConvolutionFwdAlgo_t" && tokens[i+2] == "algos") {
            token_replace(tokens, i, "cudnnConvolutionFwdAlgo_t algos[] = {$1,$2,$3,$4,$5,$6,$7,$8}", 
                "miopenConvFwdAlgorithm_t algos[] = {\n"
                "   miopenConvolutionFwdAlgoGEMM,\n"
                "   miopenConvolutionFwdAlgoDirect,\n"
                "   miopenConvolutionFwdAlgoFFT,\n"
                "   miopenConvolutionFwdAlgoWinograd,\n"
                "   miopenConvolutionFwdAlgoImplicitGEMM}");
        } else if (token == "CUDNN_CONVOLUTION_FWD_ALGO_COUNT") {
            token = "5";
        } else if (token == "cudnnConvolutionBwdFilterAlgo_t" && tokens[i+2] == "algos") {
            token_replace(tokens, i, "cudnnConvolutionBwdFilterAlgo_t algos[] = {$1,$2,$3,$4,$5,$6}",
                "miopenConvBwdWeightsAlgorithm_t algos[] = {\n"
                "   miopenConvolutionBwdWeightsAlgoGEMM,\n"
                "   miopenConvolutionBwdWeightsAlgoDirect,\n"
                "   miopenConvolutionBwdWeightsAlgoWinograd,\n"
                "   miopenConvolutionBwdWeightsAlgoImplicitGEMM}");
        } else if (token == "CUDNN_CONVOLUTION_BWD_FILTER_ALGO_COUNT") {
            token = "4";
        } else if (token == "cudnnConvolutionBwdDataAlgo_t" && tokens[i+2] == "algos") {
            token_replace(tokens, i, "cudnnConvolutionBwdDataAlgo_t algos[] = {$1,$2,$3,$4,$5,$6}",
                "miopenConvBwdDataAlgorithm_t algos[] = {\n"
                "   miopenConvolutionBwdDataAlgoGEMM,\n"
                "   miopenConvolutionBwdDataAlgoDirect,\n"
                "   miopenConvolutionBwdDataAlgoFFT,\n"
                "   miopenConvolutionBwdDataAlgoWinograd,\n"
                "   miopenTransposeBwdDataAlgoGEMM,\n"
                "   miopenConvolutionBwdDataAlgoImplicitGEMM}");
        } else if (token == "CUDNN_CONVOLUTION_BWD_DATA_ALGO_COUNT") {
            token = "6";
        } else if (token == "if" && tokens[i+1] == " (" && tokens[i+2] == "benchmark") {
            // always search best conv algorithm
            tokens[i+2] == "true";
        } else if (token == "algo" && tokens[i-1].back() == '.') {
            // cudnnConvolution{Fwd|BwdData|BwdFilter}AlgoPerf_t.algo ->
            // miopenConvAlgoPerf_t.{fwd_algo|bwd_data_algo|bwd_weights_algo}
            int j;
            for (j = i; j >= 0; --j) {
                if (tokens[j].find("cudnnFindConvolutionForwardAlgorithmEx") != string::npos) {
                    token = "fwd_algo";
                    break;
                } else if (tokens[j].find("cudnnFindConvolutionBackwardDataAlgorithmEx") != string::npos) { 
                    token = "bwd_data_algo";
                    break;
                } else if (tokens[j].find("cudnnFindConvolutionBackwardFilterAlgorithmEx") != string::npos) {
                    token = "bwd_weights_algo";
                    break;
                }
            }
            if (j < 0) 
                LOGf << "not found algorithm searching";
        } else if (token == "num_algos" && tokens[i-1] == " < " && tokens[i-2] == "i") {
            token = "1";
        } else if (token == "perf_results" && tokens[i+4] == "status") {
            token_replace(tokens, i, "perf_results[i].status == CUDNN_STATUS_SUCCESS", "true");
        }
    }
        

    for (int i = 0; i < tokens.size(); ++i) {
        auto &token = tokens[i];
        if (kCudnnToMiopenDict.find(token) != kCudnnToMiopenDict.end()) {
            token = kCudnnToMiopenDict.find(token)->second;
        } else {
            for (const auto &cudnn_symbol : kCudnnList)
                if (token == cudnn_symbol) {
                    token = "miopen" + token.substr(5);
                    break;
                }
        }
    }

    // Translate incompatible CUDNN functions
    for (int i = 0; i < tokens.size(); i++) {
        auto &token = tokens[i];
        if (startswith(token, "cudnn") || startswith(token, "CUDNN")) {
            if (kCudnnToMiopenPatterns.find(token) != kCudnnToMiopenPatterns.end()) {
                    const auto &replacement = kCudnnToMiopenPatterns.find(token)->second;
                    token_replace(tokens, i, replacement.first, replacement.second, false);
            }
        }
    }

    // Note: should not move this part ahead
    for (int i = 0; i < tokens.size(); i++) {
        auto &token = tokens[i];

        // MIOpen only supports NCHW, so we remove CUDNN tensor format related codes.
        if (token == "cudnnTensorFormat_t") {
            if (startswith(tokens[i+3], ","))
                token_replace(tokens, i, "cudnnTensorFormat_t $1,", "");
            else if (startswith(tokens[i+5], ";")) {
                token_replace(tokens, i, "cudnnTensorFormat_t $1=$2;", "");
            }
        } else if (token == "filterFormat") {
            if (startswith(tokens[i+1], ","))
                token_replace(tokens, i, "filterFormat,", "");
            if (tokens[i+1] == " == ")
                token_replace(tokens, i-1, "($1==$2)", "(true)");
            else if (tokens[i+1] == " = (")
                token = "//" + token;
        } else if (token == "checkCudaErrors" && tokens[i+2] == "cudnnSetFilterNdDescriptor") {
        // MIOpen do not support filter*, so we convert filters to tensors
            string replacement = "int _JIT_strides[5] = {0};\n"
                                 "_JIT_strides[($4)-1] = 1;\n"
                                 "for (int i = ($4)-2; i >= 0; --i)\n"
                                 "    _JIT_strides[i] = _JIT_strides[i+1] * ($5)[i+1];\n"
                                 "checkCudaErrors(miopenSetTensorDescriptor($1,$2,$4,$5,_JIT_strides))";
            token_replace(tokens, i, "checkCudaErrors(cudnnSetFilterNdDescriptor($1,$2,$3,$4,$5))", replacement, false);
        }
    } 
    return true;
}
/* ========================= PROCESS CUDNN END ========================= */


/* ========================= PROCESS CUBLAS ========================= */
static const map<string, string> kCublasToRocblasDict {
    {"cublasHandle_t", "rocblas_handle"},
    {"cublasCreate", "rocblas_create_handle"},
    {"cublasDestroy", "rocblas_destroy_handle"},

    {"cublasGemmAlgo_t", "rocblas_gemm_algo"},
    // {"cublasComputeType_t", "rocblas_datatype"},
    {"CUBLAS_GEMM_DEFAULT", "rocblas_gemm_algo_standard"},
    {"CUBLAS_GEMM_DEFAULT_TENSOR_OP", "rocblas_gemm_algo_standard"},
    // {"CUBLAS_COMPUTE_16F", ""},
    // {"CUBLAS_COMPUTE_32F", ""},
    // {"CUBLAS_COMPUTE_32F_FAST_16F", ""},
    {"CUBLAS_API_H_", "_ROCBLAS_H_"},

    {"cublasStatus_t", "rocblas_status"},
    {"cudaDataType_t", "rocblas_datatype"},
    {"cudaDataType", "rocblas_datatype"},
    {"CUDA_R_32F", "rocblas_datatype_f32_r"},
    {"CUDA_R_64F", "rocblas_datatype_f64_r"},
    {"CUDA_R_16F", "rocblas_datatype_f16_r"},

    {"cublasOperation_t", "rocblas_operation"},
    {"CUBLAS_OP_N", "rocblas_operation_none"},
    {"CUBLAS_OP_T", "rocblas_operation_transpose"},
    {"CUBLAS_OP_C", "rocblas_operation_conjugate_transpose"},

    {"cublasSgemm", "rocblas_sgemm"}
};

static const map<string, pair<string, string>> kCublasToRocblasPatterns {
    {"cublasGemmEx", std::make_pair("cublasGemmEx($1,$2,$3,$4,$5,$6,$7,$8,$9,$x,$a,$b,$c,$d,$e,$f,$g,$h,$i)", 
                                 "rocblas_gemm_ex($1,$2,$3,$4,$5,$6,$7,$8,$9,$x,$a,$b,$c,$d,$e,$f,$g,$e,$f,$g,$h,$i,0,0)")},
    {"cublasGemmStridedBatchedEx", std::make_pair("cublasGemmStridedBatchedEx($1,$2,$3,$4,$5,$6,$7,$8,$9,$x,$a,$b,$c,$d,$e,$f,$g,$h,$i,$j,$k,$l,$m)", 
                                             "rocblas_gemm_strided_batched_ex($1,$2,$3,$4,$5,$6,$7,$8,$9,$x,$a,$b,$c,$d,$e,$f,$g,$h,$i,$j,$g,$h,$i,$j,$k,$l,$m,0,0)")}
};

bool process_cublas(vector<string> &tokens) {
    for (int i = 0; i < tokens.size(); ++i) {
        auto &token = tokens[i];

        if (token == "_cudaGetErrorEnum" && tokens[i+2] == "cublasStatus_t" && tokens[i+5][1] != ';') {
            token_replace(tokens, i, "_cudaGetErrorEnum(cublasStatus_t error) {$1{$2}$3}", "_cudaGetErrorEnum(rocblas_status error) { return rocblas_status_to_string(error); }");
        } else if (kCublasToRocblasDict.find(token) != kCublasToRocblasDict.end()) {
            token = kCublasToRocblasDict.find(token)->second;
        } else if (kCublasToRocblasPatterns.find(token) != kCublasToRocblasPatterns.end()) {
            const auto &replacement = kCublasToRocblasPatterns.find(token)->second;
            token_replace(tokens, i, replacement.first, replacement.second, false);
        }
    }

    return true;
}
/* ========================= PROCESS CUBLAS END ========================= */

/* ============================ PROCESS CUB ============================= */

static const map<string, string> kCubToRocprimDict {
    {"cub::BlockScan", "rocprim::block_scan"},
    {"cub::CountingInputIterator", "rocprim::counting_iterator"},
    {"cub::DeviceScan::InclusiveSum", "rocprim::inclusive_scan"},
    {"cub::KeyValuePair", "rocprim::key_value_pair"},
    {"BlockScanT::TempStorage", "BlockScanT::storage_type"}
};

static const map<string, pair<string, string>> kCubToRocprimPatterns {
    {
        "cub::DeviceScan::InclusiveSum", 
        std::make_pair(
            "cub::DeviceScan::InclusiveSum($1,$2,$3,$4,$5)", 
            "rocprim::inclusive_scan($1,$2,$3,$4,$5,rocprim::plus<Tx>())"
        )
    },
    {
        "cub::DeviceSegmentedRadixSort::SortPairs", 
        std::make_pair(
            "cub::DeviceSegmentedRadixSort::SortPairs($1,$2,$3,$4,$5,$6,$7,$8,$9,$x)", 
            "rocprim::segmented_radix_sort_pairs($1,$2,$3,$4,$5,$6,$7,$8,$9,$x)"
        )
    },
    {
        "cub::DeviceSegmentedRadixSort::SortPairsDescending", 
        std::make_pair(
            "cub::DeviceSegmentedRadixSort::SortPairsDescending($a,$b,$c,$d,$e,$f,$g,$h,$i,$j)",
            "rocprim::segmented_radix_sort_pairs_desc($a,$b,$c,$d,$e,$f,$g,$h,$i,$j)"
        )
    },
    {
        "cub::DeviceSelect::Flagged", 
        std::make_pair(
            "cub::DeviceSelect::Flagged($1,$2,$3,$4,$5,$6,$7)",
            "rocprim::select($1,$2,$3,$4,$5,$6,$7)"
        )
    },
    {
        "cub::TransformInputIterator", 
        std::make_pair(
            "cub::TransformInputIterator<$1,$2,$3>",
            "rocprim::transform_iterator<$3,$2,$1>"
        )
    },
    {
        "cub::DeviceSegmentedReduce::ArgMax", 
        std::make_pair(
            "cub::DeviceSegmentedReduce::ArgMax($1,$2,$3,$4,$5,$6,$7)",
            "rocprim_argmax($1,$2,$3,$4,$5,$6,$7)"
        )
    },
    {
        "cub::DeviceSegmentedReduce::ArgMin", 
        std::make_pair(
            "cub::DeviceSegmentedReduce::ArgMin($1,$2,$3,$4,$5,$6,$7)",
            "rocprim_argmin($1,$2,$3,$4,$5,$6,$7)"
        )
    }
};


bool process_cub(vector<string> &tokens) {
    for (int i = 0; i < tokens.size(); ++i) {
        auto &token = tokens[i];

        if (token == "cub" && tokens[i-1].back() != '"') {
            token = "rocprim" + token.substr(3, token.size() - 3);
        } else if (token == "cuh" && tokens[i+1][0] == '>') {
            token = "hpp";
        } else if (kCubToRocprimDict.find(token) != kCubToRocprimDict.end()) {
            token = kCubToRocprimDict.find(token)->second;
        } else if (token == "BlockScanT" && tokens[i+1][0] == '(' && tokens[i+4] == "InclusiveSum") {
            token_replace(tokens, i, "BlockScanT($1).InclusiveSum($2,$3)", "BlockScanT().inclusive_scan($2,$3,$1,rocprim::plus<Tx>())", false);
        } else if (kCubToRocprimPatterns.find(token) != kCubToRocprimPatterns.end()) {
            // include rocm_warpper.h
            if (token == "cub::DeviceSegmentedReduce::ArgMax" || token == "cub::DeviceSegmentedReduce::ArgMin") {
                tokens[0] = "#include \"rocm_wrapper.h\"\n" + tokens[0];
            }
            const auto &replacement = kCubToRocprimPatterns.find(token)->second;
            token_replace(tokens, i, replacement.first, replacement.second, false);
        }
    }

    return true;
}


/* ========================== PROCESS CUB END =========================== */


/* ========================= PROCESS CUDA ========================= */
static const vector<string> kCudaList = {
    "cudaComputeModeProhibited",
    "cudaDeviceSynchronize",
    "cudaEvent_t",
    "cudaEventCreate",
    "cudaEventCreateWithFlags",
    "cudaEventDestroy",
    "cudaEventDisableTiming",
    "cudaEventElapsedTime",
    "cudaEventRecord",
    "cudaEventSynchronize",
    "cudaError_t",
    "cudaFree",
    "cudaFreeHost",
    "cudaGetDevice",
    "cudaGetDeviceCount",
    "cudaGetDeviceProperties",
    "cudaGetErrorName",
    "cudaGetLastError",
    "cudaMalloc",
    "cudaMallocHost",
    "cudaMallocManaged",
    "cudaMemcpy",
    "cudaMemcpyAsync",
    "cudaMemcpyDeviceToHost",
    "cudaMemcpyDeviceToDevice",
    "cudaMemcpyHostToDevice",
    "cudaMemGetInfo",
    "cudaMemset",
    "cudaMemsetAsync",
    "cudaSetDevice",
    "cudaStreamAddCallback",
    "cudaStreamCreate",
    "cudaStreamCreateWithFlags",
    "cudaStream_t",
    "cudaStreamDestroy",
    "cudaStreamNonBlocking",
    "cudaStreamSynchronize",
    "cudaStreamWaitEvent",
    "cudaSuccess"
};

string process_rocm(const string& src, const string& name, const map<string,string>& kargs) {
    if (name == "rocm_jittor.cc")
        return src;
        
    bool exclude_comments = false;
    if (name == "cudnn_conv_test.cc")
        exclude_comments = true;

    auto tokens = token_split(src, exclude_comments);
    for (int i = 0; i < tokens.size(); i++) {
        auto &token = tokens[i];
        if (token == "CUDA") {
            token = "HIP";
        } else if (token == "ifdef") {
            // macros
            if (tokens[i+2] == "IS_CUDA" && name != "cuda_limits.h") {
                tokens[i] = "if defined(IS_CUDA) || defined(IS_ROCM)";
                tokens[i+2] = " ";
            } else if (tokens[i+2] == "__DRIVER_TYPES_H__") {
                tokens[i+2] = "IS_ROCM";
            } else if (tokens[i+2] == "CUDNN_H_") {
                tokens[i+2] = "MIOPEN_GUARD_MIOPEN_H_";
            }
        } else if (i+2 < tokens.size() && tokens[i+1] == "." && tokens[i+2] == "h") {
            // headers
            if (token == "cuda_runtime") {
                token = "hip/hip_runtime";
            } else if (token == "cuda_runtime_api") {
                token = "hip/hip_runtime_api";
            } else if (token == "driver_types") {
                token = "hip/driver_types";
            } else if (token == "cuda_fp16") {
                token = "hip/hip_fp16";
            } else if (token == "cudnn") {
                token = "miopen/miopen";
            } else if (token == "cublas_v2" || token == "cublas") {
                token = "rocblas";
            } else if (token == "nccl") {
                token = "rccl";
            }
        } else if (startswith(token, "cuda")) {
            // cuda
            for (const auto &cuda_symbol : kCudaList)
                if (token == cuda_symbol) {   
                    token = "hip" + token.substr(4);
                    break;
                }
            if (token == "hipEventCreate" && tokens[i + 3].find(",") != string::npos) {
                token = "hipEventCreateWithFlags";
            } else if (token == "cudaDeviceProp") {
                token = "hipDeviceProp_t";
            }
        } else if (token == "auto" && tokens[i+1] == " " && tokens[i+2] == "__restrict__" && tokens[i+5] == " = (") {
            // hipcc do not support keyword __restrict__ followed by "auto"
            //      auto __restrict__ x = (T) y;    ==> T __restrict__ x = (T) y;
            //      auto* __restrict__ x = (T*) y;  ==> T* __restrict__ x = (T*) y;
            token = tokens[i+6];
            if (tokens[i+7][0] == '*')
                token = token + '*';
        } else if (token == "__trap" && startswith(tokens[i+1], "()")) {
            token = "abort";
        // } else if (startswith(token, "__shfl")) {
        //     if (token == "__shfl_sync")
        //         token_replace(tokens, i, "__shfl_sync($1,$2,$3)", "__shfl($2,$3,32)");
        //     else if (token == "__shfl_up_sync")
        //         token_replace(tokens, i, "__shfl_up_sync($1,$2,$3)", "__shfl_up($2,$3,32)");
        //     else if (token == "__shfl_down_sync")
        //         token_replace(tokens, i, "__shfl_down_sync($1,$2,$3)", "__shfl_down($2,$3,32)");
        //     else if (token == "__shfl_xor_sync")
        //         token_replace(tokens, i, "__shfl_xor_sync($1,$2,$3)", "__shfl_xor($2,$3,32)");
        } else if (token == "JPU") {
            string new_code;
            if (tokens[i+2] == "op_compiler")
                token_replace(tokens, i, 
                    "JPU(op_compiler($1,$2,$3))",
                    "rocm_jittor_op_compiler($1,$2,$3)");
            else if (tokens[i+2] == "header")
                new_code = "#include \"rocm_jittor.h\"";
            if (new_code.size())
                token_replace(tokens, i,  "JPU($1)", new_code);
        } else if (token == "use_cuda_managed_allocator" && tokens[i+1][0]==',') {
            tokens[i+2] = "0"; // disable unified address
        } else if (token == "para_opt_level" && tokens[i+1][0]==',') {
            tokens[i+2] = "4"; 
        }
    }

    process_cudnn(tokens);
    process_cublas(tokens);
    process_cub(tokens);

    auto new_src = join(tokens, "");
    
    new_src = "#include <hip/hip_runtime.h>\n" 
              "#define CUDART_VERSION 10000\n" + new_src;

    if (name == "cuda_flags.h") {
        new_src = replace(new_src, "defined(CUDART_VERSION) && CUDART_VERSION < 10000", "defined(IS_ROCM)");
    }
    if (name == "cuda_atomic.h") {
        new_src = replace(new_src, "long long", "unsigned long long");
        new_src = replace(new_src, "__longlong_as_double", "__ulonglong_as_double");
        new_src = replace(new_src, "__double_as_longlong", "__double_as_ulonglong");
        new_src = "__device__ __inline__ static unsigned long long __double_as_ulonglong(double floatVal) {\n"
                  "    return *(reinterpret_cast<unsigned long long*>(&floatVal));\n"
                  "}\n"
                  "__device__ __inline__ static double __ulonglong_as_double(unsigned long long intVal) {\n"
                  "    return *(reinterpret_cast<double*>(&intVal));\n"
                  "}\n" + new_src;
    }

    rocm_config(name, new_src);

    return new_src;
}
/* ========================= PROCESS CUDA END ========================= */


void rocm_jittor_op_compiler(string& filename, string& src, bool is_rocm, string& extra_flags) {
    if (!is_rocm) return;

    string new_src = process_rocm(src, filename, {});
    new_src = replace(new_src, "std::max( range2/4,32)", "std::max( (int)range2/4,32)");
    src = new_src;
}

}