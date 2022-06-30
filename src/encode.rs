use bmp::Image;

use crate::dct::*;

pub fn encode_from_image(image: Image) -> ImageFrequenceDomain {
    let mut compressed_image = ImageFrequenceDomain::default();
    compressed_image.set_width_and_height(&image);
    let mut luminance_time_domain = vec![vec![0f32; image.get_height() as usize]; 
        image.get_width() as usize];
    let mut blue_chrominance_time_domain = vec![vec![0f32; image.get_height() as usize]; 
        image.get_width() as usize];
    let mut red_chrominance_time_domain = vec![vec![0f32; image.get_height() as usize]; 
    image.get_width() as usize];
    for (i, j) in image.coordinates() {
        luminance_time_domain[i as usize][j as usize] = 0.299 * (image.get_pixel(i, j).r as f32) + 
            0.587 * (image.get_pixel(i, j).g as f32) + 0.114 * (image.get_pixel(i, j).b as f32);
        blue_chrominance_time_domain[i as usize][j as usize] = 0.492 * 
            ((image.get_pixel(i, j).b as f32) - luminance_time_domain[i as usize][j as usize]) + 128.0;
        red_chrominance_time_domain[i as usize][j as usize] = 0.877 * 
            ((image.get_pixel(i, j).r as f32) - luminance_time_domain[i as usize][j as usize]) + 128.0;
    }
    compressed_image.luminance.encode(luminance_time_domain, &LUMINANCE_QUANTIFICATION);
    compressed_image.blue_chrominance.encode(blue_chrominance_time_domain, &CHROMINANCE_QUANTIFICATION);
    compressed_image.red_chrominance.encode(red_chrominance_time_domain, &CHROMINANCE_QUANTIFICATION);

    compressed_image
}
