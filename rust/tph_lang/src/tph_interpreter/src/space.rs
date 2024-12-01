

/// The dimension of a space, with its total height (`height`)
/// and width (`width`). Spaces can be the main space, functions
/// space, macros space, and so on.
pub struct SpaceDimension {
    pub height: u64,
    pub width: u64
}


/// `Coords` can move in modulus in one particular direction.
/// For example, given a limit of value 5 to `l`, if `l` is
/// on position 4 and moves one extra, it will 'reappear' on
/// position 0.
/// The same goes the other way: if `l` lies on position 0 and
/// moves one less, it will reappear on position 4.
#[derive(Clone, PartialEq, Hash, Debug)]
pub struct Coords {
    l: u64,
    c: u64,
}


impl Coords {
    /// Coords always start in the top left side of a program,
    /// e.g. position `(0, 0)`
    pub fn new() -> Coords {
        Coords { l:0, c:0 }
    }

    pub fn cur_pos(&self) -> (u64, u64) {
        (self.l, self.c)
    }

    pub fn down(&mut self, limit: u64) {
        self.l = (self.l + 1) % limit;
    }

    pub fn up(&mut self, limit: u64) {
        self.l = (self.l as i64 - 1).rem_euclid(limit as i64) as u64;
    }

    pub fn right(&mut self, limit: u64) {
        self.c = (self.c + 1) % limit;
    }

    pub fn left(&mut self, limit: u64) {
        self.c = (self.c as i64 - 1).rem_euclid(limit as i64) as u64;
    }
}


/// Use this to store the position of all the characters (units)
#[derive(Debug)]
pub struct PositionMap {
    pub grid: Vec<[u64; 2]>,
}

impl PositionMap {
    pub fn new(code_lines: Vec<String>) -> PositionMap {
        // let mut grid: Vec<[u64; 2]> = Vec::new();
        let mut grid: Vec<[u64; 2]> = code_lines
            .iter()
            .enumerate()
            .flat_map(|(idx, line)| {
                line.chars().enumerate().map(move |(idx2, c)| {
                  [idx as u64, idx2 as u64]
                })
            })
            .collect();
        PositionMap { grid }
    }
}