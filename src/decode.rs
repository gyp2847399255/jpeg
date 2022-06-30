use crate::dct::*;

use bmp::{Image, px, Pixel};

pub fn decode_to_image(codes: ImageFrequenceDomain) -> Image {
    let mut image = Image::new(codes.width, codes.height);
    let mut luminance_time_domain = vec![vec![0f32; codes.height as usize]; codes.width as usize];
    codes.luminance.decode(&mut luminance_time_domain, &LUMINANCE_QUANTIFICATION);
    let mut blue_chrominance_time_domain = vec![vec![0f32; codes.height as usize]; codes.width as usize];
    codes.blue_chrominance.decode(&mut blue_chrominance_time_domain, &CHROMINANCE_QUANTIFICATION);
    let mut red_chrominance_time_domain = vec![vec![0f32; codes.height as usize]; codes.width as usize];
    codes.red_chrominance.decode(&mut red_chrominance_time_domain, &CHROMINANCE_QUANTIFICATION);
    for i in 0..codes.width as usize {
        for j in 0..codes.height as usize {
            let r = (luminance_time_domain[i][j] + 1.140 * (red_chrominance_time_domain[i][j] - 128.0)) as u8;
            let g = (luminance_time_domain[i][j] - 0.395 * (blue_chrominance_time_domain[i][j] - 128.0) -
                               0.581 * (red_chrominance_time_domain[i][j] - 128.0)) as u8;
            let b = (luminance_time_domain[i][j] + 2.032 * (blue_chrominance_time_domain[i][j] - 128.0)) as u8;
            image.set_pixel(i as u32, j as u32, px!(r, g, b));
        }
    }
    image
}