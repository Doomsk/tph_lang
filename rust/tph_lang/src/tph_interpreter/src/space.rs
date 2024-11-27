

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
pub struct Coords {
    pub l: u64,
    pub c: u64,
}

impl Coords {
    /// Coords always start in the top left side of a program,
    /// e.g. position `(0, 0)`
    pub fn new() -> Coords {
        Coords { l:0, c:0 }
    }

    pub fn down(&mut self, limit: u64) {
        self.l = (self.l as i64).wrapping_add(1) as u64 % limit;
    }

    pub fn up(&mut self, limit: u64) {
        self.l = (self.l as i64).wrapping_sub(1) as u64 % limit;
    }

    pub fn right(&mut self, limit: u64) {
        self.c = (self.c as i64).wrapping_add(1) as u64 % limit;
    }

    pub fn left(&mut self, limit: u64) {
        self.c = (self.c as i64).wrapping_sub(1) as u64 % limit;
    }
}