//! List of valid operators:
//!
//! [Right] operator `>` ([Monad]): move the execution direction to right
//!
//! [Down] operator `v` ([Monad]): move the execution direction to down
//!
//! [Left] operator `<` ([Monad]): move the execution direction to left
//!
//! [Up] operator `^` ([Monad]): move the execution direction to up
//!
//! [Filter] operator `f` ([Dyad]): filter the current stack using the LHS pipe
//!
//! [Reduce] operator `r` ([Dyad]): reduce the current stack data using the LHS pipe
//!
//! [EachMapAcc] operator `a` ([Triad]): for each item on the current pipe stack data,
//! uses in conjunction with the RHS pipe to apply the operators on the LHS pipe
//!
//! []
//!
//!
//! [SemiColon] operator `;` ([Monad]): stops the execution of an adjacent pipe
//!
//! [EndProgram] operator `.` ([Monad]): terminates the program
//!

use std::os::unix::prelude::ExitStatusExt;
use std::process::ExitCode;
use crate::operators_traits::{Monad, Dyad, Triad, OperationResult, Operator};
use crate::stack::Stack;


/// From a String, get the corresponding Operator type
pub fn get_operator<T>(data: String) -> Operator<T> {
    match data.as_str() {
        ">" => Operator::Monad(Box::new(Right {})),
        "." => Operator::Monad(Box::new(EndProgram {})),
        _ => todo!(),
    }
}


/// Right operator `>`
pub struct Right {

}

impl<T> Monad<T> for Right {
    fn compute(&self, stack: Stack) -> OperationResult<T> {
        todo!()
    }
}


/// Down operator `v`
pub struct Down {

}


/// Left operator `<`
pub struct Left {

}


/// Up operator `^`
pub struct Up {

}


/// Filter operator `f`
///
/// Filter a data (current stack data) through a function (LHS pipe).
pub struct Filter {

}


/// Reduce operator `r`
///
/// A `foldl` operator on data (current stack data) through a function (LHS pipe).
pub struct Reduce {

}


/// EachMapAcc operator `a`
///
/// For each value on the current pipe, uses in conjunction with RHS pipe to apply
/// the operations on LHS pipe.
pub struct EachMapAcc {

}


/// And operator `&`
///
/// Applies logic `and` on data.
pub struct And {

}


/// Or operator `|`
///
/// Applies logic `or` on data.
pub struct Or {

}



/// Modulus operator `%`
///
/// Applies the modulus on data, `S1 % S0` where `S0` is the first item on the stack,
/// and `S1` is the second.
pub struct Modulus {

}


/// Equal operator `=`
///
/// Do comparison between two data and returns boolean value.
pub struct Equal {

}


/// Sum operator `+`
///
/// Sum values on the stack. If [Monad], sum all the values on the current stack.
/// If [Dyad], sum the values pairwise.
pub struct Sum {

}


/// Product operator
///
/// Multiplies values on the stack. If [Monad], multiplies all the values on the
/// current stack. If [Dyad], multiply the values pairwise.
pub struct Product {

}


/// Iota operator `i`
///
/// Fills the range from a value. If [Monad], ranges from 1 to current stack head -1.
/// If [Dyad], ranges from LHS pipe to current stack head -1. If [Triad], do something
/// else. -- Triad to be properly defined.
pub struct Iota {

}


/// Input operator `b`
///
/// User input data on the stack.
pub struct Input {

}


/// FileInput operator `B`
///
/// File input data on the stack. As a [Dyad], gets from the LHS pipe which file
/// to read as string. As a [Triad], gets from the RHS pipe how to parse the data,
/// e.g. as string, numbers, etc. -- Triad to be properly defined.
pub struct FileInput {

}


/// Output operator `o`
///
/// Outputs data. If [Monad], outputs on the screen. If [Dyad], outputs according
/// to specifications (file, etc.). -- Dyad version to be properly defined.
pub struct Output {

}


/// Comma operator `,`
///
/// Cause digits pre comma to form a number and the post digits to form another
/// separated number. Ex:
/// ```ignore
/// 10,20+
/// ```
/// This is `10` and `20` that will go to the stack and be applied a `+` operator.
/// Another:
/// ```ignore
/// 100,o
/// ```
/// Although valid, it is not very useful, since the following character is an operator.
/// Digits with whitespaces will be composed as a single number in the end, ex:
/// ```ignore
/// 1 2    45 8
/// ```
/// is the same number as `12458`.
pub struct Comma {

}


/// SemiColon operator `;`
///
/// Stops the execution of an adjacent pipe. Must be used to delimiter LHS and RHS
/// pipes.
pub struct SemiColon {

}


/// EndProgram operator `.`
///
/// Terminates the program.
pub struct EndProgram {

}

impl<T> Monad<T> for EndProgram {
    fn compute(&self, _stack: Stack) -> OperationResult<T> {
        OperationResult::Exit(ExitCode::SUCCESS, "".to_string())
    }
}


