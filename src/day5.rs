pub fn day5_1(filestring: &'static str, part2: bool) -> Result<String, std::io::Error> {
    let (stacks, moves) = filestring.split_once("\n\n").unwrap();

    // Const arguments are a bitch and the char init requires const as size
    const AMOUNT_OF_STACKS: usize = 9;

    // Prepare vec of vecs to keep track of each stack
    let split_stacks: Vec<&str> = stacks.split("\n").collect();
    let mut stack_vec: Vec<Vec<char>> = [(); AMOUNT_OF_STACKS].map(|_| Vec::new()).to_vec();
    for (row, stack_row) in split_stacks.iter().enumerate() {
        for (stack_nr, col) in (1..stack_row.len()).step_by(4).enumerate() {
            let elf_crate = stack_row.chars().nth(col).unwrap();
            if elf_crate as u8 != b' '  {
                stack_vec[stack_nr].push(elf_crate);
            }
        }
    }

    // reverse order
    stack_vec = stack_vec.into_iter().map(|s| s.into_iter().rev().collect()).collect();

    // Parse the moves
    for mv in moves.split("\n") {
        let charvec: Vec<&str> = mv.split(" ").collect();
        let amount: usize = charvec[1].parse().unwrap();
        let origin: usize = charvec[3].parse::<usize>().unwrap() - 1; // zero-based stack indexing
        let dest: usize = charvec[5].parse::<usize>().unwrap() - 1;

        dbg!(&charvec);
        dbg!(&stack_vec);

        let current_stack_size = stack_vec[origin].len();
        let mut on_crane = stack_vec[origin].split_off( current_stack_size - amount);
        if !part2 {
            on_crane.reverse();
        }
        stack_vec[dest].append(&mut on_crane);

        dbg!(&stack_vec);
    }

    let mut result_string = String::from("");
    for mut stack in stack_vec {
        result_string.push(stack.pop().unwrap());
    }

    dbg!(&result_string);

    Ok(result_string)
}


#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day5_1() {
        assert_eq!(day5_1(include_str!["../data/test5_1.txt"], false).unwrap(), "CMZ");
    }

    #[test]
    fn test_day5_2() {
        assert_eq!(day5_1(include_str!["../data/test5_1.txt"], true).unwrap(), "MCD");
    }
}