use std::any::Any;
use std::process::ExitCode;
use crate::stack::PipeStack;


pub enum Operator<T> {
    Monad(Box<dyn Monad<T>>),
    Dyad(Box<dyn Dyad<T>>),
    Triad(Box<dyn Triad<T>>),
}

impl<T> Operator<T> {
    pub fn compute(&self) {
        match self {
            Operator::Monad(op) => Monad::compute(),
            Operator::Dyad(op) => Dyad::compute(),
            Operator::Triad(op) => Triad::compute(),
        }
    }
}

pub enum OperationResult<T> {
    Ok(T),
    Exit(ExitCode, String),
    None,
}


/// Accepts the stack data from the current pipe (predecessor operation)
///
/// ```ignore
///   current pipe
///      |           operator
///      |              |
///      |
/// >...................O......
/// ```
pub trait Monad<T> {
    fn compute(&self, stack: Stack) -> OperationResult<T>;
}


/// Accepts the stack data from the current pipe (predecessor operation)
/// and from the stack data of the adjacent left-hand-side pipe.
///
/// ```ignore
///   current pipe
///      |              .
///      |               . -- left-hand-side (LHS) pipe
///      |              .
/// >...................O......
///
///                     |
///                   operator
/// ```
/// Note that the LHS is relative to the operator direction, relative to
/// its pipe execution direction.
pub trait Dyad<T> {
    fn compute(&self, stack: Stack, lhs_stack: Stack) -> OperationResult<T>;
}


/// Accepts the stack data from the current pipe (predecessor operation),
/// from the stack data of the adjacent left-hand-side pipe and from the
/// stack data of the adjacent right-hand-side pipe.
///
/// ```ignore
///   current pipe
///      |              .
///      |               . -- left-hand-side (LHS) pipe
///      |              .
/// >...................O......
///                     .\_ operator
///                     .
///                      . -- right-hand-side (RHS) pipe
///                     .
/// ```
/// Note that the LHS and RHS are relative to the operator direction,
/// relative to its pipe execution direction.
pub trait Triad<T> {
    fn compute(&self, stack: Stack, lhs_stack: Stack, rhs_stack: Stack) -> OperationResult<T>;
}



