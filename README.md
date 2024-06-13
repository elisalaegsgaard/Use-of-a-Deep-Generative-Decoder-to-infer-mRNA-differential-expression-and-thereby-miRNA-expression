# Use-of-a-Deep-Generative-Decoder-to-infer-mRNA-differential-expression-and-thereby-miRNA-expression
A bachelor project in collaboration with Molekylær Medicinsk Afdeling (MOMA)

Through our bachelor's project (Bachelor of Data Science), we've gotten the opportunity to work with Molekylær Medicinsk Afdeling (MOMA) to improve the performance of the statistical tool biReact, by utilizing a deep generative decoder (DGD) to generate control samples. Both papers can be found as 
- miReact:
    Nielsen, M.M., Pedersen, J.S. miRNA activity inferred from single cell mRNA expression. Sci Rep 11, 9170 (2021). https://doi.org/10.1038/s41598-021-88480-5
    
- DGD:
    Prada-Luengo, I., Schuster, V., Liang, Y. et al. N-of-one differential gene expression without control samples using a deep generative model. Genome Biol 24, 263 (2023). https://doi.org/10.1186/s13059-023-03104-7

## Aim of the report 
The objective of this paper is to improve the performance of the statistical tool miReact. As described, we do not traditionally have control samples available in the applied setting, which can potentially have an impact on the inference accuracy of miReact. To address this limitation, we propose to apply and integrate a Deep Generative Decoder (DGD), which eliminates the need for healthy controls when inferring miRNA activity for cancer samples. We hypothesize that this integration can improve the accuracy of miReact results. Subsequently, we will evaluate the performance of the integrated model against the original miReact performance. 

For a detailed report see the PDF "Bachelor Project".

## Installation

The miReact software is written in R and available under the MIT license at:
[GitHub](https://github.com/muhligs/miReact)

The source code for DGD is released under the GNU license and it is freely available at:
[GitHub](https://github.com/Center-for-Health-Data-Science/bulkDGD )
