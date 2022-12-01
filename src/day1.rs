use std::{fs::File, io::{BufReader, BufRead}};

pub fn day1_1(filepath: &str) -> Result<i32, std::io::Error> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);

    let mut total_max: i32 = 0;
    let mut total_current: i32 = 0;

    for (_index, line) in reader.lines().enumerate() {
        let newline = line.unwrap();
        let no_number = newline.is_empty();
        if no_number {
            if total_current > total_max {
                total_max = total_current;
            }
            total_current = 0;
        } else {
            total_current += newline.parse::<i32>().unwrap();
        }
    }
    Ok(total_max)
}

pub fn day1_2(filepath: &str) -> Result<i32, std::io::Error> {
    let file = File::open(filepath)?;
    let reader = BufReader::new(file);

    let mut total_max: Vec<i32> = vec![0, 0, 0];
    let mut total_current: i32 = 0;

    for (_index, line) in reader.lines().enumerate() {
        let newline = line.unwrap();
        let no_number = newline.is_empty();
        if no_number {
            total_max.push(total_current);
            total_max.sort();
            total_max.reverse();
            total_max.pop();
            total_current = 0;
        } else {
            total_current += newline.parse::<i32>().unwrap();
        }
    }
    Ok(total_max.iter().sum())
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_day1_1() {
        assert_eq!(day1_1("data/test1_1.txt").unwrap(), 24000);
    }

    #[test]
    fn test_day1_2() {
        assert_eq!(day1_2("data/test1_1.txt").unwrap(), 45000);
    }
}