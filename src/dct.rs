use ndarray::{arr2, Array2};
use ndarray_linalg::solve::Inverse;

struct Alternating {
    pub value: i8,
    pub number: u8,
}
#[derive(Default)]
pub struct ColorFrequenceDomain {
    pub directing: Vec<f32>,
    alternating: Vec<Alternating> 
}

use std::f64::consts::PI;
fn get_dct_matrix() -> Array2<f32> {
    let mut a = [[0f32; 8]; 8];
    for i in  0..8 {
        for j in 0..8 {
            let x = if i == 0 {
                (1.0_f32 / 8.0).sqrt()
            } else {
                (2.0_f32 / 8.0).sqrt()
            };
            a[i][j] = x * (PI as f32 * (j as f32 + 0.5) * i as f32 / 8.0).cos();
        }
    }
    arr2(&a)
}

fn transpose(matrix: &Array2<f32>) -> Array2<f32> {
    let mut a = [[0f32; 8]; 8];
    for i in 0..8 {
        for j in 0..8 {
            a[i][j] = matrix[[j, i]];
        }
    }
    arr2(&a)
}

impl ColorFrequenceDomain {
    pub fn encode(&mut self, time_domain: Vec<Vec<f32>>, quantification_matrix: &[[f32; 8]; 8]) {
        let dct_matrix = get_dct_matrix();
        let dct_transpose_matrix = transpose(&dct_matrix);
        for i in (0 ..= time_domain.len() - 8).step_by(8) {
            for j in (0..= time_domain[i].len() - 8).step_by(8) {
                let mut t = Array2::zeros((8, 8));
                for u in 0..8 {
                    for v in 0..8 {
                        t[[u, v]] = time_domain[i + u][j + v];
                    }
                }
                let mut t = dct_matrix.dot(&t).dot(&dct_transpose_matrix);
                for u in 0..8 {
                    for v in 0..8 {
                        t[[u, v]] /= quantification_matrix[u][v];
                    }
                }
                let mut x = 0;
                let mut y = 0;
                let mut cnt = 0;
                self.directing.push(t[[0, 0]]);
                for u in Z_TRAVERSAL {
                    x += u[0];
                    y += u[1];
                    if t[[x as usize, y as usize]].round() as i8 == 0 {
                        cnt += 1;
                    } else {
                        self.alternating.push(Alternating { 
                            value: t[[x as usize, y as usize]].round() as i8, 
                            number: cnt
                        });
                        cnt = 0;
                    }
                }
                if t[[7, 7]].round() as i8 == 0 {
                    self.alternating.push(Alternating { 
                        value: 0, 
                        number: 0 
                    });
                }
            }
        }
    }

    pub fn decode(&self, time_domain: &mut Vec<Vec<f32>>, quantification_matrix: &[[f32; 8]; 8]) {
        let dct_matrix = get_dct_matrix().inv().unwrap();
        let dct_transpose_matrix = transpose(&dct_matrix);
        let mut alternate_current = 0;
        let mut directing_current = 0;
        let mut frequency_domain = vec![vec![0f32; time_domain[0].len()]; time_domain.len()];
        for i in (0..frequency_domain.len()).step_by(8) {
            for j in (0..frequency_domain[i].len()).step_by(8) {
                frequency_domain[i][j] = self.directing[directing_current] as f32;
                directing_current += 1;
                let mut x = i as i32;
                let mut y = j as i32;
                let mut flag = false;
                let mut cnt = 0;
                for u in Z_TRAVERSAL {
                    x += u[0];
                    y += u[1];
                    if flag {
                        frequency_domain[x as usize][y as usize] = 0.0;
                    } else if cnt == self.alternating[alternate_current].number {
                        frequency_domain[x as usize][y as usize] = self.alternating[alternate_current].value as f32;
                        if self.alternating[alternate_current].value == 0 {
                            flag = true;
                        }
                        alternate_current += 1;
                        cnt = 0;
                    } else{
                        frequency_domain[x as usize][y as usize] = 0.0;
                        cnt += 1;
                    }
                }
            }
        }
        for i in (0..frequency_domain.len()).step_by(8) {
            for j in (0..frequency_domain[i].len()).step_by(8) {
                let mut f = Array2::zeros((8, 8));
                for u in 0..8 {
                    for v in 0..8 {
                        f[[u, v]] = frequency_domain[i + u][j + v] * quantification_matrix[u][v];
                    }
                }
                let f = dct_matrix.dot(&f).dot(&dct_transpose_matrix);
                for u in 0..8 {
                    for v in 0..8 {
                        time_domain[i + u][j + v] = f[[u, v]];
                    }
                }
            }
        }
    }
}

#[derive(Default)]
pub struct ImageFrequenceDomain {
    pub width: u32,
    pub height: u32,
    pub luminance: ColorFrequenceDomain,
    pub blue_chrominance: ColorFrequenceDomain,
    pub red_chrominance: ColorFrequenceDomain,
}

pub const LUMINANCE_QUANTIFICATION: [[f32; 8]; 8] = [
    [16.0, 11.0, 10.0, 16.0, 24.0, 40.0, 51.0, 61.0],
    [12.0, 12.0, 14.0, 19.0, 26.0, 58.0, 60.0, 55.0],
    [14.0, 13.0, 16.0, 24.0, 40.0, 57.0, 69.0, 56.0],
    [14.0, 17.0, 22.0, 29.0, 51.0, 87.0, 80.0, 62.0],
    [18.0, 22.0, 37.0, 56.0, 68.0, 109.0, 103.0, 77.0],
    [24.0, 35.0, 55.0, 64.0, 81.0, 104.0, 113.0, 92.0],
    [49.0, 64.0, 78.0, 87.0, 103.0, 121.0, 120.0, 101.0],
    [72.0, 92.0, 95.0, 98.0, 112.0, 100.0, 103.0, 99.0]
];

pub const CHROMINANCE_QUANTIFICATION: [[f32; 8]; 8] = [
    [17.0, 18.0, 24.0, 47.0, 99.0, 99.0, 99.0, 99.0],
    [18.0, 21.0, 26.0, 66.0, 99.0, 99.0, 99.0, 99.0],
    [24.0, 26.0, 56.0, 99.0, 99.0, 99.0, 99.0, 99.0],
    [47.0, 66.0, 99.0, 99.0, 99.0, 99.0, 99.0, 99.0],
    [99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 99.0],
    [99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 99.0],
    [99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 99.0],
    [99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 99.0]
];

const Z_TRAVERSAL: &'static [[i32; 2]] = &[
    [0, 1], [1, -1],
    [1, 0], [-1, 1], [-1, 1],
    [0, 1], [1, -1], [1, -1], [1, -1],
    [1, 0], [-1, 1], [-1, 1], [-1, 1], [-1, 1],
    [0, 1], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1],
    [1, 0], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1],
    [0, 1], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1],
    [0, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1],
    [1, 0], [1, -1], [1, -1], [1, -1], [1, -1], [1, -1],
    [0, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1],
    [1, 0], [1, -1], [1, -1], [1, -1],
    [0, 1], [-1, 1], [-1, 1],
    [1, 0], [1, -1],
    [0, 1]
];

impl ImageFrequenceDomain {
    pub fn set_width_and_height(&mut self, image: &bmp::Image) {
        self.height = image.get_height() & !7;
        self.width = image.get_width() & !7;
    }
}

