pub mod encode;
pub mod decode;
pub mod dct;

fn main() {
    let image = bmp::open("./bmp/image.bmp").unwrap_or_else(|e| {
        panic!("Failed to open: {}", e);
    });
    let codes = encode::encode_from_image(image);
    let image = decode::decode_to_image(codes);
    let _ = image.save("a.bmp");
}
