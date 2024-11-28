use crate::space::{Coords, SpaceDimension};


/// The program current "caret" position in the program dimension.
///
/// It consists of coordinates (`coords`) as `Coords` type and its
/// current direction (`dir`) as `Direction`.
pub struct UnitPosition {
    pub coords: Coords,
    pub dir: Direction
}

impl UnitPosition {
    pub fn new() -> UnitPosition {
        UnitPosition { coords: Coords::new(), dir: Direction::RIGHT }
    }

    pub fn cur_state(&self) -> ((u64, u64), Direction) {
        (self.coords.cur_pos(), self.dir.clone())
    }

    pub fn next(&mut self, space: &SpaceDimension) {
        match self.dir {
            Direction::RIGHT => self.coords.right(space.width),
            Direction::LEFT => self.coords.left(space.width),
            Direction::DOWN => self.coords.down(space.height),
            Direction::UP => self.coords.up(space.height),
        }
    }

}


#[derive(Clone)]
pub enum Direction {
    UP,
    DOWN,
    LEFT,
    RIGHT
}