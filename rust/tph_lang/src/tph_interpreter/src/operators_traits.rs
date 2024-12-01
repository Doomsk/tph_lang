use crate::stack::Stack;


/// Accepts the stack data from the current pipe (predecessor operation)
///
/// ```
///   current pipe
///      |           operator
///      |              |
///      |
/// >...................O......
/// ```
pub trait Monad {
    fn compute(&self, stack: Stack);
}


/// Accepts the stack data from the current pipe (predecessor operation)
/// and from the stack data of the adjacent left-hand-side pipe.
///
/// ```
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
pub trait Dyad {
    fn compute(&self, stack: Stack);
}


/// Accepts the stack data from the current pipe (predecessor operation),
/// from the stack data of the adjacent left-hand-side pipe and from the
/// stack data of the adjacent right-hand-side pipe.
///
/// ```
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
pub trait Triad {
    fn compute(&self, stack: Stack);
}



