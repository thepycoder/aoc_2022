pub fn day10_1(filestring: &'static str) -> Result<u32, std::io::Error> {
    // Prepare vec of vecs to keep track of each stack
    let instructions: Vec<&str> = stacks.split("\n").collect();

    instructions.map(||)

    // dbg!(&result_string);

    Ok(result_string)
}


#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day10_1() {
        assert_eq!(day10_1(include_str!["../data/test5_1.txt"], false, 3).unwrap(), "CMZ");
    }

    #[test]
    fn test_day10_2() {
        assert_eq!(day10_1(include_str!["../data/test5_1.txt"], true, 3).unwrap(), "MCD");
    }
}