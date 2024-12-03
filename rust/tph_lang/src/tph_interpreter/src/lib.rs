#![allow(unused)]
#![allow(dead_code)]
#![allow(unused_variables)]
#![allow(unused_imports)]

use std::fs::File;
use std::io::{Read};
use std::path::Path;

mod moving;
mod space;
pub mod evaluator;
pub mod operators_traits;
mod stack;
pub mod parser;
pub mod operators;
pub mod code;

use crate::code::CodeData;
use crate::evaluator::Evaluator;


pub fn parse_file(file_name: &str) -> CodeData {
    CodeData::new(file_name)
}

pub fn run_code(code: CodeData) {
    let mut evaluator = Evaluator::new(code);
    evaluator.run();
}

#[cfg(test)]
mod tests {
    use super::*;

    // #[test]
    // fn it_works() {
    //     let result = add(2, 2);
    //     assert_eq!(result, 4);
    // }
}
