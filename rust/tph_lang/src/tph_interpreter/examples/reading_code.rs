#![allow(unused)]

use std::{env, fs};
use std::path::{PathBuf, absolute, Path};
use tph_interpreter::parse_file;
use tph_interpreter::code::CodeData;


fn main() {
    // let mut path_file = PathBuf::from("example01.tph"); // PathBuf::from("src");
    // path_file.push("tph_interpreter");
    // path_file.push("examples");
    // path_file.push("example01.tph");
    // let binding = absolute(&mut path_file).unwrap();
    // let abs_path: &str = binding.to_str().unwrap();

    let file_path = env::var("PWD") + "/src/tph_interpreter/examples/";
    let paths = fs::read_dir(file_path).unwrap();

    let res: Vec<String> = paths.into_iter().filter_map(|f| {
        let mut x = f.unwrap().path().file_name().unwrap().to_str().unwrap().to_string();
        if x.ends_with(".tph") {
            let y = (file_path.to_string() + (&x)).to_string();
            if PathBuf::from(&y).exists() {
                Some( y )
            }
            else {
                None
            }
        }
        else { Option::None }
    } ).collect();
    // println!("{:?}", res);

    // let codes: Vec<Code> = res.iter().map(|arg0| parse_file(arg0)).collect();
    // println!("{:?}", codes);
    for arg in res.iter() {
        let sub_res = parse_file(arg);
        println!("{:?}\n", sub_res);
    }
    println!("\ndone.");
    // let code = parse_file(file_path);
    // println!("{:?}", code);
}
