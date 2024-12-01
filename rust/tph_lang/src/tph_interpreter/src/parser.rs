use std::fs;
use std::path::Path;
use crate::space::PositionMap;

#[derive(Debug)]
pub struct Code {
    pub data: Vec<String>,
    pub pos_map: PositionMap,
}

impl Code {
    pub fn new(file_name: &str) -> Code {
        let data = fs::read_to_string(file_name).expect("Something went wrong");
        let as_lines: Vec<String> = data.lines().map(String::from).collect();
        let pos_map: PositionMap = PositionMap::new(as_lines.clone());
        Code { data: as_lines, pos_map }
    }
}


pub struct Int {
    pub value: i64,
}

impl Int {
    pub fn new(value: i64) -> Self { Int { value } }
    pub fn peek(&self, next_unit: String) {}
}

pub enum DataOrigin {
    LHS,
    RHS,
}

pub enum Expr {
    StackPush(Data, DataOrigin),
    StackPop,
    None,
}

pub struct Fn {
    pub name: String,
    pub args: Vec<Data>,
    pub body: Vec<Expr>,
}

pub enum Data {
    Int(i64),
    Float(f64),
    Str(String),
    Function(Fn),
    None,
}