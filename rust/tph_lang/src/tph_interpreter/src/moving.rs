use crate::space::{Coords, SpaceDimension, PositionMap};


/// The program current "caret" position in the program dimension.
///
/// It consists of coordinates (`coords`) as `Coords` type and its
/// current direction (`dir`) as `Direction`.
#[derive(Clone)]
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

    pub fn next_lhs(&mut self, pos: &PositionMap, ) {
        match self.dir {
            Direction::RIGHT => {},
            Direction::LEFT => {},
            Direction::DOWN => {},
            Direction::UP => {},
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



pub struct MoveChecker {
    pub unit_type: UnitType,
    pub cur_dir: Direction,
    pos: UnitPosition,
}

impl MoveChecker {
    pub fn new(unit_type: UnitType, cur_dir: Direction, unit_pos: UnitPosition) -> MoveChecker {
        MoveChecker { unit_type, cur_dir, pos: unit_pos.clone() }
    }

    pub fn check_lhs(&self, space: &PositionMap) {


    }
}


#[derive(Clone)]
pub enum UnitType {
    Data,
    MonadOperator,
    DyadOperator,
    EndOperator,
}