pub fn day6_1(filestring: &'static str, marker_len: usize) -> Result<usize, std::io::Error> {
    let char_vec: Vec<char> = filestring.chars().collect();
    for (i, slice) in char_vec.windows(marker_len).enumerate() {
        let unique = !(1..slice.len()).any(|i| slice[i..].contains(&slice[i - 1]));

        if unique {
            let final_answer = i + marker_len;
            return Ok(final_answer)
        }
        // dbg!(slice);
        // dbg!(unique);
    }
    // dbg!(filestring);
    Ok(0)
}


#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day6_1() {
        assert_eq!(day6_1(include_str!["../data/test6_1.txt"], 4).unwrap(), 7);
    }

    #[test]
    fn test_day6_2() {
        assert_eq!(day6_1(include_str!["../data/test6_2.txt"], 4).unwrap(), 5);
    }

    // #[test]
    // fn test_day6_2() {
    //     assert_eq!(day5_1(include_str!["../data/test5_1.txt"], true).unwrap(), 0);
    // }
}