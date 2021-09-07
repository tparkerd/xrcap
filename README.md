# 3-D Root Crown Analysis Pipeline

A pipeline to analyze 3D X-ray volumes of root crowns.

## Table of Contents

- [Installation](#installation)
  - [Dependencies](#dependencies)
- [Input & Output](#input)
  - [Description of Traits](#description-of-traits)
- [Usage](#usage)
- [Additional Information](#additional-information)
- [Credits](#credits)

## Installation

### Dependencies

This pipeline was assembled over the years, so many projects and code bases have contributed to make this pipeline what it is. As such, several dependencies are required to run this pipeline. When possible, dependencies are included for easier installation. You will need to install four core components to use this pipeline. Although details are included in our installation guide, if you encounter any issues, it's best to reference the module's own repository and documentation for assistance.

1. [3d-root-crown-analysis-pipeline](https://github.com/Topp-Roots-Lab/3d-root-crown-analysis-pipeline/) (this repo)
1. [python-rawtools](https://github.com/Topp-Roots-Lab/python-rawtools/)
1. [Gia3D](https://github.com/Topp-Roots-Lab/Gia3D)
1. [New3DTraitsForRPF](https://github.com/Topp-Roots-Lab/New3DTraitsForRPF)

See installation guide [here](INSTALL.md).

## Input

The input data consists of a `.RAW` and its paired `.DAT` file. Both of these can be generated by the NorthStar Imaging (NSI) efX-CT Software by exporting a `.RAW` volume. By default, the volume is assumed to be in unsigned 16-bit format.

## Output

The results of this pipeline are a `.TSV` of features and a `.CSV` of traits calculated from the provided volume.

### Description of Traits

Below are brief descriptions of the traits reported by this pipeline. For a more detailed description of each trait, see [implementation](IMPLEMENTATION.md).

#### Glossary

- Point cloud data (PCD): a collection of voxels of an object&mdash;derived from segemented volume or slices of 3D X-ray data.
- Root model: PCD representation of root
- Skeleton: PCD filterd using Palàyi method
- Voxel: a unit of volume in three-dimensional space; equivalent two a pixel in 2D space

#### Traits

**Name**|**Description**
-:|:-
`SurfaceArea`|The sum of exposed voxel faces on surface of the root model.
`Volume`|The sum of voxels in root model; a typical proxy for "biomass" in digital phenotyping.
`ConvexVolume`|The volume of the convex hull that encompasses the root model.
`Solidity`|The volume divided by the convex hull, a measure of the thoroughness of root exploration.
`MedR`|The median number of roots among all horizontal slices.
`MaxR`|The 84<sup>th</sup> percentile value of the number of roots among all horizontal slices.
`Bushiness`|The ratio of the maximum to the median number of roots among all horizontal slices.
`Depth`|The number of voxels of the vertical axis of the root model, a measure of the depth of the deepest root
`HorEqDiameter`|Maximum root model width among all horizontal slices.
`TotalLength`|Root length as approximated by the number of voxels in the skeleton.
`SRL`|Specific root length; the total length divided by the volume, similar to the traditional measure of total length divided by biomass.
`LengthDistr`|The ratio of root length in the upper &frac13; of the root model to the root length in the lower &frac23; of the model.
`WD_Ratio`|Width-to-depth ratio; the maximum root model width divided by the depth.
`NumberBifCl`|Estimated number of branching point in the skeleton.
`AvgSizeBifCl`|Estimated number of branches at each branching point in the skeleton.
`EdgeNum`|Number of skeleton segments between estimated branching points.
`AvgEdgeLength`|The average length of skeleton segments between estimated branching points, a measure of branching density of the root system.
`NumberTips`|Number of root tips in the root model.
`AvgRadius`|The average radius of all roots in the model, as estimated by the distance of each voxel in the skeleton from the surface of the root model.
`Elongation`|PCA on 3D point cloud, taking the ratio between PC2 variance and PC1 variance; measures how elongated the root is.
`Flatness`|PCA on 3D point cloud, taking the ratio between PC3 variance and PC2 variance; measures how flat the root is.
`Football`|PCA on (x, y) of 3D point cloud, taking the ratio between PC2 variance and PC1 variance.
`SolidityVHist` 01-20|The solidity at each slice is computed, then spline interpolated to the nt​h​ cm (1-20) below the top.
`DensityS` 1-6|The frequency of voxels with different 6 overlap ratios from side view. S6 represents the largest overlap ratio. Higher numbers in greater overlap ratio means a denser root.
`FractalDimensionS`|Fractal dimension is estimated from the projected side-view image using the box-counting method. It is a measure of how complicated a root shape is using self-similarity.
`FractalDimensionT`|Fractal dimension estimated from the projected top-view image using the box-counting method. It is a measure of how complicated a root shape is using self-similarity.
N/CH/S `Mean`|Mean estimated from the distribution of biomass/volume (N), convex hull (CH), or solidity (S) along the z-axis.
N/CH/S `Std`|Standard deviation estimated from the distribution of biomass/volume (N), convex hull (CH), or solidity (S) along the z-axis.
N/CH/S `Skewness`|Skewness, or inequality, estimated from the distribution of biomass/volume (N), convex hull (CH), or solidity (S) along the z-axis. Negative value indicates that a large number of the values are lower than the mean (left-tailed); positive value indicates that a larger number of the values are higher than the mean (right-tailed).
N/CH/S `Kurtosis`|Kurtosis, or peakiness, estimated from the distribution of biomass/volume (N), convex hull (CH), or solidity (S) along the z-axis. High value indicates that the peak of the distribution around the mean is sharp and long-tailed; low value indicates that the peak around the mean is round and short-tailed.
N/CH/S `Energy`|Energy, or uniformity, estimated from the distribution of biomass/volume (N), convex hull (CH), or solidity (S) along the z-axis. A high value indicates that the distribution has a small number of different levels.
N/CH/S `Entropy`|Entropy, the inverse of energy, estimated from the distribution of biomass/volume (N), convex hull (CH), or solidity (S) along the z-axis. A high value indicates that the distribution has a higher number of different levels.
N/CH/S `Smoothness`|Smoothness estimated from the distribution of biomass/volume (N), convex hull (CH), or solidity (S) along the z-axis. Defined as 1-11+(stddev)2

### Usage

See usage guide [here](USAGE.md).

This is an overview of the execution sequence for analyzing root crown x-ray scans.

<p align="center">
  <img alt="Root Crown Analysis Pipeline Flowchart" src="docs/img/root-crown-pipeline-flowchart.png">
</p>

### Additional Information

## Issues & Bug Reporting

If you encounter any error, problem, or would like to suggest a feature, please submit a [git issue](https://github.com/Topp-Roots-Lab/3d-root-crown-analysis-pipeline/issues).

## Related Projects

- [python-rawtools](https://github.com/Topp-Roots-Lab/python-rawtools/): A library for consuming and manipulating x-ray volume data in `.raw` format
- [Gia3D](https://github.com/Topp-Roots-Lab/Gia3D): A tool for measuring 3D traits from point cloud data
- [New3DTraitsForRPF](https://github.com/Topp-Roots-Lab/New3DTraitsForRPF): A tool for measuring traits using Kernel density estimation
- [xrt-dmt](https://github.com/Topp-Roots-Lab/xrt-dmt): A data management tool for tracking and archiving XRT (meta)data

## References

C. Bradford Barber, David P. Dobkin, & Hannu Huhdanpaa (1996). The Quickhull algorithm for convex hulls. _ACM TRANSACTIONS ON MATHEMATICAL SOFTWARE, 22(4), 469–483._ [doi:10.1.1.117.405](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.117.405).

Fakir S. Nooruddin & Greg Turk (2003). Simplification and Repair of Polygonal Models Using Volumetric Techniques. IEEE Trans. on Visualization and Computer Graphics, vol. 9, nr. 2, April 2003, pages 191-205.

Kálmán Palágyi, & Attila Kuba (1999). Directional 3D thinning using 8 subiterations. _LNCS_, 325–336. [doi:10.1.1.204.3009](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.204.3009)

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
