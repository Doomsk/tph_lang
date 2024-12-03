use crate::code::{CodeData, Direction};
use crate::operators::get_operator;
use crate::stack::{LiteralStack, PipeStack};

pub struct Evaluator {
    pub code: CodeData,
    pipe_state: PipeState,
    literal_stack: LiteralStack,
}


impl Evaluator {
    pub fn new(code: CodeData) -> Evaluator {
        Evaluator { code, literal_stack: LiteralStack::new(), pipe_state: PipeState }
    }

    pub fn run(&mut self) {
        // Always start running on pos (0, 0)
        self.compute(self.code[0][0])
    }

    pub fn compute(&mut self, unit: char) {
        let c = unit;
        match c {
            x if c.is_whitespace() => self.skip(),
            x if c.is_digit(10) => self.push_literal(x),
            x => {
                self.resolve_literals();
                let operator = get_operator(x);
                operator.compute();
            },
        }
    }

    pub fn skip(&mut self) {
        todo!()
    }

    pub fn push_literal(&mut self, unit: char) {
        self.literal_stack.push(unit)
    }

    pub fn resolve_literals(&mut self) {
        let res = self.literal_stack.pop().unwrap();
        self.pipe_state.stack.last().push(res);
    }
}


enum Unit {
    Literal(String),
    Operator(String),
    None,
}


struct PipeState {
    pub stack: Vec<PipeStack>,
    pub dir: Direction
}

impl PipeState {
    fn new(dir: Option<Direction>) -> PipeState {
        PipeState {
            stack: Vec::new(),
            dir: dir.unwrap_or_else(|| Direction::Right)
        }
    }

    fn push(&mut self, stack: PipeStack) {
        self.stack.push(stack);
    }

    fn pop(&mut self) -> Option<PipeStack> {
        self.stack.pop()
    }
}

