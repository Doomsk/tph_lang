

pub struct PipeStack {
    stack: Vec<Data>,
    pub stack_type: StackType,
}

impl PipeStack {
    pub fn new(stack_type: Option<StackType>) -> PipeStack {
        PipeStack {
            stack_type: stack_type.unwrap_or_else(|| StackType::Main),
            stack: Vec::new(),
        }
    }

    pub fn push(&mut self, data: Data) {
        self.stack.push(data);
    }

    pub fn pop(&mut self) -> Option<Data> {
        self.stack.pop()
    }
}


pub enum StackType {
    Main,
    LHS,
    RHS,
    None
}

pub enum Data {
    Int(i64),
    Float(f64),
    Str(String),
    Composite(Vec<Data>),
    None,
}

pub struct LiteralStack {
    stack: Vec<char>,
}

impl LiteralStack {
    pub fn new() -> LiteralStack {
        LiteralStack { stack: Vec::new() }
    }
    pub fn push(&mut self, c: char) {
        self.stack.push(c);
    }
}

impl<T> LiteralStack {
    pub fn pop(&mut self) -> Result<T, String> {
        let res: Result<T, String> = self.stack
            .iter()
            .collect::<String>()
            .parse::<T>()
            .map_err(|| "Failed to parse expression".to_string());
        self.stack.pop();
        res
    }
}
