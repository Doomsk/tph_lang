#![allow(unused)]
#![allow(dead_code)]
#![allow(unused_variables)]
#![allow(unused_imports)]

use std::fs::File;
use std::io::{Read};
use std::path::Path;

mod moving;
mod space;
mod evaluator;
pub mod operators_traits;
mod stack;
pub mod parser;
pub mod operators;

use parser::{Code};


pub fn parse_file(file_name: &str) -> Code {
    Code::new(file_name)
}


pub fn add(left: u64, right: u64) -> u64 {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
