use std::fs;
use std::ops::Index;


pub enum Direction {
    Right,
    Left,
    Down,
    Up,
}


#[derive(Debug, Clone)]
pub struct CodeDimension {
    pub height: u64,
    pub width: u64,
}

impl CodeDimension {
    pub fn code_size(&self) -> (u64, u64) {
        (self.height, self.width)
    }
}


#[derive(Debug)]
pub struct CodeData {
    code: Vec<Vec<char>>,
    pub dim: CodeDimension,
}

impl CodeData {
    pub fn new(file_name: &str) -> CodeData {
        let raw_data: String = fs::read_to_string(file_name).expect("Cannot open file");
        let code: Vec<Vec<char>> = raw_data.lines().map(|line| line.chars().collect()).collect();
        let dir = Direction::Right;
        let height = code.len() as u64;
        let width = code.iter().map(|s| s.len()).max().unwrap() as u64;
        let dim = CodeDimension { height, width };
        CodeData { code, dim }
    }
}

impl Index<u64> for CodeData {
    type Output = Vec<char>;

    fn index(&self, index: u64) -> &Self::Output {
        &self.code[index as usize]
    }
}