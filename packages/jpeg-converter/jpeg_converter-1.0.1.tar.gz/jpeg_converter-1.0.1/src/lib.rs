use anyhow::Context;
use pyo3::prelude::*;

mod python_module;

use image::io::Reader as ImageReader;
use image::{GenericImageView, ImageBuffer, ImageError, ImageFormat, Pixel, Rgb};

use std::io::Cursor;

use jpeg_encoder::{ColorType, Encoder, EncodingError};

use thiserror::Error;

#[pyclass]
pub struct ImageResult {
    pub buffer: Vec<f32>,
    pub width: u32,
    pub height: u32,
}

#[derive(Error, Debug)]
pub enum JpegConverterError {
    #[allow(missing_docs)]
    #[error(transparent)]
    IOError(#[from] std::io::Error),

    #[allow(missing_docs)]
    #[error(transparent)]
    EncodingError(#[from] EncodingError),

    #[allow(missing_docs)]
    #[error(transparent)]
    ImageError(#[from] ImageError),

    #[allow(missing_docs)]
    #[error(transparent)]
    OpenImageError(#[from] anyhow::Error),

    #[allow(missing_docs)]
    #[error(transparent)]
    ArrayShapeError(#[from] numpy::ndarray::ShapeError),
}

pub fn convert_image_bytes(
    image_bytes: &[u8],
    width: u16,
    height: u16,
    quality: u8,
) -> Result<ImageResult, JpegConverterError> {
    let mut encoder_buffer: Vec<u8> = Vec::new();
    let encoder = Encoder::new(&mut encoder_buffer, quality);

    encoder.encode(image_bytes, width, height, ColorType::Rgb)?;

    let img =
        image::io::Reader::with_format(Cursor::new(encoder_buffer), ImageFormat::Jpeg).decode()?;

    let mut buffer: ImageBuffer<Rgb<f32>, Vec<f32>> = ImageBuffer::new(img.width(), img.height());

    for (to, from) in buffer.pixels_mut().zip(img.pixels()) {
        let pixels = to.channels_mut();
        let rgb = from.2.channels();
        pixels[0] = f32::from(rgb[0]);
        pixels[1] = f32::from(rgb[1]);
        pixels[2] = f32::from(rgb[2])
    }

    let mut result = buffer.into_raw();
    result.shrink_to_fit();

    Ok(ImageResult {
        buffer: result,
        width: img.width(),
        height: img.height(),
    })
}

fn convert_image(image_path: String, quality: u8) -> Result<ImageResult, JpegConverterError> {
    let source = ImageReader::open(&image_path)
        .with_context(|| format!("Failed to open the image {}", &image_path))?
        .with_guessed_format()?
        .decode()
        .with_context(|| format!("Failed to decode the image {}", &image_path))?;

    convert_image_bytes(
        source.as_bytes(),
        source.width() as u16,
        source.height() as u16,
        quality,
    )
}
