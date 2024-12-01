#![allow(dead_code, unused_variables, unused_imports, unused_macros, unused)]

use std::path::PathBuf;
use tph_interpreter::parse_file;

struct Cli {
    file: PathBuf,
}

fn main() {
    let path = PathBuf::from(std::env::args().nth(1).unwrap());
    println!("tph running\n");

}
