#![cfg(feature = "extension-module")]

use crate::{convert_image, convert_image_bytes, JpegConverterError};
use numpy::PyReadonlyArray3;
use numpy::{ndarray::Array, IntoPyArray, PyArray3};
use pyo3::exceptions::{PyIOError, PyRuntimeError, PyTypeError};
use pyo3::prelude::*;

#[inline(always)]
fn type_error_check(cond: bool, msg: &str) -> PyResult<()> {
    if cond {
        Ok(())
    } else {
        Err(PyTypeError::new_err(msg.to_string()))
    }
}

/// python module implemented in Rust
#[pymodule]
fn jpeg_converter(_py: Python, m: &PyModule) -> PyResult<()> {
    impl std::convert::From<JpegConverterError> for PyErr {
        fn from(err: JpegConverterError) -> PyErr {
            match err {
                JpegConverterError::IOError(_) => PyIOError::new_err(err.to_string()),
                JpegConverterError::EncodingError(_) => PyRuntimeError::new_err(err.to_string()),
                JpegConverterError::ImageError(_) => PyRuntimeError::new_err(err.to_string()),
                JpegConverterError::OpenImageError(_) => PyRuntimeError::new_err(err.to_string()),
                JpegConverterError::ArrayShapeError(_) => PyRuntimeError::new_err(err.to_string()),
            }
        }
    }

    // Load any image as jpeg into numpy array [C=3, H, W] with dtype np.float32 with given quality.
    #[pyfn(m)]
    #[pyo3(name = "load_image_as_jpeg")]
    fn load_image_as_jpeg<'py>(
        py: Python<'py>,
        filename: &str,
        quality: u8,
    ) -> PyResult<&'py PyArray3<f32>> {
        let result = convert_image(filename.to_string(), quality)?;
        let pyarr = unsafe {
            Array::from_shape_vec_unchecked(
                (3, result.height as usize, result.width as usize),
                result.buffer,
            )
        };
        Ok(pyarr.into_pyarray(py))
    }

    // Re-convert raw decoded image from numpy uint8 array with 3 dimensional layout [C, H, W] to jpeg into numpy array with same layout width dtype np.float32 with given quality.
    // data ndarray must be contiguous
    #[pyfn(m)]
    #[pyo3(name = "convert_raw_to_jpeg")]
    fn convert_raw_to_jpeg<'py>(
        py: Python<'py>,
        data: PyReadonlyArray3<u8>,
        quality: u8,
    ) -> PyResult<&'py PyArray3<f32>> {
        let sizes = data.shape();
        type_error_check(sizes.len() == 3, "data shape must be 3 dimensional")?;
        type_error_check(
            data.is_contiguous(),
            "data ndarray must be contiguous, use np.ascontiguousarray(arr)",
        )?;
        type_error_check(sizes[0] <= 4, "layout of data must be [C <= 4, H, W]")?;

        let sizes_static: [usize; 3] = [sizes[0], sizes[1], sizes[2]];

        let height = sizes_static[1];
        let width = sizes_static[2];

        let buffer = data.as_slice()?;
        let result = convert_image_bytes(buffer, width as u16, height as u16, quality)?;
        let pyarr = Array::from_shape_vec(sizes_static, result.buffer)
            .map_err(|err| JpegConverterError::ArrayShapeError(err))?;
        Ok(pyarr.into_pyarray(py))
    }

    Ok(())
}
