pub mod encode;
pub mod decode;
pub mod dct;

use bmp::{Pixel, Image, px};

fn main() {
    let image = bmp::open("./bmp/image.bmp").unwrap_or_else(|e| {
        panic!("Failed to open: {}", e);
    });
    let codes = encode::encode_from_image(image);
    let image = decode::decode_to_image(codes);
    let _ = image.save("a.bmp");
}

#[test]
fn bmp_demo() {
    let image = bmp::open("./bmp/image.bmp").unwrap_or_else(|e| {
        panic!("Failed to open: {}", e);
    });
    let mut new_image = Image::new(image.get_width(), image.get_height());
    for (x, y) in new_image.coordinates() {
        new_image.set_pixel(x, y, px!(image.get_pixel(x, y).r, image.get_pixel(x, y).g, image.get_pixel(x, y).b));
    }
    let _ = new_image.save("a.bmp");
}