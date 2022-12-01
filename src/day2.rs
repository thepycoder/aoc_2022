use std::{fs::File, io::BufReader};


pub fn day2_1(filepath: &str) -> Result<i32, std::io::Error> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);

    Ok()
}

pub fn day2_2(filepath: &str) -> Result<i32, std::io::Error> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);

    Ok()
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day2_1() {
        assert_eq!(day2_1("data/test1_1.txt").unwrap(), 24000);
    }

    #[test]
    fn test_day2_2() {
        assert_eq!(day2_2("data/test1_1.txt").unwrap(), 45000);
    }
}