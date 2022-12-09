pub fn day3_1(filestring: &[u8]) -> Result<u32, std::io::Error> {
    let byte_halves: Vec<_> = filestring
        .split(|b| *b == b'\n')
        .map(|rucksack| rucksack.split_at(rucksack.len() / 2))
        .collect();

    let mut total = 0;
    for byte_half_tuple in byte_halves {
        let difference: Vec<_> = byte_half_tuple.0.into_iter().filter(|item| byte_half_tuple.1.contains(item)).collect();

        if difference[0].is_ascii_uppercase() {
            total += 1 + (difference[0] - b'A'  + 26) as u32;
        } else {
            total += 1 + (difference[0] - b'a') as u32;
        }
    }
    Ok(total)
}

pub fn day3_2(filestring: &[u8]) -> Result<u32, std::io::Error> {
    let bytes_vec: Vec<_> = filestring
        .split(|b| *b == b'\n')
        .collect();

    let mut total = 0;
    for bytes_window in bytes_vec.chunks(3) {
        let difference: Vec<_> = bytes_window[0]
            .into_iter()
            .filter(|item| bytes_window[1].contains(item) && bytes_window[2].contains(item))
            .collect();

        if difference[0].is_ascii_uppercase() {
            total += 1 + (difference[0] - b'A'  + 26) as u32;
        } else {
            total += 1 + (difference[0] - b'a') as u32;
        }
    }
    Ok(total)
}


#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day3_1() {
        assert_eq!(day3_1(include_bytes!["../data/test3_1.txt"]).unwrap(), 157);
    }

    #[test]
    fn test_day3_2() {
        assert_eq!(day3_2(include_bytes!["../data/test3_1.txt"]).unwrap(), 70);
    }
}