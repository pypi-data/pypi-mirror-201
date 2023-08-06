use pyo3::prelude::*;
use ril::prelude::{Image, ImageFormat, Rgba};
use std::time::{Instant};


/// Formats the sum of two numbers as string.
#[pyfunction]
fn create_image(width: u32, height: u32,  hex_color: &str, file_name: String, file_format: u8) -> PyResult<f64> {

    let now = Instant::now();

    let image_format = match file_format {
        1 => ImageFormat::Png,
        2 => ImageFormat::Jpeg,
        3 => ImageFormat::Gif,
        4 => ImageFormat::Bmp,
        5 => ImageFormat::Tiff,
        6 => ImageFormat::WebP,
        _ => ImageFormat::Png,
    };

    let color = Rgba::from_hex(hex_color).expect("Failed to convert hex to RGBA");

    if file_name.contains("debug") {
        println!("Using File Format : {:?}", image_format);
        println!("Using File Format : {:?}", color);
    }

    Image::new(width, height,  color)
        .save(image_format, file_name).expect("Error in Image Generation");

    let end = now.elapsed().as_secs_f64();
    Ok(end)
}

/// A Python module implemented in Rust.
#[pymodule]
fn blankimage(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(create_image, m)?)?;
    Ok(())
}
