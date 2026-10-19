# 3D Object Contour Dataset Generator

A tool for building contour datasets for computer vision and machine learning research. It places virtual cameras at the vertices of a geodesic dome around a 3D object, captures a snapshot from each viewpoint, and extracts the object's contour from each snapshot.

## How It Works

1. Load a 3D model.
2. Place a geodesic dome around the object. Each dome vertex is a camera position.
3. Render a snapshot of the object from every camera position.
4. Extract the contour from each snapshot.
5. Resample the contour to a fixed number of points and save it, along with the viewpoint metadata.

## Libraries Used

| Library | Purpose |
|---|---|
| **PyVista** and **trimesh** | Load meshes, build the dome around the object, and capture snapshots |
| **OpenCV** | Extract contours from the snapshots |
| **NumPy** | Array handling |
| **Matplotlib** | Draw contours (optional, for visualization) |
| **json** | Read and write the dataset files |

## Input Files

Two output files must exist before you generate a dataset. They can be empty or already contain data, so you can append to an existing dataset.

Example files with data are included: `contours.json` and `contourdata.json`.

### `contours.json`

Stores the contour points as an array of shape **N x M x 2**:

- **N**: the number of contours (the index of each contour)
- **M**: the number of points around each contour (120 in the included example data)
- **2**: the x and y coordinates of each point

### `contourdata.json`

Stores the metadata for each contour:

- the contour's index (matching its position in `contours.json`)
- the **azimuth** and **elevation** of the camera
- the **file name** of the source object

## Supported Models

Trimesh can load many file formats, but this project has only been tested with **`.obj`** files. Other formats may work, but their behavior is not guaranteed, so `.obj` is recommended.

## Data Sources

The included contours were generated from:

- **Digital Life 3D** object scans
- **SMAL** (Skinned Multi-Animal Linear model) dataset

## Citation

If you use the SMAL data, please cite:

```bibtex
@inproceedings{Zuffi:CVPR:2017,
  title         = {{3D} Menagerie: Modeling the {3D} Shape and Pose of Animals},
  author        = {Zuffi, Silvia and Kanazawa, Angjoo and Jacobs, David and Black, Michael J.},
  booktitle     = {IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)},
  month         = jul,
  year          = {2017},
  month_numeric = {7}
}
```
