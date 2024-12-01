use crate::parser::Data;

pub struct Stack {
    stack: Vec<Data>,
}

impl Stack {
    pub fn new() -> Self {
        Stack { stack: vec![] }
    }

    pub fn push(&mut self, data: Data) {
        self.stack.push(data);
    }

    pub fn pop(&mut self) -> Option<Data> {
        self.stack.pop()
    }

}
